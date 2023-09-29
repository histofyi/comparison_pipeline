from typing import Dict, List

from helpers.files import read_json, write_json

import requests


def fetch_histo_data_page(config:Dict, peptide_sequence:str, allele_slug:str) -> List:
    # Create the url for the histo API.
    peptide_api_url = f"{config['CONSTANTS']['HISTO_BASE_SETS_API_URL']}/peptide_sequences/{peptide_sequence.lower()}"

    # Initialise the list of allele filtered structures.
    allele_filtered_structures = []

    # Request the data from the API.
    r = requests.get(peptide_api_url)
    data = r.json()['set']

    page_numbers = data['pagination']['pages']

    # TODO - Handle multiple pages of data, currently we don't need to
    if len(page_numbers) > 1:
        print (f"WARNING: More than one page of data for peptide {peptide_sequence}.")

    for structure in data['members']:
        if structure['allele']['alpha']['slug'] == allele_slug:
            if structure['complex_type'] == 'class_i_with_peptide':
                allele_filtered_structures.append(structure)
    return allele_filtered_structures


def catalog_apo_pmhc_structures(**kwargs) -> Dict:
    """
    This function catalogues the apo pMHC structures from histo.

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

    # Read the list of complexes with a holo pMHC:TCR structure.
    holo_structures = read_json(f"{output_path}/data/holo_structures.json")

    apo_pmhc_structures = {}
    no_apo_pmhc_structures = []

    complex_count = 0
    structure_count = 0
    removed_structures = []
    # Iterate over the complexes.
    for complex_key in holo_structures:

        structure_complex = holo_structures[complex_key]
        allele_slug = structure_complex['allele']
        peptide = structure_complex['peptide']

        complex_apo_structures = fetch_histo_data_page(config, peptide, allele_slug)

        

        if len(complex_apo_structures) == 0:
            no_apo_pmhc_structures.append(complex_key)
            filtered_apo_structures = []

        else:
            filtered_apo_structures = []
            for structure in complex_apo_structures:

                correct_sequence_and_length = False

                for peptide_chain in structure['peptide']:
                    if 'correct_sequence_and_length' in structure['peptide'][peptide_chain]['features']:
                        correct_sequence_and_length = True
                    features = structure['peptide'][peptide_chain]['features']
                
                if correct_sequence_and_length:
                    filtered_apo_structures.append({'pbd_code':structure['pdb_code'], 'resolution':structure['resolution']})
                    structure_count += 1
                else:
                    removed_structures.append({'pbd_code':structure['pdb_code'], 'features':features})

            if len(filtered_apo_structures) == 0:
                no_apo_pmhc_structures.append(complex_key)
            else:
                if complex_key not in apo_pmhc_structures:
                    apo_pmhc_structures[complex_key] = {
                        'structures':filtered_apo_structures
                    }
                complex_count += 1
        print (f"For {allele_slug}/{peptide} there are {len(filtered_apo_structures)} apo structures.")

    write_json(f"{output_path}/data/apo_pmhc_structures.json", apo_pmhc_structures, verbose=verbose, pretty=True)
    write_json(f"{output_path}/data/missing_apo_pmhc_structures.json", no_apo_pmhc_structures, verbose=verbose, pretty=True)

