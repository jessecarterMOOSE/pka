import lammps_helper as l
import sys

# parse arguments
int_file = sys.argv[1]  # dump file of ints
vac_file = sys.argv[2]  # dump file of vacs
out_file = sys.argv[3]  # output file

# big dataframe to store results, index will be atom id
# combined_df = pd.DataFrame(columns=['type', 'x', 'y', 'z'])

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
