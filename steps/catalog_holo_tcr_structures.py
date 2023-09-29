from typing import Dict, List

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

    exclusions = read_json(f"input/exclusions.json")['holo']

    # Create the url for the histo API.
    holo_api_url = f"{config['CONSTANTS']['HISTO_BASE_SETS_API_URL']}/complex_types/class_i_with_peptide_and_alpha_beta_tcr"

    # Get the first page of data from the histo API, this will give us the number of pages to retrieve.
    r = requests.get(holo_api_url)
    data = r.json()['set']  
    page_numbers = data['pagination']['pages']

    # Initialise the list of holo TCR structures.
    holo_structures = {}
    holo_tcr_sequences = {}
    holo_complexes = {}

    # Initialise the structure count. This is the complete number of structures.
    holo_structure_count = 0
    # Initialise the complex count. This is the number of unique pMHC complexes.
    complex_count = 0
    # Initialise the exclusion count. This is the number of structures excluded from the analysis.
    exclusion_count = 0

    rejections = []

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

            tcr_details = {}
            for chain in ['tcr_alpha', 'tcr_beta']:

                if chain not in structure['assigned_chains']:
                    tcr_details[chain] = None
                else:
                    if 'subgroup' not in structure['assigned_chains'][chain]:
                        subgroup = None
                    else:
                        subgroup = structure['assigned_chains'][chain]['subgroup']
                    tcr_details[chain] = {
                        'sequence': structure['assigned_chains'][chain]['sequence'],
                        'subgroup': subgroup
                    }



            # Check if the structure is in the exclusions list. 
            # Structures are excluded for several reasons, including:
            # - the TCR binding in a non-canonical orientation
            # - technical issues with the structure, e.g. weird chain labels

            # If the structure is not in the exclusions list, add it to the list of holo structures.
            if pdb_code not in exclusions:

                holo_tcr_sequences[pdb_code] = tcr_details
                # Create a complex key, this is a compound key of the allele and peptide.
                complex_key = f"{allele}_{peptide.lower()}"

                holo_complexes[pdb_code] = complex_key
                
                # Check if the peptide is long enough to be a canonical peptide.
                if len(peptide) >= 8:

                    # We only want complexes with "normal" peptides, i.e. no weird amino acids or modifications.
                    correct_sequence_and_length = False

                    for peptide_chain in structure['peptide']:
                        if 'correct_sequence_and_length' in structure['peptide'][peptide_chain]['features']:
                            correct_sequence_and_length = True
                        features = structure['peptide'][peptide_chain]['features']
                    
                    # If the peptide is a "normal" peptide.
                    if correct_sequence_and_length:

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
                        # Add the structure to the list of rejections, have a look at these, they might be useful to understand later
                        rejections.append({'pdb_code':pdb_code, 'features':features})
            else:
                # Increment the exclusion count.
                exclusion_count += 1
                

    # Write the holo structures to file.
    write_json(f"{output_path}/data/holo_structures.json", holo_structures, verbose, pretty=True)

    # Write the holo TCR sequences to file.
    write_json(f"{output_path}/data/holo_tcr_sequences.json", holo_tcr_sequences, verbose, pretty=True)

    # Write the holo complexes to file.
    write_json(f"{output_path}/data/holo_complexes.json", holo_complexes, verbose, pretty=True)

    # Create the action output.
    action_output = {
        'holo_structures_processed':holo_structure_count,
        'complexes_processed':complex_count, 
        'exclusions_processed':exclusion_count,
        'rejection_count':len(rejections),
        'rejections':rejections
    }

    return action_output