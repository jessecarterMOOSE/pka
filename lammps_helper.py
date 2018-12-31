import pandas as pd
import numpy as np


def read_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]


def read_dump(filename, return_header=False):
    lines = read_file(filename)
    # loop through looking for keywords
    for i, line in enumerate(lines):
        if line.startswith('ITEM: TIMESTEP'):
            timestep = int(lines[i+1].strip())
        if line.startswith('ITEM: NUMBER OF ATOMS'):
            atom_number = int(lines[i+1].strip())
        if line.startswith('ITEM: BOX BOUNDS'):
            xlo, xhi = [float(a) for a in lines[i+1].strip().split()]
            ylo, yhi = [float(a) for a in lines[i+2].strip().split()]
            zlo, zhi = [float(a) for a in lines[i+3].strip().split()]
        if line.startswith('ITEM: ATOMS'):
            columns = line.split()[2:]
            break
    info = {'timestep': timestep, 'number of atoms': atom_number,
            'xlo': xlo, 'xhi': xhi, 'ylo': ylo, 'yhi': yhi, 'zlo': zlo, 'zhi': zhi}

    df = pd.read_csv(filename, index_col=0, skiprows=9, names=columns, delim_whitespace=True)

    if return_header:
        return df, info

    return df


def read_ave_time(filename):
    lines = read_file(filename)
    # keywords are on the second line
    columns = lines[1].split()[2:]  # these are the data headers
    return pd.read_csv(filename, index_col=0, skiprows=2, names=columns, delim_whitespace=True)
