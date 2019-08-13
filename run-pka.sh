#! /bin/bash

# simple bash script to select atom and velocity and run a pka simulation

# set some parameters, will attempt to look for restart file based on this information
end_time=0.1  #  set the (minimum) end time of the simulation, units are picoseconds
pka_energy=1  # pka energy in keV
Nx=10  # (half) box size
T=300  # temperature

# LAMMPS dump file containing atoms to be selected to be a PKA
pka_file="pka_atoms/dump.shell-T-$T-Nx-$Nx.txt"

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
dump_dir=dump/$pka_energy-keV-T-$T-Nx-$Nx/run-$run_number
rm -rf $dump_dir
mkdir -p $dump_dir
echo "writing output to $dump_dir..."

# make some more output directories for different dumps
mkdir $dump_dir/all $dump_dir/defects $dump_dir/combined_defects

# run pka simulation and use the above info
mpiexec -np 4 ./lammps -in in.pka -v pka_id $pka_id -v vx $vx -v vy $vy -v vz $vz -v end_time $end_time -v dump_dir $dump_dir -v Nx $Nx -v T $T

# combine separate int/vac dumps into a single
cd $dump_dir/defects
for file in dump.ints.*.txt
do
  echo "processing $file..."
  vac_file=`echo $file | sed 's/ints/vacs/'`
  out_file=`echo $file | sed 's/ints/defects/'`
  python ../../../../combine_defect_files.py $file $vac_file ../combined_defects/$out_file
done
cd ../..
