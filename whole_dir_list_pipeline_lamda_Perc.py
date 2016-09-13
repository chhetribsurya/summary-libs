import os
import re
import glob

abs_parent_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IVth_batch"
dir_pattern = "SL*/"
hist(c(1:9))

goto_sub_dir = "bam_files"
out_directory = os.path.join(abs_parent_dir_path, "summary_ofall_LIBS")
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

#####(not_needed) output_file = os.path.join(out_directory,"bismark_read_count.txt")
dir_list = [ each_dir[:-1] for each_dir in glob.glob(abs_parent_dir_path + "/" + dir_pattern)]


abs_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IVth_batch"
SL_List = ["SL120264","SL120272","SL120273"]

goto_sub_dir = "bam_files"
out_directory = os.path.join(abs_dir_path,"summary_ofall_LIBS")
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

#####(not_needed) output_file = os.path.join(out_directory,"bismark_read_count.bed_test")

custom_dir_list = [ os.path.join(abs_dir_path, each_SL) for each_SL in SL_List ]

for each_dir in custom_dir_list:
    each_dir_basename= os.path.basename(each_dir)
    print "\n\nProcessing Lib.. : ", each_dir_basename  + "\n"
    file_list = glob.glob(os.path.join(each_dir,goto_sub_dir,"*%s*.txt"%(each_dir_basename)))

    final_raw_read = []
    final_unique_hit = []

    get_uniq_outfile = os.path.join(out_directory, each_dir_basename + "_" + "bismark_read_count.bed" )
    with open(get_uniq_outfile, "w") as outfile:
        for each_file in file_list:
            with open(each_file, "r") as file:

                data = file.read()

                raw_read_pattern =  "Sequence pairs analysed in total:\s(\d+)"
                regex_next = re.compile(raw_read_pattern)
                read_count = regex_next.findall(data)
                final_raw_read.extend(read_count)

                unique_hit_pattern = "Number of paired-end alignments with a unique best hit:\s(\d+)"
                regex_next = re.compile(unique_hit_pattern)
                uniquehit_count = regex_next.findall(data)
                final_unique_hit.extend(uniquehit_count)


        #print final_raw_read
        #print final_unique_hit

        #Convert list of strings to int lists
        read_list_int = map(int, final_raw_read)
        #read_list_int = [int(each) for each in final_raw_read]
        output_print = "Final read count for %s : %s" %(each_dir_basename, sum(read_list_int))
        print output_print
        outfile.write(output_print + "\n")

        #convert list of strings to int lists
        uniqe_list_int = map(int, final_unique_hit)
        #read_list_int = [int(each) for each in final_unique_hit]
        output_print1 = "Final unique_hit count for %s : %s" %(each_dir_basename, sum(uniqe_list_int))
        print output_print1
        outfile.write(output_print1 + "\n")


# with open(file1, "r") as file:
#     data = file.read()
    
#     pattern1 = "Total methylated C's in CpG context:\s(\d+)"
#   regex_1 = re.compile(pattern)
#   regex_list = regex_1.findall(data)
 

#   pattern2 = "Total unmethylated C's in CpG context:\s(\d+)"
#   regex_2 = re.compile(pattern2)
#   regex_list = regex_2.findall(data)
