#! /bin/bash

# simple bash script to select atom and velocity and run a pka simulation

# set the (minimum) end time of the simulation
end_time=1  # picoseconds

# set pka energy
pka_energy=1  # pka energy in keV

# LAMMPS dump file containing atoms to be selected to be a PKA
dump_file="dump/dump.shell-10.txt"

# select atom from file and velocity vector that points at the simulation box origin
data_array=(`python pick_pka.py $dump_file $pka_energy --center`)

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
rm -f dump/dump.all.* dump/dump.ints.* dump/dump.vacs.*

# run pka simulation and use the above info
mpiexec -np 4 ./lammps -in in.pka -v pka_id $pka_id -v vx $vx -v vy $vy -v vz $vz -v end_time $end_time
