from create_folder_structure import create_folder_structure
from catalog_holo_tcr_structures import catalog_holo_tcr_structures
from catalog_apo_pmhc_structures import catalog_apo_pmhc_structures
from catalog_apo_tcr_structures import catalog_apo_tcr_structures


def stub_function():
    pass

download_holo_tcr_structures = stub_function
download_holo_mhc_structures = stub_function
align_mhc_holo_structures = stub_function
align_tcr_holo_structures = stub_function
process_rmsds = stub_function
create_plots = stub_function
create_images = stub_function
build_datasets = stub_function

steps = {
    '1': {
        'function': create_folder_structure,
        'title_template':'the apo TCR structures from histo.',
        'title_verb': ['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '2': {
        'function': catalog_holo_tcr_structures,
        'title_template':'the apo TCR structures from histo.',
        'title_verb': ['Cataloguing','Catalogs'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '3': {
        'function': catalog_apo_pmhc_structures,
        'title_template':'the apo pMHC structures from histo.',
        'title_verb': ['Cataloguing','Catalogs'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '4': {
        'function': catalog_apo_tcr_structures,
        'title_template':'the apo TCR structures from stcrdab.',
        'title_verb': ['Cataloguing','Catalogs'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': False
    },
    '5': {
        'function': download_holo_tcr_structures,
        'title_template':'the holo TCR structures from STCRDab.',
        'title_verb': ['Downloading','Downloads'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '6': {
        'function': align_mhc_holo_structures,
        'title_template':'the the holo pMHC structures against the apo structures.',
        'title_verb': ['Aligning','Aligns'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '7': {
        'function': align_tcr_holo_structures,
        'title_template':'the the holo TCR structures against the apo structures.',
        'title_verb': ['Aligning','Aligns'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '8': {
        'function': process_rmsds,
        'title_template':'the RMSDs for the apo vs holo structures.',
        'title_verb': ['Processing','Processes'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '9': {
        'function': create_plots,
        'title_template':'the relevant plots for the structures.',
        'title_verb': ['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '10': {
        'function': create_images,
        'title_template':'the relevant images for the structures.',
        'title_verb': ['Creating','Creates'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    },
    '11': {
        'function': build_datasets,
        'title_template':'the datasets on apo/holo pMHC:TCR for the comparisons microservice.',
        'title_verb': ['Building','Builds'],
        'is_multi': False,
        'multi_param': None,
        'multi_options': None,
        'has_progress': True
    }
}