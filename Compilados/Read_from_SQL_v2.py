#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importa librerias
import pyodbc as pyo
import pandas as pd
import os
import glob
import numpy as np
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


# In[2]:


#Conexión con la base de datos
cnxn = pyo.connect(driver='{SQL Server Native Client 11.0}',
                            server='10.94.13.112',
                            database='xSPCNagares',
                            uid='INGPROC',
                            pwd='IngProcMahle2+')


# In[3]:


cursor = cnxn.cursor()

cursor.execute("SELECT COUNT(*) FROM OBCS2_EST_CLI")
row = cursor.fetchone()
print ("Numero de filas: " + str(row[0]))


# In[4]:


#Query a la tabla del test
data = pd.read_sql("SELECT * FROM OBCS2_EST_CLI", cnxn) #Lee todos registros
#data = pd.read_sql("SELECT TOP(10000) * FROM OBCS2_EST_CLI", cnxn) #Lee los primeros 10000 registros


# In[19]:


data.head()
data.describe()


# In[39]:


#Muestra números de serie en la base de datos
data['SerialNumber'].unique()


# In[42]:


DUT = 'SN59103'
if (DUT is not None):
    data_DUT=data[(data['SerialNumber'] == DUT)]
    data_plot = data_DUT[['Date'] + ['Value'] + ['Measure']].copy()
else: 
    data_DUT = {}
    data_plot = {}


# In[46]:


pivoted_data = data_plot.pivot(index="Date", columns = "Measure", values = "Value").reset_index()
pivoted_data.columns.name=None


# In[47]:


dtale.show(pivoted_data)


# In[50]:


#Lee las columnas
medidas = pivoted_data.columns
medidas


# In[51]:


#Filtra las medidas que empiezan por OBC (CAN)
medidas_OBC = list(filter(lambda x: x.startswith('OBC'), medidas)) 
medidas_OBC


# In[52]:


#Filtra las medidas que empiezan por OBC (CAN)
medidas_PFC = list(filter(lambda x: x.startswith('PFC'), medidas)) 
medidas_PFC


# In[57]:


#Inicializa directorio, nombre y resolución de las gráficas
test = "Prueba Base de datos"
directory = r'C:\Users\m0081459\Documents\Jupyter\Results\Pruebas MS SQL Server'
os.chdir(directory)
dirName = directory + '\Combined csvs'
dirPlot = directory + '\Plots'
simplification_rate = 1;

try:
    os.mkdir(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
    
try:
    os.mkdir(dirPlot)
    print("Directory " , dirPlot ,  " Created ") 
except FileExistsError:
    print("Directory " , dirPlot ,  " already exists")

file_type = ".html"
os.chdir(dirPlot)
resolution = [1920, 1080]
resolution_4k = [4096, 2160] 

data['Value'] = [x.replace(',', '.') for x in data['Value']]
export_extension = 'csv'
pivoted_data.to_csv(dirName + "\\" + DUT + " - " + test + "_from_SQL" + "." +export_extension)
print("File creation completed")


# In[58]:


HV_DC_labels_V = ['OBC_OutputVoltage']
HV_DC_labels_I = ['OBC_OutputCurrent']
HVDC_labels = HV_DC_labels_V + HV_DC_labels_I


# In[60]:


#Plot HV DC measurements
file_name = test + " HV DC measurements"
file = file_name  + file_type
fig_dc = go.Figure() 
for i in HV_DC_labels_V:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_dc.add_trace(go.Scatter(y = values, x = date, name=i, yaxis = "y1", line_shape='hv'))
for i in HV_DC_labels_I:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_dc.add_trace(go.Scatter(y = values, x = date, name=i, yaxis ="y2", line_shape='hv'))
fig_dc.layout.update(
    title = file_name,
    xaxis=dict(
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),       
    yaxis=dict(
        title="Voltage[V]",
        showline = True,
        linewidth=1, 
        linecolor='black',        
        showgrid = True,
        gridcolor = 'lightgrey'
    ),
    yaxis2=dict(
        title="Current[A]",
        overlaying="y1",
        side="right",
        showline = True,
        linewidth=1, 
        linecolor='blue',        
        showgrid = True,
        gridcolor = 'lightblue'
    ),    
)
fig_dc.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig_dc.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig_dc.update_layout(spikedistance=1000, hoverdistance=100)
fig_dc.layout.hovermode = 'x'
fig_dc.layout.xaxis.tickfont.size = 8
fig_dc.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_dc.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_dc.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig_dc, filename = file_name + file_type)
fig_dc.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[62]:


#Señales a mostrar del PFC
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'Pacific_V_Ph1', 'Pacific_V_Ph2','Pacific_V_Ph3','SUP_CommandVDCLink_V']
HV_AC_labels_V = [i for i in medidas if i in HV_AC_labels_V]
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1','Pacific_I_Ph1', 'Pacific_I_Ph2', 'Pacific_I_Ph3']
HV_AC_labels_I = [i for i in medidas if i in HV_AC_labels_I]
HV_AC_labels_P = ['Pacific_P_Ph1', 'Pacific_P_Ph2', 'Pacific_P_Ph3']
HV_AC_labels_P = [i for i in medidas if i in HV_AC_labels_P]


# In[64]:


#Plot HV AC measurements
file_name = test + " HV AC measurements"
file = file_name  + file_type
fig_ac = go.Figure() 
data_medida={}
for i in HV_AC_labels_V:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_ac.add_trace(go.Scatter(y = values, x = date, name=i, yaxis = "y1", line_shape='hv'))
for i in HV_AC_labels_I:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_ac.add_trace(go.Scatter(y = values, x = date, name=i, yaxis ="y2", line_shape='hv'))
fig_ac.layout.update(
    title = file_name,
    xaxis=dict(
        title = 'Time',
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),    
    yaxis=dict(
        title="Voltage[V]",
        range=[0,700],
        showline = True,
        linewidth=1, 
        linecolor='black',        
        showgrid = True,
        gridcolor = 'lightgrey'
    ),
    yaxis2=dict(
        title="Current[A]",
        overlaying="y1",
        side="right",
        range=[0,50],
        showline = True,
        linewidth=1, 
        linecolor='blue',        
        showgrid = True,
        gridcolor = 'lightblue'
    ),    
)

fig_ac.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig_ac.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig_ac.update_layout(spikedistance=1000, hoverdistance=100)
fig_ac.layout.hovermode = 'x'
fig_ac.layout.xaxis.tickfont.size = 8

fig_ac.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_ac.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_ac.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig_ac, filename = file_name + file_type)
fig_ac.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[71]:


import matplotlib.pyplot as plt

ax = plt.gca()
pivoted_data.plot(kind='line',x='Date',y='PFC_IPH1_RMS_0A1',color='red', ax=ax)


# In[81]:


data[data.Measure == ['PFC_IPH1_RMS_0A1']].describe()


# In[ ]:




