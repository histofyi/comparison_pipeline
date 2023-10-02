from typing import Dict, List

from helpers.files import read_json, write_json

import pandas as pd

from localpdb import PDB

from fuzzywuzzy import fuzz



def get_tcr_pdbcode_list() -> List:
    """
    This function queries STCRDab using pandas to generate a list of pdbcodes contained within the resource

    Returns:
      List: a list of pdb codes relating to structures in STCRDab
    """
    df = pd.read_html('http://opig.stats.ox.ac.uk/webapps/stcrdab/Browser?all=true')[0]
    pdb_codes = pd.concat([df['PDB']])
    return pdb_codes



def catalog_apo_tcr_structures(**kwargs):

    verbose = kwargs['verbose']
    config = kwargs['config']
    output_path = kwargs['output_path']

    holo_structures = read_json(f"{output_path}/data/holo_structures.json")
    holo_tcr_sequences = read_json(f"{output_path}/data/holo_tcr_sequences.json")
    holo_complexes = read_json(f"{output_path}/data/holo_complexes.json")

    tcr_pdb_codes = get_tcr_pdbcode_list()

    lpdb = PDB(db_path=config['PATHS']['LOCALPDB_PATH'])

    likely_matches = {}
    possible_matches = {}

    apo_structures = {}

    print (f"{len(tcr_pdb_codes)} TCR structure pdb codes retrieved from STCRDab.")

    non_holo_tcr_structures = [pdb_code for pdb_code in tcr_pdb_codes if pdb_code not in holo_complexes]

    print (f"{len(non_holo_tcr_structures)} are not holo structures (as defined from histo search)")

    for pdb_code in non_holo_tcr_structures:
        entries = lpdb.chains[lpdb.chains.index.str.contains(pdb_code)]
        chains = [chain for chain in entries.index]
        
        chain_list = []

        for chain in chains:
            sequence = entries.loc[chain]['sequence']
            if sequence not in chain_list and len(sequence) > 100 and len(sequence) < 300:
                if len(chain_list) == 0:
                    chain_list.append(sequence)
                else:
                    for test_sequence in chain_list:
                        ratio = fuzz.ratio(test_sequence, sequence) / 100
                        if ratio < 0.9:
                            chain_list.append(sequence)

        matches = {}

        for chain_sequence in chain_list:
            for test_pdb_code in holo_tcr_sequences:
                for test_chain in ['tcr_alpha', 'tcr_beta']:
                    if holo_tcr_sequences[test_pdb_code][test_chain]:
                        test_sequence = holo_tcr_sequences[test_pdb_code][test_chain]['sequence']
                        ratio = fuzz.ratio(test_sequence, chain_sequence) / 100
                        if ratio > 0.98:
                            if not test_chain in matches:
                                matches[test_chain] = {
                                    'sequence': chain_sequence,
                                    'ratio': ratio,
                                    'test_pdb_code': test_pdb_code
                                }
                                print (f"Apo structure {pdb_code} has a {ratio}% match to holo {test_pdb_code} {test_chain}")
                            break
                        elif chain_sequence in test_sequence or test_sequence in chain_sequence:
                            if not test_chain in matches:
                                matches[test_chain] = {
                                    'sequence': chain_sequence,
                                    'ratio': ratio, 
                                    'test_pdb_code': test_pdb_code
                                }
                                print (f"Apo structure {pdb_code} contains match to holo {test_pdb_code} {test_chain}")
                            break
        if len(matches) == 2:
            print (f"{pdb_code} has both chains matched")
            print ('')
            likely_matches[pdb_code] = matches
        elif len(matches) == 1:
            print (f"{pdb_code} has one chain matched")
            print ('')
            possible_matches[pdb_code] = matches

    print (f"{len(likely_matches)} likely matches")
    print (f"{len(possible_matches)} possible matches")





