from subprocess import Popen, PIPE

file_path = 'C:\SUAgent\dist\SUAgent.jar'
analyze_module = 'DevExpress'

# Gene modules:
gene_modules = ['SoftMol', 'SoftDxp', 'SoftFlw', 'SoftBio', 'SoftCtg', 'SoftAcc', 'SoftHla',
                'SoftBioChem', 'SoftPathDx']

line_length = 150
# Final results output
final_output = ''
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
    affected_environments = []

    # Divided list/dictionaries operation:
    for key, v in env_dict.items():  # range of all dicts
        candidates_final = []
        candidates_tmp = []

        primary_key = 0
        for i in v:
            i.append(primary_key)
            primary_key += 1

        # Make list of all modules per given env - from item[1]
        for item in v:  # range of one dict
            modules_tmp.append(item[1])
            modules_per_env = set(modules_tmp)

        # Clear list from non-gene, non-checkable items
        for i in reversed(v):
            if (i[3] not in modules_per_env) and (analyze_module not in i[3]):
                v.remove(i)

        # All DevExpress -ends positions
        analyzed_module_ends_list = [x for x in v if analyze_module in x[3]]

        # Not displaying environments with no DevExpress:
        if len(analyzed_module_ends_list) != 0:

            gene_modules_per_env = [x for x in modules_per_env if x in gene_modules]

            final_output += '\nENVIRONMENT: ' + str(key) + '\n\n'

            analyzed_module_ends_list_unique = []

            final_output += '\nInvolved modules: \n\n'
            for item in analyzed_module_ends_list:
                analyzed_module_ends_list_unique.append(str(item[3]) + ' ' + str(item[4]))
                final_output += ' - ' + str(item[1]) + ' ' + str(item[2]) + '\n'

            final_output += "\nDevExpress versions on environment: \n\n"
            analyzed_module_ends_list_unique = set(analyzed_module_ends_list_unique)
            for item in analyzed_module_ends_list_unique:
                final_output += ' - ' + str(item) + '\n'
            if len(analyzed_module_ends_list_unique) > 1:
                affected_environments.append(str(key)+'('+str(len(analyzed_module_ends_list_unique))+')')

            final_output += '\nGene modules on Environments:\n\n'
            for item in gene_modules_per_env:
                final_output += ' - ' + str(item) + '\n'

            final_output += '\nGene modules indirect connections with DevExpress: \n\n'
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
            if list_2 is not None:
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
            if list_3 is not None:
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

            for i in candidates_final:
                #Make string
                indexes_list = i[0][5:]
                final_string = 'GENE_MODULE: '
                for item in indexes_list:
                    string = [x for x in v if x[5] == item]
                    final_string += str(string[0][1]) + '[ver: ' + (str(string[0][2]))+']'
                    if analyze_module not in string[0][3]:
                        final_string += ' --> '
                    elif analyze_module in string[0][3]:
                        final_string += ' --> ' + str(string[0][3]) + '[ver: ' + (str(string[0][4]))+']'
                final_output += final_string + '\n'
            final_output += '-'*line_length +'\n'
        else:
            final_output += '\nENVIRONMENT: ' + str(key) + '\n\n'
            final_output += '\n\nNO GENE MODULES\n\n'
            final_output += '-' * line_length + '\n'
    final_output += '#'*line_length + '\n'
    final_output += 'Affected environments list (and how many different versions is detected):\n'
    final_output += str(', '.join(affected_environments))
    final_output += '\n'+'#'*line_length

print(final_output)











