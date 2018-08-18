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
            cmd = ('meica.py -e {0} -d {1} --prefix {2} '
                   '--OVERWRITE'.format(te_str, file_str, out_dir))
            # subprocess.call(cmd.split(' '))

            # Run v2.5 of the component selection algorithm
            out_dir = op.join(ds_dir, 'derivatives/tedana_v2.5/')
            tedana_workflow(data=files, tes=tes, mask=mask_file,
                            out_dir=out_dir, component_algorithm='v2.5')

            # Run v3.2 of the component selection algorithm
            out_dir = op.join(ds_dir, 'derivatives/tedana_v3.2/')
            tedana_workflow(data=files, tes=tes, mask=mask_file,
                            out_dir=out_dir, component_algorithm='v3.2')
