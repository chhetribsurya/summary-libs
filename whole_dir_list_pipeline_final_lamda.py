import os
import re
import glob
import gzip
import subprocess
import sys

#####################################################################################
abs_parent_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IIIrd_batch"    #
dir_pattern = "SL*/"                                                                #
                                                                                    #
goto_sub_dir = "Lambda_Bisulfite_Conv_Eff"                                          #
#goto_orig_SL_dir = "/gpfs/gpfs1/myerslab/data/Libraries"                           #
#####################################################################################

out_directory = os.path.join(abs_parent_dir_path, "summary_ofall_LIBS")
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

dir_list = [ each_dir[:-1] for each_dir in glob.glob(abs_parent_dir_path + "/" + dir_pattern)]
print dir_list

for each_dir in dir_list:
    each_dir_basename= os.path.basename(each_dir)
    print "\n\nProcessing Lib.. : ", each_dir_basename  + "\n"
    file_list = glob.glob(os.path.join(each_dir,goto_sub_dir,"*%s*.txt" %(each_dir_basename)))
    #fastq_file_list = glob.glob(os.path.join(goto_orig_SL_dir,each_dir_basename,"*%s*.gz" %(each_dir_basename)))

    Total_meth_count = []
    Total_unmeth_count = []

    get_uniq_outfile = os.path.join(out_directory, each_dir_basename + "_" + "lambda_percent.bed" )
    with open(get_uniq_outfile, "w") as outfile:
        for each_file in file_list:
            with open(each_file, "r") as file:

                data = file.read()

                meth_cpg_pattern =  "Total methylated C's in CpG context:\s(\d+)"
                regex_next = re.compile(meth_cpg_pattern)
                meth_count = regex_next.findall(data)
                Total_meth_count.extend(meth_count)

                unmeth_cpg_pattern = "Total unmethylated C's in CpG context:\s(\d+)"
                regex_next = re.compile(unmeth_cpg_pattern)
                unmeth_count = regex_next.findall(data)
                Total_unmeth_count.extend(unmeth_count)

        try: 
            #Convert list of strings to int lists
            Total_meth_count_int = sum(map(int, Total_meth_count))
            Total_unmeth_count_int = sum(map(int, Total_unmeth_count))
            Meth_percent = round(float(Total_meth_count_int)/float(Total_meth_count_int + Total_unmeth_count_int)*100, 2)

            output_print = "Lambda_methylation_percentage for %s : %s" %(each_dir_basename, Meth_percent)
            print output_print
            outfile.write(output_print + "\n")

        #except (ZeroDivisionError, NameError):
        except (ZeroDivisionError):
            error_print = "Note: please check %s, probably your lambda file is missing\n" %(each_dir_basename) 
            print error_print
            outfile.write(error_print + "\n")


