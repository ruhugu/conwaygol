#-*- coding: utf-8 -*-
from __future__ import (print_function, division, 
                        absolute_import, unicode_literals)

from cellularautomata2d import CellAutomata2D
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors as colors
from matplotlib import animation

class ConwayGoL(CellAutomata2D):  

    def __init__(self, xlen, ylen, pbc=True, cmap="Purples"):
        CellAutomata2D.__init__(self, xlen, ylen, pbc=pbc, dtype=bool,
                                show_cbar=False)

        # Create auxiliar lattices
        self._auxlatt = np.zeros((self.ylen, self.xlen), dtype=int)
        self._ns_neigh = np.zeros((self._ylen_bc, self._xlen_bc), dtype=int)
        self._births = np.zeros((self.ylen, self.xlen), dtype=self.dtype)
        self._deaths = np.zeros((self.ylen, self.xlen), dtype=self.dtype)

        # Create colormap for plots
        self.vmincolor = 0 - 0.5
        self.vmaxcolor = 1+ 0.5
        bounds = np.arange(0, 1, 2) - 0.5
        self.cnorm = colors.BoundaryNorm(bounds, 256)
        self.cmap = plt.cm.get_cmap(cmap, 2)


    def randomfill(self):
        """Fill the lattice randomly with values in the given range.

        """
        for idx, height in np.ndenumerate(self.latt):
            self.latt[idx] = np.random.randint(0, 2, dtype=bool)

        return

    def randomfill_mass(self, mass, resetlatt=True):
        """Fill the lattice randomly with a given total mass.

        """
        if mass > self.size:
            raise ValueError("The given mass is bigger than the number"
                             "of cells.")
        if resetlatt:
            self.resetlattice()

        # Generate list of unasigned cells indices
        empty_idxs = list(range(self.size))

        for i in range(mass):
            # Select and fill random empty cell
            aux_idx = np.random.randint(0, len(empty_idxs) - 1)
            flat_idx = empty_idxs[aux_idx]
            #while self.latt.flat[flat_idx] != False:
            #flat_idx = np.random.randint(0, self.size-1)
            self.latt.flat[flat_idx] = True
            del(empty_idxs[aux_idx])

        return

    def _evolvestep(self):
        """Evolve the system one step.

        Returns
        -------
            is_active : bool
                True if the lattice have moved and False otherwise.

        """
        # Find number of neighbours of each cell
        self._ns_neigh.fill(0)
        self._ns_neigh += np.roll(self._latt_bc, +1, axis=0)
        self._ns_neigh += np.roll(self._latt_bc, -1, axis=0)
        self._ns_neigh += np.roll(self._latt_bc, +1, axis=1)
        self._ns_neigh += np.roll(self._latt_bc, -1, axis=1)
        self._ns_neigh += np.roll(self._latt_bc, (+1, +1), axis=(0, 1))
        self._ns_neigh += np.roll(self._latt_bc, (+1, -1), axis=(0, 1))
        self._ns_neigh += np.roll(self._latt_bc, (-1, +1), axis=(0, 1))
        self._ns_neigh += np.roll(self._latt_bc, (-1, -1), axis=(0, 1))

        # Calculate births
        self._births = np.logical_and((self._ns_neigh==3)[self._latt_idx],
                                      np.logical_not(self.latt))
        self._auxlatt += self._births

        # Calculate deaths
        self._deaths = np.logical_and(
                np.logical_or((self._ns_neigh>3)[self._latt_idx], 
                              (self._ns_neigh<2)[self._latt_idx]), self.latt)
        self._auxlatt -= self._deaths

        # Update lattice
        self.latt += self._births
        self.latt -= self._deaths

        is_active = self._auxlatt.any()

        return is_active
        

    def measurecascade(self, maxtime=10000, retarray=False):
        """Measure the duration and number of affected cells of a cascade.

        Parameters
        ----------
            maxtime : int
                Maximum number of steps.

            retarray : bool
                If True, return a bool array with True values in the 
                cells affected by the cascade.

        Returns
        -------
            duration : int
                Duration of the cascade in steps. If the cascade does
                not end before mastime is reached, -1 is returned.

            cascadesize : int
                Number of cells affected by the cascade.

            cascadecells : bool array, optional
                Array with True in the cells affected by the cascade.

        """

        duration = 0
        # Array of cells in the cascade
        cascadecells = np.zeros((self._ylen_bc, self._xlen_bc), dtype=bool)
        active = True
        while active and (duration < maxtime):
            active = self._evolvestep()
            np.logical_or(cascadecells, (self._auxlatt != 0), cascadecells)
            duration += 1*int(active)

        cascadesize = (cascadecells.astype(int)).sum()

        # If system have not relaxed return -1 as duration
        if active:
            duration = -1

        output = duration, cascadesize

        if retarray == True:
            output.append(cascadecells)
            
        return output
        

    def animatecascade(self, maxtime=10000, steps_per_frame=1, frame_interval=300):
        """Animate the evolution of a cascade.
        
        Parameters
        ----------
            nframes : int
                Number of frames in the animation.

            steps_per_frame : int
                Number of time steps advanced in each frame.

            frame_interval : float
                Interval between frames in miliseconds.

        Returns
        -------
            anim

        """

        # Measure the cascade duration (up to maxtime)
        inilatt = np.copy(self.latt)
        duration, size = self.measurecascade(maxtime=maxtime)
        self.latt = inilatt

        # Initiliaze array of cells in the cascade
        cascadearray = np.zeros((self.ylen, self.xlen), dtype=bool)

        # Update function
        def update(i, cascadearray, self, im, im_cluster):
            self._evolvestep()
            np.logical_or(cascadearray, (self._auxlatt[self._latt_idx] != 0), 
                          cascadearray)
            im.set_array(self.latt)
            im_cluster.set_array(cascadearray)
            return im

        # Plot configuration
        fig, ax = plt.subplots(figsize=(3,3))
        
        ncolors = 2
        cmap_alpha = (plt.get_cmap("Wistia_r"))(np.arange(ncolors))
        cmap_alpha[:,-1] = np.array((0., 0.6))
        cmap_alpha = colors.ListedColormap(cmap_alpha)
        im = ax.imshow(self.latt, cmap="Greys", vmin=self.vmincolor, 
                       vmax=self.vmaxcolor, interpolation=None)
        im_cluster = ax.imshow(cascadearray, cmap=cmap_alpha,
                               vmin=0, vmax=1, interpolation=None)
        cbar = fig.colorbar(im, ax=ax)

        fig.tight_layout()

        nframes = duration
        anim = animation.FuncAnimation(fig, update, frames=nframes, 
                                       blit=False, fargs=(cascadearray, self,
                                       im, im_cluster))
        return anim


#    def findlimitcycle(self, maxtime=50):
#        history = np.zeros((maxtime+1, self.ylen, self.xlen))
#
#        foundcycle = False
#        relaxtime = -1
#        period = -1  # This will be returned if no cycle is found
#
#        j_step = 0
#        while (not foundcycle) and j_step <= maxtime:
#            history[j_step] = self.latt 
#            self.evolve(1)
#            j_step += 1
#
#            for i in reversed(range(j_step)):
#                if (history[i] == self.latt).all(): 
#                    foundcycle = True
#                    period = j_step - i
#                    relaxtime = j_step
#                    break
#
#        return period, relaxtime
