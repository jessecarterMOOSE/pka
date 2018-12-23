#! /bin/bash

# simple bash script to select atom and velocity and run a pka simulation

# set some simple parameters
export pka_energy=1000.0  # pka energy in eV

# LAMMPS dump file containing atoms to be selected to be a PKA
export atom_file="dump/dump.shell-10.txt"

# select atom from file and velocity vector that points at the simulation box origin
data_array=(`python -c "import os; import lammps_helper as l; print ' '.join(map(str, l.pick_atom_and_velocity(os.environ['atom_file'], float(os.environ['pka_energy']))))"`)

# break out info
pka_id=${data_array[0]}
vx=${data_array[1]}
vy=${data_array[2]}
vz=${data_array[3]}

# print info
echo "for PKA:"
echo "  using atom id: $pka_id"
echo "  x-velocity: $vx"
echo "  y-velocity: $vy"
echo "  z-velocity: $vz"

# clean up before running
rm -rf dump/dumpall.*

# run pka simulation and use the above info
 mpiexec -np 4 ./lammps -in in.pka -v pka_id $pka_id -v vx $vx -v vy $vy -v vz $vz
