#! /bin/bash

# simple bash script to select atom and velocity and run a pka simulation

# set some parameters, will attempt to look for restart file based on this information
end_time=0.1  #  set the (minimum) end time of the simulation, units are picoseconds
pka_energy=1  # pka energy in keV
Nx=8  # (half) box size
T=300  # temperature
thermostat_edge=0  # apply thermostat to outer edges of box
electronic_stopping=0  # apply electronic stopping, using file below
electronic_stopping_file="IronInIron.txt"  # should be in the electronic_stopping_files/ directory

# LAMMPS dump file containing atoms to be selected to be a PKA
box_string=Nx-${Nx}-T-$T
pka_file=outputs/$box_string/equilibrate/dump.shell.txt

# select atom from file and velocity vector that points at the simulation box origin
data_array=(`python pick_pka.py $pka_file $pka_energy --center`)

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

# make a unique directory for this run
run_number=`python get_run_number.py $pka_energy $T $Nx`
pka_dir=outputs/$box_string/pka/$pka_energy-keV/run-$run_number
rm -rf $pka_dir
mkdir -p $pka_dir
echo "writing output to $pka_dir..."

# make some more output directories for different dumps
mkdir $pka_dir/all $pka_dir/ints $pka_dir/vacs $pka_dir/defects

# run pka simulation and use the above info
mpiexec -np 4 ./lammps -in in.pka -sf opt -log $pka_dir/log.lammps \
  -v pka_id $pka_id -v vx $vx -v vy $vy -v vz $vz -v end_time $end_time -v Nx $Nx -v T $T -v dump_dir $pka_dir \
  -v thermostat_edge $thermostat_edge -v electronic_stopping $electronic_stopping -v electronic_stopping_file electronic_stopping_files/$electronic_stopping_file

# combine separate int/vac dumps into a single
python combine_defect_files.py $pka_dir

