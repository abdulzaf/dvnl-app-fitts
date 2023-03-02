# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 15:06:08 2023

@author: zafar
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.ndimage import label
from scipy.signal import find_peaks

# Read
df_vel = pd.read_csv('./pilot.csv')
df_pos = pd.read_csv('./pilot_pos.csv')

x = df_pos['finger x']
v = df_vel['finger x']

# Outcome measures
# Movement onset: >20mm/s
v_on_20 = np.abs(v.copy())
v_on_20[v_on_20<20] = 0
v_on_20[:500] = 0
v_on_20[1500:] = 0

lbl, num_lbl = label(v_on_20.values)
move_on_20 = []
move_off_20 = []
for i in range(num_lbl):
    idx = np.where(lbl==(i+1))[0]
    move_time = idx[-1] - idx[0]
    if move_time > 10:
        move_on_20.append(idx[0])
        move_off_20.append(idx[-1])

# Movement onset: >100mm/s
v_on_100 = np.abs(v.copy())
v_on_100[v_on_100<100] = 0
v_on_100[:500] = 0
v_on_100[1500:] = 0

lbl, num_lbl = label(v_on_100.values)
move_off_100 = []
for i in range(num_lbl):
    idx = np.where(lbl==(i+1))[0]
    move_time = idx[-1] - idx[0]
    if move_time > 10:
        move_off_100.append(idx[-1])
        
# Peak velocity
pk_vel, _ = find_peaks(np.abs(v), height=500, distance=20)

# plt.plot(v_on)
# plt.hlines(20, 0, len(v_on))
# Movement offset: <20mm/s
x -= x[0]
plt.figure()
plt.plot(x)
plt.plot(move_on_20, x[move_on_20], 'go')
plt.plot(move_off_20, x[move_off_20], 'ro')
plt.plot(move_off_100, x[move_off_100], 'mo')
plt.plot(pk_vel, x[pk_vel], 'ko')
# plt.vlines(move_on_20, -75, 75, color='g')
# plt.vlines(move_off_20, -75, 75, color='r')
# plt.vlines(move_off_100, -75, 75, color='m')
# plt.plot(label)