import pandas as pd
import numpy as np


def read_dump(filename, read_header=False):
    with open(filename, 'r') as f:
        lines = f.readlines()
        # loop through looking for keywords
        for i, line in enumerate(lines):
            linestrip = line.strip()
            if linestrip.startswith('ITEM: TIMESTEP'):
                timestep = int(lines[i+1].strip())
            if linestrip.startswith('ITEM: NUMBER OF ATOMS'):
                atom_number = int(lines[i+1].strip())
            if linestrip.startswith('ITEM: BOX BOUNDS'):
                xlo, xhi = [float(a) for a in lines[i+1].strip().split()]
                ylo, yhi = [float(a) for a in lines[i+2].strip().split()]
                zlo, zhi = [float(a) for a in lines[i+3].strip().split()]
            if linestrip.startswith('ITEM: ATOMS'):
                columns = linestrip.split()[2:]
                break
    info = {'timestep': timestep, 'number of atoms': atom_number,
            'xlo': xlo, 'xhi': xhi, 'ylo': ylo, 'yhi': yhi, 'zlo': zlo, 'zhi': zhi}

    df = pd.read_csv(filename, index_col=0, skiprows=9, names=columns, delim_whitespace=True)

    if read_header:
        return df, info

    return df


def unit_vector(v):
    return v/np.sqrt(np.sum(np.square(v)))


def pick_atom(df):
    id = int(df.sample().index.values)
    m, x, y, z = df[['mass', 'x', 'y', 'z']].loc[id].values
    return id, m, x, y, z


def pick_atom_from_file(filename):
    df = read_dump(filename)
    return pick_atom(df)


def pick_atom_and_velocity(filename, energy):
    id, m, x, y, z = pick_atom_from_file(filename)
    speed = np.sqrt(2.0*energy*1.602e-19/m/1.66e-27)*0.01  # convert m/s to A/ps for LAMMPS
    velocity_vector = -1.0*speed*unit_vector([x, y, z])  # aim back at origin

    return id, velocity_vector[0], velocity_vector[1], velocity_vector[2]

