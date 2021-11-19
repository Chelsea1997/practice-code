'''
dataframe exercie
'''

import argparse
import pandas as  pd


def parse_args():
    parser =  argparse.ArgumentParser(description = 'This is class exercise 3')
    parser.add_argument('-InputFile',metavar="-InputFile",type=str,help="imput file name")
    parser.add_argument("-OutputFile", metavar="-OutputFile", type=str, help="output file name")
    print("successful")
    args = parser.parse_args()
    return args



def read_data(input_file):
    input_file1 = pd.ExcelFile(input_file)
    dt_well = pd.read_excel(input_file1, 'WellData')
    dt_dictionary = pd.read_excel(input_file1, 'Dictionary')
    print("data read")
    return dt_well, dt_dictionary





def calculate_ratio(dt_well):
    
    df1 = dt_well[dt_well['TargetType'] == 'Ch1Unknown']
    df2= dt_well[dt_well['TargetType'] == 'Ch2Unknown']

    dt_well_sl = pd.merge(df1, df2, left_on = 'Well', right_on = 'Well', how = 'outer')
    dt_well_sl['Ratio'] = dt_well_sl['Concentration_y']/(dt_well_sl['Concentration_y']+dt_well_sl['Concentration_x'])

    print("ratio calculated")
    return dt_well_sl



def master_merge(dt_dictionary, dt_well_sl):
    dt_master = pd.merge(dt_dictionary, dt_well_sl, left_on = 'Well', right_on = 'Well', how = 'outer')
    print("aprt 4 done")
    return dt_master



def pivot(dt_master):
    dt_output1 = dt_master.pivot_table(index=['Strain1','Strain2','Replicate'],columns=('Time Point'),values='Ratio').rename_axis(None,axis=1)
    print("part 5 done")
    return dt_output1



def strain_avg(dt_output1):
    dt_output2 = dt_master.pivot_table(index=['Strain1','Strain2'],columns=('Time Point'),values="Ratio").rename_axis(None,axis=1)
    print("part 6 done")
    return dt_output2




def write_data(output_file, dt_output1, dt_output2):
    writer = pd.ExcelWriter(output_file)

    dt_output1.to_excel(writer, sheet_name='All_data')
    dt_output2.to_excel(writer, sheet_name='Average_data')
    writer.save()
    

if __name__ == '__main__':
    args = parse_args()
    dt_well, dt_dictionary = read_data(args.InputFile)
    dt_well_sl = calculate_ratio(dt_well)
    dt_master = master_merge(dt_dictionary, dt_well_sl)
    dt_output1 = pivot(dt_master)
    dt_output2 = strain_avg(dt_output1)
    write_data(args.OutputFile, dt_output1, dt_output2)