import os
import re
import glob
import gzip
import subprocess
import tarfile

#zcat $file | split -l 72000000 -d - $OUTPUT_DIR/$LIB/$SPLIT_NAME

abs_parent_dir_path = "/gpfs/gpfs1/home/schhetri/wgbs_run/wgbs_split_IVth_batch"
dir_pattern = "SL*/"

goto_sub_dir = "bam_files"
goto_orig_SL_dir = "/gpfs/gpfs1/myerslab/data/Libraries"


out_directory = os.path.join(abs_parent_dir_path, "summary_ofall_LIBS")
if not os.path.exists(out_directory):
    os.makedirs(out_directory)

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




        #print final_analysed_read
        #print final_unique_hit

        #Convert list of strings to int lists
        read_analysed_int = map(int, final_analysed_read)
        #read_analysed_int = [int(each) for each in final_analysed_read]
        output_print = "Final bismark analysed read_count for %s : %s" %(each_dir_basename, sum(read_analysed_int)*2)
        print output_print
        outfile.write(output_print + "\n")

        #convert list of strings to int lists
        uniqe_hit_list_int = map(int, final_unique_hit)
        #read_analysed_int = [int(each) for each in final_unique_hit]
        output_print1 = "Final bismark aligned unique_hit count for %s : %s" %(each_dir_basename, sum(uniqe_hit_list_int)*2)
        print output_print1
        outfile.write(output_print1 + "\n")

        #convert list of strings to int lists
        output_print1 = "Total raw_read count for %s : %s" %(each_dir_basename, sum(Total_raw_read))
        print output_print1
        outfile.write(output_print1 + "\n")




#tar = tarfile.open("yourFile.tar.gz")
#tar.extractall("folderWithExtractedFiles")
#with gzip.open(fname) as f:
    
#os.path.getsize(file)
#num_lines = sum(1 for line in open('myfile.txt') if line.rstrip()) ## for filter empty lines
#file = "/home/surya/Desktop/suraj_dai_thesis.txt" #string not a file object
#a = os.system("cat " + file + "|wc -l")
#48 #type(a) = int
# In [105]: a = os.system("ls -l " + file)
# -rw-rw-r-- 1 surya surya 17345 May 24 22:59 /home/surya/Desktop/suraj_dai_thesis.txt


# import subprocess

# proc = subprocess.Popen(["cat", "/etc/services"], stdout=subprocess.PIPE, shell=True)
# (out, err) = proc.communicate()
# print "program output:", out

#or using function like below:

# from subprocess import PIPE, Popen

# def cmdline(command):
#     process = Popen(
#         args=command,
#         stdout=PIPE,
#         shell=True
#     )
#     return process.communicate()[0]

# print cmdline("cat /etc/services") # or, cmdline("cat " + file)
# print cmdline('ls')
# print cmdline('rpm -qa | grep "php"')
# print cmdline('nslookup google.com')



# You might also want to look at the subprocess module, which was built to replace the whole family of Python popen-type calls.
# import subprocess
# output = subprocess.check_output("cat /etc/services", shell=True)
# The advantage it has is that there is a ton of flexibility with how you invoke commands, where the standard in/out/error streams are connected, etc.


#os.system returns the exit status of the command not the output of the command. 
#To capture the output of a command you should look into the subprocess module.
#subprocess.check_output("zcat " + file1 + " | wc --bytes", shell=True)
# Output the size in bytes of file1 with a trailing new line character
#However it is probably better to use other python modules/methods to do that as suggested by other as it is preferable to do things directly in Python.


#os.system doesn't returns the output, use subprocess.check_output for that
#If you look at the os.system docs, they explicitly tell you that it has "limitations" and that "the subprocess module has more powerful facilities for spawning new processes and retrieving their results", and that "using that module is preferable to using this function.
# In [116]: subprocess.check_output("cat " + file + "|wc -l", shell=True )
# Out[116]: '48\n'

# In [117]: a = subprocess.check_output("cat " + file + "|wc -l", shell=True )

# In [118]: a
# Out[118]: '48\n'

# In [119]: int(a)
# Out[119]: 48

