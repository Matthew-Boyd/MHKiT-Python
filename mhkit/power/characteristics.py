import pandas as pd
import numpy as np
from scipy.signal import hilbert
import datetime

def instantaneous_frequency(um):

    """
    Calculates the instantaneous frequency of a measured voltage
    
     
    Parameters
    -----------
    um: pandas Series or DataFrame
        measured voltage source (V) index by time 

        
    Returns
    ---------
    frequency: pandas DataFrame
        the frequency of the measured voltage (Hz) index by time 
    """  
    assert isinstance(um, (pd.Series, pd.DataFrame)), 'um must be of type pd.Series or pd.DataFrame'
   
    if isinstance(um.index[0], datetime.datetime):
        t = (um.index - datetime.datetime(1970,1,1)).total_seconds()
    else:
        t = um.index

    dt = pd.Series(t).diff()[1:]

    if isinstance(um,pd.Series):
        um = um.to_frame()

    columns  = um.columns
    frequency=pd.DataFrame(columns=columns)
    for column in um.columns:
        f = hilbert(um[column])
        instantaneous_phase = np.unwrap(np.angle(f))
        instantaneous_frequency = np.diff(instantaneous_phase) /(2.0*np.pi) * (1/dt)
        frequency[column] = instantaneous_frequency
        
    return frequency

def dc_power(voltage, current):
    """
    Calculates DC power from voltage and current

    Parameters
    -----------
    voltage: pandas Series or DataFrame
        Measured DC voltage [V] indexed by time
    current: pandas Series or DataFrame
        Measured three phase current [A] indexed by time
    
    Returns
    --------
    P: pandas DataFrame
        DC power [W] from each channel and gross power indexed by time
    """
    assert isinstance(voltage, (pd.Series, pd.DataFrame)), 'voltage must be of type pd.Series or pd.DataFrame'
    assert isinstance(current, (pd.Series, pd.DataFrame)), 'current must be of type pd.Series or pd.DataFrame'
    
    # rename columns in current the calculation
    col_map = dict(zip(current.columns, voltage.columns))
    
    P = current.rename(columns=col_map)*voltage
    coln = list(range(1,len(P.columns)+1))
    P.columns = coln
    
    P['Gross'] = P.sum(axis=1, skipna=True) 
    
    return P

def ac_power_three_phase(voltage, current, power_factor, line_to_line=False):
    """
    Calculates magnitude of apparent power from line to neutral voltage and current 

    Parameters
    -----------
    voltage: pandas DataFrame
        Time series of all three measured voltage phases [V] indexed by time
    current: pandas DataFrame 
        Time series of all three measured current phases [A] indexed by time
    power_factor: float 
        Power factor for the system
    line_to_line: bool
        Set to true if the given voltage measurements are line_to_line
    
    Returns
    --------
    P: pandas DataFrame
        magnitude of apparent power [volt-amperes] indexed by time
    """
    assert isinstance(voltage, pd.DataFrame), 'voltage must be of type pd.DataFrame'
    assert isinstance(current, pd.DataFrame), 'current must be of type pd.DataFrame'
    assert len(voltage.columns) == 3, 'voltage must have three columns'
    assert len(current.columns) == 3, 'current must have three columns'
    assert current.shape == voltage.shape, 'current and voltage must be of the same size'
    
    # rename columns in current the calculation
    col_map = dict(zip(current.columns, voltage.columns))

    if line_to_line:
        power = current.rename(columns=col_map).abs()*(voltage.abs()*np.sqrt(3))
    else:
        power = current.rename(columns=col_map).abs()*voltage.abs()
        
    P = power.sum(axis=1)*power_factor
    P = P.to_frame('Power')
    
    return P
