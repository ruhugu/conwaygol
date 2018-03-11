# Calculate and visualice how a perturbed "trajectory" separates from the original one as time passes.

import os
import sys
from matplotlib import pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conwaygol import ConwayGoL

# Parameters
L = 50
nframes = 200
fps = 10
# Perturbation position
# TODO: kill a random cell
y_pert = 25
x_pert = 25

# Generate the lattices 
game1 = ConwayGoL(L, L)
game2 = ConwayGoL(L, L)
game1.randomfill()
game2.latt = game1.latt
#game.relax()

# Perturbe the second configuration
game2.latt[y_pert,x_pert] = not game.latt[y_pert,x_pert]

# Create discrete colormap 
# https://stackoverflow.com/questions/14777066/matplotlib-discrete-colorbar
# Color list
colorlist = [(0.,0.,0.,1.0),  # white
             (.067,.8,.8,1.0),  # orange
             (.563,.8,.8,1.0),  # blue
             (.5,.5,.5,1.0)]  # gray
# create the new map
cmap = cmap.from_list('Custom cmap', colorlist, len(colorlist))

# define the bins and normalize
bounds = np.linspace(0, len(colorlist), len(colorlist) + 1)
norm = mpl.colors.BoundaryNorm(bounds, len(colorlist))

def combine(game1, game2):
    """Return an array with the differences between two game instances.

    A cell value of 0 in thw returned array means that it is dead in both game1 and game2. 1 means that it is alive in game1 and dead in game2, while 2 means the opposite. 3 means that the cell is alive in both game1 and game2.

    """
    #TODO: DOCS
    return game1 + 2*game2

comb_latt = combine(game1, game2)

# Create the animation
fig, ax = plt.subplots()
im = ax.imshow(comb_latt, cmap=self.cmap, norm=norm, interpolation=None)
 
def update(i, game1, game2, comb_latt, im):
    """Update function of the animation.

    """
    game1.evolve()
    game2.evolve()
    comb_latt = combine(game1, game2)
    im.set_array(comb_latt)

    return im

anim = animation.FuncAnimation(fig, update, frames=nframes, 
                               blit=True, fargs=(game1, game2, comb_latt, im))

# Show the animation
plt.show()

# Save animation to file (this does not work if plt.show() has been used before)
# As mp4
#anim.save("clusterevolutionL{0}.mp4".format(L), dpi=300, fps=fps,
#          extra_args=['-vcodec', 'libx264'])
# As GIF (imagemagick must be installed)
#anim.save("clusterevolutionL{0}.gif".format(L), dpi=150, fps=fps,
#          writer='imagemagick')
