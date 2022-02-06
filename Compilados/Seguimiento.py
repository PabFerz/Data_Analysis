#!/usr/bin/env python
# coding: utf-8

# In[112]:


import os
import glob
import time
import math
import numpy as np
import pandas as pd
import scipy as sp
import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots
import cufflinks as cf
#import orca
import dtale
get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()


# In[113]:


#Clases
#Temporizador
class Timer:

    def __init__(self):
        self.start = time.time()

    def start(self):
        self.start = time.time()

    def log(self):
        logger = time.time() - self.start
        print('Tiempo de procesamiento: ',logger, "s")

    def milestone(self):
        self.start = time.time()


# In[114]:


def save_xls(list_dfs, xls_path, sheets_names):
    with ExcelWriter(xls_path) as writer:
        for n, df in enumerate(list_dfs):
            df.to_excel(writer, sheets_names[n])
        writer.save()


# In[142]:


os.getcwd()


# In[146]:


#A editar según lo que se quiera mostrar

#Ruta donde grabar los archivos. Edita con la de tu pc!
directory = os.getcwd()

timer = Timer()
os.chdir(directory)
dirName = directory + '\\Tableau import'

try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
    
import_extension = 'xlsx'
import_file = [i for i in sorted(glob.glob('*.{}'.format(import_extension)), key=os.path.getmtime)]
print("Archivos cargados:", *import_file ,sep = '\n\t')

#combined_csv = pd.concat([pd.read_csv(f, sep = ';', decimal = ',', usecols = usecols, low_memory = False) for f in all_filenames])
try:
    df = pd.read_excel(import_file[-1])
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
except FileExistsError:
    print("Error al cargar el archivo.")
timer.log()


# In[116]:


df = df.dropna(axis=0, subset=['Serial Number'])
#df = df.dropna(axis=1, how='all')


# In[117]:


#Columnas a mantener
if("Sample Remarks" not in df.columns):
    df = df.rename(columns = {"Remarks": "Sample Remarks"})
Dut_labels = ["DUT count","Serial Number","Product","Type","Delivery date","Manufacturing Date Cooler","Manufacturing Date OBC","Cooler Number","SW version","SW label","HW Maturity","HW label","Reworks","Issue","Root Cause","Affected PCB","Affected component","Internal/External","Validation phase","Leg","Leg Completion/DUT","Current Location","Current owner","Sample Status","Internal/\nExternal","Polarion link","Result External","Result Internal","Sample Remarks"]
Dut_labels = [i for i in df.columns if i in Dut_labels]
Test_labels = [i for i in df.columns if i not in Dut_labels]
df_DUTs = df[Dut_labels].copy()
df_Tests = df[Test_labels].copy()


# In[118]:


#Pivot tabla
timer =Timer()
df_melt = pd.melt(df, id_vars=Dut_labels, var_name="Test", value_name="Value", ignore_index = False)
#pivoted_data.columns.name=None
df_melt = df_melt.sort_values(["DUT count", "Test"], ascending = [True, True])
df_melt.reset_index(drop=True, inplace=True)
timer.log()


# In[131]:


test_info_labels = ["Status", "Progress", "Target", "Completion", "Start Date", "Scheduled Start Date", "Scheduled End Date", "End Date", "Remarks"]
tests_details = [x for x in Test_labels if any(i in x for i in test_info_labels)]
test_list = [x for x in Test_labels if x not in tests_details]
#Simplicar tabla
Serial_Numbers = df_melt["Serial Number"].unique()


# In[132]:


timer = Timer()
df_simplificada = df_melt.copy()
lista_filas = []
#fila_to_remove = []
for i in Serial_Numbers:
    for x in test_list:
        #print("Pieza " + i + "- Test " + x)
        test_info = [x + " " + j for j in test_info_labels]
        if x not in test_info: test_info.insert(0,x)
        value = df_melt["Value"][(df_melt["Test"] == x) & (df_melt["Serial Number"] == i)]
        #print(value)
        if value.values[0] == "x":
                #fila = df_melt[(df_simplificada["Test"] == x) & (df_melt["Serial Number"] == i)]
                lista_filas = lista_filas + [value.index[0] + x for x in list(range(len(test_info_labels)))]
                """
                for k in test_info: 
                    fila = df_melt[(df_simplificada["Test"] == k) & (df_melt["Serial Number"] == i)]
                    if not fila.empty:
                        lista_filas = lista_filas + [x for x in list(range(len(test_info_labels)))]
                        #fila_to_remove = fila_to_remove + [fila.index[0]]
                        #print("\tBorrando " + k + " Valor de fila: " + str(fila.index[0]))                                            
                        #df_simplificada.drop(fila.index[0] + [x for x in list(range(len(test_info_labels)))], inplace = True)
            """
#df_melt = df_melt.reset_index(drop=True)
timer.log()


# In[133]:


df_simplificada = df_melt.iloc[lista_filas] 
df_simplificada[["Test", "Test Details"]] = df_simplificada.Test.str.split(" - ", expand=True)
df_simplificada = df_simplificada.sort_values(["DUT count", "Test"], ascending = [True, True])
df_simplificada = df_simplificada[df_simplificada["Test Details"].notna()]
df_simplificada.reset_index(drop=True,inplace = True)
#dtale.show(df_simplificada)


# In[134]:


df_export = df_simplificada.copy()
df_export = pd.concat([df_export, pd.DataFrame(columns = test_info_labels)])


# In[136]:


index_test = df_export.index[df_export['Value']==1].tolist()
for i in index_test:
    value_col = df_export.iloc[i,df_export.columns.get_loc("Test Details")]
    write_col = df_export.columns.get_loc(value_col)
    dut = df_export["Serial Number"].iloc[i]
    test_info_included = df_export["Test Details"][(df_export["Serial Number"]==dut) &(df_export["Test"]==i)].unique()
    #print(write_col)
    for j in range(len(test_info_included)):
        df_export.iloc[i, write_col] = df_export.iloc[i+j,  df_export.columns.get_loc("Value")]
        #print(j)
    #print(write_col)


# In[137]:


df_final = pd.DataFrame(columns = df_export.columns)
for x in df_export["Serial Number"].unique():
    for y in df_export["Test"].unique():            
        df_prueba = df_export[(df_export["Serial Number"]==x) &(df_export["Test"]==y)]
        test_info_included = df_prueba["Test Details"].unique()
        for i in range(len(test_info_included)):
            for j in range(len(test_info_included)):
                if test_info_included[i] == df_prueba.iloc[j, df_prueba.columns.get_loc("Test Details")]:
                    df_prueba.iloc[0, df_prueba.columns.get_loc(test_info_included[j])] =  df_prueba.iloc[j, df_prueba.columns.get_loc("Value")]
                    #print(test_info_included[i] + ": " + df_prueba.iloc[j, df_prueba.columns.get_loc("Test Details")] + " = " + str(df_prueba.iloc[j, df_prueba.columns.get_loc("Value")]))
        df_final = pd.concat([df_final, df_prueba])
        df_final = df_final.dropna(subset=test_info_labels, how='all')
        df_final.reset_index(drop = True, inplace = True)
#df_final.head()


# In[141]:


timer =Timer()
from pandas import ExcelWriter
export_extension = 'xlsx'
sheets = ["Tests", "DUTs"]
directorio_excel = dirName + "\\" + "Seguimiento de Piezas" + "." +export_extension
"""
writer = pd.ExcelWriter('directorio_excel', engine='xlsxwriter')
df_export.to_excel(directorio_excel, sheet_name = "Tests")
df_DUTs.to_excel(directorio_excel, sheet_name = "DUTs")
writer.save()
"""
save_xls([df_final, df_DUTs], directorio_excel, sheets)
print("File creation completed. Directory: " + directorio_excel)
timer.log()


# In[ ]:


get_ipython().system('jupyter nbconvert --to python *.ipynb')


# In[ ]:




