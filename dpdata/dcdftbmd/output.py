import os
from pathlib import Path
import re
from collections import OrderedDict
import numpy as np

    

def get_frames (fname, begin = 0, step = 1) :

    if not os.path.isdir(fname):
        raise RuntimeError('fname must be a folder')
    
    eV = 2.72113838565563E+01 # hartree to eV
    angstrom = 5.29177208590000E-01 # Bohr to Angstrom

    root_path = Path(fname)

    lattice = []
    with open(root_path.joinpath('dftb.inp')) as fin:
        for line in fin:
            if 'TV' in line:
                arr = line.split()
                lattice.append(list(map(float, arr[1:4])))
    lattice_frame = np.array(lattice)


    energy_matcher = re.compile(
        r'^\s+Final .*-DFTB Energy =\s+([-+]?\d*\.*\d+)')
    
    forces = []
    energies = []
    cur_step = -1
    with open(root_path.joinpath('dftb.out')) as fin:
        for line in fin:
            res = energy_matcher.match(line)
            if res:
                cur_step += 1
                _ = next(fin)
                _ = next(fin)
                line = next(fin)
                if 'Total forces' not in line:
                    raise RuntimeError('Parser error')
                _ = next(fin)
                _ = next(fin)
                _ = next(fin)
                _ = next(fin)
                force_frame = []
                for line in fin:
                    if '------' in line:
                        break
                    arr = line.split()
                    force_frame.append(list(map(float, arr[1:4])))
                if cur_step < begin:
                    continue
                if (cur_step - begin) % step != 0:
                    continue
                forces.append(force_frame)
                energy_frame = float(res.group(1))*eV
                energies.append(energy_frame)

    forces_array = np.array(forces, dtype=float)
    forces_array = forces_array * eV / angstrom
    cur_step = -1
    coordinates = []
    
    counter = OrderedDict()
    atom_symbols = []
    with open(root_path.joinpath('traject')) as fin:
        for line in fin:
            cur_step += 1
            nat = int(line)
            coord_frame = []
            _ = next(fin)
            for _ in range(nat):
                line = next(fin)
                arr = line.split()
                coord_frame.append(list(map(float, arr[1:4])))
                if cur_step == 0:
                    if arr[0] in counter:
                        counter[arr[0]] += 1
                    else:
                        counter[arr[0]] = 1
                    atom_symbols.append(arr[0])

            if cur_step < begin:
                continue
            if (cur_step - begin) % step != 0:
                continue
            coordinates.append(coord_frame)


    atom_names = list(counter.keys())  
    atom_numbs = list(counter.values())
    atom_types = [atom_names.index(x) for x in atom_symbols]

    lattices = [lattice_frame for _ in range(len(coordinates))]
    
    # print(len(forces), len(energies), len(coordinates))

    return atom_names, atom_numbs, atom_types, \
        np.array(lattices), np.array(coordinates), np.array(energies), \
            forces_array
    