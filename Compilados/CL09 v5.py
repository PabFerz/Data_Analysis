#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import glob
import numpy as np
import pandas as pd
import scipy as sp

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.plotly as py
import plotly
import cufflinks as cf
import orca
import dtale
get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()


# In[2]:


test = 'CL09 3ph - SN38451'
directory = r'C:\Users\M0081459\Documents\1_Proyectos\1_OBCP\1_Validation\8_Test results\D3_1\Ensayos Piezas D3_1\CL09\Nueva carpeta'
os.chdir(directory)
dirName = directory + '\Combined csvs'
dirPlot = directory + '\Plots'
simplification_rate = 3;

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

import_extension = 'csv'
all_filenames = [i for i in sorted(glob.glob('*.{}'.format(import_extension)), key=os.path.getmtime)]


# In[4]:


#combined_csv = pd.concat([pd.read_csv(f, sep = ';', decimal = ',', usecols = usecols, low_memory = False) for f in all_filenames])
combined_csv = pd.concat([pd.read_csv(f, sep = ';', decimal = ',', low_memory = False) for f in all_filenames])

#Remove zeros from data
#combined_csv_nozeros = combined_csv.loc[:, (combined_csv != '0').any(axis=0)]
#combined_csv_nozeros = combined_csv.T[combined_csv.any()].T

#Remove NaN values
#data = combined_csv[pd.notnull(combined_csv_nozeros['Time'])]

#If the sampling rate is to high use the simplifacation rate variable to reduce the number of data points to plot
data = combined_csv.loc[:, combined_csv.columns != 'Measurement']
data = data.iloc[np.arange(0,data.shape[0], simplification_rate)]
data.insert(0, 'Measurement', np.arange(0,data.shape[0]))
#data = data.dropna(axis=0, subset=['BMS_HighestChargeCurrentAllow'])
#export to csv
export_extension = 'xlsx'
data.to_excel(dirName + "\combined_csv_ordered" + " - " + test + "." +export_extension)
print("File creation completed")


# In[63]:


#Variables to be plot separately on each plot
temperature_labels = ['PFC_Temp_M1_C', 'PFC_Temp_M4_C', 'C_chamber_T_actl', 'Chiller_T_Actl', 'DUT_external_temp', 'DCHV_ADC_NTC_MOD_5', 'DCHV_ADC_NTC_MOD_6']
temperature_labels = [i for i in data.columns if i in temperature_labels]
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'Pacific_V_Ph1']
HV_AC_labels_V = [i for i in data.columns if i in HV_AC_labels_V]
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1','Pacific_I_Ph1']
HV_AC_labels_I = [i for i in data.columns if i in HV_AC_labels_I]
HV_AC_labels = HV_AC_labels_V + HV_AC_labels_I
HV_DC_labels_V = ['DCHV_ADC_VOUT', 'Regatron_V']
HV_DC_labels_V = [i for i in data.columns if i in HV_DC_labels_V]
HV_DC_labels_I = ['DCHV_ADC_IOUT', 'Regatron_I']
HV_DC_labels_I = [i for i in data.columns if i in HV_DC_labels_I]
HV_DC_labels = HV_DC_labels_V + HV_DC_labels_I
LV_DC_labels_V = ['DCLV_Measured_Voltage']
LV_DC_labels_V = [i for i in data.columns if i in LV_DC_labels_V]
LV_DC_labels_I = ['DCLV_Measured_Current']
LV_DC_labels_I = [i for i in data.columns if i in LV_DC_labels_I]
LV_DC_labels = LV_DC_labels_V + LV_DC_labels_I
status_labels = ['PFC_PFCStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault', 'OBC_PowerMax']
#status_labels = ['PFC_PFCStatus', 'DCLV_DCLVStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault']
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
    'C_chamber_T_actl': "Climatic Chamber: Temp",
    'Chiller_T_actl': "Chiller: Coolant Temp",
    'DCHV_ADC_NTC_MOD_5': "CAN: DCDC HV NTC 5",
    'DCHV_ADC_NTC_MOD_6': "CAN: DCDC HV NTC 6",
    'OBC_PowerMax': "CAN: Max Power (derating)",
    'OBC_OBCTemp': "CAN: Max Measured Temperature",
    'C_chamber_HR_actl': "Climatic Chamber: Humidity",
    
    
}
HVAC_labels = {
    'PFC_VPH12_RMS_V': "CAN: Phase_1 input Voltage",
    'PFC_VPH23_RMS_V': "CAN: Phase_2 input Voltage",
    'PFC_VPH31_RMS_V': "CAN: Phase_3 input Voltage",
    'PFC_IPH1_RMS_0A1': "CAN: Phase_1 input Current",
    'PFC_IPH2_RMS_0A1': "CAN: Phase_2 input Current",
    'PFC_IPH3_RMS_0A1': "CAN: Phase_3 input Current",    
    'PFC_Vdclink_V': "CAN: DC Link Voltage",
    'Pacific_V_Ph1': "AC Power supply Voltage",
    'Pacific_I_Ph1': "AC Power supply Current",
    'OBC_PowerMax': "CAN: Max Power (derating)",
}
HVDC_labels = {
    'DCHV_ADC_VOUT': "CAN: HV DCDC output Voltage",
    'DCHV_ADC_IOUT': "CAN: HV DCDC output Current",
    'Regatron_V': "HV DC output Load Voltage",
    'Regatron_I': "HV DC output Load Current",
    'OBC_PowerMax': "CAN:Max Power (derating)",
}

LVDC_labels = {
    'DCLV_Measured_Current': "CAN: LV DCDC output Current",
    'VCU_DCDCVoltageReq': "CAN: LV DCDC output Voltage sepoint",
    'OBC_PowerMax': "CAN: Max Power (derating)",
}

data_plot = data[['Measurement'] + status_labels+HV_AC_labels_V+HV_AC_labels_I+HV_DC_labels_V+HV_DC_labels_I+LV_DC_labels+temperature_labels+dl1_labels+dl2_labels+['PS_relay_status']].copy()
data_plot.insert(0, 'Time', data['Time'] + data['Date']);
#data_plot['OBC_PowerMax'] = data_plot['OBC_PowerMax']/1000;
#date_shortened = [x[:-5] + " " for x in data["Date"]]
data_plot.insert(0, 'Time_shortened', data['Date'] + " " + data['Time']);

file_type = ".html"
os.chdir(dirPlot)
resolution = [1920, 1080]
resolution_4k = [4096, 2160] 


# In[6]:


dtale.show(data_plot, ignore_duplicate=True)


# In[51]:


data_plot = data_plot[data_plot['Chiller_T_Actl'] != 0]
data_plot = data_plot[data_plot['Regatron_V'] >= 260]


# In[8]:


#Plot temperatures
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_temp = data_plot[temperature_labels + ['Time_shortened']].copy()
for i in Temp_labels:
    data_plot_temp.rename(columns={i: Temp_labels[i]}, inplace=True)
fig = data_plot_temp.iplot(title = file_name, x = 'Time_shortened', xTitle = 'Time[h]', yTitle = "Temperature [C]",asFigure = True, filename = file_name)
fig.layout.margin['t'] = 60
fig.layout.margin['b'] = 140
fig.layout.yaxis.range = [-50, 90]
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
plotly.offline.plot(fig, filename = file)


# In[9]:


#Plot HV AC measurements
file_name = test + " - HV AC measurements"
file = file_name  + file_type
fig = go.Figure() 
for i in range(len(HV_AC_labels_V)):
   fig.add_trace(go.Scatter(y = data_plot[HV_AC_labels_V[i]], x = data_plot['Time_shortened'], name=HVAC_labels[HV_AC_labels_V[i]], yaxis = "y1"))
for i in range(len(HV_AC_labels_I)):
   fig.add_trace(go.Scatter(y = data_plot[HV_AC_labels_I[i]], x = data_plot['Time_shortened'], name=HVAC_labels[HV_AC_labels_I[i]], yaxis ="y2"))
fig.layout.update(
    title = file_name,
    yaxis=dict(
        title="Voltage[V]",
        range=[0,700]
    ),
    yaxis2=dict(
        title="Current[A]",
        overlaying="y1",
        side="right",
        range=[0,50]
    )
)
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
#Plot HV DC measurements
file_name = test + " HV DC measurements"
file = file_name  + file_type
fig = go.Figure() 
for i in range(len(HV_DC_labels_V)):
   fig.add_trace(go.Scatter(y = data_plot[HV_DC_labels_V[i]], x = data_plot['Time_shortened'], name=HVDC_labels[HV_DC_labels_V[i]], yaxis = "y1"))
for i in range(len(HV_DC_labels_I)):
   fig.add_trace(go.Scatter(y = data_plot[HV_DC_labels_I[i]], x = data_plot['Time_shortened'], name=HVDC_labels[HV_DC_labels_I[i]], yaxis ="y2"))
fig.layout.update(
    title = file_name,
    yaxis=dict(
        title="Voltage[V]",
        range=[0,500]
    ),
    yaxis2=dict(
        title="Current[A]",
        overlaying="y1",
        side="right",
        range=[0,50]
    )
)
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[66]:


data_plot['OBC_Fault'] = data_plot['OBC_Fault'].map({0:0, 64:1, 128:2, 255:3})

#Create subplots
#Select data
#Plot datalogger
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_dl = data_plot[temperature_labels + ['Time_shortened']].copy()
for i in Temp_labels:
    data_plot_dl.rename(columns={i: Temp_labels[i]}, inplace=True)
fig_1 = data_plot_dl.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Plot HV AC
file_name = test + " - HV AC measurements"
file = file_name  + file_type
data_plot_ac = data_plot[HV_AC_labels_V + HV_AC_labels_I + ['Time_shortened']].copy()
for i in HVAC_labels:
    data_plot_ac.rename(columns={i: HVAC_labels[i]}, inplace=True)
fig_2 = data_plot_ac.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Plot HV DC
file_name =  test + " - HV DC measurements"
file = file_name  + file_type
data_plot_hvdc = data_plot[HV_DC_labels_V + HV_DC_labels_I + ['Time_shortened']+['PS_relay_status']].copy()
for i in HVDC_labels:
    data_plot_hvdc.rename(columns={i: HVDC_labels[i]}, inplace=True)
fig_3 = data_plot_hvdc.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Create figure with subplots
fig = plotly.tools.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC'))

#Combine plots
for i in range(len(temperature_labels)):
   fig.append_trace(fig_1.data[i], 1, 1)
for i in range(len(HV_AC_labels)):
   fig.append_trace(fig_2.data[i], 2, 1)
for i in range(len(HV_DC_labels)+1):
   fig.append_trace(fig_3.data[i], 3, 1)

#Edit format
fig.update_yaxes(showgrid=True)
fig.update_xaxes(showgrid=True)
plot_name = "Datalogger Temps HVDC and LVDC measurements"
file_name = test + plot_name
fig.layout.title.text = test
#fig.layout.xaxis.title = "Time[h]"
fig.layout.yaxis.range = [-45, 115]
fig.layout.yaxis3.range = [0, 500]
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.layout.yaxis.title = "Temperature"
fig.layout.yaxis2.title = "Current/Voltage"
fig.layout.yaxis3.title = "Current/Voltage"

#Show plot
file = test + "- Temps AC and DC measurements"
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[76]:


data_plot['OBC_Fault'] = data_plot['OBC_Fault'].map({0:0, 64:1, 128:2, 255:3})

#Create subplots
#Select data
#Plot datalogger
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_dl = data_plot[temperature_labels + ['Time_shortened']].copy()
for i in Temp_labels:
    data_plot_dl.rename(columns={i: Temp_labels[i]}, inplace=True)
fig_1 = data_plot_dl.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Plot HV AC
file_name = test + " - HV AC measurements"
file = file_name  + file_type
data_plot_ac = data_plot[HV_AC_labels_V + HV_AC_labels_I + ['Time_shortened']].copy()
for i in HVAC_labels:
    data_plot_ac.rename(columns={i: HVAC_labels[i]}, inplace=True)
fig_2 = data_plot_ac.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Plot HV DC
file_name =  test + " - HV DC measurements"
file = file_name  + file_type
data_plot_hvdc = data_plot[HV_DC_labels_V + HV_DC_labels_I + ['Time_shortened']].copy()
for i in HVDC_labels:
    data_plot_hvdc.rename(columns={i: HVDC_labels[i]}, inplace=True)
fig_3 = data_plot_hvdc.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Plot Faults
file_name =  test + " - Faults"
file = file_name  + file_type
data_plot_faults = data_plot[['Time_shortened']+['PS_relay_status']].copy()
fig_4 = data_plot_faults.iplot(title = file_name, x = 'Time_shortened', asFigure = True, filename = file_name)

#Create figure with subplots
fig = plotly.tools.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC', 'Faults'))

#Combine plots
for i in range(len(temperature_labels)):
   fig.append_trace(fig_1.data[i], 1, 1)
for i in range(len(HV_AC_labels)):
   fig.append_trace(fig_2.data[i], 2, 1)
for i in range(len(HV_DC_labels)):
   fig.append_trace(fig_3.data[i], 3, 1)
for i in range(1):
   fig.append_trace(fig_4.data[i], 4, 1)

#Edit format
fig.update_yaxes(showgrid=True)
fig.update_xaxes(showgrid=True)
plot_name = "Datalogger Temps HVDC and LVDC measurements"
file_name = test + plot_name
fig.layout.title.text = test
#fig.layout.xaxis.title = "Time[h]"
fig.layout.yaxis.range = [-45, 115]
fig.layout.yaxis3.range = [0, 500]
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.layout.yaxis.title = "Temperature"
fig.layout.yaxis2.title = "Current/Voltage"
fig.layout.yaxis3.title = "Current/Voltage"
fig.layout.yaxis4.title = "Faults"


#Show plot
file = test + "- Temps AC and DC measurements"
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[16]:


dtale.show(data,ignore_duplicate=True)


# In[56]:


data_plot_hvdc


# In[71]:


data_plot['PS_relay_status'].unique()


# In[55]:


data_plot['PS_relay_status'] = data_plot['PS_relay_status'].astype(int)


# In[ ]:




