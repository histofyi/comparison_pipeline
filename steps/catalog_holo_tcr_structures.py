from typing import Dict, List, Tuple

from helpers.files import read_json, write_json

import requests


def fetch_histo_data_page(api_url:str, page_number:int) -> List:
    """
    This function fetches a page of data from the histo API.
    """
    url = f"{api_url}?page_number={page_number}"
    r = requests.get(url)
    data = r.json()['set']['members']
    return data


def catalog_holo_tcr_structures(**kwargs) -> Dict:
    """
    This function catalogues the holo pMHC:TCR structures from histo.

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

    exclusions = read_json(f"input/exclusions.json")

    # Create the url for the histo API.
    holo_api_url = f"{config['CONSTANTS']['HISTO_BASE_SETS_API_URL']}/complex_types/class_i_with_peptide_and_alpha_beta_tcr"

    # Get the first page of data from the histo API, this will give us the number of pages to retrieve.
    r = requests.get(holo_api_url)
    data = r.json()['set']  
    page_numbers = data['pagination']['pages']

    # Initialise the list of holo TCR structures.
    holo_structures = {}

    # Initialise the structure count. This is the complete number of structures.
    holo_structure_count = 0
    # Initialise the complex count. This is the number of unique pMHC complexes.
    complex_count = 0
    # Initialise the exclusion count. This is the number of structures excluded from the analysis.
    exclusion_count = 0


    for page_number in page_numbers:

        print (f"Processing page {page_number}.")
        # Get the data for the page.
        structures = fetch_histo_data_page(holo_api_url, page_number)

        # Iterate through the structures and create a dictionary of complexes with holo structures.
        for structure in structures:
        
            # extract the data from the structure.
            pdb_code = structure['pdb_code']
            allele = structure['allele']['alpha']['slug']
            peptide = structure['assigned_chains']['peptide']['sequence']
            resolution = structure['resolution']

            # Check if the structure is in the exclusions list. 
            # Structures are excluded for several reasons, including:
            # - the TCR binding in a non-canonical orientation
            # - technical issues with the structure, e.g. weird chain labels

            # If the structure is not in the exclusions list, add it to the list of holo structures.
            if pdb_code not in exclusions:

                # Create a complex key, this is a compound key of the allele and peptide.
                complex_key = f"{allele}_{peptide.lower()}"

                # Check if the peptide is long enough to be a canonical peptide.
                if len(peptide) >= 8:

                    # Check if the complex is already in the list of holo structures.
                    if complex_key not in holo_structures:  
                        if verbose:
                            print (f"Found new complex {complex_key}.")
                        # If the complex is not in the list of holo structures, add it.
                        holo_structures[complex_key] = {
                            'allele':allele,
                            'peptide':peptide,
                            'structures':[]
                        }
                        # Increment the complex count.
                        complex_count += 1
                    # Add the structure to the list of holo structures.
                    holo_structures[complex_key]['structures'].append({
                        'pdb_code':pdb_code,
                        'resolution':resolution
                    })
                    # Increment the structure count.
                    holo_structure_count += 1
            else:
                # Increment the exclusion count.
                exclusion_count += 1
                

    # Write the holo structures to file.
    write_json(f"{output_path}/data/holo_structures.json", holo_structures, verbose, pretty=True)

    action_output = {
        'holo_structures_processed':holo_structure_count,
        'complexes_processed':complex_count, 
        'exclusions_processed':exclusion_count
    }

    return action_output