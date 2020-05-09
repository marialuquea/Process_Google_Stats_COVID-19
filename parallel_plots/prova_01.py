import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import math

#------------some parameters------------------------------#
# Figure_abs = "Parallel_abs_val.png" #the name of the output figure
# Figure_rel = "Parallel_abs_percentage.png"#the name of the output figure
# Working_folder = "C:/Users/berna/Desktop/New-folder_2/"

ynames_abs = ["Scenarios\n", "GHG\n[Mt]", "PM\n[Mt]", "SO2\n[Mt]", "NOx\n[Mt]", "Groups\n"]
ynames_percent = ["Scenarios\n", "GHG\n[%]", "PM\n[%]", "SO2\n[%]", "NOx\n[%]", "Groups\n"]

colorlist = ['yellow', 'darkorange', 'green', 'cornflowerblue', 'darkblue', 'darkorchid', 'red']# a list of 7 colors, one for each scenario

Figure_width = 8. #cm
Figure_height = 5. #cm
Image_resolution = 300. #dpi
Font_headings = 14 #font-size of the parallel axes headings
linesWidth = 4. #thickness of lines
linesOpa = 0.5 #opacity of lines color
#---------------------------------------------------------

# Read CSV
ys = np.delete(np.array(pd.read_csv("parallel_plots_tot_abs.csv")), 6, 1)

# change order of columns
idx = [5, 1, 2, 3, 4, 0]
ys = ys[:, idx]

ymins = ys.min(axis=0)
ymaxs = ys.max(axis=0)
ymins -= (ymaxs - ymins) * 0.05  # add 5% padding below and above
ymaxs += (ymaxs - ymins) * 0.05
dys = ymaxs - ymins

# transform all data to have the range of scenarios (1-7)
scaler = MinMaxScaler(feature_range=(ys[:, 0].min(), ys[:, 0].max()))
ys_pd = pd.DataFrame(data=ys)  
ys_pd[[1, 2, 3, 4, 5]] = scaler.fit_transform(ys_pd[[1, 2, 3, 4, 5]])
zs = ys_pd.values

def roundup(x, type):
    return int(math.ceil(x / float(type))) * int(type)

def rounddown(x, type):
    return int(math.floor(x/float(type))) * int(type)


def print_figure():
    fig, host = plt.subplots(figsize=(Figure_width, Figure_height))
    
    axes = [host] + [host.twinx() for i in range(ys.shape[1] - 1)]
    for i, ax in enumerate(axes):
        ax.set_ylim(ymins[i], ymaxs[i])
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        if ax != host:
            ax.spines["right"].set_position(("axes", i / (ys.shape[1] - 1)))
    
    # axes[1].set_yticks(range(0, 3100, 1000))
    # axes[2].set_yticks([0.1, 0.2, 0.3, 0.4, 0.5])
    # axes[3].set_yticks([0, 1, 2, 3, 4])
    # axes[4].set_yticks([1, 2, 3])
    axes[5].set_yticks([1, 2, 3, 4])
    
    # host.set_xlim(0, ys.shape[1] - 1)
    host.set_xticks(range(ys.shape[1]))
    host.set_xticklabels(ynames_abs, fontsize=Font_headings)
    
    host.tick_params(axis='x', which='major', pad=7)
    host.spines['right'].set_visible(False)
    host.xaxis.tick_top()
    host.set_title('Parallel Coordinates for absolute values', fontsize=18, pad=12)
    
    # Line Colours
    Colslist = []
    for ii in range(0,4):
        for i in range(0, 7):
            Colslist.append(colorlist[i])
    
    # For each row of the dataset
    for j in range(ys.shape[0]):
        # create bezier curves
        verts = list(zip([x for x in np.linspace(0, len(ys) - 1, len(ys) * 3 - 2, endpoint=True)],
                         np.repeat(zs[j, :], 3)[1:-1]))
        codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
        path = Path(verts, codes)
        patch = patches.PathPatch(path, facecolor='none', lw=linesWidth, alpha=0.5, edgecolor=Colslist[j])
        host.add_patch(patch)
    
    plt.tight_layout()
    
print_figure()





# plt.savefig(Working_folder+Figure_abs, dpi=Image_resolution, facecolor='w', edgecolor='w')
# ####################################################################################################


# ys = np.delete(np.array(pd.read_csv("parallel_plots_tot_percent.csv")), 6, 1)
# # your_permutation = [5, 1, 2, 3, 4, 0]
# # idx = np.empty_like(your_permutation)
# # idx[your_permutation] = np.arange(len(your_permutation))
# # #print(ys[:, idx])  # return a rearranged copy
# # ys = ys[:, idx]

# ymins = ys.min(axis=0)
# ymaxs = ys.max(axis=0)
# dys = ymaxs - ymins
# ymins -= dys * 0.05  # add 5% padding below and above
# ymaxs += dys * 0.05

# dys = ymaxs - ymins

# # transform all data to be compatible with the main axis
# zs = np.zeros_like(ys)
# zs[:, 0] = ys[:, 0]
# zs[:, 1:] = (ys[:, 1:] - ymins[1:]) / dys[1:] * dys[0] + ymins[0]
# # Scale columns to numbers between 1 and 4
# scaler = MinMaxScaler(feature_range=(1,4))
# ys_pd = pd.DataFrame(data=ys)  
# ys_pd[[1, 2, 3, 4]] = scaler.fit_transform(ys_pd[[1, 2, 3, 4]])



# fig, host = plt.subplots(figsize=(Figure_width, Figure_height))

# axes = [host] + [host.twinx() for i in range(ys.shape[1] - 1)]
# for i, ax in enumerate(axes):
#     ax.set_ylim(ymins[i], ymaxs[i])
#     ax.spines['top'].set_visible(False)
#     ax.spines['bottom'].set_visible(False)
#     if ax != host:
#         ax.spines['left'].set_visible(False)
#         ax.yaxis.set_ticks_position('right')
#         ax.spines["right"].set_position(("axes", i / (ys.shape[1] - 1)))

# host.set_xlim(0, ys.shape[1] - 1)
# host.set_xticks(range(ys.shape[1]))
# host.set_xticklabels(ynames_percent, fontsize=Font_headings)

# host.tick_params(axis='x', which='major', pad=7)
# host.spines['right'].set_visible(False)
# host.xaxis.tick_top()
# #host.set_title('Parallel Coordinates', fontsize=18, pad=12)

# Colslist = []
# for ii in range(0,4):
#     for i in range(0, 7):
#         Colslist.append(colorlist[i])


# for j in range(ys.shape[0]):
#     # create bezier curves
#     verts = list(zip([x for x in np.linspace(0, len(ys) - 1, len(ys) * 3 - 2, endpoint=True)],
#                      np.repeat(zs[j, :], 3)[1:-1]))
#     codes = [Path.MOVETO] + [Path.CURVE4 for _ in range(len(verts) - 1)]
#     path = Path(verts, codes)
#     patch = patches.PathPatch(path, facecolor='none', lw=linesWidth, alpha=0.7, edgecolor=Colslist[j])
#     host.add_patch(patch)

# plt.tight_layout()

# plt.savefig(Working_folder+Figure_rel, dpi=Image_resolution, facecolor='w', edgecolor='w')