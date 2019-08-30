import lammps_helper as l
import sys
from glob import glob
import os.path

# parse arguments
if len(sys.argv) != 2:
  print 'takes one argument - the dump directory that contains "ints" "vacs" and "defects" directories'
  quit()
dir = sys.argv[1]

# find files
int_files = glob(os.path.join(dir, 'ints', 'dump.ints.*.txt'))

# loop over files
for int_file in sorted(int_files):
  # generate other filenames from this filename
  vac_file = int_file.replace('ints', 'vacs')
  out_file = int_file.replace('ints', 'defects')
  print 'combining {} and {} into {}...'.format(int_file, vac_file, out_file)

  # read files
  int_df, info = l.read_dump(int_file, return_header=True)
  vac_df = l.read_dump(vac_file)

  # total number of atoms
  info['number of atoms'] = int_df.index.size + vac_df.index.size

  # call ints type 1 and vacs type 2
  int_df['type'] = 1
  vac_df['type'] = 2

  # vac headers need to be renamed
  vac_df.rename(inplace=True, index=str, columns={'f_cell_coords[1]': 'x', 'f_cell_coords[2]': 'y', 'f_cell_coords[3]': 'z'})

  # put data together
  combined_df = int_df[['type', 'x', 'y', 'z']]
  combined_df = combined_df.append(vac_df[['type', 'x', 'y', 'z']])

  # write dump
  l.write_dump(out_file, info, combined_df)
