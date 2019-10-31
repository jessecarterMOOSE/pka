from glob import glob
import os.path
import lammps_helper as l
import argparse
import pandas as pd
import numpy as np


def pka_path(keV, Nx, T, run=None):
    # return path to run data
    box_string = 'Nx-{}-T-{}'.format(Nx, T)
    base_path = os.path.join('outputs', box_string, 'pka', '{}-keV'.format(keV))
    if run:
        base_path = os.path.join(base_path, 'run-{}'.format(str(run).zfill(3)))
    return base_path


def parse_data(keV, Nx, T):
    # get ready to store a bunch of DataFrames in a dict, indexed by run number
    df_dict = dict()

    # get ready to store end-of-run data in a DataFrame, indexed by run number
    columns = ['end_time', 'vacs', 'max_vacs', 'wrapped', 'closest_approach', 'steps', 'runtime_hours']
    end_data_df = pd.DataFrame(columns=columns)

    # loop over output from pka runs
    for file in sorted(glob(os.path.join(pka_path(keV, Nx, T), 'run-*', 'time-history.txt'))):
        # read datafile into pandas DataFrame
        df = l.read_ave_time(file)
        # save dataframe into dict, indexed by run number
        run_number = int(os.path.basename(os.path.dirname(file)).split('-')[-1])
        df_dict[run_number] = df
        # get runtime from log, if available
        logfile = os.path.join(os.path.dirname(file), 'log.lammps')
        runtime = np.nan
        if os.path.isfile(logfile):
            with open(logfile, 'r') as f:
                wall_line = [line.strip() for line in f.readlines() if line.startswith('Total wall time')]
            if len(wall_line) > 0:
                h, m, s = [int(i) for i in wall_line[0].split()[-1].split(':')]
                walltime = 3600.0*h + 60.0*m + s
        # save end-of-run data
        wrapped_flag = bool(np.count_nonzero(df['v_wrap_flag'].values))
        closest_approach = df['c_min_d'].min()
        steps = df.index[-1]
	end_data_df = end_data_df.append(pd.DataFrame(index=[run_number], columns=columns,
            data=dict(end_time=df['v_time'].iloc[-1],
                      vacs=df['c_num_vacs'].iloc[-1],
                      max_vacs=df['c_num_vacs'].max(),
                      wrapped=wrapped_flag,
                      closest_approach=closest_approach,
                      steps=steps,
                      runtime_hours=h+m/60.0+s/3600.0)))

    return df_dict, end_data_df


if __name__== "__main__":
    # run from command line with arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('keV', type=int, help='pka energy in keV')
    parser.add_argument('Nx', type=int, help='(half) box size in lattice units')
    parser.add_argument('T', type=int, help='temperature in K')
    args = parser.parse_args()

    df_dict, end_data_df = parse_data(args.keV, args.Nx, args.T)

    print('summary:')
    print(pd.DataFrame(end_data_df, dtype=object))
    print
    print('averages:')
    print(end_data_df[['end_time', 'vacs', 'max_vacs', 'steps', 'runtime_hours']].mean())
