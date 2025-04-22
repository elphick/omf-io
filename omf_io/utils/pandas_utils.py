import tokenize
from io import StringIO
from token import STRING
from typing import Literal

import pandas as pd
import numpy as np
from pandas import CategoricalDtype


def is_nullable_integer_dtype(series: pd.Series) -> bool:
    """

    Args:
        series: The series

    Returns:
        bool: True if series contains nullable integer
    """

    return True if str(series.dtype)[0] == "I" else False


def to_nullable_integer_dtype(series: pd.Series) -> pd.Series:
    """ Convert an int series to a nullable integer dtype

    Args:
        series: The series

    Returns:
        pd.Series: The series with nullable dtype
    """

    return series.astype(str(series.dtype).replace("i", "I")) if is_nullable_integer_dtype(series) else series


def to_numpy_integer_dtype(series: pd.Series) -> pd.Series:
    """ Convert a nullable int series to a numpy integer dtype

    Args:
        series: The series

    Returns:
        pd.Series: The series with nullable dtype
    """

    return series.astype(str(series.dtype).replace("I", "i")) if is_nullable_integer_dtype(series) else series


def parse_vars_from_expr(expr: str) -> list[str]:
    """ Parse variables from a pandas query expression string.

    Args:
        expr: The expression string

    Returns:
        list[str]: The list of variables
    """
    variables = set()
    tokens = tokenize.generate_tokens(StringIO(expr).readline)
    logical_operators = {'and', 'or', '&', '|'}
    inside_backticks = False
    current_var = []

    for token in tokens:
        if token.string == '`':
            if inside_backticks:
                # End of backtick-enclosed variable
                variables.add(' '.join(current_var))
                current_var = []
            inside_backticks = not inside_backticks
        elif inside_backticks:
            if token.type in {tokenize.NAME, STRING}:
                current_var.append(token.string)
        elif token.type == tokenize.NAME and token.string not in logical_operators:
            variables.add(token.string)

    return list(variables)


def create_test_blockmodel(shape: tuple[int, int, int],
                           block_size: tuple[float, float, float],
                           corner: tuple[float, float, float],
                           is_tensor=False) -> pd.DataFrame:
    """
    Create a test blockmodel DataFrame.

    Args:
        shape: Shape of the block model (x, y, z).
        block_size: Size of each block (x, y, z).
        corner: The lower left (minimum) corner of the block model.
        is_tensor: If True, create a tensor block model. Default is False, which creates a regular block model.
            The MultiIndex levels for a regular model are x, y, z.  For a tensor model they are x, y, z, dx, dy, dz.
            The tensor model created is a special case where dx, dy, dz are the same for all blocks.

    Returns:
    pd.DataFrame: DataFrame containing the block model data.

    """

    num_blocks = np.prod(shape)

    # Generate the coordinates for the block model
    x_coords = np.arange(corner[0] + block_size[0] / 2, corner[0] + shape[0] * block_size[0], block_size[0])
    y_coords = np.arange(corner[1] + block_size[1] / 2, corner[1] + shape[1] * block_size[1], block_size[1])
    z_coords = np.arange(corner[2] + block_size[2] / 2, corner[2] + shape[2] * block_size[2], block_size[2])

    # Create a meshgrid of coordinates
    xx, yy, zz = np.meshgrid(x_coords, y_coords, z_coords, indexing='ij')

    # Flatten the coordinates
    xx_flat_c = xx.ravel(order='C')
    yy_flat_c = yy.ravel(order='C')
    zz_flat_c = zz.ravel(order='C')

    # Create the attributes
    c_order_xyz = np.arange(num_blocks)

    # assume the surface of the highest block is the topo surface
    surface_rl = corner[2] + shape[2] * block_size[2]

    # Create the DataFrame
    df = pd.DataFrame({
        'x': xx_flat_c,
        'y': yy_flat_c,
        'z': zz_flat_c,
        'c_style_xyz': c_order_xyz})

    # Set the index to x, y, z
    df.set_index(keys=['x', 'y', 'z'], inplace=True)
    df.sort_index(level=['x', 'y', 'z'], inplace=True)
    df.sort_index(level=['z', 'y', 'x'], inplace=True)
    df['f_style_zyx'] = c_order_xyz
    df.sort_index(level=['x', 'y', 'z'], inplace=True)

    df['depth'] = surface_rl - zz_flat_c

    # Check the ordering - confirm that the c_order_xyz and f_order_zyx columns are in the correct order
    assert np.array_equal(df.sort_index(level=['x', 'y', 'z'])['c_style_xyz'].values, np.arange(num_blocks))
    assert np.array_equal(df.sort_index(level=['z', 'y', 'x'])['f_style_zyx'].values, np.arange(num_blocks))

    # Check the depth using a pandas groupby
    depth_group = df.groupby('z')['depth'].unique().apply(lambda x: x[0]).sort_index(ascending=False)
    assert np.all(surface_rl - depth_group.diff().index == depth_group.values)

    if is_tensor:
        # Create the dx, dy, dz levels
        df['dx'] = block_size[0]
        df['dy'] = block_size[1]
        df['dz'] = block_size[2]

        # Set the index to x, y, z, dx, dy, dz
        df.set_index(keys=['dx', 'dy', 'dz'], append=True, inplace=True)

    return df


def aggregate(df: pd.DataFrame, agg_dict: dict, cat_treatment: Literal['majority', 'proportions'] = 'majority',
              proportions_as_columns: bool = False) -> pd.DataFrame:
    """
    Aggregate a DataFrame using a provided dictionary.

    Args:
        df: The DataFrame to aggregate.
        agg_dict: A dictionary where keys are the columns to be aggregated and values are the weight columns.
        cat_treatment: A string indicating how to treat categorical columns.
                       'majority' returns the majority category, 'proportions' returns the proportions of each category.
        proportions_as_columns: A boolean indicating whether to return category proportions as separate columns.

    Returns:
        pd.DataFrame: The aggregated DataFrame with columns in the same order as the incoming DataFrame.
    """
    result = {}
    weight_columns = set(agg_dict.values())

    for weight_col in weight_columns:
        # Get columns that share the same weight column
        cols_with_weight = [col for col, w_col in agg_dict.items() if w_col == weight_col]
        if cols_with_weight:
            weights = df[weight_col].values
            weighted_values = df[cols_with_weight].values * weights[:, np.newaxis]
            aggregated_values = np.sum(weighted_values, axis=0) / np.sum(weights)
            result.update({col: aggregated_values[i] for i, col in enumerate(cols_with_weight)})

    # Sum columns that are not in the agg_dict
    for col in df.columns:
        if col not in agg_dict:
            if isinstance(df[col].dtype, CategoricalDtype):
                if cat_treatment == 'majority':
                    result[col] = df[col].mode()[0]  # Get the majority category
                elif cat_treatment == 'proportions':
                    proportions = df[col].value_counts(normalize=True).to_dict()
                    if proportions_as_columns:
                        for cat, prop in proportions.items():
                            result[f"{col}_{cat}"] = prop
                    else:
                        result[col] = proportions
            else:
                result[col] = df[col].sum()

    # Create a DataFrame from the result dictionary
    aggregated_df = pd.DataFrame([result])

    # Manage the final column order
    if proportions_as_columns:
        # loop through the columns and add them, extending with cat classes
        final_columns = []
        for col in df.columns:
            if col in result:
                final_columns.append(col)
            elif isinstance(df[col].dtype, CategoricalDtype) and cat_treatment == 'proportions':
                for cat in df[col].cat.categories:
                    final_columns.append(f"{col}_{cat}")
        aggregated_df = aggregated_df[final_columns]
    else:
        # Ensure the columns are in the same order as the incoming DataFrame
        aggregated_df = aggregated_df[df.columns]

    return aggregated_df