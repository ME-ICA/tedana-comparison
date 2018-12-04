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
# import subprocess
import os.path as op

from tedana.workflows import tedana_workflow

from utils import get_preproc_data


def run_tedana(files, tes, seed):
    tes = [te * 1000 for te in tes]
    sub = re.findall('sub-[0-9a-zA-Z]+_', files[0])[0][:-1]
    ds_dir = files[0][:files[0].index(sub)]

    # Baseline
    # tedpca=mle, gscontrol=None, combmode=t2s, sourceTEs=-1, no wvpca, no tedort
    name = ('tedana_tedpca-mle_gscontrol-None_combmode-t2s_ste-optcom_'
            'wvpca-False_tedort-False_seed-{0:03d}'.format(seed))
    out_dir = op.join(ds_dir, 'derivatives', name, sub, 'func')
    tedana_workflow(data=files, tes=tes, tedpca='mle', gscontrol=None,
                    combmode='t2s', ste=-1, wvpca=False, tedort=False,
                    out_dir=out_dir)

    # Fit models to concatenated data (sourceTEs = 0)
    # tedpca=mle, gscontrol=None, combmode=t2s, sourceTEs=0, no wvpca, no tedort
    name = ('tedana_tedpca-mle_gscontrol-None_combmode-t2s_ste-all_'
            'wvpca-False_tedort-False_seed-{0:03d}'.format(seed))
    out_dir = op.join(ds_dir, 'derivatives', name, sub, 'func')
    tedana_workflow(data=files, tes=tes, tedpca='mle', gscontrol=None,
                    combmode='t2s', ste=0, wvpca=False, tedort=False,
                    out_dir=out_dir)
