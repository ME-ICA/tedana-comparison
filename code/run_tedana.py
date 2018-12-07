# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Run pipelines on all datasets for comparison.


sourceTEs: 0 (all echoes), -1 (opt com)
combmode: t2s, linear (depending on tedana-dev opinions on ME-ICA/tedana#93)
gscontrol: None, gsr, t1c, gsr & t1c
tedpca: mle, kundu, kundu-stabilize
wvpca: on and off
tedort: on and off
"""
import re
import json
import os.path as op

from tedana.workflows import tedana_workflow


def make_str(dict_):
    """
    Make name string from dictionary of values.
    """
    ste_name_dict = {0: 'catd', -1: 'optcom'}
    lst = []
    for key, value in dict_.items():
        if key == 'ste':
            # we don't want that -1 because of the hyphen
            value = ste_name_dict[value]

        # Join list arguments (i.e., gscontrol) with ampersand
        if isinstance(value, list):
            value = '&'.join(value)

        lst.append('{0}-{1}'.format(str(key), str(value)))
    str_ = '_'.join(lst)
    return str_


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
    tes = [te * 1000 for te in tes]
    sub = re.findall('sub-[0-9a-zA-Z]+_', files[0])[0][:-1]
    ds_dir = files[0][:files[0].index(sub)]

    for combmode in ['t2s', 'linear']:
        for gscontrol in [['t1c'], ['gsr', 't1c']]:
            for ste in [-1, 0]:
                for tedort in [False, True]:
                    for tedpca in ['mle', 'kundu']:
                        for wvpca in [False, True]:
                            args = {'combmode': combmode,
                                    'gscontrol': gscontrol,
                                    'ste': ste,
                                    'tedort': tedort,
                                    'tedpca': tedpca,
                                    'wvpca': wvpca}
                            name = make_str(args)
                            name = name + '_seed-{0:03d}'.format(seed)
                            out_dir = op.join(ds_dir, 'derivatives', name, sub, 'func')
                            tedana_workflow(data=files, tes=tes, fixed_seed=seed,
                                            out_dir=out_dir, debug=True, **args)


def run_dset(dset_dict):
    n_iterations = 1
    for sub in dset_dict.keys():
        for run in dset_dict[sub].keys():
            files = dset_dict[sub][run]['files']
            tes = dset_dict[sub][run]['echo_times']
            for seed in range(n_iterations):
                run_tedana(files, tes, seed)


if __name__ == '__main__':
    with open('all_files.json', 'r') as fo:
        all_dict = json.load(fo)

    for dset in all_dict.keys():
        dataset_dict = all_dict[dset]
        run_dset(dataset_dict)
