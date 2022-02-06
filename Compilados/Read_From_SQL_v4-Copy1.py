#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importa librerias
import time
import timer
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


# In[3]:


#Conexión con la base de datos
cnxn = pyo.connect(driver='{SQL Server Native Client 11.0}',
                            server='10.94.13.112',
                            database='xSPCNagares',
                            uid='INGPROC',
                            pwd='IngProcMahle2+')


# In[4]:


#Muestra número de filas en la base de datos
cursor = cnxn.cursor()
cursor.execute("SELECT COUNT(*) FROM OBCS2_EST_CLI")
row = cursor.fetchone()
print ("Numero de filas: " + str(row[0]))


# In[5]:


#Numeros de series de las piezas en la base de datos
timer = Timer()
cursor.execute("SELECT DISTINCT SerialNumber FROM OBCS2_EST_CLI")
print("Lista de números de serie:")
i=1
for row in cursor:
    print ("\t"+str(i)+" - " + row[0])
    i+=1
timer.log()


# In[6]:


#Test incluidos en la base de datos
timer = Timer()
cursor.execute("SELECT DISTINCT Test FROM OBCS2_EST_CLI")
print("Lista de tests:")
i=1
for row in cursor:
    print ("\t"+str(i)+" - " + row[0])
    i+=1
timer.log()    


# In[7]:


#Meddias diferentes
timer = Timer()
cursor.execute("SELECT DISTINCT Measure FROM OBCS2_EST_CLI")
print("Lista de tests:")
i=1
for row in cursor:
    print ("\t"+str(i)+" - " + row[0])
    i+=1
timer.log()    


# In[8]:


#A editar según lo que se quiera mostrar

#Ruta donde grabar los archivos. Edita con la de tu pc!
directory = r'C:\Users\m0081459\Documents\Jupyter\Results\Pruebas MS SQL Server'

#Señales
temperature_labels = ['DCDC_Temperature','PFC_Temp_M1_C', 'PFC_Temp_M4_C', 'Climatic chamber temperature', 'Chiller temperature','Chiller temperature1']
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'Pacific_V_Ph1', 'Pacific_V_Ph2','Pacific_V_Ph3']
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1','Pacific_I_Ph1', 'Pacific_I_Ph2', 'Pacific_I_Ph3']
HV_AC_labels_P = ['Pacific_P_Ph1', 'Pacific_P_Ph2', 'Pacific_P_Ph3']
HV_DC_labels_V = ['DCHV_ADC_VOUT', 'BMS_HighestChargeVoltageAllow', 'E.L. High Voltage (V)']
HV_DC_labels_I = ['DCHV_ADC_IOUT', 'BMS_HighestChargeCurrentAllow', 'E.L. High Voltage (A)']
HV_DC_labels_P = ['Regatron_P']
LV_DC_labels_V = ['DCLV_Measured_Voltage', 'E.L. Low Voltage (V)']
LV_DC_labels_I = ['DCLV_Measured_Current', 'E.L. Low Voltage (A)']
#status_labels = ['PFC_PFCStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault', 'OBC_PowerMax', 'Actual_Cycle']
status_labels = ['BMS_OnBoardChargerEnable']
signal_list = temperature_labels+HV_AC_labels_V+HV_AC_labels_I+HV_AC_labels_P+HV_DC_labels_V+HV_DC_labels_I+HV_DC_labels_P+LV_DC_labels_V+LV_DC_labels_I+status_labels
placeholder= '?'
placeholders= ', '.join(placeholder for unused in signal_list)

#Fase validation
val_phase = "Pre-DV"

#Columnas
columnas = ["Date", "SerialNumber", "Test", "Measure", "Value"]

#Test
ensayo = 'prueba11_CL10'

#Serial number
sn = 'SN95271'

#Titulo
test = val_phase + " " + sn + " - Prueba Base de datos"

#Queries
Query_w_señales = "SELECT {0} FROM [xSPCNagares].[dbo].[OBCS2_EST_CLI] WHERE Test= '{1}' and SerialNumber = '{2}' and Measure IN ".format(', '.join(columnas),ensayo,sn)
Query_w_señales = Query_w_señales + "(%s)" % placeholders

timer = Timer()
data = pd.read_sql(Query_w_señales, cnxn, params=signal_list, columns=columnas)
timer.log()


# In[ ]:


#CUIDADO! Esta query carga toda la tabla

#Query a la tabla del test
timer = Timer()
data_all = pd.read_sql("SELECT * FROM OBCS2_EST_CLI", cnxn) #Lee todos registros
#data = pd.read_sql("SELECT TOP(10000) * FROM OBCS2_EST_CLI", cnxn) #Lee los primeros 10000 registros
timer.log()


# In[10]:


#Primeras lineas de datos importados
data.head()


# In[9]:


#Resumen de los datos importados
data.describe()


# In[10]:


#Muestra números de serie en la tabla importada
print("Lista de piezas importadas:")
for i in data['SerialNumber'].unique():
    print("\t",i)


# In[11]:


#Muestra tests en la tabla importada
print("Lista de tests importados:")
for i in data['Test'].unique():
    print("\t", i)


# In[15]:


#Filtra la pieza y ensayo con el que se quiere trabajar
data_DUT=data[(data['SerialNumber'] == sn)].copy()
data_DUT['Value'] = [x.replace(',', '.') for x in data_DUT['Value']]
data_DUT['Value']=data_DUT['Value'].astype(float)   
data_DUT = data_DUT[data_DUT['Test'] == ensayo]
data_DUT = data_DUT[['Date'] + ['Value'] + ['Measure']]


# In[16]:


#Muestra matriz resultado
dtale.show(data_DUT, ignore_duplicate=True)


# In[19]:


#Modifica la forma de la matriz para crear columnas con cada una de las medidas
timer =Timer()
pivoted_data = data_DUT.reset_index().pivot(index="Date", columns = "Measure", values = "Value")
pivoted_data.columns.name=None
timer.log()


# In[ ]:


#Muestra matriz resultado
dtale.show(pivoted_data, ignore_duplicate=True)


# In[ ]:


#Lee las columnas
medidas = pivoted_data.columns
for i in medidas:
    print(i)


# In[ ]:


#Inicializa directorio, nombre y resolución de las gráficas
os.chdir(directory)
dirName = directory + '\Combined csvs' + "\\" + val_phase+ "\\" + ensayo + "\\" + sn
dirPlot = directory + '\Plots' + "\\" + val_phase+ "\\" + ensayo + "\\" + sn
simplification_rate = 1;

try:
    os.makedirs(dirName)
    print("Directory " , dirName ,  " Created ") 
except FileExistsError:
    print("Directory " , dirName ,  " already exists")
    
try:
    os.makedirs(dirPlot)
    print("Directory " , dirPlot ,  " Created ") 
except FileExistsError:
    print("Directory " , dirPlot ,  " already exists")

export_extension = 'csv'
#pivoted_data.to_csv(dirName + "\\" + test + "_from_SQL" + "." +export_extension)
data.to_csv(dirName + "\\" + "CompletDatabase" + "_from_SQL" + "." +export_extension)
print("File creation completed")


# In[21]:


#Variables to be plot separately on each plot
temperature_labels = [i for i in pivoted_data.columns if i in temperature_labels]
HV_AC_labels_V = [i for i in pivoted_data.columns if i in HV_AC_labels_V]
HV_AC_labels_I = [i for i in pivoted_data.columns if i in HV_AC_labels_I]
HV_AC_labels_P = [i for i in pivoted_data.columns if i in HV_AC_labels_P]
HV_AC_labels = HV_AC_labels_V + HV_AC_labels_I + HV_AC_labels_P
HV_DC_labels_V = [i for i in pivoted_data.columns if i in HV_DC_labels_V]
HV_DC_labels_I = [i for i in pivoted_data.columns if i in HV_DC_labels_I]
HV_DC_labels_P = [i for i in pivoted_data.columns if i in HV_DC_labels_P]
HV_DC_labels = HV_DC_labels_V + HV_DC_labels_I + HV_DC_labels_P
LV_DC_labels_V = [i for i in pivoted_data.columns if i in LV_DC_labels_V]
LV_DC_labels_I = [i for i in pivoted_data.columns if i in LV_DC_labels_I]
LV_DC_labels = LV_DC_labels_V + LV_DC_labels_I
#status_labels = ['PFC_PFCStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault', 'OBC_PowerMax', 'Actual_Cycle']
status_labels = [i for i in pivoted_data.columns if i in status_labels]
#Data logger labels
#Datalogger 1
dl1_labels = ['DL1_CH1_Q1_1253', 'DL1_CH2_Q2_1253_PFC', 'DL1_CH3_Q3_1253_PFC', 'DL1_CH4_Q4_1253_PFC', 'DL1_CH5_Q5_1253_PFC', 'DL1_CH6_Q6_1253_PFC', 'DL1_CH7_Q7_1253_PFC' 'DL1_CH8_Q8_1253_PFC', 'DL1_CH9_TR', 'DL1_CH10_LR', 'DL1_CH11_Q1_1212_HV', 'DL1_CH12_Q2_1212_HV', 'DL1_CH13_Q3_1212_HV', 'DL1_CH14_Q4_1212_HV', 'DL1_CH15_Q5_1212_HV', 'DL1_CH16_Q6_1212_HV', 'DL1_CH17_Q7_1212_HV', 'DL1_CH18_Q8_1212_HV','DL1_CH19_D37_1213_RECTIFIER', 'DL1_CH20_D38_1213_RECTIFIER']
dl1_labels = [i for i in pivoted_data.columns if i in dl1_labels]
#Datalogger 2
dl2_labels = ['DL2_CH1_D39_1213_RECTIFIER', 'DL2_CH2_D40_1213_RECTIFIER', 'DL2_CH3_D41_1213_RECTIFIER', 'DL2_CH4_D42_1213_RECTIFIER', 'DL2_CH5_D42_1213_RECTIFIER', 'DL2_CH6_D44_1213_RECTIFIER', 'DL2_CH7_TX_PUSH_PULL_A' 'DL2_CH8_TX_PUSH_PULL_B', 'DL2_CH9_LBOOST_3', 'DL2_CH10_BACK_CONTROL', 'DL2_CH11_Q1_1258_DCDC', 'DL2_CH12_Q2_1258_DCDC', 'DL2_CH13_Q3_1258_DCDC', 'DL2_CH14_Q4_1258_DCDC', 'DL2_CH15_Q5_1258_DCDC', 'DL2_CH16_Q6_1258_DCDC', 'DL2_CH17_Q7_1258_DCDC', 'DL2_CH18_Q8_1258_DCDC','DL2_CH19_LBUCK_A', 'DL2_CH20_LBUCK_B']
dl2_labels = [i for i in pivoted_data.columns if i in dl2_labels]

#Label dictionary
Temp_labels = {
    'PFC_Temp_M1_C': "CAN: Temp NTC 1 (cooler)",
    'PFC_Temp_M4_C': "CAN: Temp NTC 4 (cooler)",
    'DCDC_Temperature': "CAN: DCDC Temp",
    'Climatic chamber temperature': "Chamber Temp",
    'Chiller temperature': "Chiller Temp"
}
HVAC_labels = {
    'PFC_VPH12_RMS_V': "CAN: Phase 1 Input Voltage",
    'PFC_VPH23_RMS_V': "CAN: Phase 2 Input Voltage",
    'PFC_VPH31_RMS_V': "CAN: Phase 3 Input Voltage",
    'PFC_IPH1_RMS_0A1': "CAN: Phase 1 Input Current",
    'PFC_IPH2_RMS_0A1': "CAN: Phase 2 Input Current",
    'PFC_IPH3_RMS_0A1': "CAN: Phase 3 Input Current",    
    'PFC_Vdclink_V': "DC Link Voltage",    
    'OBC_PowerMax': "Max P (derating)",
    'SUP_CommandVDCLink_V': 'PFC DC Link command',
    'P_in': 'Pacific: Total P'
}
HVDC_labels = {
    'DCHV_ADC_VOUT': "CAN: HV DCDC Output Voltage",
    'DCHV_ADC_IOUT': "CAN: HV DCDC Output current",
    'BMS_HighestChargeVoltageAllow': "Max Charging Voltage Allowed",
    'BMS_HighestChargeCurrentAllow': "Max Charging Current Allowed",
    'E.L. High Voltage (A)': "HV ELoad: HV Current",
    'E.L. High Voltage (V)': "HV ELoad: HV Voltage",
    'Regatron_P': "Regatron P",    
    'OBC_PowerMax': "Max P (derating)",
}

LVDC_labels = {
    'DCLV_Measured_Current': "CAN: LV DCDC output Current",
    'DCLV_Measured_Voltage': "CAN: LV DCDC output Voltage",
    'OBC_PowerMax': "CAN: Max Power (derating)",
    'E.L. Low Voltage (A)': "LV ELoad: Current",
    'E.L. Low Voltage (V)': "LV ELoad: Voltage"    
}

Status_labels = {
    'BMS_OnBoardChargerEnable': "OBC Charger Enable",
}

#Construye matrix para gráficas
data_plot = pivoted_data[['Date'] + status_labels+HV_AC_labels_V+HV_AC_labels_I+HV_AC_labels_P+HV_DC_labels_V+HV_DC_labels_I+HV_DC_labels_P+LV_DC_labels+temperature_labels+dl1_labels+dl2_labels].copy()
file_type = ".html"
os.chdir(dirPlot)
resolution = [1920, 1080]
resolution_4k = [4096, 2160] 


# In[ ]:


#Plot temperatures
print("Mostrando Temperaturas...")
timer = Timer()
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_temp = pivoted_data[temperature_labels + ['Date']].copy()
for i in Temp_labels:
    data_plot_temp.rename(columns={i: Temp_labels[i]}, inplace=True)
fig_temp = data_plot_temp.iplot(title = file_name, x = 'Date', xTitle = 'Time[h]', line_shape='hv', yTitle = "Temperature [ºC]",asFigure = True, filename = file_name)

""""
annotations = [dict(
                x=data_plot_temp['Time_shortened'][data_plot_temp[i] == data_plot_temp[i].max()].iloc[0],
                y=data_plot_temp[i].max(),
                text= i + ': ' + str(data_plot_temp[i].max()),
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-40,
                font=dict(
                            color="black",
                            size=6
                        ),
            ) for i in Temp_labels.values()]
fig_temp.update_layout(annotations = annotations)
"""""

fig_temp.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig_temp.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig_temp.update_layout(spikedistance=1000, hoverdistance=100)
fig_temp.layout.hovermode = 'x'
fig_temp.layout.margin['t'] = 60
fig_temp.layout.margin['b'] = 60
fig_temp.layout.yaxis.range = [-50, 110]
fig_temp.layout.xaxis.tickfont.size = 7
fig_temp.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_temp.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_temp.layout.legend.bgcolor='rgba(0,0,0,0)'
fig_temp.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
plotly.offline.plot(fig_temp, filename = file)
timer.log()


# In[ ]:


#Plot HV DC measurements
print("Mostrando lecturas de HV DC...")
timer = Timer()
file_name = test + " HV DC measurements"
file = file_name  + file_type
fig_dc = go.Figure() 
for i in HV_DC_labels_V:   
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_dc.add_trace(go.Scatter(y = values, x = date, name=HVDC_labels[i], yaxis = "y1", line_shape='hv'))
for i in HV_DC_labels_I:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_dc.add_trace(go.Scatter(y = values, x = date, name=HVDC_labels[i], yaxis ="y2", line_shape='hv'))
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
timer.log()


# In[ ]:


#Plot HV AC measurements
print("Mostrando lecturas de HV AC...")
timer = Timer()
file_name = test + " HV AC measurements"
file = file_name  + file_type
fig_ac = go.Figure() 
data_medida={}
for i in HV_AC_labels_V:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_ac.add_trace(go.Scatter(y = values, x = date, name=HVAC_labels[i], yaxis = "y1", line_shape='hv'))
for i in HV_AC_labels_I:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_ac.add_trace(go.Scatter(y = values, x = date, name=HVAC_labels[i], yaxis ="y2", line_shape='hv'))
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
timer.log()


# In[ ]:


#Plot LV DC measurements
print("Mostrando medidas del LV DC...")
timer = Timer()
file_name = test + " LV DC measurements"
file = file_name  + file_type
fig_lv = go.Figure() 
data_medida={}
for i in LV_DC_labels_V:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_lv.add_trace(go.Scatter(y = values, x = date, name=LVDC_labels[i], yaxis = "y1", line_shape='hv'))
for i in LV_DC_labels_I:
    values = pivoted_data[i]
    date = pivoted_data['Date']
    fig_lv.add_trace(go.Scatter(y = values, x = date, name=LVDC_labels[i], yaxis ="y2", line_shape='hv'))
fig_lv.layout.update(
    title = file_name,
    xaxis=dict(
        title = 'Time',
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),    
    yaxis=dict(
        title="Voltage[V]",
        range=[0,20],
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
        range=[0,150],
        showline = True,
        linewidth=1, 
        linecolor='blue',        
        showgrid = True,
        gridcolor = 'lightblue'
    ),    
)

fig_lv.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig_lv.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig_lv.update_layout(spikedistance=1000, hoverdistance=100)
fig_lv.layout.hovermode = 'x'
fig_lv.layout.xaxis.tickfont.size = 8

fig_lv.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_lv.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_lv.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig_lv, filename = file_name + file_type)
fig_lv.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
timer.log()


# In[ ]:


#Create figure with subplots
print("Mostrando medidas generales...")
timer = Timer()
fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC'))

#Combine plots
for i in range(len(temperature_labels)):
    fig.append_trace(fig_temp.data[i], 1, 1)
for i in range(len(HV_AC_labels_V + HV_AC_labels_I)):
    fig.append_trace(fig_ac.data[i], 2, 1)
for i in range(len(HV_DC_labels_V + HV_DC_labels_I)):
    fig.append_trace(fig_dc.data[i], 3, 1)

#Edit format
fig.layout.hovermode = 'x'
plot_name = "Temp, HVAC and HVDC measurements"
file_name = test + plot_name
fig.layout.title.text = test
#fig.layout.xaxis.title = "Time[h]"
fig.layout.yaxis.range = [-45, 115]
fig.layout.yaxis3.range = [0, 500]
fig.layout.xaxis1.tickfont.size = 4
fig.layout.xaxis2.tickfont.size = 4
fig.layout.xaxis3.tickfont.size = 4
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.layout.yaxis.title = "Temperature (ºC)"
fig.layout.yaxis2.title = "Current/Voltage"
fig.layout.yaxis3.title = "Current/Voltage"


#Show plot
file = test + "- Temp, AC and DC measurements"
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
timer.log()


# In[ ]:




