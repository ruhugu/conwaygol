# Calculate and visualice how a perturbed "trajectory" separates from the original one as time passes.

import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
from matplotlib import animation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conwaygol import ConwayGoL

# Parameters
L = 80
y_pert = L/2 # Perturbation x position
x_pert = L/2 # Idem y
nframes = 100
fps = 5
figylen = 3.5
figxlen = 1.8*figylen

# Auxiliar functions
def combine(game1, game2):
    """Return an array with the differences between two game instances.

    A cell value of 0 in the returned array means that it is dead in both game1 and game2. 1 means that it is alive in game1 and dead in game2, while 2 means the opposite. 3 means that the cell is alive in both game1 and game2.

    """
    #TODO: DOCS
    return game1.latt + 2*game2.latt

def separation(game1, game2):
    """Measure the number of different cells between two lattices.

    """
    return np.abs(game1.latt - game2.latt).sum()


# Create discrete colormap from a list of colors
# https://matplotlib.org/gallery/images_contours_and_fields/custom_cmap.html
# Color list
colorlist = ["#FFFFFF",  # white
             "#FFA500",  # orange
             "#005aff",  # blue
             "#505050"]  # gray
# Create the new map
cmap = colors.LinearSegmentedColormap.from_list(
        "custom", colorlist, N=len(colorlist))

# Create the norm for the colormap
bounds = np.linspace(0, len(colorlist), len(colorlist) + 1)
norm = colors.BoundaryNorm(bounds, len(colorlist))


# Generate the lattices 
game1 = ConwayGoL(L, L)
game2 = ConwayGoL(L, L)
game1.randomfill()
game2.latt = game1.latt

# Perturbe the second configuration
game2.latt[y_pert,x_pert] = not game2.latt[y_pert,x_pert]


# Empty vectors to store the mass and separation
ms_1 = np.zeros(nframes, dtype=int)
ms_2 = np.zeros(nframes, dtype=int)
sep = np.zeros(nframes, dtype=int)

# Time vector
ts = np.arange(nframes)

# Calculate mass and separation
inilatt_1 = np.copy(game1.latt)
inilatt_2 = np.copy(game2.latt)
for i in range(nframes):
    ms_1[i] = game1.mass()
    ms_2[i] = game2.mass()
    sep[i] = separation(game1, game2)
    game1.evolve()
    game2.evolve()
game1.latt = inilatt_1 
game2.latt = inilatt_2  

# Calculate first combined lattice (needed to initialize the plot)
comb_latt = combine(game1, game2)


# Create figures and axes
fig = plt.figure(figsize = (figxlen, figylen))
ax_latt = fig.add_subplot(121) 
ax_sep = fig.add_subplot(224, xlim=(1, nframes), ylim=(1, np.amax(sep)))
ax_mass = fig.add_subplot(222, xlim=(1, nframes),
                          ylim=(min(np.amin(ms_1), np.amin(ms_2)),
                          max(np.amax(ms_1), np.amax(ms_2))),
                          sharex=ax_sep)
plt.setp(ax_mass.get_xticklabels(), visible=False)
ax_sep.set_xlabel("Time")
ax_sep.set_ylabel("Separation (cells)")
ax_mass.set_ylabel("Mass")

# Initialize the plots
im = ax_latt.imshow(comb_latt, cmap=cmap, norm=norm, interpolation=None)
plot_sep = ax_sep.loglog(ts[0:1], sep[0:1], color="darkviolet")[0]
plot_mass1 = ax_mass.loglog(ts[0:1], ms_1[0:1], color=colorlist[1])[0]
plot_mass2 = ax_mass.loglog(ts[0:1], ms_2[0:1], color=colorlist[2])[0]
fig.tight_layout()
 

# Create the animation
def update(i, game1, game2, comb_latt, ts, ms_1, ms_2, sep, im,
           plot_mass1, plot_mass2, plot_sep):
    """Update function for the animation.

    """
    # Evolve and recalculate the lattice
    game1.evolve()
    game2.evolve()
    comb_latt = combine(game1, game2)
    # Replot
    im.set_array(comb_latt)
    plot_mass1.set_data(ts[:i+1], ms_1[:i+1])
    plot_mass2.set_data(ts[:i+1], ms_2[:i+1])
    plot_sep.set_data(ts[:i+1], sep[:i+1])

    return im, plot_mass1, plot_mass2, plot_sep

anim = animation.FuncAnimation(fig, update, frames=nframes, interval=1000./fps,
                               blit=True, fargs=(game1, game2, comb_latt, ts,
                               ms_1, ms_2, sep, im, plot_mass1, plot_mass2,
                               plot_sep))

# Show the animation
#plt.show()

# Save animation to file (this does not work if plt.show() has been used before)
# As mp4
#anim.save("butterflyL{0}.mp4".format(L), dpi=300, fps=fps,
#          extra_args=['-vcodec', 'libx264'])
# As GIF (imagemagick must be installed)
anim.save("butterflyL{0}.gif".format(L), dpi=150, fps=fps,
          writer='imagemagick')
