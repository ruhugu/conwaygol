
<img align="right" width="270" height="240"
     src="https://raw.githubusercontent.com/ruhugu/conwaygol/master/output_examples/conwayL50.gif">

# conwaygol
Python implementation of [Conway's game of life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life).

This python module allows to create, analyse and visualize lattices following this model.


## Required packages

This modules requires both [matplotlib](https://matplotlib.org/) and [numpy](http://www.numpy.org/) to be installed.


## Some output examples

Relaxation process of 100 simulations in a 50x50 lattice ([script](https://github.com/ruhugu/conwaygol/blob/master/scripts/relaxation.py)).

<img src="https://raw.githubusercontent.com/ruhugu/conwaygol/master/output_examples/relaxationL50N100.png" alt="Drawing" width="500"/>


Propagation of a local perturbaction in a 80x80 lattice. A random configuration is perturbed locally (the state of the cell in the center is changed) and the evolution of both the pertubed and unpertubed lattices is tracked. Black cells are those which are alive in both simulations, blue cells are only alive in the unperturbed one, orange ones are only alive in the perturbed one and finally white cells are dead in both simulations ([script](https://github.com/ruhugu/conwaygol/blob/master/scripts/butterfly.py)).

<img src="https://raw.githubusercontent.com/ruhugu/conwaygol/master/output_examples/butterflyL80.gif" alt="Drawing" width="700"/>

Estimation of the Lyapunov exponent of the system using a separation graph like the one in the previous examples. Each of the curves for the different system sizes is the average of 200 simulations ([script](https://github.com/ruhugu/conwaygol/blob/master/scripts/lyapunov.py)).

<img src="https://raw.githubusercontent.com/ruhugu/conwaygol/master/output_examples/separation.png" alt="Drawing" width="600"/>


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

