from typing import Dict

from pipeline import Pipeline

from steps import steps

import toml

def run_pipeline(**kwargs) -> Dict:
    pipeline = Pipeline()

    pipeline.load_steps(steps)

    pipeline.run_step('1') # Create folder structure.
    #pipeline.run_step('2') # Download apo TCR structures from histo.
    #pipeline.run_step('3') # Download holo TCR structures from histo.
    #pipeline.run_step('4') # Download holo TCR structures from STCRDab.
    #pipeline.run_step('5') # Remove altlocs in structures.
    #pipeline.run_step('6') # Rename apo TCR structure.
    #pipeline.run_step('7') # Align holo pMHC structures against the apo structures.
    #pipeline.run_step('8') # Align holo TCR structures against the apo structures.
    #pipeline.run_step('9') # Process RMSDs.
    #pipeline.run_step('10') # Create plots.
    #pipeline.run_step('11') # Create images.
    #pipeline.run_step('12') # Build datasets.

    action_logs = pipeline.finalise()

    return action_logs

def main():

    output = run_pipeline()

if __name__ == '__main__':
    main()