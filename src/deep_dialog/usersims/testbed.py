import random

class TestBed:
    goal_dict = {}
    banned_keys = []
    goal_change_prob = 0.0

    stats_dict = {}

    #TODO:
    # Create program to change run configs (3rd party, should modify the .sh scripts). --things like #episodes, read/write path, train/test bit
    # Program will then write information like % chance array to a file to be read here in init.
    # Program should then be able to output results like %accuracy

    #def __init__:
    # init should real from config file that is set by script, and set local variables
    # these variables can then be accessed in regions of the usersim_rule.py program and
    # take certain actions or reply with certain information.
    # There should also be a function for writing reports to an output file based on stats gathered

    def init_stats_dict(self, num_events):
        for i in range(0,num_events):
            temp_str = "event_"+str(i)
            self.stats_dict[temp_str] = 0
        self.stats_dict["total"] = 0

        print(self.stats_dict)

    def collect_stats(self, event):
        """
        event==0: a: r in g_u_i / u: i
        event==1: a: r in history_slots / u: i
        event==2: a: r in g_u_r / u: r
        """
        # if(event == 0):
        #     print("a: r in g_u_i / u: i")
        # elif(event == 1):
        #     print("a: r in history_slots / u: i")
        # elif(event == 2):
        #     print("a: r in g_u_r / u: r")
        # else:
        #     print("COLLECT STATS ERROR")
        #     return

        self.stats_dict["event_"+str(event)] = self.stats_dict["event_"+str(event)] + 1
        self.stats_dict["total"] = self.stats_dict["total"] + 1

    # Creates dictionary to easily access possible value space
    def build_goal_dict(self, full_list):
        self.goal_dict = {} #Reset goal_dict

        for goal in full_list['all']: #For all example goals in list
            for key in goal['inform_slots']: #In given goal's inform slots, put into dictionary
                if(key not in self.goal_dict):
                    self.goal_dict[key] = []
                if(goal['inform_slots'][key] not in self.goal_dict[key]):
                    self.goal_dict[key].append(goal['inform_slots'][key])


    def event_rand_slot_change(self, probability, state, goal, key='no_key',):
        # TODO: Somewhere in here we want to randomly change slot value permanently as an almost random mutation,
        # not in response to anything
        assert probability >= 0 and probability <= 1

        if(random.randint(0,int(1/probability)) == 0): #Upper value can be how susceptible to change a user is
            print("Modified!")
            # self.rand_change_slot(key)
            return self.random_history_sample(state, goal)
        else:
            print("UNMODIFIED")
            return state, goal

    # # Will change a random slot in given goal with a random value for that slot
    def rand_change_slot(self, key='no_key'):
        if(key == 'no_key'):
            slot_list = list(self.goal['inform_slots']) #TODO: Possibly modify to only use slots from history?
            key = slot_list[random.randint(0,len(slot_list)-1)]

            if(key in self.banned_keys):
                return self.rand_change_slot()

        poss_value_list = list(self.goal_dict[key])
        random_slot_value = poss_value_list[random.randint(0,len(poss_value_list)-1)]


        #TODO: Debug
        # print("Key: ", key, " old val: ", self.goal['inform_slots'][key], " new val: ", random_slot_value)

        # print "#### DEBUG ####"
        # print self.state
        # print "###############"
        # print self.goal
        # exit()

        print "Changing: ", key, " from value: ", self.goal['inform_slots'][key], " to value: ", random_slot_value

        self.goal['inform_slots'][key] = random_slot_value
        #TODO: Make sure these are being changed
        if(key in self.state['history_slots']):
            self.state['history_slots'][key] = random_slot_value #Actually has a value to change
        # if(key in self.state['rest_slots']): # Shouldn't need to change anything since rest is just the key and no value
            # self.state['rest_slots'][key] = random_slot_value

    #POST CONDITION: self.state['inform_slots'][rand_key] will be populated with a new value, so that an
    #outgoing request (or inform?) can have this value with the purpose of contradicting something on agent side
    def random_history_sample(self, state, goal):
        previous_keys_list = list(state['history_slots'])
        if(len(previous_keys_list) == 0):
            return state, goal
        # print(previous_keys_list)
        old_key = previous_keys_list[random.randint(0,len(previous_keys_list)-1)]

        #Not a valid key anyway
        #TODO: What if history key was never in goal inform_slots? Has to be
        if(old_key not in goal['inform_slots']):
            # self.random_history_sample() #TODO: Potential stack overflow?
            return state, goal

        #Get new value to go with old key
        poss_value_list = list(self.goal_dict[old_key])
        random_slot_value = poss_value_list[random.randint(0,len(poss_value_list)-1)]
        # print(old_key, random_slot_value)

        #by nature, this key shoudln't be in inform_slots because it's history - what about if in request slots?

        # print("Changing slot: ", old_key, " with old value: ", self.state['inform_slots'][old_key], " to: ", random_history_sample)
        #Find find slot that was informed or requested (does it even matter?), then make arbitrary request with this as inform slot
        #Shouldn't goal inform slots be changed too?
        state['history_slots'][old_key] = random_slot_value # Ensures that outgoing message has modification
        state['inform_slots'][old_key] = random_slot_value # Ensures that outgoing message has modification
        goal['inform_slots'][old_key] = random_slot_value # Changes goal so that change is permanent

        return state, goal









##### CODE GARBAGE CAN ########
def event_rand_slot_change_old(self, probability, key='no_key'):
    # TODO: Somewhere in here we want to randomly change slot value permanently as an almost random mutation,
    # not in response to anything
    assert probability >= 0 and probability <= 1

    if(random.randint(0,int(1/probability)) == 0): #Upper value can be how susceptible to change a user is
        print("Modified!")
        # self.rand_change_slot(key)
        self.random_history_sample()
    else:
        print("UNMODIFIED")

# # Will change a random slot in given goal with a random value for that slot
def rand_change_slot_old(self, key='no_key'):
    if(key == 'no_key'):
        slot_list = list(self.goal['inform_slots']) #TODO: Possibly modify to only use slots from history?
        key = slot_list[random.randint(0,len(slot_list)-1)]

        if(key in self.banned_keys):
            return self.rand_change_slot()

    poss_value_list = list(self.goal_dict[key])
    random_slot_value = poss_value_list[random.randint(0,len(poss_value_list)-1)]


    #TODO: Debug
    # print("Key: ", key, " old val: ", self.goal['inform_slots'][key], " new val: ", random_slot_value)

    # print "#### DEBUG ####"
    # print self.state
    # print "###############"
    # print self.goal
    # exit()

    print "Changing: ", key, " from value: ", self.goal['inform_slots'][key], " to value: ", random_slot_value

    self.goal['inform_slots'][key] = random_slot_value
    #TODO: Make sure these are being changed
    if(key in self.state['history_slots']):
        self.state['history_slots'][key] = random_slot_value #Actually has a value to change
    # if(key in self.state['rest_slots']): # Shouldn't need to change anything since rest is just the key and no value
        # self.state['rest_slots'][key] = random_slot_value

#POST CONDITION: self.state['inform_slots'][rand_key] will be populated with a new value, so that an
#outgoing request (or inform?) can have this value with the purpose of contradicting something on agent side
def random_history_sample_old(self):
    previous_keys_list = list(self.state['history_slots'])
    # print(previous_keys_list)
    old_key = previous_keys_list[random.randint(0,len(previous_keys_list)-1)]

    #Not a valid key anyway
    #TODO: What if history key was never in goal inform_slots? Has to be
    if(old_key not in self.goal['inform_slots']):
        self.random_history_sample() #TODO: Potential stack overflow?
        return

    #Get new value to go with old key
    poss_value_list = list(self.goal_dict[old_key])
    random_slot_value = poss_value_list[random.randint(0,len(poss_value_list)-1)]
    # print(old_key, random_slot_value)

    #by nature, this key shoudln't be in inform_slots because it's history - what about if in request slots?

    # print("Changing slot: ", old_key, " with old value: ", self.state['inform_slots'][old_key], " to: ", random_history_sample)
    #Find find slot that was informed or requested (does it even matter?), then make arbitrary request with this as inform slot
    #Shouldn't goal inform slots be changed too?
    self.state['inform_slots'][old_key] = random_slot_value # Ensures that outgoing message has modification
    self.goal['inform_slots'][old_key] = random_slot_value # Changes goal so that change is permanent
