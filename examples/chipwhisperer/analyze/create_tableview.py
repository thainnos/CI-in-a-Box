#!/usr/bin/python3

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

global_mean_diffs = np.load('../analyze/results/global_mean_diffs.npy')
global_mean_diffs_hex = np.load('../analyze/results/global_mean_diffs_hex.npy')
color_mask = np.load('../analyze/results/color_mask.npy')

num_rows = 10
num_subkeys = 16

fig, ax = plt.subplots(figsize=(20, 15))
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top')

my_cmap = plt.cm.get_cmap('BuGn_r').copy()
my_cmap.set_bad('#D22B31')  # color of mask on heatmap

annotations = (np.asarray([
    "{0}\n{1:.5f}".format(string, value)
    for string, value in zip(global_mean_diffs_hex[:, :num_rows].flatten(),
                             global_mean_diffs[:, :num_rows].flatten())
])).reshape(num_subkeys, num_rows)

sns.heatmap(np.transpose(global_mean_diffs[:, :num_rows]),
            annot=np.transpose(annotations),
            cmap=my_cmap,
            ax=ax,
            mask=np.transpose(color_mask[:, :num_rows]),
            annot_kws={'fontweight': 'bold'},
            cbar=False,
            fmt='')

sns.heatmap(np.transpose(global_mean_diffs[:, :num_rows]),
            annot=np.transpose(annotations),
            alpha=0,
            ax=ax,
            mask=1 - np.transpose(color_mask[:, :num_rows]),
            annot_kws={
                'color': 'w',
                'fontweight': 'bold'
            },
            cbar=False,
            fmt='')

ax.set_xlabel('Subkey\n', fontweight='bold', fontsize=14)
ax.set_ylabel('Key Guess\n', fontweight='bold', fontsize=14)

plt.xticks(rotation=0)
plt.yticks(rotation=0)
plt.show()
