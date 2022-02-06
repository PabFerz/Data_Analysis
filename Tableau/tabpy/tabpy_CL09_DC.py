#!/usr/bin/env python
# coding: utf-8

# In[5]:


import os
import glob
import numpy as np
import pandas as pd
import scipy as sp
import cufflinks as cf

def CleanStandsDataset(data):
    test = 'CL09 DCDC - DUT1'
    data = data.loc[:, data.columns != 'Measurement']
    simplification_rate = 5;
    data = data.iloc[np.arange(0,data.shape[0], simplification_rate)]
    data.insert(0, 'Measurement', np.arange(0,data.shape[0]))
    #Variables to be plot separately on each plot
    temperature_labels = ['PFC_Temp_M1_C', 'PFC_Temp_M4_C', 'Chiller_T_Actl', 'OBC_OBCTemp', 'DCHV_ADC_NTC_MOD_5', 'DCHV_ADC_NTC_MOD_6']
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
    
    return(data)

def get_output_schema():
    return pd.DataFrame({
        'Measurement': prep_int(),
        'Time':prep_datetime(),
        'OBC_PowerMax':prep_decimal(),
        'PFC_Temp_M1_C': prep_decimal(),
        'PFC_Temp_M4_C': prep_decimal(),
        'Chiller_T_Actl': prep_string(),
        'DCHV_ADC_NTC_MOD_5': prep_decimal(),
        'DCHV_ADC_NTC_MOD_6': prep_decimal(),
        'OBC_OBCTemp': prep_decimal(),
    })
        
#data types for the get_output_schema:
    # prep_string() --> String
    # prep_decimal() --> Decimal
    # prep_int() --> Integer
    # prep_bool() --> Boolean
    # prep_date() --> Date
    # prep_datetime() --> DateTime


# In[ ]:




