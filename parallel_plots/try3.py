# -*- coding: utf-8 -*-
"""
Created on Sat May  9 12:31:35 2020

@author: Maria
"""


import matplotlib.pyplot as plt
from matplotlib import ticker
import pandas as pd
import numpy as np

df_original = pd.read_csv('parallel_plots_tot_abs.csv')
df = df_original.copy()

cols = ['ghg', 'pm2', 'so2', 'nox', 'group_id']
x = [i for i, _ in enumerate(cols)]
colours = ['red', 'orange', 'yellow', 'lightgreen', 
           'lightblue', 'purple', 'pink']

# create dict of categories: colours for scenario_id
colours = {df['scenario_id'].astype('category').cat.categories[i]: colours[i] for i, _ in enumerate(df['scenario_id'].astype('category').cat.categories)}

# Create (X-1) sublots along x axis
fig, axes = plt.subplots(1, len(x)-1, sharey=False, figsize=(15,5))

# Get min, max and range for each column
# Normalize the data for each column
min_max_range = {}
for col in cols:
    min_max_range[col] = [df[col].min(), df[col].max(), np.ptp(df[col])]
    df[col] = np.true_divide(df[col] - df[col].min(), np.ptp(df[col]))


# Plot each row
for i, ax in enumerate(axes):
    # print(i, ax)
    for idx in df.index:
        scenario_category = df.loc[idx, 'scenario_id']
        ax.plot(x, df.loc[idx, cols], colours[scenario_category])
    ax.set_xlim([x[i], x[i+1]])
    print('min:\t', df_original.min(axis=0)['ghg'])
    print('max:\t', df_original.max(axis=0)['ghg'])
    # print(range(df[i].min(), df[i].max(), np.ptp(df[col])))
    
# axes[0].set_yticks([0, 500, 1000, 1500, 2000])
# axes[1].set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
# axes[2].set_yticks([0, 1, 2, 3, 4])
# axes[3].set_yticks([1, 2, 3])
# axes[4].set_yticks([1, 2, 3, 4])

# Set the tick positions and labels on y axis for each plot
# Tick positions based on normalised data
# Tick labels are based on original data
def set_ticks_for_axis(dim, ax, ticks):
    min_val, max_val, val_range = min_max_range[cols[dim]]
    step = val_range / float(ticks-1)
    tick_labels = [round(min_val + step * i, 2) for i in range(ticks)]
    norm_min = df[cols[dim]].min()
    norm_range = np.ptp(df[cols[dim]])
    norm_step = norm_range / float(ticks-1)
    ticks = [round(norm_min + norm_step * i, 2) for i in range(ticks)]
    ax.yaxis.set_ticks(ticks)
    ax.set_yticklabels(tick_labels)


for dim, ax in enumerate(axes):
    ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
    set_ticks_for_axis(dim, ax, ticks=6)
    ax.set_xticklabels([cols[dim]])

# Move the final axis' ticks to the right-hand side
ax = plt.twinx(axes[-1])
dim = len(axes)
ax.xaxis.set_major_locator(ticker.FixedLocator([x[-2], x[-1]]))
set_ticks_for_axis(dim, ax, ticks=6)
ax.set_xticklabels([cols[-2], cols[-1]])

# Remove space between subplots
plt.subplots_adjust(wspace=0)

# Add legend to plot
plt.legend(
    [plt.Line2D((0,1),(0,0), color=colours[cat]) for cat in df['scenario_id'].astype('category').cat.categories],
    df['scenario_id'].astype('category').cat.categories,
    bbox_to_anchor=(1.2, 1), loc=2, borderaxespad=0.)

plt.title("Parallel plots for total absolute values")

plt.show()

'''
plt.figure()
pd.plotting.parallel_coordinates(
    df[['scenario_id', 'ghg', 'pm2', 'so2', 'nox', 'group_id']], 
    'scenario_id')
plt.show()
'''