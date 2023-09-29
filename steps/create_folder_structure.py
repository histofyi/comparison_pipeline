from typing import Dict, List, Tuple

from helpers.files import create_folder




def create_folder_structure(**kwargs) -> Dict:
    """
    This function creates the output folder structure for the pipeline.

    Args:
        **kwargs: Arbitrary keyword arguments.

    Returns:
        Dict: A dictionary containing the output of the action.

    Keyword Args:
        verbose (bool): Whether or not to print verbose output.
        config (dict): The configuration dictionary.
        output_path (str): The path to the output folder.
    """
    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']

    # Create the folder structure as a set of folders in an array.
    folders = ['data', 'structures/holo_pmhc_tcr/raw', 'structures/apo_pmhc/raw', 'structures/apo_tcr/raw', 'structures/holo_pmhc_tcr/clean', 'structures/apo_pmhc/clean', 'structures/apo_tcr/clean']


    # Initialise the folder creation count.
    folder_creation_count = 0

    # Iterate through the folders and create them
    for folder in folders:    
        create_folder(f"{output_path}/{folder}", verbose)
        folder_creation_count += 1
    
    action_output = {
        'folders_processed':folder_creation_count
    }

    return action_output
