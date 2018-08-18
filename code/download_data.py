# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Download datasets for comparison from OpenNeuro.
"""
import os.path as op
from nistats.datasets import (fetch_openneuro_dataset_index,
                              fetch_openneuro_dataset, select_from_index)


def download_dataset(dataset_version):
    """
    Download a dataset from OpenNeuro using nistats functions.
    """
    _, urls = fetch_openneuro_dataset_index(dataset_version=dataset_version)
    urls = select_from_index(urls, n_subjects=1)
    temp_urls1 = [url for url in urls if 'derivatives' not in url]
    temp_urls2 = [url for url in urls if 'derivatives/fmriprep' in url]
    urls = temp_urls1 + temp_urls2
    _, _ = fetch_openneuro_dataset(urls=urls, dataset_version=dataset_version,
                                   data_dir=op.abspath('../data/'))


if __name__ == "__main__":
    DSETS = ['ds000210_R1.0.1', 'ds000254_R1.0.0', 'ds000258_R1.0.0']
    for dset in DSETS:
        download_dataset(dset)
