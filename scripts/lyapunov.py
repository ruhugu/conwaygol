# -*- coding: utf-8 -*-
# Measure the Lyapunov exponent of the system

import os
import sys
import numpy as np
from matplotlib import pyplot as plt

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from conwaygol import ConwayGoL

# Parameters
Ls = [10, 20, 40, 80, 160]
nsteps = 200 # Number of timesteps
nsims = 200 # Number of simulations

figylen = 3.5
figxlen = 1.8*figylen


# Define auxiliar function
def separation(game1, game2):
    """Measure the number of different cells between two lattices.

    """
    return np.abs(game1.latt - game2.latt).sum()


# Initialize systems
# ========================================
# Matrix to store the mean separation for all systems sizes
sep_mean = np.zeros((len(Ls), nsteps), dtype=int)

# Vector to store the number of trajectories where the difference
# survived until the end of the measurements (for each size)
ns_survived = np.zeros(len(Ls), dtype=int)

# Measure
# ========================================
# Create time vector
ts = np.arange(nsteps)

# Calculate separation in each timestep averaged over simulations
# (only if the difference survives)
for j_L, L in enumerate(Ls):
    # Generate the lattices 
    game1 = ConwayGoL(L, L)
    game2 = ConwayGoL(L, L)

    # Specify the perturbation position 
    # (since we are using PBC, this is completely irrelevant)
    y_pert = L/2 # Perturbation x position
    x_pert = L/2 # Idem y

    # Initialize auxiliar vector to store separation sum over 
    # different simulation
    sep_sum = np.zeros(nsteps, dtype=int)

    for j_sim in range(nsims):
        print("L: {0} ({1}/{2}), nsim: {3}/{4}".format(
                L, j_L + 1, len(Ls), j_sim + 1, nsims))
        # Set initial random state with perturbation in one lattice
        game1.randomfill() 
        game2.latt = game1.latt
        game2.latt[y_pert,x_pert] = not game2.latt[y_pert,x_pert]

        sep_sim = np.zeros(nsteps, dtype=int)

        for i in range(nsteps):
            sep = separation(game1, game2)
            survived = (sep != 0)

            # If the difference has dissapeared, break the loop
            if not survived:
                break

            sep_sim[i] = sep
            game1.evolve()
            game2.evolve()

        # If the perturbation survived, add the data to the accumulated sum
        if survived:
            sep_sum += sep_sim
            ns_survived[j_L] += 1

    # Compute the mean of the separation trajectories
    sep_mean[j_L] = sep_sum.astype(float)/ns_survived[j_L]


# Visualization
# ========================================
lyap = 1.5

fig = plt.figure(figsize = (figxlen, figylen))
ax = fig.add_subplot(111) 

# Data
for j_L, L in enumerate(Ls):
    ax.loglog(
            ts.astype(float), sep_mean[j_L].astype(float), 
            label="L={0} ({1:.2f} surv. rate)".format(L,
                    float(ns_survived[j_L])/nsims))

# Expected Lyapunov exponent
ax.loglog(
        ts, 10.*np.power(ts, lyap), "--", color="black",
        label="Slope = {0}".format(lyap))

ax.legend()
ax.set_xlabel("Time")
ax.set_ylabel(u"Separation (nº cells)")
fig.tight_layout()

fig.savefig("separation.png")
#plt.show()
