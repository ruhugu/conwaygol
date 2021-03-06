# Calculate and plot how the mass of a system evolve with time.

import os
import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
from matplotlib import animation

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conwaygol import ConwayGoL


# TODO: store the data in logarithmically spaced times 

# Parameters
L = 1000
inimass = L*L/2
nsteps = 100000
nsim = 50
figylen = 3
figxlen = 1.62*figylen

# Generate the lattice
game = ConwayGoL(L, L)

# Empty vectors to store the mass and separation
ms = list()

# Time vector
ts = np.arange(nsteps)

# Calculate
for j_sim in range(nsim):
    print("Simulation {0}/{1}".format(j_sim + 1, nsim))
    # Reset lattice and fill randomly
    game.randomfill_mass(inimass)
    # Append new vector to store the mass
    ms.append(np.zeros(nsteps, dtype=int))
    for j_time in range(nsteps):
        ms[j_sim][j_time] = game.mass()
        game.evolve()

# Create and configurate figures and axes
fig, ax = plt.subplots(figsize=(figxlen, figylen))
ax.set_ylabel("Fill fraction")
ax.set_xlabel("Time")
fig.tight_layout()
 
# Plot all the trajectories
for j_sim in range(nsim):
    ax.loglog(ts, ms[j_sim]/float(game.size), alpha=0.5)

# Plot mean trajectory
ms_sum = np.zeros(nsteps, dtype=int)
for m_vec in ms:
    ms_sum += m_vec
ms_mean = ms_sum/float(nsim)
ax.loglog(ts, ms_mean/float(game.size), color="black")

# Store the mean curve
np.savetxt("relaxationL{0}N{1}.dat".format(L, nsim), np.vstack((ts, ms_mean)))

# Show the plot
#plt.show()

# Save plot to file (this does not work if plt.show() has been used before)
fig.savefig("relaxationL{0}N{1}.png".format(L, nsim))
