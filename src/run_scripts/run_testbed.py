import os
import sys
from csv import reader

#TODO:
# Create program to change run configs (3rd party, should modify the .sh scripts). --things like #episodes, read/write path, train/test bit
# Program will then write information like % chance array to a file to be read here in init.
# Program should then be able to output results like %accuracy

#def __init__:
# init should real from config file that is set by script, and set local variables
# these variables can then be accessed in regions of the usersim_rule.py program and
# take certain actions or reply with certain information.
# There should also be a function for writing reports to an output file based on stats gathered

#1.) read from file with run configs - line by line --create big string that can be appended at the end of the script

def test_main(filename):
    #Read config file
    list_of_rows = []
    with open(filename, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        # print list_of_rows

    for line in list_of_rows:
        train = int(line[0])#line['train'] #will determine training or just running outputs (saved to file) run_mode 3 == train, 2 == test
        num_episodes = int(line[1])#line['num_episodes'] #used in runscript --'num_episodes'
        out_path = line[2].strip(" ")#line['out_path'] #used in runscript --'write_model_dir'
        in_path = line[3].strip(" ")#line['in_path'] #used in runscript --'trained_model_path'
        #pct_array = line['pct_arry'] #just write to file that can be red on userside

        #TODO: Write to static file shared universally

        built_str = "--run_mode {0} \
                  --episodes {1} \
                  --write_model_dir ./deep_dialog/checkpoints/rl_agent/{2} \
                  --trained_model_path ./deep_dialog/checkpoints/rl_agent/{3} \ ".format(train, num_episodes, out_path, in_path)

        cmd_str="echo \"" + built_str + "\" | sh template_script.sh"
        # print cmd_str
        os.system(cmd_str)

if __name__ == "__main__":
   test_main(sys.argv[1])
