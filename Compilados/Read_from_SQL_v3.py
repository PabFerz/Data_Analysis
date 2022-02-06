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


# In[112]:


cursor = cnxn.cursor()

cursor.execute("SELECT COUNT(*) FROM OBCS2_EST_CLI")
row = cursor.fetchone()
print ("Numero de filas: " + str(row[0]))


# In[ ]:


#Query a la tabla del test
data = pd.read_sql("SELECT * FROM OBCS2_EST_CLI", cnxn) #Lee todos registros
#data = pd.read_sql("SELECT TOP(10000) * FROM OBCS2_EST_CLI", cnxn) #Lee los primeros 10000 registros


# In[ ]:


data.head()
data.describe()


# In[ ]:


#Muestra números de serie en la base de datos
data['SerialNumber'].unique()


# In[ ]:


#Muestra tests en la base de datos
data['Test'].unique()


# In[ ]:


#Filtra la pieza y ensayo con el que se quiere trabajar
DUT = 'SN59103'
Ensayo = 'Prueba2_CL08_pro'

data_DUT=data[(data['SerialNumber'] == DUT)].copy()
data_DUT['Value'] = [x.replace(',', '.') for x in data_DUT['Value']]
data_DUT['Value']=data_DUT['Value'].astype(float)   
data_DUT = data_DUT[data_DUT['Test'] == Ensayo]
data_DUT = data_DUT[['Date'] + ['Value'] + ['Measure']]


# In[ ]:


#Modifica la forma de la matriz para crear columnas con cada una de las medidas
pivoted_data = data_DUT.pivot(index="Date", columns = "Measure", values = "Value").reset_index()
pivoted_data.columns.name=None


# In[ ]:


#Muestra matriz resultado
dtale.show(pivoted_data, ignore_duplicate=True)


# In[ ]:


#Lee las columnas
medidas = pivoted_data.columns
medidas


# In[ ]:


#Filtra las medidas que empiezan por OBC (CAN)
medidas_OBC = list(filter(lambda x: x.startswith('OBC'), medidas)) 
medidas_OBC


# In[ ]:


#Filtra las medidas que empiezan por OBC (CAN)
medidas_PFC = list(filter(lambda x: x.startswith('PFC'), medidas)) 
medidas_PFC


# In[ ]:


#Inicializa directorio, nombre y resolución de las gráficas
test = DUT + " - Prueba Base de datos"
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

export_extension = 'csv'
pivoted_data.to_csv(dirName + "\\" + test + "_from_SQL" + "." +export_extension)
print("File creation completed")


# In[ ]:


#Variables to be plot separately on each plot
temperature_labels = ['DCDC_Temperature','PFC_Temp_M1_C', 'PFC_Temp_M4_C', 'C_chamber_T_actl']
temperature_labels = [i for i in data.columns if i in temperature_labels]
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'Pacific_V_Ph1', 'Pacific_V_Ph2','Pacific_V_Ph3']
HV_AC_labels_V = [i for i in data.columns if i in HV_AC_labels_V]
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1','Pacific_I_Ph1', 'Pacific_I_Ph2', 'Pacific_I_Ph3']
HV_AC_labels_I = [i for i in data.columns if i in HV_AC_labels_I]
HV_AC_labels_P = ['Pacific_P_Ph1', 'Pacific_P_Ph2', 'Pacific_P_Ph3']
HV_AC_labels_P = [i for i in data.columns if i in HV_AC_labels_P]
HV_AC_labels = HV_AC_labels_V + HV_AC_labels_I + HV_AC_labels_P
HV_DC_labels_V = ['DCHV_ADC_VOUT', 'BMS_HighestChargeVoltageAllow']
HV_DC_labels_V = [i for i in data.columns if i in HV_DC_labels_V]
HV_DC_labels_I = ['DCHV_ADC_IOUT', 'BMS_HighestChargeCurrentAllow']
HV_DC_labels_I = [i for i in data.columns if i in HV_DC_labels_I]
HV_DC_labels_P = ['Regatron_P']
HV_DC_labels_P = [i for i in data.columns if i in HV_DC_labels_P]
HV_DC_labels = HV_DC_labels_V + HV_DC_labels_I + HV_DC_labels_P
LV_DC_labels_V = ['DCLV_Measured_Voltage']
LV_DC_labels_V = [i for i in data.columns if i in LV_DC_labels_V]
LV_DC_labels_I = ['DCLV_Measured_Current']
LV_DC_labels_I = [i for i in data.columns if i in LV_DC_labels_I]
LV_DC_labels = LV_DC_labels_V + LV_DC_labels_I
#status_labels = ['PFC_PFCStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault', 'OBC_PowerMax', 'Actual_Cycle']
status_labels = ['BMS_OnBoardChargerEnable']
status_labels = [i for i in data.columns if i in status_labels]
#Data logger labels
#Datalogger 1
dl1_labels = ['DL1_CH1_Q1_1253', 'DL1_CH2_Q2_1253_PFC', 'DL1_CH3_Q3_1253_PFC', 'DL1_CH4_Q4_1253_PFC', 'DL1_CH5_Q5_1253_PFC', 'DL1_CH6_Q6_1253_PFC', 'DL1_CH7_Q7_1253_PFC' 'DL1_CH8_Q8_1253_PFC', 'DL1_CH9_TR', 'DL1_CH10_LR', 'DL1_CH11_Q1_1212_HV', 'DL1_CH12_Q2_1212_HV', 'DL1_CH13_Q3_1212_HV', 'DL1_CH14_Q4_1212_HV', 'DL1_CH15_Q5_1212_HV', 'DL1_CH16_Q6_1212_HV', 'DL1_CH17_Q7_1212_HV', 'DL1_CH18_Q8_1212_HV','DL1_CH19_D37_1213_RECTIFIER', 'DL1_CH20_D38_1213_RECTIFIER']
dl1_labels = [i for i in data.columns if i in dl1_labels]
#Datalogger 2
dl2_labels = ['DL2_CH1_D39_1213_RECTIFIER', 'DL2_CH2_D40_1213_RECTIFIER', 'DL2_CH3_D41_1213_RECTIFIER', 'DL2_CH4_D42_1213_RECTIFIER', 'DL2_CH5_D42_1213_RECTIFIER', 'DL2_CH6_D44_1213_RECTIFIER', 'DL2_CH7_TX_PUSH_PULL_A' 'DL2_CH8_TX_PUSH_PULL_B', 'DL2_CH9_LBOOST_3', 'DL2_CH10_BACK_CONTROL', 'DL2_CH11_Q1_1258_DCDC', 'DL2_CH12_Q2_1258_DCDC', 'DL2_CH13_Q3_1258_DCDC', 'DL2_CH14_Q4_1258_DCDC', 'DL2_CH15_Q5_1258_DCDC', 'DL2_CH16_Q6_1258_DCDC', 'DL2_CH17_Q7_1258_DCDC', 'DL2_CH18_Q8_1258_DCDC','DL2_CH19_LBUCK_A', 'DL2_CH20_LBUCK_B']
dl2_labels = [i for i in data.columns if i in dl2_labels]

#Label dictionary
Temp_labels = {
    'PFC_Temp_M1_C': "CAN: Temp NTC 1 (cooler)",
    'PFC_Temp_M4_C': "CAN: Temp NTC 4 (cooler)",
    'DCDC_Temperature': "CAN: DCDC Temp",
    'C_chamber_T_actl': "Chamber Temp"
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
    'Regatron_P': "Regatron P",    
    'OBC_PowerMax': "Max P (derating)",
}

LVDC_labels = {
    'DCLV_Measured_Current': "CAN: LV DCDC output Current",
    'DCLV_Measured_Voltage': "CAN: LV DCDC output Voltage",
    'OBC_PowerMax': "CAN: Max Power (derating)",
}

Status_labels = {
    'BMS_OnBoardChargerEnable': "OBC Charger Enable",
}

#data.insert(0, 'P_in', P_in)
data_plot = data_DUT[['Measurement'] + status_labels+HV_AC_labels_V+HV_AC_labels_I+HV_AC_labels_P+HV_DC_labels_V+HV_DC_labels_I+HV_DC_labels_P+LV_DC_labels+temperature_labels+dl1_labels+dl2_labels+['PFC_IOM_ERR_UVLO_ISO7']].copy()
data_plot.insert(0, 'Time', data['Time']);
#data_plot['PS_relay_status'] = data_plot['PS_relay_status'].map({True:1, False:0})
#data_plot['OBC_Fault'] = data_plot['OBC_Fault'].map({0:0, 64:1, 128:2, 255:3})
#data_plot['OBC_PowerMax'] = data_plot['OBC_PowerMax']/1000;
#date_shortened = [x[:-5] + " " for x in data["Date"]]
data_plot.insert(0, 'Time_shortened', data['Date'] + " " + data['Time']);

file_type = ".html"
os.chdir(dirPlot)
resolution = [1920, 1080]
resolution_4k = [4096, 2160] 


# In[102]:


HV_DC_labels_V = ['OBC_OutputVoltage']
HV_DC_labels_I = ['OBC_OutputCurrent']
HVDC_labels = HV_DC_labels_V + HV_DC_labels_I


# In[103]:


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


# In[104]:


#Señales a mostrar del PFC
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'Pacific_V_Ph1', 'Pacific_V_Ph2','Pacific_V_Ph3','SUP_CommandVDCLink_V']
HV_AC_labels_V = [i for i in medidas if i in HV_AC_labels_V]
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1','Pacific_I_Ph1', 'Pacific_I_Ph2', 'Pacific_I_Ph3']
HV_AC_labels_I = [i for i in medidas if i in HV_AC_labels_I]
HV_AC_labels_P = ['Pacific_P_Ph1', 'Pacific_P_Ph2', 'Pacific_P_Ph3']
HV_AC_labels_P = [i for i in medidas if i in HV_AC_labels_P]


# In[105]:


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


# In[ ]:




