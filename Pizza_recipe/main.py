"""
A Bokeh server app that generates a pizza recipe based on:
- size of the baking tray (rectangular)
- desired thickness of the pizza.

Run the server using the following command in your terminal:
bokeh serve --show Pizza_recipe_gen.py
"""
import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.models import Column, Row
from bokeh.models import Slider,Spacer,RadioButtonGroup,Div
from bokeh.models import CustomJS
from bokeh.models import LabelSet
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

## Basic definitions
percentages=pd.Series({'flour':0.542,'autolisi water':0.353,'dough water':0.081,'salt':0.011,'olive oil':0.011,'yeast':0.0075})
ingredient_names=['flour', 'autolisi\nwater', 'dough\nwater', 'salt', 'olive oil', 'yeast']
ingredient_names_simple=[s.replace('\n',' ') for s in ingredient_names]
ingredient_amounts=[0.542, 0.353, 0.081, 0.011, 0.011, 0.0075]
source = ColumnDataSource(data=dict(ingredient_names=ingredient_names, ingredient_amounts=ingredient_amounts)) 
source.data["labelset_text"] = [f'{ia:.1f} g' for ia in ingredient_amounts]

thickness_factors={'Thin':0.4,'Medium':0.5,'Thick':0.6}
thickness_labels = [key for key in thickness_factors]

## Create plots and widgets
# Text widgets
title = Div(text='Pizza recipe generator', width_policy='fit', style={'font-size': '300%', 'color': '#035988','font-weight':'bold'},width=900)
subtitle = Div(text='Please enter the information below:', width_policy='fit')
thickness_text = Div(text='How thick do you want your pizza to be?', width_policy='fit')
ingredients = Div(text='', width_policy='fit')
spacer=Spacer(height=70)
directions_title = Div(text="<b>Directions:</b>", style={'font-size': '200%', 'color': '#007C00'})
directions = Div(text='', width_policy='fit',width=900)

# Sliders and buttons
thickness_button_group = RadioButtonGroup(labels=thickness_labels, active=1)
thickness_button_group.js_on_click(CustomJS(code="""
    console.log('thickness_button_group: active=' + this.active, this.toString())
"""))
tray_number = Slider(title='How many trays of pizza would you like to bake?', start=1, end=10, step=1, value=1)
tray_length = Slider(title='Baking tray length (cm)', start=5, end=100, step=1, value=30)
tray_width = Slider(title='Baking tray width (cm)', start=5, end=100, step=1, value=45)

# Make ingredients bar plot
p = figure(x_range=ingredient_names, height=350, toolbar_location=None, title="Ingredients", y_axis_type="log",y_range=[1,500])
p.vbar(x='ingredient_names', top='ingredient_amounts', width=0.9, source=source, bottom=0.01,
       line_color='white', fill_color=factor_cmap('ingredient_names', palette=Spectral6, factors=ingredient_names))
p.xaxis.major_label_text_font_size = '12pt'
p.xaxis.major_label_text_color = 'Black'
p.y_range.start = 0.1
p.xgrid.grid_line_color = None
# Add labels to the bars
source.data["labelset_text"] = [f'{ia:.1f} g' for ia in ingredient_amounts]
labels = LabelSet(x='ingredient_names', y='ingredient_amounts', text='labelset_text',
              x_offset=0, y_offset=0, source=source, render_mode='canvas', level='glyph',text_align='center')
p.add_layout(labels)

# Add callbacks
def update():
   ingredient_amounts, n_trays, active_button=recalc_ingredients()
   p.title.text = f'Ingredients for {n_trays} {active_button.lower()} pizza:'
   source.data["labelset_text"] = [f'{ia:.1f} g' for ia in ingredient_amounts]
   source.data["ingredient_amounts"] = ingredient_amounts
   p.y_range.end = 10**(np.log10(np.max(source.data['ingredient_amounts']))*1.1)
   directions.text=update_directions(ingredient_names_simple,ingredient_amounts,n_trays)

def recalc_ingredients():
   n_trays=tray_number.value
   active_button=thickness_labels[thickness_button_group.active]
   thickness_factor=thickness_factors[active_button]
   baking_tray_surface=tray_length.value*tray_width.value
   total_dough_weight=baking_tray_surface*thickness_factor*n_trays
   ingredient_amounts=percentages*total_dough_weight
   return ingredient_amounts, n_trays,active_button

def callback(attr, old, new):
   ingredient_amounts, n_trays, active_button = recalc_ingredients()
   source.data['ingredient_amounts']=ingredient_amounts
   p.title.text = f'Ingredients for {n_trays} {active_button.lower()} pizza:'
   source.data["labelset_text"] = [f'{ia:.1f} g' for ia in ingredient_amounts]
   source.data["ingredient_amounts"] = ingredient_amounts
   p.y_range.end = 10**(np.log10(np.max(source.data['ingredient_amounts']))*1.1)
   directions.text=update_directions(ingredient_names_simple,ingredient_amounts,n_trays)

def update_directions(ingredient_names_simple,ingredient_amounts,n_trays):
   recipe = pd.Series(ingredient_amounts, index=ingredient_names_simple)
   text=f"<span style='color: #C54A53;font-weight:bold;font-size:150%'>Day 1</span><br>Make a dough with all of the flour ({recipe['flour']:.0f} g) and the autolisi water ({recipe['autolisi water']:.0f} g). Use a planetary mixer with its kneading hook at speed n1 for ~5 min. Then stop the mixer and leave the dough to rest for 20 min, covered with a plastic film.<br> Restart the mixer at 1st speed adding all the yeast ({recipe['yeast']:.1f} g) and gradually about half of the dough water ({recipe['dough water']/2:.0f} g). Keep going for 7 min, then increase the speed to 2 for additional 5 min.\n When increasing to second speed add the salt ({recipe['salt']:.1f} g) and then the remaining water ({recipe['dough water']/2:.0f} g) until complete absorbtion. Finally, add the olive oil to the mix ({recipe['olive oil']:.1f} g). At the end of this kneading phase the dough will be smooth and strung.<br><br> Once you're done extract the dough with wet hands and place it in a big oiled bowl. Fold the dough to give some strength (check some youtube video if you don't know what this is). Put the dough to rest in the fridge (4°C) for 8 to 24 h (the longer the better).<br><br><span style='color: #C54A53;font-weight:bold;font-size:150%'>Day 2</span><br>"

   if n_trays>1:
      total_dough_weight=ingredient_amounts.sum()
      mass_per_tray=total_dough_weight/n_trays
      text+=f"We now cut the dough in {n_trays} parts, preferably inside the bowl in order not to deflate it. The mass of each part will have to be {mass_per_tray:.1f} g. "
      
   text+=f"We fold again the dough and place it in hermetic container(s), covered in semolina, where we'll leave it to grow at room temperature for 2.5-3 h.<br><br> In order to spread the dough let's prepare a generous semolina layer on the table, then let's pull out the dough from the container with a spatula, put on the table and follow these steps: <br> 1 Sprinkle the top with some semolina <br> 2 'close' the dough's border by pressing with your fingers throughout the perimeter <br> 3 gently spread the dough in the central part, starting from the top to the bottom and viceversa <br> 4 flip the dough and repeat the steps above <br> 5 when the dough is slightly smaller than the tray, lift it, lay it on your forearm and gently shake it to remove the excess semolina <br> 6 lay the dough on the oiled tray and press it with your fingers in order to spread it trough the entire tray.<br><br> Season the pizza before baking. Two simple preparations are 'pizza bianca' and 'pizza rossa'.<br> For pizza bianca use olive oil and some coarse salt.<br> For pizza rossa put in a bowl some tomato souce, olive oil, some salt, oregano and a crushed garlic clove.<br><br> In order to bake preheat your home oven to maximum temperature (ideally 290-300°C) and cook for 10 minutes (or longer if lower temperature) laying the tray as low as possible in the oven."

   return text

tray_number.on_change('value', callback)
tray_length.on_change('value', callback)
tray_width.on_change('value', callback)
thickness_button_group.on_change('active', callback)

# Arrange widgets in layouts
title_row=Row(title)
widgets_col=Column(subtitle,tray_number,tray_length,tray_width,thickness_text,thickness_button_group,spacer,directions_title)
recipe_col=Column(p)
directions_row=Row(directions)
layout = Column(title_row,Row(widgets_col,recipe_col),directions_row)

update()
curdoc().add_root(layout)
