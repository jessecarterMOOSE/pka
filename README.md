# A simple PKA simulator using LAMMPS

## Basics

This repo provides scripts for launching PKA (Primary Knock-On) simulations using the open-source LAMMPS package for molecular dynamics. Simple scripts are 
provided to perform 
equilibration at temperature, the PKA simulation, and post-process the results. Due to the random nature of PKA's, several runs are needed to
gather enough data to have a sense of the statistical variation for a given condition. These scripts will create separate output directories for
each simulation and number them accordingly. A simple python script is provided to automatically gather the available data and provide results.

## Requirements

1. A LAMMPS installation is needed with the VORONOI package installed in order to perform defect analysis on-the-fly and minimize post-processing.
2. Standard python-2 with the pandas package.
3. An interatomic potential that has been "stiffened" at small spacings. Such potentials are available at the NIST interatomic potentials repository.

## Procedure

Performing a PKA simulation is a two-step process: 1) bring a box of atoms up to the desired temperature/pressure, and 2) do the PKA simulation.
Each step is performed separately here, where the simulation is saved following the equilibration step and each PKA simulation uses the end-state of the
equilibration step as a starting point, randomly choosing a different atom as the PKA each time.

1. Equilibration: Run LAMMPS using the in.equilibrate script. The script is set up such that the temperature (T) and half box size (Nx) can be set via
the command line like so:
> ./lammps -in in.equilibrate -v T 300 -v Nx 20

The above example would run the simulation to 300 K, 40 lattice constants on a side, and 0 pressure. Other parameters such as the potential and number of
time steps can of course be changed in the file, and they should be. The parameters are set to provide a system that can run quickly on my laptop.

2. Run PKA: Edit the top of the run-pka.sh script to match the temperature and box size from step 1, pick a PKA energy in keV, then run. Also check the end time 
and such to meet your needs. The script handles the directory creation and PKA picking and defect file placements. 

3. After several runs, run "analyze_pka_data.py" with the correct arguments, for example:
> python analyze_pka_data.py 1 20 300

will gather data from runs at 1 keV, Nx=20, and T=300 and report some statistics.
