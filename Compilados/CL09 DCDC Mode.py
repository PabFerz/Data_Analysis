#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import glob
import numpy as np
import pandas as pd
import scipy as sp
import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots
import cufflinks as cf
import orca
import dtale
get_ipython().run_line_magic('matplotlib', 'inline')
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
init_notebook_mode(connected=True)
cf.go_offline()


# In[220]:


test = 'CL09 DCDC - DUT1'
directory = r'C:\Users\M0081459\Documents\1_Proyectos\1_OBCP\1_Validation\8_Test results\D3_1\Ensayos Piezas D3_1\CL09\DCDC mode\DUT1'
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

import_extension = 'csv'
all_filenames = [i for i in sorted(glob.glob('*.{}'.format(import_extension)), key=os.path.getmtime)]


# In[221]:


all_filenames


# In[222]:


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
#data.to_excel(dirName + "\combined_csv_ordered" + " - " + test + "." +export_extension)
print("File creation completed")


# In[238]:


#Variables to be plot separately on each plot
temperature_labels = ['PFC_Temp_M1_C', 'PFC_Temp_M4_C', 'Chiller_T_actl', 'OBC_OBCTemp', 'DCHV_ADC_NTC_MOD_5', 'DCHV_ADC_NTC_MOD_6']
temperature_labels = [i for i in data.columns if i in temperature_labels]
HV_AC_labels_V = ['PFC_VPH12_RMS_V','PFC_VPH23_RMS_V','PFC_VPH31_RMS_V','PFC_Vdclink_V', 'SUP_CommandVDCLink_V']
HV_AC_labels_V = [i for i in data.columns if i in HV_AC_labels_V]
HV_AC_labels_I = ['PFC_IPH1_RMS_0A1','PFC_IPH2_RMS_0A1','PFC_IPH3_RMS_0A1']
HV_AC_labels_I = [i for i in data.columns if i in HV_AC_labels_I]
HV_AC_labels_P = []
HV_AC_labels_P = [i for i in data.columns if i in HV_AC_labels_P]
HV_AC_labels = HV_AC_labels_V + HV_AC_labels_I + HV_AC_labels_P
HV_DC_labels_V = ['Pacific_V_RMS_L1', 'OBC_OutputVoltage']
HV_DC_labels_V = [i for i in data.columns if i in HV_DC_labels_V]
HV_DC_labels_I = ['Pacific_I_RMS_L1', 'DCDC_InputCurrent']
HV_DC_labels_I = [i for i in data.columns if i in HV_DC_labels_I]
HV_DC_labels_P = ['Pacific_P_ACT_L1']
HV_DC_labels_P = [i for i in data.columns if i in HV_DC_labels_P]
HV_DC_labels = HV_DC_labels_V + HV_DC_labels_I + HV_DC_labels_P
LV_DC_labels_V = ['DCLV_Measured_Voltage']
LV_DC_labels_V = [i for i in data.columns if i in LV_DC_labels_V]
LV_DC_labels_I = ['DCLV_Measured_Current']
LV_DC_labels_I = [i for i in data.columns if i in LV_DC_labels_I]
LV_DC_labels = LV_DC_labels_V + LV_DC_labels_I
status_labels = ['PFC_PFCStatus', 'DCHV_DCHVStatus ', 'OBC_Status', 'OBC_Fault', 'OBC_PowerMax', 'Actual_Cycle']
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
    'PFC_VPH12_RMS_V': "PFC: V_in Ph1",
    'PFC_VPH23_RMS_V': "PFC: V_in Ph2",
    'PFC_VPH31_RMS_V': "PFC: V_in Ph3",
    'PFC_IPH1_RMS_0A1': "PFC: I_in Ph1",
    'PFC_IPH2_RMS_0A1': "PFC: I_in Ph2",
    'PFC_IPH3_RMS_0A1': "PFC: I_in Ph3",    
    'PFC_Vdclink_V': "DCLink V",
    'OBC_PowerMax': "Max P (derating)",
    'SUP_CommandVDCLink_V': 'PFC DC Link command',
    'P_in': 'Pacific: Total P'
}
HVDC_labels = {
    'OBC_OutputVoltage': "DCHV: V",
    'Pacific_V_RMS_L1': "Pacific: V_out",
    'Pacific_I_RMS_L1': "Pacific: I_out",
    'DCDC_InputCurrent': "DCDD: I_in",
    'OBC_PowerMax': "Max P (derating)",
}

LVDC_labels = {
    'DCLV_Measured_Current': "CAN: LV DCDC output Current",
    'DCLV_Measured_Voltage': "CAN: LV DCDC output Voltage",
    'OBC_PowerMax': "CAN: Max Power (derating)",
}

data_plot = data[['Measurement'] + status_labels+HV_AC_labels_V+HV_AC_labels_I+HV_AC_labels_P+HV_DC_labels_V+HV_DC_labels_I+HV_DC_labels_P+LV_DC_labels+temperature_labels+dl1_labels+dl2_labels].copy()
HV_AC_labels_P = HV_AC_labels_P + ["P_in"]
data_plot.insert(0, 'Time', data['Time'] + data['Date']);
data_plot['OBC_PowerMax'] = data_plot['OBC_PowerMax']/1000;
data_plot.insert(0, 'Time_shortened', data['Date'] + " " + data['Time']);

file_type = ".html"
os.chdir(dirPlot)
resolution = [1920, 1080]
resolution_4k = [4096, 2160] 


# In[224]:


dtale.show(data_plot, ignore_duplicate=True)


# In[259]:


#Plot temperatures
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_temp = data_plot[temperature_labels + ['Time_shortened']].copy()
for i in Temp_labels:
    data_plot_temp.rename(columns={i: Temp_labels[i]}, inplace=True)
fig = data_plot_temp.iplot(title = file_name, x = 'Time_shortened', xTitle = 'Time[h]', yTitle = "Temperature [C]",asFigure = True, filename = file_name)
fig.layout.update(
    title = file_name,
    xaxis=dict(
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),
    yaxis=dict(
        range=[-30,100],
        showgrid = True,
        gridcolor = 'lightgrey'
    ),    
)
fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.layout.hovermode = 'x unified'
fig.layout.margin['t'] = 60
fig.layout.margin['b'] = 140
fig.layout.yaxis.range = [-50, 110]
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
plotly.offline.plot(fig, filename = file)


# In[235]:


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
    xaxis=dict(
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
fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.layout.hovermode = 'x'
fig.layout.xaxis.tickfont.size = 8
fig.layout.yaxis2.tickfont.size = 8
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[236]:


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
    xaxis=dict(
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),       
    yaxis=dict(
        title="Voltage[V]",
        range=[0,500],
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
fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.layout.hovermode = 'x'
fig.layout.xaxis.tickfont.size = 8
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[255]:


#Plot LV DC measurements
file_name = test + " LV DC measurements"
file = file_name  + file_type
fig = go.Figure() 
for i in range(len(LV_DC_labels_V)):
   fig.add_trace(go.Scatter(y = data_plot[LV_DC_labels_V[i]], x = data_plot['Time_shortened'], name=LVDC_labels[LV_DC_labels_V[i]], yaxis = "y1", line_shape='hv'))
for i in range(len(LV_DC_labels_I)):
   fig.add_trace(go.Scatter(y = data_plot[LV_DC_labels_I[i]], x = data_plot['Time_shortened'], name=LVDC_labels[LV_DC_labels_I[i]], yaxis ="y2", line_shape='hv'))
fig.layout.update(
    title = file_name,
    xaxis=dict(
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
        range=[0,300],
        showline = True,
        linewidth=1, 
        linecolor='blue',        
        showgrid = True,
        gridcolor = 'lightblue'
    ),    
)
fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.layout.hovermode = 'x'
fig.layout.xaxis.tickfont.size = 8
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[ ]:


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
data_plot_ac = data_plot[HV_AC_labels['Time_shortened']].copy()
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

#Create figure with subplots
fig = plotly.tools.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC'))

#Combine plots
for i in range(len(temperature_labels)):
   fig.append_trace(fig_1.data[i], 1, 1)
for i in range(len(HV_AC_labels)):
   fig.append_trace(fig_2.data[i], 2, 1)
for i in range(len(HV_DC_labels)):
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


# In[ ]:


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
data_plot_faults = data_plot[['Time_shortened']+['OBC_Fault']+['PFC_IOM_ERR_UVLO_ISO7']+ ['PFC_PFCStatus'] + ['PS_relay_status']].copy()
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
for i in range(4):
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


# In[ ]:


dtale.show(data,ignore_duplicate=True)


# In[ ]:


media.insert(0, 'Medida', np.arange(media.shape[0]));


# In[176]:


new_data = data_plot.copy()
efficiency = abs(new_data['Regatron_P'])/P_in*100
efficiency[efficiency > 100] = 100
efficiency.replace([np.inf, -np.inf], 0,inplace=True)
new_data.insert(0, 'Efficiency', efficiency);
new_data = new_data.loc[~new_data.index.duplicated(keep='first')]

media = new_data['Efficiency'].rolling(60).mean()
new_data.insert(0, 'Media', media);

eff_labels = ['Efficiency', 'Media']

"""
new_data = new_data[new_data['P_in']> 0.6]
new_data = new_data[new_data['Efficiency']> 10]
"""


# In[177]:


new_data[HV_AC_labels].max()


# In[36]:


#Plot temperatures
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_temp = new_data[temperature_labels + ['Time_shortened']+['Efficiency']].copy()
fig = data_plot_temp.iplot(title = file_name, x = 'Time_shortened', xTitle = 'Time[h]', yTitle = "Temperature [C]",asFigure = True, filename = file_name)
fig.layout.margin['t'] = 60
fig.layout.margin['b'] = 140
fig.layout.yaxis.range = [-50, 110]
fig.layout.xaxis.tickfont.size = 7
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)
plotly.offline.plot(fig, filename = file)


# In[156]:


#Plot Efficiency
file_name = test + " - Efficiency"
file = file_name  + file_type
fig = go.Figure()
for i in range(len(HV_AC_labels_P)):
   fig.add_trace(go.Scatter(y = new_data[HV_AC_labels_P[i]], x = new_data['Time_shortened'], name=HVAC_labels[HV_AC_labels_P[i]], yaxis = "y1"))
for i in range(len(HV_DC_labels_P)):
   fig.add_trace(go.Scatter(y = new_data[HV_DC_labels_P[i]], x = new_data['Time_shortened'], name=HVDC_labels[HV_DC_labels_P[i]]))
for i in range(len(eff_labels)):
   fig.add_trace(go.Scatter(y = new_data[eff_labels[i]], x = new_data['Time_shortened'], name=eff_labels[i], yaxis ="y2"))
fig.layout.update(
    title = file_name,
    xaxis=dict(
        showline = True, 
        linewidth=1, 
        linecolor='black',
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),
    yaxis=dict(
        title="Power[P]",
        range=[0,15],
        showline = True,
        linewidth=1, 
        linecolor='black',        
        showgrid = True,
        gridcolor = 'lightgrey'
    ),
    yaxis2=dict(
        title="Efficiency [%]",
        overlaying="y1",
        side="right",
        range=[0,100],
        showline = True,
        linewidth=1, 
        linecolor='blue',        
        showgrid = True,
        gridcolor = 'lightblue'
    ),    
)
fig.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig.update_layout(spikedistance=1000, hoverdistance=100)
fig.layout.hovermode = 'x unified'
fig.layout.xaxis.tickfont.size = 8
fig.layout.yaxis2.tickfont.size = 8
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[246]:


P_out = data_plot['DCLV_Measured_Current'] * data_plot['DCLV_Measured_Voltage']


# In[247]:


P_out.max()


# In[ ]:




