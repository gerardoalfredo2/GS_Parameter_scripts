# -*- coding: utf-8 -*-
"""
Created on Tue Aug 02 14:46:03 2016

@author: Gerardo Alfredo Alarcon Rivas
"""
'''This function saves take a string and save this in a new line of the input file'''
import sys
import timeit
import os.path 
import pandas as pd

def get_files(directory,exte):
 files_name=[]
 import glob
 print directory+exte
 files_name= glob.glob(directory+exte)
 return files_name #returns a list with the file names
 
def logger(cadena, file_):
         f = open(file_, 'a')
         f.write(cadena+"\n") # python will convert \n to os.linesep
         f.close()

'''The parser take on xml file and create a tree form this
the code write and output file in a tabular format with all the elements of the
initial file. THe code can parse the exported xml files from Huawei PM counters
from all the levels'''
def parameter_compacter(Input_folder, OutPut_file):
    files=[]
    files=list(get_files(Input_folder,"*.txt"))
    cols=['Date','File','Parameter_name']
    Output_file = pd.DataFrame(columns=cols)
    #print Output_file
    for file_ in files:
         #print file_
         try:
             df = pd.read_csv(file_,sep='\t',header=(0))
             table_name= str(list(file_.split("\\"))[-1]).replace(".txt","")
             date=str(df.iloc[0]['Date'])
             #print date,table_name
             params=list(df.columns)
             for key in params:
                 not_needed=["Date",'RNC_name',"RNCName","RNC_Name","id","Id","Id_2","vsDataType","vsDataFormatVersion"]
                 if (key not in not_needed) and (key.count("}")==0):
                     inputs=pd.DataFrame([[date,table_name,key]],columns=cols)
                # print inputs
                     Output_file=pd.concat([Output_file,inputs])
              
         except (ValueError, SyntaxError):
            print "The file %s has a wrong data structure...\n\n\n\n"%file_
            #pass
    print Output_file
    if os.path.exists(OutPut_file+'Parameter_list.txt')==False:
        Output_file.to_csv(OutPut_file+'Parameter_list.txt',sep='\t', index=False)    
    else:
        os.remove(OutPut_file+'Parameter_list.txt')
        Output_file.to_csv(OutPut_file+'Parameter_list.txt',sep='\t', index=False)
     #   cols=list(df.columns)
        
    return 0 


parameter_compacter('C:\\Users\\VervebaMX2\\Documents\\Projects\\XML_Parsing\\TEst\\Test_allEricssonXML3G\\Results\\','C:\\Users\\VervebaMX2\\Documents\\Projects\\XML_Parsing\\TEst\\Test_allEricssonXML3G\\')

  
   


