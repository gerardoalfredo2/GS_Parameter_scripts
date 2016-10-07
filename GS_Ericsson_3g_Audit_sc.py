def GS_Audit_Ericsson3g(par_file, input_folder):
    import pandas
    import os.path
    import numpy as np
    df = pandas.read_excel(open(par_file, 'rb'), sheetname='Parameter_list')
    parameters = df.set_index('ID')
    directory_files = df['File'].tolist()
    directory_files = list(set(directory_files))
    col = ['RNC_name','Id','Id_2','Actual_Value','Correct_Value','Parameter_name']
    par_celdas = pandas.DataFrame( columns=col)
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
            #Create a pandas dataframe with the value of the parameters
            '''
            for para in par_to_update:
                #print para
                par_fullname = para
                #print par_fullname
                parameters_name = str(parameters.loc[par_fullname , 'Parameter_name'])
                #print parameters_name
                GS_value = str(parameters.loc[par_fullname, 'GS_OSS_val'])
                GS_value=str.split(GS_value)

                #print type(GS_value)
                if str(GS_value[0]) == '-':
                    #print "Dentro de Standard: -\n Fuera de standard: -\n Porcentaje: -"
                    parameters.loc[par_fullname, 'Total_of_elements'] = '-'
                    parameters.loc[par_fullname, 'Alignments'] = '-'
                    parameters.loc[par_fullname, 'Discrepances'] = '-'
                    parameters.loc[par_fullname, 'Perc_Discrepances'] = '-'
                else:
                    values_compare = pandas.Series(GS_value)
                    temp = table_audit[parameters_name]
                    temp = temp.astype(str)
                    #print 'temp: ', type(temp)
                    exits = pandas.Series(temp.isin(values_compare))
                    #print exits
                    counts = exits.value_counts()
                    #print counts

                    dtro_std =dict(counts).get(True)
                    if dtro_std==None:
                        dtro_std=0
                    ou_std = dict(counts).get(False)
                    if ou_std==None:
                        ou_std=0
                    total_count = table_audit[parameters_name].count()
                    if total_count == 0:
                        #print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (dtro_std, ou_std, '0')
                        parameters.loc[par_fullname, 'Total_of_elements'] = total_count
                        parameters.loc[par_fullname, 'Alignments'] = dtro_std
                        parameters.loc[par_fullname, 'Discrepances'] = ou_std
                        parameters.loc[par_fullname, 'Perc_Discrepances'] = 0
                        #print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (dtro_std, ou_std, '0')
                    else:
                        parameters.loc[par_fullname, 'Total_of_elements'] = total_count
                        parameters.loc[par_fullname, 'Alignments'] = dtro_std
                        parameters.loc[par_fullname, 'Discrepances'] = ou_std
                        parameters.loc[par_fullname, 'Perc_Discrepances'] = 100 * (float(dtro_std) / float(total_count))
                        #print "Dentro de Standard: %s\n Fuera de standard: %s\n Porcentaje: %s" % (dtro_std, ou_std,100*( float(dtro_std) / float(total_count)))
            '''
            for para in par_to_update:
                #print para
                par_fullname = para
                print '\npa_fullname: ', par_fullname
                parameters_name = str(parameters.loc[par_fullname, 'Parameter_name'])
                print 'parameter_name: ',parameters_name
                GS_value = str(parameters.loc[par_fullname, 'GS_OSS_val'])
                GS_value = str.split(GS_value)
                print GS_value
                if str(GS_value[0]) == '-':
                    pass

                else:
                    #print par_celdas

                    values_compare = pandas.Series(GS_value)
                    print 'Values to Compare',values_compare
                    list_par=table_audit[parameters_name]
                    temp=table_audit[table_audit.columns[0:4]]
                    temp.columns = ['Date', 'RNC_name', 'Id','Id_2']
                    temp['Actual_Value'] = list_par.values
                    temp = temp.astype(str)
                    print 'temp: ', type(temp)
                    #print temp

                    complains = temp[temp['Actual_Value'].isin(values_compare) == False]

                    complains['Correct_Value'] = ','.join(GS_value)


                    complains['Parameter_name'] = par_fullname
                    print complains
                    par_celdas = [par_celdas, complains]
                    par_celdas = pandas.concat(par_celdas)
                ''''''


    print par_celdas
    #print parameters
    writer = pandas.ExcelWriter(input_folder+'CM_Parameter_Audit.xlsx')
    parameters.to_excel(writer, 'Parameter_audit')
    par_celdas.to_excel(writer,'Parameter_Audit_Cell', index=False)
    writer.save()





GS_Audit_Ericsson3g(
    'C:\Users\VervebaMX2\Documents\Projects\Python Scripts\CM&PM Parsers\GS Parameters Audit\CrossCheck3G_ericsson_v2.xlsx',
    'C:\\Users\\VervebaMX2\\Documents\\Projects\\XML_Parsing\\TEst\\Test_allEricssonXML3G\\Results\\')
