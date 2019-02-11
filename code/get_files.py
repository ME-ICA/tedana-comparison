# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Compile list of files in datasets for processing
"""
import json
import os.path as op
from bids.layout import BIDSLayout


def get_files():
    with open('dset_config.json', 'r') as fo:
        CONFIG = json.load(fo)

    DATA_DIR = op.abspath('/home/data/nbc/external-datasets/ds001491/')

    all_info = {}
    for dset_name in list(CONFIG.keys())[:3]:
        layout = BIDSLayout(op.join(DATA_DIR, dset_name))
        cfg = CONFIG[dset_name]
        task = cfg['task']
        dset_info = {}
        for sub in layout.get_subjects():
            runs = layout.get_runs(subject=sub, task=task)
            sub_info = {}
            for run in runs:
                run_info = {}
                run_info['files'] = []
                run_info['echo_times'] = []
                for echo in sorted(layout.get_echoes(subject=sub, task=task,
                                                     run=run)):
                    raw_files = layout.get(subject=sub, task=task, run=run,
                                           echo=echo, extensions='.nii.gz')
                    preproc_files = layout.get(subject=sub, task=task, run=run,
                                               root='afni-step1', echo=echo,
                                               extensions='.nii.gz',
                                               desc='realign')
                    preproc_files = raw_files[:]
                    if len(preproc_files) != 1:
                        print(preproc_files)
                        raise Exception('BAD')

                    # Replace filename with path when using new version of bids
                    run_info['files'].append(preproc_files[0].filename)
                    metadata = layout.get_metadata(preproc_files[0].filename)
                    run_info['echo_times'].append(metadata['EchoTime'])
                sub_info[run] = run_info
            dset_info[sub] = sub_info
        all_info[dset_name] = dset_info

    with open('all_files.json', 'w') as fo:
        json.dump(all_info, fo, indent=4, sort_keys=True)


if __name__ == '__main__':
    get_files()
