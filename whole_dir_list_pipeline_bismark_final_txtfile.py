import os
import re
import glob
import gzip
import subprocess

###########################################################################################
abs_parent_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IInd_batch_reRunned" #
#abs_parent_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IIIrd_batch"        #
dir_pattern = "SL*/"                                                                      #
                                                                                          #
goto_sub_dir = "bam_files"                                                                #
#goto_sub_dir = "bam_files/log_files"                                                     #
goto_orig_SL_dir = "/gpfs/gpfs1/myerslab/data/Libraries"                                  #
###########################################################################################

out_directory = os.path.join(abs_parent_dir_path, "summary_ofall_LIBS")
if not os.path.exists(out_directory):
    os.makedirs(out_directory)


coverage_metrics = subprocess.check_output("head -3 " + os.path.join(abs_parent_dir_path, "*metrics.txt"), shell=True )
print coverage_metrics + "\n"
with open(os.path.join(out_directory,"coverage_metrics.txt"), "w") as outfile:
    outfile.write(coverage_metrics)


dir_list = [ each_dir[:-1] for each_dir in glob.glob(abs_parent_dir_path + "/" + dir_pattern)]

for each_dir in dir_list:
    each_dir_basename= os.path.basename(each_dir)
    print "\n\nProcessing Lib.. : ", each_dir_basename  + "\n"
    file_list = glob.glob(os.path.join(each_dir,goto_sub_dir,"*%s*.txt" %(each_dir_basename)))
    fastq_file_list = glob.glob(os.path.join(goto_orig_SL_dir,each_dir_basename,"*%s*.gz" %(each_dir_basename)))
    print fastq_file_list

    Total_raw_read = []
    final_analysed_read = []
    final_unique_hit = []

    get_uniq_outfile = os.path.join(out_directory, each_dir_basename + "_" + "bismark_read_count.bed" )
    with open(get_uniq_outfile, "w") as outfile:
        for each_file in file_list:
            with open(each_file, "r") as file:

                data = file.read()

                raw_read_pattern =  "Sequence pairs analysed in total:\s(\d+)"
                regex_next = re.compile(raw_read_pattern)
                read_count = regex_next.findall(data)
                final_analysed_read.extend(read_count)

                unique_hit_pattern = "Number of paired-end alignments with a unique best hit:\s(\d+)"
                regex_next = re.compile(unique_hit_pattern)
                uniquehit_count = regex_next.findall(data)
                final_unique_hit.extend(uniquehit_count)

        for each_fastq in fastq_file_list:
            num_lines = subprocess.check_output("zcat " + each_fastq + "|wc -l", shell=True )
            num_fastq_reads = int(num_lines)/4
            Total_raw_read.append(num_fastq_reads)


        output_print1 = "Total raw_read count for %s : %s" %(each_dir_basename, sum(Total_raw_read))
        print output_print1
        #outfile.write(output_print1 + "\n")

        #convert list of strings to int lists
        uniqe_hit_list_int = map(int, final_unique_hit)
        output_print1 = "Final bismark aligned unique_hit count for %s : %s" %(each_dir_basename, sum(uniqe_hit_list_int)*2)
        print output_print1
        outfile.write(output_print1 + "\n")


        #Convert list of strings to int lists
        read_analysed_int = map(int, final_analysed_read)
        output_print = "Final bismark analysed read_count for %s : %s" %(each_dir_basename, sum(read_analysed_int)*2)
        print output_print
        #outfile.write(output_print + "\n")


