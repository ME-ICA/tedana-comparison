"""
Generate some plots
"""
import os
import os.path as op
from os import remove
from glob import glob

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import nibabel as nib
from nipype.algorithms import confounds as nac
from nilearn import plotting, image
from nilearn.masking import compute_epi_mask
from niworkflows.viz import plots

color_dict = {'accepted': 'green',
              'midk': 'yellow',
              'rejected': 'red',
              'ignored': 'gray'}


def plot_spectra(ct_df):
    fig, ax = plt.subplots(figsize=(10, 10))

    for clf in ct_df['classification'].unique():
        red_df = ct_df.loc[ct_df['classification'] == clf]
        if red_df.shape[0] > 0:
            kappas = red_df['kappa']
            rhos = red_df['rho']
            varex = red_df['normalized variance explained']
            ax.scatter(x=kappas, y=rhos, color=color_dict.get(clf, 'gray'), alpha=0.5,
                       edgecolors='black', label=clf, s=(varex*50)+25)

    ax.set_xlabel('Kappa')
    ax.set_ylabel('Rho')
    legend = ax.legend(frameon=True)
    for legend_handle in legend.legendHandles:
        legend_handle.set_sizes([50])

    return fig, ax


def plot_image(img, vmin=None, vmax=None):
    if isinstance(img, str):
        img = nib.load(img)

    dat = img.get_data()
    if vmin:
        dat[dat < vmin] = np.max((vmin, 0))
        vmin = np.min(dat)
    if not vmax:
        vmax = np.max(dat)

    coords = np.arange(-10, 62, 2, int)
    n_cols = 8
    n_rows = int(len(coords) / n_cols)
    start = 0
    end = n_cols

    fig, axes = plt.subplots(nrows=n_rows, figsize=(2*n_cols, 4*n_rows))
    for row in range(n_rows):
        row_coords = coords[start:end]
        plotting.plot_stat_map(
            stat_map_img=img, bg_img=None, display_mode='z',
            cut_coords=row_coords, axes=axes[row],
            annotate=False, vmax=vmax)
        start += n_cols
        end += n_cols
    return fig, axes


def plot_anatomical(img):
    if isinstance(img, str):
        img = nib.load(img)

    coords = np.arange(-10, 62, 2, int)
    n_cols = 8
    n_rows = int(len(coords) / n_cols)
    start = 0
    end = n_cols

    fig, axes = plt.subplots(nrows=n_rows, figsize=(2*n_cols, 4*n_rows))
    for row in range(n_rows):
        row_coords = coords[start:end]
        plotting.plot_anat(
            img, display_mode='z',
            cut_coords=row_coords, axes=axes[row],
            annotate=False)
        start += n_cols
        end += n_cols
    return fig, axes


def generate_plots(tedana_dir, out_dir=None):
    # TEDPCA
    comptable_file = op.join(tedana_dir, 'comp_table_pca.txt')
    comptable = pd.read_csv(comptable_file, sep='\t')
    fig, ax = plot_spectra(comptable)
    fig.savefig(op.join(out_dir, 'tedpca_metrics.png'), dpi=400)

    # TEDICA
    comptable_file = op.join(tedana_dir, 'comp_table_ica.txt')
    comptable = pd.read_csv(comptable_file, sep='\t')
    fig, ax = plot_spectra(comptable)
    fig.savefig(op.join(out_dir, 'tedica_metrics.png'), dpi=400)

    # T2*
    f = op.join(tedana_dir, 't2sv.nii')
    m = compute_epi_mask(f).get_data()
    fig, ax = plot_image(f, vmin=0, vmax=100)
    fig.savefig(op.join(out_dir, 't2s.png'), dpi=400)

    # S0
    f = op.join(tedana_dir, 's0v.nii')
    fig, ax = plot_image(f)
    fig.savefig(op.join(out_dir, 's0.png'), dpi=400)

    # OC
    f = op.join(tedana_dir, 'ts_OC.nii')

    # OC TSNR
    tsnr = nac.TSNR()
    tsnr.inputs.in_file = f
    res = tsnr.run()
    fig, ax = plot_image(res.outputs.tsnr_file)
    fig.savefig(op.join(out_dir, 'optcom_tsnr.png'), dpi=400)

    # OC Carpet
    fig, ax = plt.subplots(figsize=(16, 6))
    plots.plot_carpet(f, m, subplot=ax)
    fig.savefig(op.join(out_dir, 'optcom_carpet.png'), dpi=400)

    # MEDN
    f = op.join(tedana_dir, 'dn_ts_OC.nii')
    img = nib.load(f)

    # MEDN TSNR
    tsnr = nac.TSNR()
    tsnr.inputs.in_file = f
    res = tsnr.run()
    fig, ax = plot_image(res.outputs.tsnr_file)
    fig.savefig(op.join(out_dir, 'medn_tsnr.png'), dpi=400)

    # MEDN STD
    data = img.get_data()
    data = np.std(data, axis=-1)
    img2 = nib.Nifti1Image(data, img.affine)
    fig, ax = plot_image(img2)
    fig.savefig(op.join(out_dir, 'medn_std.png'), dpi=400)

    # MEDN Mean
    data = img.get_data()
    data = np.mean(data, axis=-1)
    img2 = nib.Nifti1Image(data, img.affine)
    fig, ax = plot_anatomical(img2)
    fig.savefig(op.join(out_dir, 'medn_mean.png'), dpi=400)

    # MEDN Carpet
    fig, ax = plt.subplots(figsize=(16, 6))
    plots.plot_carpet(f, m, subplot=ax)
    fig.savefig(op.join(out_dir, 'medn_carpet.png'), dpi=400)

    # Cleanup
    remove(res.outputs.mean_file)
    remove(res.outputs.stddev_file)
    remove(res.outputs.tsnr_file)


if __name__ == '__main__':
    ted_dir = '/Users/tsalo/Documents/tsalo/tedana-comparison/sandbox/TED.p06.mlepca/'
    out = '/Users/tsalo/Documents/tsalo/tedana-comparison/reports/figures/'
    generate_plots(ted_dir, out)
