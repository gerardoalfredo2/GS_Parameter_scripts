def GS_Audit_Ericsson3g(par_file, input_folder):
    import pandas
    import os.path
    import numpy as np
    df = pandas.read_excel(open(par_file, 'rb'), sheetname='Parameter_list')
    parameters = df.set_index('ID')
    directory_files = df['File'].tolist()
    directory_files = list(set(directory_files))

    # Load of Parameter file with parameters values
    df_filtered = parameters[(parameters['IN GS'] == 1)]
    parameters = df_filtered[['Parameter_name', 'GS_ValueATT', 'GS_OSS_val']]

    col_name = (u'Parameter_name', u'GS_ValueATT', u'GS_OSS_val', u'Total_of_elements', u'Alignments', u'Discrepances', u'Perc_Discrepances')
    parameters = parameters.reindex(columns=list(col_name), fill_value=0)
    #parameters['GS_OSS_val'] = parameters['GS_OSS_val'].astype(str)
    for tab_name in directory_files:
        if os.path.exists(input_folder + "%s.txt" % (tab_name)) == True:
            # Load File MO File
            # This loop load every file using directory_files array
            myfile = input_folder + "%s.txt" % (tab_name)
            #print myfile

            table_audit = pandas.read_csv(myfile, sep='\t', header=(0))
            parameters = parameters.reindex(columns=list(col_name), fill_value=0)

            # Load parameters to audit
            df = df[(df['IN GS'] == 1)]
            par_to_update = (df[df['File'] == tab_name])['ID'].tolist()
            #print par_to_update
            for para in par_to_update:
                print para
                par_fullname = para
                print par_fullname
                parameters_name = str(parameters.loc[par_fullname , 'Parameter_name'])
                print parameters_name
                GS_value = str(parameters.loc[par_fullname, 'GS_OSS_val'])
                # print table_audit[[parameters_name]]
                print GS_value
                print type(GS_value)
                if GS_value == '-':
                    print "Dentro de Standard: -\n Fuera de standard: -\n Porcentaje: -"
                    parameters.loc[par_fullname, 'Total_of_elements'] = '-'
                    parameters.loc[par_fullname, 'Alignments'] = '-'
                    parameters.loc[par_fullname, 'Discrepances'] = '-'
                    parameters.loc[par_fullname, 'Perc_Discrepances'] = '-'
                else:
                    temp = table_audit[parameters_name]
                    temp = temp.astype(str)
                    print type(temp)
                    dtro_std = (temp == GS_value).sum()
                    ou_std = (temp != GS_value).sum()
                    total_count = table_audit[parameters_name].count()
                    if total_count == 0:
                        print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (
                        dtro_std, ou_std, '0')
                        parameters.loc[par_fullname, 'Total_of_elements'] = total_count
                        parameters.loc[par_fullname, 'Alignments'] = dtro_std
                        parameters.loc[par_fullname, 'Discrepances'] = ou_std
                        parameters.loc[par_fullname, 'Perc_Discrepances'] = 0
                        print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (
                            dtro_std, ou_std, '0')
                    else:
                        parameters.loc[par_fullname, 'Total_of_elements'] = total_count
                        parameters.loc[par_fullname, 'Alignments'] = dtro_std
                        parameters.loc[par_fullname, 'Discrepances'] = ou_std
                        parameters.loc[par_fullname, 'Perc_Discrepances'] = 100 * (float(dtro_std) / float(total_count))
                        print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (
                        dtro_std, ou_std,100*( float(dtro_std) / float(total_count)))
    print parameters
    writer = pandas.ExcelWriter(input_folder+'output.xlsx')
    parameters.to_excel(writer, 'Parameter_audit')
    writer.save()





GS_Audit_Ericsson3g(
    'C:\Users\VervebaMX2\Documents\Projects\Python Scripts\CM&PM Parsers\GS Parameters Audit\CrossCheck3G_ericsson_v2.xlsx',
    'C:\\Users\\VervebaMX2\\Documents\\Projects\\XML_Parsing\\TEst\\Test_allEricssonXML3G\\Results\\')
