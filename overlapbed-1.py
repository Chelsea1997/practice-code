#!/usr/bin/env python3

import argparse
import time
#from time import clock
overlapping = []
contained = []

Timer_start = time.process_time()

def check_overlaping(chrom, chrom_x_start, chrom_x_end, chrom_y_start, chrom_y_end, is_join, min_overlap):
    join_line = "\t".join([chrom, str(chrom_x_start), str(chrom_x_end)]) + '\t+\t' + "\t".join([chrom, str(chrom_y_start), str(chrom_y_end)])
    overlap_line = "\t".join([chrom, str(chrom_x_start), str(chrom_x_end)])
    overlap_len = min(chrom_x_end,chrom_y_end) - max(chrom_y_start, chrom_x_start)
    if overlap_len >0:
        print('   %s \t %s \t %s \t + \t %s %s'%(chrom, chrom_x_start,chrom_x_end, chrom_y_start,chrom_y_end))
        chrom_x_len = chrom_x_end-chrom_x_start
        chrom_y_len = chrom_y_end-chrom_y_start
        min_len = min(chrom_y_len,chrom_x_len)
        if chrom_y_start <= chrom_x_start < chrom_x_end <= chrom_y_end:
            containing_line = "\t".join([chrom, str(chrom_x_start), str(chrom_x_end)])
            if is_join:
                contained.append(join_line)
            else:
                contained.append(containing_line)
        if min_overlap < 1 and overlap_len/chrom_x_len >= min_overlap:
            if chrom_x_start <= chrom_y_start < chrom_x_end or  chrom_x_start <= chrom_y_end < chrom_x_end:
                overlap_line = "\t".join([chrom, str(chrom_x_start), str(chrom_x_end)])
            if is_join:
                overlapping.append(join_line)
            else:                     
                overlapping.append(line)

# Returns index of x in arr if overlap present, else -1 

def binary_search(chrom, arr, low, high, x_tup, is_join, min_overlap): 
    chrom_x_start = x_tup[0]
    chrom_x_end = x_tup[1]
    
    # Check base case 
    if high >= low: 
  
        mid = (high + low) // 2
        y_tupe = arr[mid]
        chrom_y_start = y_tupe[0]
        chrom_y_end = y_tupe[1]
        
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        if chrom_x_end < chrom_y_start: 
            return binary_search(chrom,arr, low, mid - 1, x_tup, is_join, min_overlap) 
  
        # Else the element can only be present in right subarray 
        elif chrom_x_start > chrom_y_end: 
            return binary_search(chrom,arr, mid + 1, high, x_tup, is_join, min_overlap)
        else:
            check_overlaping(chrom, chrom_x_start, chrom_x_end, chrom_y_start, chrom_y_end, is_join, min_overlap)
            prev_check(chrom, arr, low, high, mid, x_tup, is_join, min_overlap)
            after_check(chrom, arr, low, high, mid, x_tup, is_join, min_overlap)
            return mid
      
    else: 
        # Element is not present in the array 
        return -1


def prev_check(chrom, arr, low, high, pos, x_tup, is_join, min_overlap): 
    chrom_x_start = x_tup[0]
    chrom_x_end = x_tup[1]
    
    # Check base case 
    if high >= low: 
        i = 0
        while i <1:
            pos -= 1
            if pos >=low:
                y_tupe = arr[pos]
                chrom_y_start = y_tupe[0]
                chrom_y_end = y_tupe[1]
                if chrom_x_start > chrom_y_end: 
                    return -1
                else:
                    check_overlaping(chrom, chrom_x_start, chrom_x_end, chrom_y_start, chrom_y_end, is_join, min_overlap)
            else:
                return -1


def after_check(chrom, arr, low, high, pos, x_tup, is_join, min_overlap): 
    chrom_x_start = x_tup[0]
    chrom_x_end = x_tup[1]
    
    # Check base case 
    if high >= low: 
        i = 0
        while i <1:
            pos += 1
            if pos <= high:
                y_tupe = arr[pos]
                chrom_y_start = y_tupe[0]
                chrom_y_end = y_tupe[1]
                if chrom_x_end < chrom_y_start:
                    return -1
                else:
                    check_overlaping(chrom, chrom_x_start, chrom_x_end, chrom_y_start, chrom_y_end, is_join, min_overlap)
            else:
                return -1

def overlapbed(file_1, file_2, out_file, is_join, min_overlap):
    ref_intervals = []
    intron_dict = {}
    exp_intervals = []
    bed_dict = {}
    chro=None
    with open(file_1, "r") as f:
      for line in f:
        line = line.strip().split("\t")
  	 #print(line)
        tmp_chr=line[0]
        start=line[1]
        end=line[2]
        if chro is None:
      	  chro =  tmp_chr
        elif tmp_chr != chro:
      #print(exp_intervals)
          tmp_dict = exp_intervals.copy()
      #print("33333333",tmp_dict)
          bed_dict.update({chro: tmp_dict})
          chro =  tmp_chr
          exp_intervals.clear()
          
        exp_intervals.append(( int(start), int(end)))
         #print(exp_intervals)
    with open(file_2, "r") as f:
     for line in f:
      line = line.strip().split("\t")
      #print(line)
      tmp_chr=line[0]
      start=line[1]
      end=line[2]
  	#print(start)
      if chro is None:
          chro =  tmp_chr
      elif tmp_chr != chro:
          #print(exp_intervals)
      	  tmp_dict = ref_intervals.copy()
      	  #print("33333333",tmp_dict)
      	  intron_dict.update({chro: tmp_dict})
      	  chro =  tmp_chr
      	  ref_intervals.clear()
      	  #print(ref_intervals)
      ref_intervals.append((int(start),int(end)))

   
    for chrom in bed_dict:
        bed_tup_list = bed_dict[chrom]
        if chrom in intron_dict.keys():
            intron_tup_list = intron_dict[chrom]
            for bed_tup in bed_tup_list:
                
                result = binary_search(chrom, intron_tup_list, 0, len(intron_tup_list)-1, bed_tup, is_join, min_overlap)
             
        #break
    with open(out_file, 'w') as out_file:
        lines = contained.copy()
        if min_overlap < 1:
            lines = overlapping.copy()
        for line in lines:
            out_file.write(line + '\n')
    print('Time:',str( time.process_time()-Timer_start))
            
       
def main():
    parser = argparse.ArgumentParser(prog='overlapBed', description='test  overlapBed')
    parser.add_argument('-i1',type=str, help='(non-overlapping intervals) BED files to intersect')
    parser.add_argument('-i2',type=str, help='(non-overlapping intervals) BED files to intersect')
    parser.add_argument('-m',type=float,default= 0.5,help='minimum_overlap, range(0.0, 1.01), default 0.5')
    parser.add_argument('-o',type=str, help='(overlapping intervals) BED files to intersect')
    
    parser.add_argument('--j', default=False, action="store_true" , help="join two entries")
    args = parser.parse_args()
    print('Start processing overlaping Bed files!...')
    overlapbed(args.i1, args.i2, args.o, args.j, args.m )

if __name__ == "__main__":
    main()
