# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Download datasets for comparison from OpenNeuro.
"""
import json
import shutil
import os.path as op

from nistats.datasets import (fetch_openneuro_dataset_index,
                              fetch_openneuro_dataset, select_from_index)


def download_dataset(cfg):
    """
    Download a dataset from OpenNeuro using nistats functions.
    """
    dataset_version = cfg['version']

    _, urls = fetch_openneuro_dataset_index(dataset_version=dataset_version)

    # Just download based on subject for now.
    # Don't want to accidentally ignore anats or field maps.
    sub = 'sub-{0}'.format(cfg['subject'])
    urls = select_from_index(urls)
    temp_urls1 = [url for url in urls if ('derivatives' not in url) and
                  (sub in url)]
    temp_urls2 = [url for url in urls if ('derivatives' not in url) and
                  ('sub-' not in url)]
    urls = sorted(list(set(temp_urls1 + temp_urls2)))

    _, _ = fetch_openneuro_dataset(urls=urls, dataset_version=dataset_version,
                                   data_dir=op.abspath('../data/'))


if __name__ == '__main__':
    with open('dset_config.json', 'r') as fo:
        CONFIG = json.load(fo)

    for dset in CONFIG.keys():
        for item_cfg in CONFIG[dset]:
            download_dataset(item_cfg)

        dataset_version = item_cfg['version']
        dataset = dataset_version.split('_')[0]
        dset_dir = op.abspath('../data/{0}/{1}/uncompressed'
                              '/'.format(dataset, dataset_version))
        temp = op.abspath('../data/temp/')
        dest = op.abspath('../data/{0}/'.format(dataset))
        shutil.move(dset_dir, temp)
        shutil.rmtree(dest)
        shutil.move(temp, dest)
