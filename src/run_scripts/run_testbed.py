import os
import sys
import csv

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
    with open(filename, 'r') as read_obj: #filename is probably run_configs.csv
        # pass the file object to reader() to get the reader object
        csv_reader = csv.reader(read_obj)
        # Pass reader object to list() to get a list of lists
        list_of_rows = list(csv_reader)
        # print list_of_rows


    # METHODS NUMS:
    # 0: CONTROL
    # 1:
    # 2:
    # 3:
    # 4:
    #---- MIXES ----
    # 5:

    # Train: 3 = ??, 2= ??
    # { method, train, train_epoch_start, num_episodes, in_path, out_path, [aggresiveness_list] }
    # Row
    # { method, train_split, [aggresiveness_list], [epoch data], ave_reward, success_rate, ave_turns, current_epoch,epoch_time }
    pct_array = []
    for line in list_of_rows:
        method = int(line[0])
        train = int(line[1])#line['train'] #will determine training or just running outputs (saved to file) run_mode 3 == train, 2 == test
        #THIS IS ACTUALLY NUM EPOCHS (#episodes where its trained)
        goal_shift_epoch = (int(line[2]))
        num_episodes = int(line[3])#line['num_episodes'] #used in runscript --'num_episodes'
        out_path = line[4].strip(" ")#line['out_path'] #used in runscript --'write_model_dir'
        in_path = line[5].strip(" ")#line['in_path'] #used in runscript --'trained_model_path'
        #pct_array = line['pct_arry'] #just write to file that can be red on userside

        print "in and out!!"
        print in_path
        print out_path

        del pct_array[:]
        pct_array.append(method)
        pct_array.append(goal_shift_epoch) #TODO: Make sure user uses this -- whoever reads from config_array.csv
        for i in range(6, len(line)):
            pct_array.append(float(line[i]))

        with open('config_array.csv','w') as result_file:
            wr = csv.writer(result_file)
            wr.writerow(pct_array)


        if(in_path == "NULL"):
            built_str = "--run_mode {0} \
                      --episodes {1} \
                      --write_model_dir ./deep_dialog/checkpoints/rl_agent{2} \ ".format(train, num_episodes, out_path)
        else:
            #Copy file we are thinking of to a universal name?
            # cmd_str="cp `ls -Art ./deep_dialog/checkpoints/rl_agent{0}*.p | tail -1` universal.p".format(in_path)
            # print cmd_str

            os.system("rm ../deep_dialog/checkpoints/rl_agent{0}/universal.p".format(in_path))

            os.system("cp `ls -Art ../deep_dialog/checkpoints/rl_agent{0}/*.p | tail -1` ../deep_dialog/checkpoints/rl_agent{0}/universal.p".format(in_path))
            # os.system("echo \"howdy\"")

            built_str = "--run_mode {0} \
                      --episodes {1} \
                      --write_model_dir ./deep_dialog/checkpoints/rl_agent{2} \
                      --trained_model_path ./deep_dialog/checkpoints/rl_agent{3}/universal.p \ ".format(train, num_episodes, out_path, in_path)

        cmd_str="echo \"" + built_str + "\" | sh template_script.sh"
        # print cmd_str
        os.system(cmd_str)

if __name__ == "__main__":
   test_main(sys.argv[1])
