#%%
import pandas as pd

"""
Script that generates a pizza recipe based on:
size of the baking tray (rectangular)
desired thickness of the pizza
"""
#%%
print('80% hydration pizza')
percentages=pd.Series({'flour':0.542,'autolisi water':0.353,'dough water':0.081,'salt':0.011,'olive oil':0.011,'yeast':0.0075})

thickness_factors={'thin':0.4,'medium':0.5,'thick':0.6}

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

#input tray amounts
while True:
   n_trays=input("Please enter how many trays you'd like to bake (default '1'):")
   if not n_trays:
      n_trays="1"
   try:
      # convert r from string to list
      n_trays = int(n_trays)
   except ValueError:
      print('Please enter 1 integer number')
      continue
   else:
      break

#input pizza thickness
while True:
   print("How thick would you like your pizza to be?")
   thickness=input("Please enter either 'thin', 'medium', or 'thick' (default medium):")
   if not thickness:
      thickness='medium'
      thickness_factor=thickness_factors[thickness]
   try:
      # convert r from string to list
      thickness_factor=thickness_factors[thickness.lower()]
   except KeyError:
      print("Please enter either 'thin', 'medium', or 'thick'")
      continue
   else:
      break

total_dough_weight=baking_tray_surface*thickness_factor*n_trays
recipe=percentages*total_dough_weight

print(f'Ingredients for {n_trays} {thickness} pizza (g):')
print(percentages*total_dough_weight)

preparation=f"Directions:\n Make a dough with all of the flour ({recipe['flour']:.1f} g) and the autolisi water ({recipe['autolisi water']:.1f} g). Use a planetary mixer with its kneading hook at speed n1 for ~5 min. Then stop the mixer and leave the dough to rest for 20 min, covered with a plastic film.\n Restart the mixer at 1st speed adding all the yeast ({recipe['yeast']:.1f} g) and gradually about half of the dough water ({recipe['dough water']/2:.0f} g). Keep going for 7 min, then increase the speed to 2 for additional 5 min.\n When increasing to second speed add the salt ({recipe['salt']:.1f} g) and then the remaining water ({recipe['dough water']/2:.0f} g) until complete absorbtion. Finally, add the olive oil to the mix ({recipe['olive oil']/2:.0f} g). At the end of this kneading phase the dough will be smooth and strung.\n \n Once you're done extract the dough with wet hands and place it in a big oiled bowl. Fold the dough to give some strength (check some youtube video if you don't know what this is). Put the dough to rest in the fridge (4°C) for 8 to 24 h (the longer the better). \n \n"

if n_trays>1:
   mass_per_tray=total_dough_weight/n_trays
   preparation+=f"We now cut the dough in {n_trays} parts, preferably inside the bowl in order not to deflate it. The mass of each part will have to be {mass_per_tray:.1f} g. "

preparation+=f"We fold again the dough and place it in hermetic container(s), covered in semolina, where we'll leave it to grow at room temperature for 2.5-3 h.\n \n In order to spread the dough let's prepare a generous semolina layer on the table, then let's pull out the dough from the container with a spatula, put on the table and follow these steps: \n 1 Sprinkle the top with some semolina \n 2 'close' the dough's border by pressing with your fingers throughout the perimeter \n 3 gently spread the dough in the central part, starting from the top to the bottom and viceversa \n 4 flip the dough and repeat the steps above \n 5 when the dough is slightly smaller than the tray, lift it, lay it on your forearm and gently shake it to remove the excess semolina \n 6 lay the dough on the oiled tray and press the dough with your fingers in order to spread it trough the entire tray.\n \n Season the pizza before baking. Two simple preparations are 'pizza bianca' and 'pizza rossa'.\n For pizza bianca use olive oil and some coarse salt. Stir everything and then spread on the pizza dough.\n For pizza rossa put in a bowl some tomato souce, olive oil, some salt, oregano and a crushed garlic clove.\n\n In order to cook preheat your home oven to maximum temperature (ideally 290-300°C) and cook for 10 minutes (or longer if lower temperature) laying the tray as low as possible in the oven."

print(preparation)