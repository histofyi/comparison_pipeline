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

    folders = ['data', 'structures/holo_pmhc_tcr', 'structures/apo_pmhc', 'structures/apo_tcr']

    folder_creation_count = 0
    for folder in folders:    
        create_folder(f"{output_path}/folder", verbose)
        folder_creation_count += 1
    
    action_output = {
        'folders_processed':folder_creation_count
    }

    return action_output
