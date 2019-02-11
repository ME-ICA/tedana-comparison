# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Run pipelines on all datasets for comparison.
"""
import json
# import subprocess
import os.path as op

from tedana.workflows import tedana_workflow

from utils import get_preproc_data


if __name__ == '__main__':
    with open('dset_config.json', 'r') as fo:
        CONFIG = json.load(fo)

    DATA_DIR = op.abspath('../data')

    for dset_name in CONFIG.keys():
        for item_cfg in CONFIG[dset_name]:
            files, tes, mask_file = get_preproc_data(dset_name, item_cfg,
                                                     DATA_DIR)
            te_str = ','.join([str(te) for te in tes])
            file_str = ','.join(files)
            ds_dir = op.join(DATA_DIR, dset_name, item_cfg['version'],
                             'uncompressed')

            # Run AFNI's meica.py
            out_dir = op.join(ds_dir, 'derivatives/afni/')
            meica_script = op.abspath('../dependencies/afni/meica.py')
            cmd = ('{0} -e {1} -d {2} --prefix {3} '
                   '--OVERWRITE'.format(meica_script, te_str, file_str,
                                        out_dir))
            # subprocess.call(cmd.split(' '))

            # Run ME-ICA/me-ica
            out_dir = op.join(ds_dir, 'derivatives/kundu_v3.2/')
            meica_script = op.abspath('../dependencies/me-ica/meica.py')
            cmd = ('{0} -e {1} -d {2} --prefix {3} '
                   '--OVERWRITE'.format(meica_script, te_str, file_str,
                                        out_dir))
            # subprocess.call(cmd.split(' '))

            # Run ME-ICA/tedana
            # Run v2.5 of the component selection algorithm
            out_dir = op.join(ds_dir, 'derivatives/tedana_v2.5/')
            tedana_workflow(data=files, tes=tes, mask=mask_file,
                            out_dir=out_dir)
