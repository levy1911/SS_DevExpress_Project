

from subprocess import Popen, PIPE

file_path = 'C:\SUAgent\dist\SUAgent.jar'
analyze_module = 'DevExpress'

# Gene modules:
gene_modules = ['SoftMol', 'SoftDxp', 'SoftFlw', 'SoftBio', 'SoftCtg', 'SoftAcc', 'SoftHla',
                'SoftBioChem', 'SoftPathDx']

with Popen(['java', '-jar', file_path], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
    env_name = ''
    env_dict = {}
    module_list = []
    for line in p.stdout:
        current = line.split('|')[:-1]  # Split returned lines into lists
        temp_list = [current[0], current[1], current[2], current[3], current[4]]
        # temp_list sample: ['Q172',  'CSFLockAdmin', '1.0.1.44.5',  'SSO',    '7.1.1.9.4']
        #                 [[current[0], current[1],   current[2], current[3], current[4]]

        # Divide returned data for one dictionary per given environment
        # form: {'env_name': [list of [lists with module data]]}
        if module_list != [] and module_list[-1][0] != current[0]:
            module_list = []
            module_list.append(temp_list)
        else:
            module_list.append(temp_list)

        env_dict[current[0]] = module_list



    modules_tmp = []
    modules_per_env = []
    second_analyze = []

    # Divided list/dictionaries operation:
    for key, v in env_dict.items():  # range of all dicts
        candidates_final = []
        candidates_tmp = []
        print(['\n\nENV: \n'])
        print('#####################\n')
        print(key)
        print('#####################\n')
        primary_key = 0
        for i in v:
            i.append(primary_key)
            primary_key += 1

        # Make list of all modules per given env - from item[1]
        for item in v:  # range of one dict
            modules_tmp.append(item[1])
            modules_per_env = set(modules_tmp)


        #Clear list from non-gene, non-checkable items
        for i in reversed(v):
            if (i[3] not in modules_per_env) and ('DevExpress' not in i[3]):
                v.remove(i)



        analyzed_module_ends_list = [x for x in v if analyze_module in x[3]]
        for item in analyzed_module_ends_list:
            print(item)

        tmp = []
        tmp2 = []
        for item in analyzed_module_ends_list:
            tmp = [x+[item[5]] for x in v if item[1] in x[3]]
            tmp2.append(tmp)

        # make one list
        list_1 = []
        for x in tmp2:
            for item in x:
                if item[1] in gene_modules:
                    candidates_tmp.append(item)
                else:
                    list_1.append(item)

        ##########START#############
        tmp2 = []
        for item in list_1:
            #print(item[6])
            tmp = [x+[item[5], item[6]] for x in v if item[1] in x[3]]
            tmp2.append(tmp)

        # make one list
        list_2 = []
        for x in tmp2:
            for item in x:
                if item[1] in gene_modules:
                    candidates_tmp.append(item)
                else:
                    list_2.append(item)


        ##########STOP############
        tmp2 = []
        for item in list_2:
            tmp = [x + [item[5], item[6], item[7]] for x in v if item[1] in x[3]]
            tmp2.append(tmp)

        # make one list
        list_3 = []
        for x in tmp2:
            for item in x:
                if item[1] in gene_modules:
                    candidates_tmp.append(item)
                else:
                    list_3.append(item)

        ##########STOP############
        ##########START#############
        tmp2 = []
        for item in list_3:
            tmp = [x + [item[5], item[6], item[7], item[8]] for x in v if item[1] in x[3]]
            tmp2.append(tmp)

        # make one list
        list_4 = []
        for x in tmp2:
            for item in x:
                if item[1] in gene_modules:
                    candidates_tmp.append(item)
                else:
                    list_4.append(item)

        ##########STOP############

        indexes_list = []
        inside_list = []
        for item in candidates_tmp:
            inside_list.append(item)
            indexes_list = item[6:]
            for i in v:
                if i[5] in indexes_list:
                    inside_list.append(i)
            candidates_final.append(inside_list)
            inside_list = []
        #print('candidate')
        #for x in candidates_final:
           # for i in x:
            #    print(i)
       # print('stop')

        for i in candidates_final:
            #Make string
            indexes_list = i[0][5:]
            final_string = 'GENE_MODULE: '
            for item in indexes_list:
                string = [x for x in v if x[5] == item]
                final_string += str(string[0][1]) + '[ver: ' + (str(string[0][2]))+']'
                if 'DevExpress' not in string[0][3]:
                    final_string += ' --> '
                elif 'DevExpress' in string[0][3]:
                    final_string += ' --> ' + str(string[0][3]) + '[ver: ' + (str(string[0][4]))+']'
            print(final_string)













