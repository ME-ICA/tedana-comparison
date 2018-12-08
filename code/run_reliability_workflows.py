# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Run base pipeline on one dataset many times.
"""
import re
import json
import os.path as op
from shutil import copyfile

from tedana.workflows import tedana_workflow


def run_tedana(files, tes, seed):
    """
    Run tedana workflow across a range of parameters

    Parameters
    ----------
    files : list of str
        Echo-specific preprocessed data files
    tes : list of floats
        Echo times in seconds
    seed : int
        Random seed
    """
    out_dir = '/scratch/tsalo006/reliability_analysis/tedana_outputs/'
    tes = [te * 1000 for te in tes]
    sub = re.findall('sub-[0-9a-zA-Z]+_', files[0])[0][:-1]
    ds_dir = files[0][:files[0].index(sub)]
    name = 'base_tedana_seed-{0:03d}'.format(seed)
    ted_dir = op.join(ds_dir, 'derivatives', name, sub, 'func')
    tedana_workflow(data=files, tes=tes, fixed_seed=seed,
                    out_dir=ted_dir, debug=True,
                    tedpca='mle', wvpca=False, combmode='t2s',
                    ste=-1, gscontrol=None)
    # Grab the files we care about
    log_file = op.join(ted_dir, 'runlog.tsv')
    out_log_file = op.join(out_dir, '{0}_seed-{1:03d}_log.tsv'.format(sub, seed))
    ct_file = op.join(ted_dir, 'comp_table_ica.txt')
    out_ct_file = op.join(out_dir, '{0}_seed-{1:03d}_comptable.txt'.format(sub, seed))
    dn_file = op.join(ted_dir, 'dn_ts_OC.nii')
    out_dn_file = op.join(out_dir, '{0}_seed-{1:03d}_denoised.nii'.format(sub, seed))
    copyfile(log_file, out_log_file)
    copyfile(ct_file, out_ct_file)
    copyfile(dn_file, out_dn_file)


def run_dset(dset_dict):
    n_iterations = 1000
    for sub in dset_dict.keys():
        for run in dset_dict[sub].keys():
            files = dset_dict[sub][run]['files']
            tes = dset_dict[sub][run]['echo_times']
            for seed in range(n_iterations):
                run_tedana(files, tes, seed)


if __name__ == '__main__':
    with open('ds01491_files.json', 'r') as fo:
        all_dict = json.load(fo)

    for dset in all_dict.keys():
        dataset_dict = all_dict[dset]
        run_dset(dataset_dict)
