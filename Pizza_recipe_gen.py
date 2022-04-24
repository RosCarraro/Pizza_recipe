#%%
import numpy as np
import pandas as pd

"""
Script that generates a pizza recipe based on
hidration - not yet
size of the baking tray (rectangular)
desired thickness of the pizza
"""
#%%
percentages=pd.Series({'flour':0.542,'autolisi water':0.353,'dough water':0.081,'salt':0.011,'olive oil':0.011,'yeast':0.0075})

thickness_factor=pd.Series({'thin':0.4,'medium':0.5,'thick':0.6})

# input baking tray size/surface
while True:
   baking_tray_size=input('Please enter your baking tray size in cm, as 2 comma separated values (default "30,45"):')
   if not baking_tray_size:
      baking_tray_size="30,45"
   try:
      # convert r from string to list
      baking_tray_size = list(map(int, baking_tray_size.split(","))) 
   except ValueError:
      print('Please enter 2 (numeric) lengths')
      continue
   if len(baking_tray_size) != 2:
      print('Please enter exactly 2 (numeric) lengths')
      continue
   else:
      # len(baking_tray_size) >= 2:
      #print('good')
      break
baking_tray_surface=baking_tray_size[0]*baking_tray_size[1]

total_dough_weight=baking_tray_surface*thickness_factor

for index, value in total_dough_weight.items():
   print(f'Ingredients for a {index} pizza (g):')
   print(percentages*value)