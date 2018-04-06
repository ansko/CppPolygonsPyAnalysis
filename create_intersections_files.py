#!/usr/bin/env python3


def create_intersections_files():
    """
    Reads files with lists of every particle intersections.
    Produces list of intersectiions.
    For example:
        1:2
        2:1    ->    [[1, 2], [2, 1]]
        3:  
    """
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    folder_crosses = '/home/anton/Projects/FEM/crosses'
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                # open file with list of every particle's intersections
                system_name = 'tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname = folder_crosses + '/' + system_name
                fin = open(fname, 'r')
                # processging intersections
                intersections = []
                for line in fin:
                    ls = line.split(':')
                    if len(ls) > 2:
                        particle_num = int(ls[0])
                        for other_particle_idx in range(1, len(ls) - 1):
                            other_particle_num = int(ls[other_particle_idx])
                            intersections.append([particle_num, other_particle_num])
                fout = open('intersections/' + system_name, 'w')
                for intersection in intersections:
                    str_out = str(intersection[0]) + ' ' + str(intersection[1])
                    fout.write(str_out + '\n')
    return None


if __name__ == '__main__':
     create_intersections_files()
