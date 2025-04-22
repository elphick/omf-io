import logging
from pathlib import Path
import omf

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def write_omf_element(element: omf.base.ProjectElement, output_file: Path, overwrite: bool = False):
    """
    Write an OMF element to a file, handling new or existing files.

    Args:
        element (omf.base.ProjectElement): The OMF element to write.
        output_file (Path): The file path to save the OMF element.
        overwrite (bool): Whether to overwrite the file if it exists.

    Raises:
        FileExistsError: If the file exists and overwrite is False.
    """

    # Validate the element
    element.validate()

    if output_file.exists():
        if not overwrite:
            raise FileExistsError(f"The file '{output_file}' already exists. Use overwrite=True to overwrite it.")
        logger.info(f"Overwriting existing file: {output_file}")
    else:
        logger.info(f"Creating new file: {output_file}")
        # Ensure the directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        # Create a new OMF project
        project = omf.Project(name=element.name)
        omf.save(project, str(output_file))

    # Write the element to the file
    project = omf.load(str(output_file))
    # Check if the element already exists in the project
    element_names = [element.name for e in project.elements]
    if element.name in element_names:
        if not overwrite:
            raise FileExistsError(f"Element '{element.name}' already exists in the project. Use overwrite=True to replace it.")
        else:
            logger.warning(f"Element '{element.name}' already exists in the project. It will be replaced.")
            # Remove the existing element
            project.elements = [e for e in project.elements if e.name != element.name]
    project.elements.append(element)
    omf.save(project=project, filename=str(output_file), mode='w')
    logger.info(f"OMF file written to: {output_file}")
