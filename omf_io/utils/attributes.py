import omf

def generate_omf_attributes(data):
    """
    Generate a list of OMF attributes from a DataFrame.

    Args:
        data (pd.DataFrame): DataFrame containing attributes and their values.

    Returns:
        list: A list of OMF attributes.
    """
    attributes = []
    for attr_name in data.columns:
        # skip the color column
        if attr_name.endswith('_color'):
            continue
        if f"{attr_name}_color" in data.columns:
            # Create a CategoryColormap attribute
            attributes.append(
                omf.attribute.CategoryAttribute(
                    array=list(range(len(data[attr_name].unique()))),
                    categories=omf.attribute.CategoryColormap(
                        indices=list(range(len(data[attr_name].unique()))),
                        values=list(data[attr_name].unique()),
                        colors=data[f"{attr_name}_color"].values.tolist(),
                    ),
                    location='vertices',
                )
            )
        elif data[attr_name].dtype == 'object' or data[attr_name].dtype.name == 'category':
            # Handle non-numeric attributes (e.g., strings) as CategoryAttribute without colors
            attributes.append(
                omf.attribute.CategoryAttribute(
                    array=data[attr_name].values,
                    categories=omf.attribute.CategoryColormap(
                        indices=list(range(len(data[attr_name].unique()))),
                        values=list(data[attr_name].unique())
                    )
                )
            )
        else:
            # Create a NumericAttribute for numeric cases
            attributes.append(
                omf.attribute.NumericAttribute(
                    array=data[attr_name].values
                )
            )
    return attributes