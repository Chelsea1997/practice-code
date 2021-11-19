#!/usr/bin/env python3

import argparse
import subprocess
from multiprocessing import Process, Manager
import timeit
dict = Manager().dict()
pair_list = []

def dnadiff(dict, file_1, file_2, thread_id):
    ani = '0'
    dnadiff_out_prefix = file_1.split('.')[0] + '_' + file_2.split('.')[0]
    dnadiff_out_prefix_reverse = file_2.split('.')[0] + '_' + file_1.split('.')[0]
    tmp_ani = '0'
    if dnadiff_out_prefix in dict:
        tmp_ani = dict[dnadiff_out_prefix]
    elif dnadiff_out_prefix_reverse in dict:
        tmp_ani = dict[dnadiff_out_prefix_reverse]
    if tmp_ani == '0':
        print('Thread %s: processing dnadiff for pair %s:%s..!'%(thread_id, file_1, file_2))
        out_file = dnadiff_out_prefix + '.report'
        cmd = ['dnadiff', '-p', dnadiff_out_prefix , file_1, file_2]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        o, e = proc.communicate()

       
        line = open(out_file, 'r').readlines()[18]
        ani = line.split('    ')[-1].strip()
        print('Thread %s: Ani for pair %s:%s is %s!'%(thread_id, file_1, file_2, ani))
        dict[dnadiff_out_prefix] = ani


def append_pair_list(file_1, file_2):
    pair = file_1 + ':' + file_2
    #print(pair)
    pair_reverse = file_2 + ':' + file_1
    dnadiff_out_prefix = file_1.split('.')[0] + '_' + file_2.split('.')[0]
    #print("diff",dnadiff_out_prefix)
    dnadiff_out_prefix_reverse = file_2.split('.')[0] + '_' + file_1.split('.')[0]
    if pair not in pair_list and pair_reverse not in pair_list:
        pair_list.append(pair)
        print(pair_list)
    if dnadiff_out_prefix not in dict and dnadiff_out_prefix_reverse not in dict:
        dict[dnadiff_out_prefix] = '0'
        #print(dict)


def parallel_ani(file_list, out_file, t):
    #generate unique pair_list
    global dict
    for file in file_list:
        #print(file)
        targ_list =  file_list.copy()
        #print("file bafter copy",targ_list)
        targ_list.remove(file)
        #print("targ_list",targ_list)
        for target in targ_list:
            append_pair_list(file, target)  # function is called

    index = 0
    while index < len(pair_list):
        procs = []
        print('-'*80)
        for i in range(t):
            pair_files = pair_list[index].split(':')
            print('Starting thread %s: files %s'%(str(i), str(pair_files)))
            if len(pair_files)==2:
                proc = Process(target=dnadiff, args=(dict, pair_files[0], pair_files[1],i))
                procs.append(proc)
                proc.start()
            index += 1
            if index >= len(pair_list):
                break
        for thread_index, proc in enumerate(procs):
            proc.join()
            print('Finishing thread %s'%thread_index)

    print(dict)

    with open(out_file, 'w') as out_file:
        print('-'*18*len(file_list))
        out_file.write('-'*18*len(file_list) + '\n')
        line = ' '*13+ '\t' + "\t".join(file_list)
        print(line)
        out_file.write(line + '\n')
        print('-'*18*len(file_list))
        out_file.write('-'*18*len(file_list) + '\n')
        for index, file in enumerate(file_list):
            targ_list =  file_list.copy()
            print("before",targ_list)
            targ_list.remove(file)
            print("after",targ_list)
            return_pair_list = []
            for target in targ_list:
                ani = '0'
                pair = file.split('.')[0] + '_' + target.split('.')[0]
                pair_reverse = target.split('.')[0] + '_' + file.split('.')[0]
                if pair in dict:
                    ani = dict[pair]
                    print("ani",ani)
                elif pair_reverse in dict:
                    ani = dict[pair_reverse]
                return_pair_list.append(ani)
                print("list",return_pair_list)
            return_pair_list.insert(index, '100')
            line_value = file + ' | ' '\t' + "\t".join(return_pair_list)
            print(line_value)
            out_file.write(line_value + '\n')
            print('-'*18*len(file_list))
            out_file.write('-'*18*len(file_list) + '\n')


def main():
    parser = argparse.ArgumentParser(prog='parallel_ani', description='parallel processing ani')
    parser.add_argument('-i', metavar='bed_file_1', nargs='+', type=str, help='(non-overlapping intervals) BED files to intersect')
    parser.add_argument('-o', metavar='output', type=str, help='(overlapping intervals) BED files to intersect')
    parser.add_argument('-t', metavar='threads', type=int,  default= 1,
                    help='numbers of threads')
    args = parser.parse_args()
    print('Start processing computing average nucleotide identity (ANI) for each pair of file list %s!...'%str(args.i))
    start = timeit.default_timer()
    parallel_ani(args.i,args.o, args.t)

    stop = timeit.default_timer()
    print('Run Time: ', stop - start) 

if __name__ == "__main__":
    main()
