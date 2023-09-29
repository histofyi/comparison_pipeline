from typing import Dict, List, Tuple
import os

from helpers.files import read_json, write_json, create_folder, write_file


import requests






def download_apo_tcr_structures(**kwargs):
    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']

    holo_api_url = f"{config['CONSTANTS']['HISTO_BASE_SETS_API_URL']}/complex_types/class_i_with_peptide_and_alpha_beta_tcr"

    r = requests.get(holo_api_url)
    data = r.json()['set']  
    page_numbers = data['pagination']['pages']



    holo_structure_count = 0
    complex_count = 0

    print (page_numbers)
    print (output_path)

    action_output = {}

    return action_output