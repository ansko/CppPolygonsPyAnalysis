#!/usr/bin/env python3


import copy
import math

import pprint
pprint=pprint.PrettyPrinter(indent=4).pprint


def get_clusters_from_files():
    cubic_cell_size = 5.0
    culster_folder = 'clusters'
    minmaxes_folder = '/home/anton/Projects/FEM/minmax'
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    cluster_properties_entry = {'cluster_size': None,
                                'cluster_x_len': None,
                                'cluster_y_len': None,
                                'cluster_z_len': None,
                                'particles': []}
    clusters = {tau: {str(N): [] for N in Ns} for tau in taus}
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                # analyzing file with list of clusters in the system
                system_name = 'tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname = culster_folder + '/' + system_name
                fin = open(fname, 'r')
                clusters_in_system = []
                for line in fin:
                    ls = line.split()
                    if len(ls) < 2:
                        continue
                    cluster = [int(ls[i]) for i in range(len(ls))]
                    clusters_in_system.append(cluster)
                for cluster in clusters_in_system:
                    entry = copy.deepcopy(cluster_properties_entry)
                    entry['cluster_size'] = len(cluster)
                    entry['particles'] = cluster
                    clusters[tau][str(N)].append(entry)
    for tau in taus:
        for N in Ns:
            for attempt in range(5):
                # analyzing file with particle minmaxes
                system_name = 'tau' + tau + 'N' + str(N) + '_' + str(attempt)
                fname = minmaxes_folder + '/' + system_name
                fin = open(fname, 'r')
                minmaxes = []
                for line in fin:
                    ls = line.split(':') # number:minx:miny:minz:maxx:maxy:maxz
                    minmaxes.append([float(ls[1]), float(ls[2]), float(ls[3]),
                                     float(ls[4]), float(ls[5]), float(ls[6])])
                # calculating every cluster's size
                for cluster in clusters[tau][str(N)]:
                    min_x = cubic_cell_size
                    min_y = cubic_cell_size
                    min_z = cubic_cell_size
                    max_x = 0
                    max_y = 0
                    max_z = 0
                    for particle in cluster['particles']:
                        min_x = min(min_x, minmaxes[particle][0])
                        min_y = min(min_y, minmaxes[particle][1])
                        min_z = min(min_z, minmaxes[particle][2])
                        max_x = max(max_x, minmaxes[particle][3])
                        max_y = max(max_x, minmaxes[particle][4])
                        max_z = max(max_x, minmaxes[particle][5])
                    cluster['cluster_x_len'] = max_x - min_x
                    cluster['cluster_y_len'] = max_y - min_y
                    cluster['cluster_z_len'] = max_z - min_z
    #pprint(clusters)
    return clusters


def analyze_average_clusteriaztion_rate():
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    clusters = get_clusters_from_files()
    average_clusterization_rates = {tau: {str(N): 0 for N in Ns} for tau in taus}
    box_volume = 125.0
    filler_R = 0.87
    filler_h = 0.1
    sin_central = math.sin(2 * math.pi / 6)
    filler_particle_volume = 6 * filler_R**2 / 2 * sin_central * filler_h
    for tau in taus:
        for N in Ns:
            clusterized_particles_number = 0
            clusters_number = len(clusters[tau][str(N)])
            particles_number = N * 5 # 5 == attempts_number
            for cluster in clusters[tau][str(N)]:
                clusterized_particles_number += cluster['cluster_size']
            rate = clusterized_particles_number / particles_number
            average_clusterization_rates[tau][str(N)] = rate
    heading_str = '  N     rate\n'
    for tau in taus:
        fout = open('clusterization_rates' + tau, 'w')
        fout.write(heading_str)
        for N in Ns:
            filler_fi = filler_particle_volume * N / box_volume
            rate = average_clusterization_rates[tau][str(N)]
            str_out = '%.3f' % filler_fi + '\t' + '%.2f' % rate + '\n'
            fout.write(str_out)


def analyze_average_cluster_size():
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    clusters = get_clusters_from_files()
    average_clusteriz_sizes = {tau: {str(N): 0 for N in Ns} for tau in taus}
    box_volume = 125.0
    filler_R = 0.87
    filler_h = 0.1
    sin_central = math.sin(2 * math.pi / 6)
    filler_particle_volume = 6 * filler_R**2 / 2 * sin_central * filler_h
    for tau in taus:
        for N in Ns:
            ave_cluster_size = 0  
            clusters_number = len(clusters[tau][str(N)])
            for cluster in clusters[tau][str(N)]:
                ave_cluster_size += cluster['cluster_size']
            ave_cluster_size /= clusters_number * N
            average_clusteriz_sizes[tau][str(N)] = ave_cluster_size
    heading_str = '  N  ave_cluster_size\n'
    for tau in taus:
        fout = open('cluster_sizes' + tau, 'w')
        fout.write(heading_str)
        for N in Ns:
            filler_fi = filler_particle_volume * N / box_volume
            size = average_clusteriz_sizes[tau][str(N)]
            str_out = '%.3f' % filler_fi + '\t' + '%.2f' % size + '\n'
            fout.write(str_out)


def analyze_average_cluster_length():
    Ns = [4, 8, 12, 16, 20, 24, 28, 30]
    taus = ['1.5', '2.5', '5']
    clusters = get_clusters_from_files()
    average_cluster_lengths = {tau: { str(N): [0, 0, 0] for N in Ns
                                    } for tau in taus
                              }
    box_len = 5.0
    box_volume = box_len**3
    filler_R = 0.87
    filler_h = 0.1
    sin_central = math.sin(2 * math.pi / 6)
    filler_particle_volume = 6 * filler_R**2 / 2 * sin_central * filler_h
    for tau in taus:
        for N in Ns:
            cluster_size_sum_x = 0
            cluster_size_sum_y = 0
            cluster_size_sum_z = 0
            for cluster in clusters[tau][str(N)]:
                cluster_size_sum_x += cluster['cluster_x_len']
                cluster_size_sum_y += cluster['cluster_y_len']
                cluster_size_sum_z += cluster['cluster_z_len']
            average_cluster_lengths[tau][str(N)][0] += cluster_size_sum_x
            average_cluster_lengths[tau][str(N)][1] += cluster_size_sum_y
            average_cluster_lengths[tau][str(N)][2] += cluster_size_sum_z
            average_cluster_lengths[tau][str(N)][0] /= len(clusters[tau][str(N)])
            average_cluster_lengths[tau][str(N)][1] /= len(clusters[tau][str(N)])
            average_cluster_lengths[tau][str(N)][2] /= len(clusters[tau][str(N)])
    heading_str = '  fi    ave_size\n'
    for tau in taus:
        fout = open('cluster_sizes' + tau, 'w')
        fout.write(heading_str)
        for N in Ns:
            cluster = average_cluster_lengths[tau][str(N)]
            filler_fi = filler_particle_volume * N / box_volume
            ave_length = (cluster[0] + cluster[1] + cluster[2]) / 3 / box_len
            str_out = '%.3f' % filler_fi + '\t' + '%.2f' % ave_length + '\n'
            fout.write(str_out)

if __name__ == '__main__':
    #get_clusters_from_files()
    #analyze_average_clusteriaztion_rate()
    analyze_average_cluster_size() # size in particles
    #analyze_average_cluster_length()
