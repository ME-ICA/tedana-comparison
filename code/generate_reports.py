# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""
Generate reports for comparison.
"""
import os.path as op

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_component(ax, ts, comp_num, df):
    ax.plot(ts, color='black')
    ax.set_yticks([])
    ax.set_title('Component {0}'.format(comp_num))
    if df.loc[comp_num, 'classification'] == 'accepted':
        ax.set_facecolor('honeydew')
    elif df.loc[comp_num, 'classification'] == 'midk':
        ax.set_facecolor('lemonchiffon')
    elif df.loc[comp_num, 'classification'] == 'rejected':
        ax.set_facecolor('mistyrose')
    elif df.loc[comp_num, 'classification'] == 'ignored':
        ax.set_facecolor('gainsboro')


def plot_pca(meica_dir, mmix_file, comptable_file, label):
    """
    """
    # Plot component time series
    component_ts = np.loadtxt(mmix_file)
    ct_df = pd.read_csv(comptable_file, sep='\t')
    n_rows = int(np.ceil(component_ts.shape[0] / 2))

    fig, axes = plt.subplots(nrows=n_rows, ncols=2,
                             sharex=True, figsize=(14, 200))
    c = 0
    for i in range(n_rows):
        plot_component(axes[i, 0], component_ts[c, :], c, ct_df)
        c += 1
        if c < component_ts.shape[0]:
            plot_component(axes[i, 1], component_ts[c, :], c, ct_df)
            c += 1
        else:
            axes[i, 1].set_visible(False)

    axes[-1, 0].set_xlim(0, component_ts.shape[1]-1)
    axes[-1, 0].set_xticks([])
    fig.tight_layout()
    fig.savefig(op.join(meica_dir, 'figures/{0}_components.svg'.format(label)),
                dpi=400)

    # Plot Kappa, Rho, and variance explained
    fig, ax = plt.subplots(figsize=(10, 10))

    for clf in color_dict.keys():
        red_df = ct_df.loc[ct_df['classification'] == clf]
        if red_df.shape[0] > 0:
            kappas = red_df['kappa']
            rhos = red_df['rho']
            varex = red_df['variance explained (normalized)']
            ax.scatter(x=kappas, y=rhos, color=color_dict[clf], alpha=0.5,
                       edgecolors='black', label=clf, s=(varex*50)+25)

    ax.set_xlabel('Kappa')
    ax.set_ylabel('Rho')
    legend = ax.legend(frameon=True)
    for legend_handle in legend.legendHandles:
        legend_handle.set_sizes([50])

    fig.savefig(op.join(meica_dir, 'figures/{0}_metrics.svg'.format(label)),
                dpi=400)


def generate_report(meica_dir):
    # Plot PCA components
    mmix_file = op.join(meica_dir, 'mepca_mix.1D')
    comptable_file = op.join(meica_dir, 'comp_table_pca.txt')
    plot_decomp(meica_dir, mmix_file, comptable_file, 'pca')

    # Plot ICA components
    mmix_file = op.join(meica_dir, 'meica_mix.1D')
    comptable_file = op.join(meica_dir, 'comp_table_ica.txt')
    plot_decomp(meica_dir, mmix_file, comptable_file, 'ica')


if __name__ == '__main__':
    pass
