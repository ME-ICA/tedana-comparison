"""
Run meica.py
"""
import json
# import subprocess
import os.path as op

from utils import get_preproc_data


if __name__ == '__main__':
    with open('dset_config.json', 'r') as fo:
        CONFIG = json.load(fo)

    DATA_DIR = op.abspath('../data')

    for dset_name in CONFIG.keys():
        for item_cfg in CONFIG[dset_name]:
            files, tes = get_preproc_data(dset_name, item_cfg, DATA_DIR)
            te_str = ','.join([str(te) for te in tes])
            file_str = ','.join(files)
            ds_dir = op.join(DATA_DIR, dset_name, item_cfg['version'],
                             'uncompressed')
            out_dir = op.join(ds_dir, 'derivatives/afni/')
            cmd = ('meica.py -e {0} -d {1} --prefix {2} '
                   '--OVERWRITE'.format(te_str, file_str, out_dir))
            print(cmd)
            # subprocess.call(cmd.split(' '))
