from subprocess import Popen, PIPE


class Seeker:

    # Gene modules:
    gene_modules = ['SoftMol', 'SoftDxp', 'SoftFlw', 'SoftBio', 'SoftCtg', 'SoftAcc', 'SoftHla',
                    'SoftBioChem', 'SoftPathDx']
    line_length = 150
    # Final results output
    final_output = ''

    # Second file data
    second_output = ''
    second_output_list = []
    second_gene_ver = ''
    second_gene_ver = ''
    second_env_name = ''
    second_client_name = ''
    second_devE_ver = ''
    second_output_list_sorted = []

    def seek(self, analyze_module='DevExpress', output_filename='dependency_report.txt', second_filename = 'short_dep_report.txt', file_path='C:\SUAgent\dist\SUAgent.jar'):
        '''

        :param analyze_module: Which module needs to be searched for
        :param output_filename: Filename of end results
        :param file_path: Path to SUAgent.jar (derby db connector)
        :return: Name of prepared file (ex. report.txt)
        '''

        with Popen(['java', '-jar', file_path], stdout=PIPE, bufsize=1, universal_newlines=True) as p:
            env_dict = {}
            module_list = []
            for line in p.stdout:
                current = line.split('|')[:-1]  # Split returned lines into lists
                temp_list = [current[0], current[1], current[2], current[3], current[4], current[5]]
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
            affected_environments = []
            dev_version_linked_to_gene = []

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
                    # Get client name for second file
                    self.second_client_name = item[5]
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

                    gene_modules_per_env = [x for x in modules_per_env if x in self.gene_modules]

                    self.final_output += '\nENVIRONMENT: ' + str(key) + '\n'

                    self.final_output += '\nCLIENT: ' + self.second_client_name + '\n\n'

                    # Get Environment name for second file
                    self.second_env_name = str(key)

                    analyzed_module_ends_list_unique = []

                    self.final_output += '\nInvolved modules: \n\n'
                    for item in analyzed_module_ends_list:
                        analyzed_module_ends_list_unique.append(str(item[3]) + ' ' + str(item[4]))
                        self.final_output += ' - ' + str(item[1]) + ' ' + str(item[2]) + '\n'

                    self.final_output += '\nGene modules on Environments:\n\n'
                    for item in gene_modules_per_env:
                        self.final_output += ' - ' + str(item) + '\n'

                    # Main algorithm
                    tmp2 = []
                    for item in analyzed_module_ends_list:
                        tmp = [x+[item[6]] for x in v if item[1] in x[3]]
                        tmp2.append(tmp)

                    # make one list
                    list_1 = []
                    for x in tmp2:
                        for item in x:
                            if item[1] in self.gene_modules:
                                candidates_tmp.append(item)
                            else:
                                list_1.append(item)

                    ##########START#############
                    tmp2 = []
                    for item in list_1:
                        tmp = [x+[item[6], item[7]] for x in v if item[1] in x[3]]
                        tmp2.append(tmp)

                    # make one list
                    list_2 = []
                    for x in tmp2:
                        for item in x:
                            if item[1] in self.gene_modules:
                                candidates_tmp.append(item)
                            else:
                                list_2.append(item)

                    ##########STOP############
                    if list_2 is not None:
                        tmp2 = []
                        for item in list_2:
                            tmp = [x + [item[6], item[7], item[8]] for x in v if item[1] in x[3]]
                            tmp2.append(tmp)

                        # make one list
                        list_3 = []
                        for x in tmp2:
                            for item in x:
                                if item[1] in self.gene_modules:
                                    candidates_tmp.append(item)
                                else:
                                    list_3.append(item)

                    ##########STOP############
                    ##########START#############
                    if list_3 is not None:
                        tmp2 = []
                        for item in list_3:
                            tmp = [x + [item[6], item[7], item[8], item[9]] for x in v if item[1] in x[3]]
                            tmp2.append(tmp)

                        # make one list
                        list_4 = []
                        for x in tmp2:
                            for item in x:
                                if item[1] in self.gene_modules:
                                    candidates_tmp.append(item)
                                else:
                                    list_4.append(item)

                    ##########STOP############

                    inside_list = []
                    for item in candidates_tmp:
                        inside_list.append(item)
                        indexes_list = item[6:]
                        for i in v:
                            if i[6] in indexes_list:
                                inside_list.append(i)
                        candidates_final.append(inside_list)
                        inside_list = []

                    # Build list of actual DevExpress version (linked to gene)
                    dev_version_linked_to_gene_tmp = []
                    for dev in analyzed_module_ends_list:
                        for candidate in candidates_final:
                            if dev in candidate:
                                dev_version_linked_to_gene_tmp.append(dev)
                    dev_version_linked_to_gene = []

                    for x in dev_version_linked_to_gene_tmp:
                        list_el = str(x[3] + ' ' + x[4])
                        dev_version_linked_to_gene.append(list_el)

                    self.final_output += "\nDevExpress versions on environment: \n\n"
                    for item in set(dev_version_linked_to_gene):
                        self.final_output += ' - ' + str(item) + '\n'
                    self.final_output += '\n'
                    if len(set(dev_version_linked_to_gene)) >= 1:
                        affected_environments.append(str(key) + '(' + str(len(set(dev_version_linked_to_gene))) + ')')

                    self.final_output += '\nGene modules indirect connections with DevExpress: \n\n'

                    for i in candidates_final:
                        # Make string
                        indexes_list = i[0][6:]
                        final_string = 'GENE_MODULE: '
                        for item in indexes_list:
                            string = [x for x in v if x[6] == item]
                            # Get gene version for second file
                            if str(string[0][1]) in self.gene_modules:
                                self.second_gene_ver = str(string[0][2])
                            final_string += str(string[0][1]) + '[ver: ' + (str(string[0][2]))+']'
                            if analyze_module not in string[0][3]:
                                final_string += ' --> '
                            elif analyze_module in string[0][3]:
                                final_string += ' --> ' + str(string[0][3]) + '[ver: ' + (str(string[0][4]))+']'
                        self.final_output += final_string + '\n'
                    self.final_output += '-'*self.line_length + '\n'
                else:
                    self.final_output += '\nENVIRONMENT: ' + str(key) + '\n\n'
                    self.final_output += '\n\nNO GENE MODULES\n\n'
                    self.final_output += '-' * self.line_length + '\n'
                # Build list of 'essentials' for second file (in order to be able to sort)
                if len(set(dev_version_linked_to_gene)) >= 1:
                    second_tmp_list = [self.second_client_name, self.second_env_name, self.second_gene_ver,
                                       set(dev_version_linked_to_gene)]
                    self.second_output_list.append(second_tmp_list)
            self.final_output += '#'*self.line_length + '\n'
            self.final_output += 'Affected environments list (and how many different versions is detected):\n'
            self.final_output += str(', '.join(affected_environments))
            self.final_output += '\n'+'#'*self.line_length

            # Build second file:
            self.second_output_list_sorted = sorted(self.second_output_list, key=lambda x: x[2])
            second_env_tmp = []
            for item in self.second_output_list_sorted:
                if item[1] not in second_env_tmp:
                    self.second_output += 'Env name: ' + item[1] + '\n'
                    second_env_tmp.append(item[1])
                    self.second_output += 'Gene ver: ' + item[2] + '\n'
                    self.second_output += 'Client: ' + item[0] + '\n'
                    self.second_output += "\nDevExpress versions on env: \n\n"
                    for dev in item[3]:
                        self.second_output += ' - ' + str(dev) + '\n'
                    self.second_output += '-' * self.line_length + '\n'

        sample_file = open(output_filename, "w")
        second_file = open(second_filename, "w")
        #print(self.final_output)
        #print(self.second_output)
        sample_file.write(self.final_output)
        second_file.write(self.second_output)
        return output_filename, second_filename












