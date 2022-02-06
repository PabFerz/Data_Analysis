#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


test = 'CL08 DUT2 D3-1'
directory = r'C:\Users\m0118367\Documents\Validation\CL08\TestLogs\DUT2 - SN34859\CL08 - DUT11 11.135_D3_1_34859'
os.chdir(directory)
dirName = directory + '\Combined csvs'
dirPlot = directory + '\Plots'
simplification_rate = 5;

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


# In[3]:


all_filenames


# In[4]:


#combined_csv = pd.concat([pd.read_csv(f, sep = ';', decimal = ',', usecols = usecols, low_memory = False) for f in all_filenames])
combined_csv = pd.concat([pd.read_csv(f, sep=';', decimal = ',', low_memory=False, error_bad_lines=False) for f in all_filenames])

#Remove zeros from data
#combined_csv_nozeros = combined_csv.loc[:, (combined_csv != '0').any(axis=0)]
#combined_csv_nozeros = combined_csv.T[combined_csv.any()].T

#Remove NaN values
data = combined_csv[pd.notnull(combined_csv['Time'])]

#If the sampling rate is to high use the simplifacation rate variable to reduce the number of data points to plot
data = combined_csv.loc[:, combined_csv.columns != 'Measurement']
data = data.iloc[np.arange(0,data.shape[0], simplification_rate)]
data.insert(0, 'Measurement', np.arange(0,data.shape[0]))
#data = data.dropna(axis=0, subset=['BMS_HighestChargeCurrentAllow'])
#export to csv
export_extension = 'xlsx'
#data.to_excel(dirName + "\combined_csv_ordered" + " - " + test + "." +export_extension)
print("File creation completed")


# In[9]:


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
data_plot = data[['Measurement'] + status_labels+HV_AC_labels_V+HV_AC_labels_I+HV_AC_labels_P+HV_DC_labels_V+HV_DC_labels_I+HV_DC_labels_P+LV_DC_labels+temperature_labels+dl1_labels+dl2_labels+['PFC_IOM_ERR_UVLO_ISO7']].copy()
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


# In[10]:


#data_plot =data_plot[data_plot['PFC_Vdclink_V'] <=660]
#data_plot =data_plot[data_plot['PFC_Temp_M1_C'] >=70]
#data_plot =data_plot[data_plot['PFC_Temp_M4_C'] >=70]
#data_plot =data_plot[data_plot['DCDC_Temperature'] >=70]
#data_plot =data_plot[data_plot['PFC_IPH1_RMS_0A1'] >=4]
#data_plot =data_plot[data_plot['DCHV_ADC_IOUT'] >=6]
#data_plot = data_plot[data_plot['DCLV_Measured_Voltage']<20]
#test_duration = 1200
#data_plot['Measurement'] = np.arange(0, data_plot.shape[0])/data_plot.shape[0]*test_duration 


# In[11]:


dtale.show(data_plot, ignore_duplicate=True)


# In[12]:


#Plot temperatures
file_name = test + " - Temperature measurement"
file = file_name  + file_type
data_plot_temp = data_plot[temperature_labels + ['Time_shortened']].copy()
for i in Temp_labels:
    data_plot_temp.rename(columns={i: Temp_labels[i]}, inplace=True)
fig_temp = data_plot_temp.iplot(title = file_name, x = 'Time_shortened', xTitle = 'Time[h]', line_shape='hv', yTitle = "Temperature [ºC]",asFigure = True, filename = file_name)

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


# In[40]:


#Plot HV AC measurements
file_name = test + " - HV AC measurements"
file = file_name  + file_type
fig_ac = go.Figure() 
for i in range(len(HV_AC_labels_V)):
   fig_ac.add_trace(go.Scatter(y = data_plot[HV_AC_labels_V[i]], x = data_plot['Time_shortened'], name=HVAC_labels[HV_AC_labels_V[i]], yaxis = "y1", line_shape='hv'))
for i in range(len(HV_AC_labels_I)):
   fig_ac.add_trace(go.Scatter(y = data_plot[HV_AC_labels_I[i]], x = data_plot['Time_shortened'], name=HVAC_labels[HV_AC_labels_I[i]], yaxis ="y2", line_shape='hv'))
fig_ac.layout.update(
    title = file_name,
    xaxis=dict(
        title = 'Time[h]',
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
fig_ac.layout.yaxis2.tickfont.size = 8
fig_ac.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_ac.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_ac.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig_ac, filename = file)
fig_ac.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[25]:


#Plot HV DC measurements

#Create figure with subplots
fig_dc = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Voltage','Current','OBC Charging Enable'))

#Combine plots
for i in range(len(HV_DC_labels_V)):
   fig_dc.append_trace(go.Scatter(y = data_plot[HV_DC_labels_V[i]], x = data_plot['Time_shortened'], name=HVDC_labels[HV_DC_labels_V[i]]), 1, 1)
for i in range(len(HV_DC_labels_I)):
   fig_dc.append_trace(go.Scatter(y = data_plot[HV_DC_labels_I[i]], x = data_plot['Time_shortened'], name=HVDC_labels[HV_DC_labels_I[i]]), 2, 1)
for i in range(len(status_labels)):
   fig_dc.append_trace(go.Scatter(y = data_plot[status_labels[i]], x = data_plot['Time_shortened'], name=Status_labels[status_labels[i]]), 3, 1)

#Edit format
fig_dc.layout.hovermode = 'x'
plot_name = "HV DC measurements"
file_name = test + " " + plot_name
fig_dc.layout.title.text = file_name
#fig_dc.layout.xaxis.title = "Time[h]"
fig_dc.layout.yaxis.range = [0, 500]
fig_dc.layout.yaxis2.range = [0, 40]
fig_dc.layout.yaxis3.range = [0, 2]
fig_dc.layout.xaxis1.tickfont.size = 4
fig_dc.layout.xaxis2.tickfont.size = 4
fig_dc.layout.xaxis3.tickfont.size = 4
fig_dc.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_dc.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_dc.layout.legend.bgcolor='rgba(0,0,0,0)'
fig_dc.layout.yaxis.title = "Voltage (V)"
fig_dc.layout.yaxis2.title = "Current (A)"
fig_dc.layout.yaxis3.title = "OBC Status"


plotly.offline.plot(fig_dc, filename = file_name + file_type)
fig_dc.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[31]:


#Plot LV DC measurements
file_name = test + " LV DC measurements"
file = file_name  + file_type
fig_lv = go.Figure() 
for i in range(len(LV_DC_labels_V)):
   fig_lv.add_trace(go.Scatter(y = data_plot[LV_DC_labels_V[i]], x = data_plot['Time_shortened'], name=LVDC_labels[LV_DC_labels_V[i]], yaxis = "y1", line_shape='hv'))
for i in range(len(LV_DC_labels_I)):
   fig_lv.add_trace(go.Scatter(y = data_plot[LV_DC_labels_I[i]], x = data_plot['Time_shortened'], name=LVDC_labels[LV_DC_labels_I[i]], yaxis ="y2", line_shape='hv'))
fig_lv.layout.update(
    title = file_name,
    xaxis=dict(
        title="Time[h]",
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
plotly.offline.plot(fig_lv, filename = file)
fig_lv.write_image(dirPlot + "\\" + file_name + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[8]:


#Plot Faults
file_name = test + " - Faults"
file = file_name  + file_type
fig_f = go.Figure()
faults = ['OBC_Fault']+['PFC_IOM_ERR_UVLO_ISO7'] + ['PS_relay_status']
for i in range(len(faults)):
   fig_f.add_trace(go.Scatter(y = data_plot[faults[i]], x = data_plot['Time_shortened'], name=faults[i], yaxis = "y1", line_shape='hv'))
fig_f.layout.update(
    title = file_name,
    xaxis=dict(
        showgrid = True,      
        gridcolor = 'lightgrey', 
    ),       
    yaxis=dict(
        title="Faults",
        range=[0,4],
        showline = True,
        linewidth=1, 
        linecolor='black',        
        showgrid = True,
        gridcolor = 'lightgrey'
    ),    
)
iso_7 = data_plot[data_plot['PFC_IOM_ERR_UVLO_ISO7'] == data_plot['PFC_IOM_ERR_UVLO_ISO7'].max()]
annotations = [dict(
                x=iso_7['Time_shortened'].iloc[i],
                y=iso_7['PFC_IOM_ERR_UVLO_ISO7'].iloc[i],
                text= "ISO_7",
                showarrow=True,
                arrowhead=7,
                ax=0,
                ay=-200,
                font=dict(
                            color="red",
                            size=12
                        ),
            ) for i in np.arange(len(iso_7))]
fig_f.update_layout(annotations = annotations)

fig_f.update_xaxes(showspikes=True, spikecolor="green", spikesnap="cursor", spikemode="across")
fig_f.update_yaxes(showspikes=True, spikecolor="orange", spikethickness=2)
fig_f.update_layout(spikedistance=1000, hoverdistance=100)
fig_f.layout.hovermode = 'x'
fig_f.layout.xaxis.tickfont.size = 8
fig_f.layout.paper_bgcolor='rgba(0,0,0,0)'
fig_f.layout.plot_bgcolor='rgba(0,0,0,0)'
fig_f.layout.legend.bgcolor='rgba(0,0,0,0)'
plotly.offline.plot(fig_f, filename = file_name + file_type)
fig_f.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[ ]:


#Create figure with subplots
fig = plotly.subplots.make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC', 'Faults'))

#Combine plots
for i in range(len(temperature_labels)):
   fig.append_trace(fig_temp.data[i], 1, 1)
for i in range(len(HV_AC_labels_V + HV_AC_labels_I)):
   fig.append_trace(fig_ac.data[i], 2, 1)
for i in range(len(HV_DC_labels_V + HV_DC_labels_I)):
   fig.append_trace(fig_dc.data[i], 3, 1)
for i in range(len(faults)):
   fig.append_trace(fig_f.data[i], 4, 1)

#Edit format
fig.layout.hovermode = 'x'
plot_name = "Temps AC, DC and faults"
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
fig.layout.yaxis.title = "Temperature"
fig.layout.yaxis2.title = "Current/Voltage"
fig.layout.yaxis3.title = "Current/Voltage"
fig.layout.yaxis4.title = "Faults"


#Show plot
file = test + "- Temps AC, DC and faults"
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[41]:


#Create figure with subplots
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


# In[ ]:


#Create figure with subplots
fig = plotly.subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, subplot_titles = ('Temperature','HVAC','HVDC'))

#Combine plots
for i in range(len(temperature_labels)):
   fig.append_trace(fig_temp.data[i], 1, 1)
for i in range(len(HV_DC_labels_V + HV_DC_labels_I)):
   fig.append_trace(fig_dc.data[i], 2, 1)
for i in range(len(LV_DC_labels_V + LV_DC_labels_I)):
   fig.append_trace(fig_lv.data[i], 3, 1)

#Edit format
fig.layout.hovermode = 'x'
plot_name = "Temps HV DC and LV DC measurements"
file_name = test + plot_name
fig.layout.title.text = test
#fig.layout.xaxis.title = "Time[h]"
fig.layout.yaxis.range = [-45, 115]
fig.layout.yaxis3.range = [0, 200]
fig.layout.xaxis1.tickfont.size = 8
fig.layout.xaxis2.tickfont.size = 8
fig.layout.xaxis3.tickfont.size = 8
fig.layout.paper_bgcolor='rgba(0,0,0,0)'
fig.layout.plot_bgcolor='rgba(0,0,0,0)'
fig.layout.legend.bgcolor='rgba(0,0,0,0)'
fig.layout.yaxis.title = "Temperature"
fig.layout.yaxis2.title = "Current/Voltage"
fig.layout.yaxis3.title = "Current/Voltage"


#Show plot
file = test + "- Temps HV DC and LV DC measurements"
plotly.offline.plot(fig, filename = file_name + file_type)
fig.write_image(dirPlot + "\\" + file + ".pdf", width = resolution[0], height = resolution[1], scale = 1)


# In[ ]:


media = data_plot[temperature_labels].rolling(1000).mean()


# In[ ]:


media.insert(0, 'Medida', np.arange(media.shape[0]));


# In[ ]:


new_data = data_plot.copy()
efficiency = abs(new_data['Regatron_P'])/P_in*100
efficiency[efficiency > 100] = 100
efficiency.replace([np.inf, -np.inf], 0,inplace=True)
new_data.insert(0, 'Efficiency', efficiency);
new_data = new_data.loc[~new_data.index.duplicated(keep='first')]
eff_labels = ['Efficiency', 'Media']

"""
new_data = new_data[new_data['P_in']> 0.6]
new_data = new_data[new_data['Efficiency']> 10]
"""


# In[ ]:


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


# In[ ]:


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


# In[ ]:


media = new_data['Efficiency'].rolling(60).mean()
new_data.insert(0, 'Media', media);


# In[ ]:




