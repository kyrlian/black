# kyrlian 20231114

import streamlit
import random
from PIL import Image, ImageColor
import colorsys
import numpy as np

rgb_to_hsv=np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb=np.vectorize(colorsys.hsv_to_rgb)

streamlit.title("Black")

# streamlit side pane
with streamlit.sidebar:
    streamlit.write("Image size")
    px_w = streamlit.slider("pixel width",1,100,40)
    px_h = streamlit.slider("pixel height",1,100,40)
    nb_w = streamlit.slider("number of columns",1,100,16)
    nb_h = streamlit.slider("number of rows",1,100,16)
    img_w = px_w * nb_w
    img_h = px_h * nb_h
    basecolor = streamlit.color_picker('Base color', '#000000')
    (r_base,g_base,b_base)=ImageColor.getrgb(basecolor)
    (h_base,s_base,l_base)=rgb_to_hsv(r_base,g_base,b_base)

    streamlit.write("Row variance")
    hue_var_row = streamlit.slider("Row hue variance",0,360,10)
    sat_var_row = streamlit.slider("Row saturation variance",0,100,10)
    light_var_row = streamlit.slider("Row lightness variance",0,100,10)

    streamlit.write("Column variance")
    hue_var_col = streamlit.slider("Column hue variance",0,360,10)
    sat_var_col = streamlit.slider("Column saturation variance",0,100,10)
    light_var_col = streamlit.slider("Column lightness variance",0,100,10)
    
    seed = streamlit.text_input("seed", "42")

def bind(x,min,max):
    if x < min:
        return min
    elif x > max:
        return max
    return x

# init image grid
grid = []
for j in range(nb_h):
    row=[]
    h_row = bind( h_base + random.randint(-hue_var_row,hue_var_row), 0, 360)
    s_row =  bind( s_base + random.randint(-sat_var_row,sat_var_row), 0, 100)
    l_row =  bind( l_base + random.randint(-light_var_row,light_var_row), 0, 100)
    for i in range(nb_w):
        h_col =  bind( h_row + random.randint(-hue_var_col,hue_var_col), 0, 360)
        s_col =  bind( s_row + random.randint(-sat_var_col,sat_var_col), 0, 100)
        l_col =  bind( l_row + random.randint(-light_var_col,light_var_col), 0, 100)
        # random color
        (r_col,g_col,b_col)=ImageColor.getrgb(f"hsl({h_col},{s_col}%,{l_col}%)")
        color =  (r_col,g_col,b_col)
        row.append(color)
    grid.append(row)

# create PIL image
img = Image.new('RGB', (img_w, img_h), color='black')

# Add the squares
for j in range(nb_h):
    row  = grid[j]
    for i in range(nb_w):
        color=row[i]
        img.paste(Image.new('RGB', (px_w, px_h), color=color), (i*px_w, j*px_h))


# convert PIL image to Streamlit image and display
streamlit_image = streamlit.image(img)