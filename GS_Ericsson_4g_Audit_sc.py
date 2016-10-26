def GS_Audit_Ericsson4g(par_file, input_folder):
    import pandas
    import os.path
    import datetime
    import numpy as np
    capitalizer = lambda x: x.upper()
    df = pandas.read_excel(open(par_file, 'rb'), sheetname='Parameter_list')
    parameters = df.set_index('ID')
    cellsites = pandas.read_excel(open(par_file, 'rb'), sheetname='4gCells')

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

            for para in par_to_update:
                #print para
                par_fullname = para
                #print par_fullname
                parameters_name = str(parameters.loc[par_fullname , 'Parameter_name'])
                #print parameters_name
                GS_value = str(parameters.loc[par_fullname, 'GS_OSS_val'])
                GS_value=str.split(GS_value,',')

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

            for para in par_to_update:
                #print para
                par_fullname = para
                #print '\npa_fullname: ', par_fullname
                parameters_name = str(parameters.loc[par_fullname, 'Parameter_name'])
                #print 'parameter_name: ',parameters_name
                GS_value = str(parameters.loc[par_fullname, 'GS_OSS_val'])
                GS_value = str.split(GS_value , ',')
                GS_value = [str(x) for x in GS_value]
                #GS_value = [x.upper() for x in GS_value]

                #print GS_value
                if str(GS_value[0]) == '-':
                    pass

                else:
                    #print par_celdas

                    values_compare = pandas.Series(GS_value)
                    #print 'Values to Compare',values_compare
                    list_par=table_audit[parameters_name]
                    temp=table_audit[table_audit.columns[0:4]]
                    temp.columns = ['Date', 'RNC_name', 'Id','Id_2']
                    temp['Actual_Value'] = list_par
                    temp = temp.astype(str)
                    #par_celdas['Actual_Value'] = map(lambda x: x.upper(), par_celdas['Actual_Value'])
                    #print 'temp: ', type(temp)
                    #print temp


                    complains = temp[temp['Actual_Value'].isin(values_compare) == False]

                    complains['Correct_Value'] = str(','.join(GS_value))
                    complains['Parameter_name'] = str(par_fullname)

                    names_op = ['IUSA', 'NEXTEL', 'ATT']
                    for ind in complains.index:

                        print str(ind)
                        # print str(par_celdas.loc[ind, 'Id'])
                        if str(complains.loc[ind, 'Id']) == str(complains.loc[ind, 'RNC_name']):
                            complains.loc[ind, 'Cell_name'] = ''
                        elif str(complains.loc[ind, 'Id']) == str(complains.loc[ind, 'Id_2']):
                            complains.loc[ind, 'Cell_name'] = complains.loc[ind, 'Id']

                        elif '-' in str(complains.loc[ind,'Id']):
                            print 'neighbor',complains.loc[ind,'Id']
                            variab= str(list(str(complains.loc[ind,'Id']).split('-'))[0])
                            complains.loc[ind,'Cell_name'] = variab
                        elif '_' in list(complains.loc[ind, 'Id']):
                            complains.loc[ind, 'Cell_name'] = str(complains.loc[ind, 'Id_2'])
                        elif str(complains.loc[ind, 'Id']) == '1':
                            complains.loc[ind, 'Cell_name'] = str(complains.loc[ind, 'Id_2'])
                        else:
                            complains.loc[ind, 'Cell_name'] = str(complains.loc[ind, 'Id'])
                        print 'index: ', ind
                        print str(complains.loc[ind, 'Cell_name'])

                    #print complains
                    par_celdas = [par_celdas, complains]
                    par_celdas = pandas.concat(par_celdas)
    #temporal


    #print par_celdas
    #print parameters


    print 'Starting slowthing'
    print "Total of elements are ",len(par_celdas.index)
    par_celdas.rename(columns={'Cell_name': 'Sitio'}, inplace=True)

    print cellsites
    print par_celdas
    par_celdas= par_celdas[['Date', 'RNC_name', 'Sitio', 'Id','Id_2','Parameter_name','Actual_Value','Correct_Value']]
    par_celdas = par_celdas.merge(cellsites, on='Sitio', how='inner')
    #par_celdas = pandas.merge(par_celdas, cellsites, on='Cell_name')
    #par_celdas = pandas.concat([par_celdas, cellsites], axis=1, join='outer')




    #par_celdas['Actual_Value']=par_celdas['Actual_Value'].str.capitalize()
    par_celdas['Actual_Value']=map(lambda x: x.upper(), par_celdas['Actual_Value'])
    #par_celdas['Correct_Value'] = par_celdas['Correct_Value'].str.capitalize()
    par_celdas['Correct_Value']=map(lambda x: x.upper(), par_celdas['Correct_Value'])
    par_celdas=par_celdas.query('Actual_Value != Correct_Value')


    writer = pandas.ExcelWriter(input_folder+'CM_Parameter_Audits.xlsx')
    parameters.to_excel(writer, 'Parameter_audit', index=False)
    par_celdas.to_excel(writer,'Parameter_Audit_Cell', index=False)
    try:
        writer.save()
    except:
        print ' The file exceed the number of rows of excel file, the data will be saved in %sCM_Parameter_Audits_Parameter_Audit_Cells.txt' %(input_folder)
        filenam = input_folder + 'CM_Parameter_Audits_summary.txt'
        parameters.to_csv(filenam, header=True, index=False,low_memory=False,chunksize=100)
        par_celdas.to_csv(input_folder+'CM_Parameter_Audit_Cells.txt', header=True, index=False,low_memory=False,chunksize=100)
    print "Process Finished"








GS_Audit_Ericsson4g(
   'C:\Users\VervebaMX2\Documents\Projects\Python Scripts\CM&PM Parsers\GS Parameters Audit\CrossCheckLTE_ericsson_v2.xlsx',
   'C:\\Users\\VervebaMX2\\Documents\\Projects\\XML_Parsing\\TEst\\Test_allEricssonXMLLTE\\Results\\')

