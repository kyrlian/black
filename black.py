# kyrlian 20231114

import streamlit
import random
from PIL import Image, ImageColor
from colorsys import rgb_to_hsv, hsv_to_rgb
import numpy as np

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
    (h_base,s_base,v_base)=rgb_to_hsv(r_base,g_base,b_base)#1,1,256
    streamlit.write(f"h:{h_base}, s:{s_base}, v:{v_base}")

    streamlit.write("Row variance")
    hue_var_row = streamlit.slider("Row hue variance",0.0,1.0)
    sat_var_row = streamlit.slider("Row saturation variance",0.0,1.0)
    value_var_row = streamlit.slider("Row value variance",0,255)

    streamlit.write("Column variance")
    hue_var_col = streamlit.slider("Column hue variance",0.0,1.0)
    sat_var_col = streamlit.slider("Column saturation variance",0.0,1.0)
    value_var_col = streamlit.slider("Column value variance",0,255)
    
    seed = streamlit.text_input("seed", "42")

def bind(x,min,max):
    if x < min:
        return min
    elif x > max:
        return max
    return x

def get(grid,i,j):
    return grid[bind(j,0,nb_h-1)][bind(i,0,nb_w-1)]

def genrow(h_row,s_row,v_row):
    row=[]
    for i in range(nb_w):
        h_col =  bind( h_row + (random.random()-.5)*hue_var_col, 0, 1)
        s_col =  bind( s_row + (random.random()-.5)*sat_var_col, 0, 1)
        v_col =  bind( v_row + (random.random()-.5)*value_var_col, 0, 255)
        # random color
        (r_col,g_col,b_col)=hsv_to_rgb(h_col,s_col,v_col)
        row.append( (int(r_col),int(g_col),int(b_col)))
    return row

# init image grid
def initgrid():
    grid = []
    for j in range(nb_h):
        h_row = bind( h_base + (random.random()-.5)*hue_var_row, 0, 1)
        s_row =  bind( s_base + (random.random()-.5)*sat_var_row, 0, 1)
        v_row =  bind( v_base + (random.random()-.5)*value_var_row, 0, 255)
        grid.append(genrow(h_row,s_row,v_row))
    return grid

def transform(grid,fn,nb):
    basegrid=grid
    for n in range(nb):
        newgrid=[]
        for j in range(nb_h):
            row=[]
            for i in range(nb_w):
                newcolor = fn(basegrid,i,j)
                row.append(newcolor)
            newgrid.append(row)
        basegrid=newgrid
    return newgrid

def fire(grid,i,j):
    if j < nb_h-1:
        (r,g,b) = (0,0,0)
        for s in [-1,0,1]:
            (tr,tg,tb) = get(grid,i+s,j+1)
            r += tr
            g += tg
            b += tb
        return (int(r/3),int(g/3),int(b/3))
    else:
        return get(grid,i,j)
        # return (255,random.randint(0,255),0)

# create PIL image
def drawimg(grid):
    img = Image.new('RGB', (img_w, img_h), color='black')
    # draw the squares from the grid
    for j in range(nb_h):
        for i in range(nb_w):
            color=grid[j][i]
            img.paste(Image.new('RGB', (px_w, px_h), color=color), (i*px_w, j*px_h))
    # convert PIL image to Streamlit image and display
    streamlit_image = streamlit.image(img)

drawimg(transform(initgrid(),fire,10))
drawimg(initgrid())