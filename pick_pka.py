import lammps_helper as l
import numpy as np

# Pick an atom from a dump file and return its id and three velocity components that give the specified kinetic energy.
# Inputs: LAMMPS dump file, kinetic energy in keV, and an optional argument '--center' that points the velocity at the box origin.
# Otherwise, the direction is chosen at random.


def unit_vector(v):
    return v/np.sqrt(np.sum(np.square(v)))


def pick_atom(df):
    id = int(df.sample().index.values)
    m, x, y, z = df[['mass', 'x', 'y', 'z']].loc[id].values
    return id, m, x, y, z


def pick_atom_from_file(filename):
    df = l.read_dump(filename)
    return pick_atom(df)


def pick_atom_and_velocity(filename, energy, point_at_center=False):
    id, m, x, y, z = pick_atom_from_file(filename)
    speed = np.sqrt(2.0*energy*1.602e-19/m/1.66e-27)*0.01  # convert m/s to A/ps for LAMMPS
    if point_at_center:
        velocity_vector = -1.0*speed*unit_vector([x, y, z])  # aim back at origin
    else:
        velocity_vector = speed*unit_vector(np.random.normal(size=3))  # http://mathworld.wolfram.com/SpherePointPicking.html

    return id, velocity_vector[0], velocity_vector[1], velocity_vector[2]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('dump_file', help='name of dump file to pick an atom from')
    parser.add_argument('energy', help='kinetic energy of pka in keV')
    parser.add_argument('--center', action='store_true', help='point velocity at box origin')

    args = parser.parse_args()

    id, vx, vy, vz = pick_atom_and_velocity(args.dump_file, float(args.energy)*1000.0, args.center)

    print ' '.join(map(str, [id, vx, vy, vz]))