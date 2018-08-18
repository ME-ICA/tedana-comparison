"""
Utility functions
"""
import os.path as op

import numpy as np
from bids.grabbids import BIDSLayout


def get_preproc_data(dset, cfg, data_dir='../data'):
    """
    Get echo-sorted list of fMRIPrep-preprocessed files and echo times in ms.
    """
    keys = ['subject', 'run', 'task']
    data_dir = op.abspath(data_dir)
    dset_dir = op.join(data_dir, dset, cfg['version'], 'uncompressed')
    layout = BIDSLayout(dset_dir)

    kwargs = {k: cfg[k] for k in keys if k in cfg.keys()}

    echoes = sorted(layout.get_echoes())
    in_files = []
    echo_times = []
    for i, echo in enumerate(echoes):
        # Get echo time in ms
        orig_file = layout.get(modality='func', type='bold',
                               extensions='nii.gz', echo=echo, **kwargs)
        if len(orig_file) != 1:
            raise Exception('{0} files found for echo {1} of {2}: '
                            '{3}'.format(len(orig_file), echo, dset, cfg))

        orig_file = orig_file[0].filename
        metadata = layout.get_metadata(orig_file)
        echo_time = metadata['EchoTime'] * 1000
        echo_times.append(np.round(echo_time, 3))  # be wary, but seems okay

        # Get preprocessed file associated with echo
        func_file = orig_file.replace(dset_dir,
                                      op.join(dset_dir, 'derivatives/fmriprep'))
        func_file = func_file.replace('bold.nii.gz',
                                      'bold_space-MNI152NLin2009cAsym_preproc.nii.gz')

        if not op.isfile(func_file):
            # print('File DNE: {0}'.format(func_file))
            pass
        in_files.append(func_file)

        if i == 0:
            mask_file = func_file.replace('_preproc.nii.gz', '_brainmask.nii.gz')

        if not op.isfile(mask_file):
            # print('File DNE: {0}'.format(mask_file))
            pass
    return in_files, echo_times, mask_file
