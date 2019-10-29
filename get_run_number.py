from glob import glob
import sys
import os.path

# given a directory look for existing "run" directories (run-001, run-002, etc.) and print the string of the next available number
# run this like: "python get_run_number.py <keV> <T> <Nx>"


# parse command line
if len(sys.argv) != 4:
    print 'run like this: python {} <keV> <T> <Nx>'.format(sys.argv[0])
    exit()
keV=sys.argv[1]
T=sys.argv[2]
Nx=sys.argv[3]

# default padding
padding = 3

# helper function to take variables and make a path
def get_dirname(keV, T, Nx, run=None):
    mypath = os.path.join('outputs', 'Nx-{}-T-{}'.format(Nx, T), 'pka', '{}-keV'.format(keV))
    if run:
        mypath = os.path.join(mypath, 'run-{}'.format(str(run).zfill(padding)))
    return mypath

# look for what's available
run_dirs = sorted(glob(os.path.join(get_dirname(keV, T, Nx), 'run-*')))

# if nothing found, use 001
if len(run_dirs) == 0:
    print str(1).zfill(padding)
    exit()

# otherwise loop from 1 to max and find one that doesn't exist
max_run = int(run_dirs[-1].split('-')[-1])
for i in range(1, max_run+2):
    dir = get_dirname(keV, T, Nx, run=i)
    if not os.path.isdir(dir):
        print str(i).zfill(padding)
        exit()

