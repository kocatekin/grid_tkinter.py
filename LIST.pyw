import tkinter as tk
from tkinter import *
import os
import math
import tkinter.messagebox
import PIL
from PIL import Image
import time
from random import randint
import sys


def resize_files(image_paths):
    for image in image_paths:
        try:
            imagex = Image.open(image)
        except:
            continue
        #new line to get rid of some errors
        imagex = imagex.convert('RGB')
        imagex.thumbnail((1170,2532), Image.LANCZOS)
        imagex.save(f"{image}")
    return image_paths

def delete_files(image_paths):
    for path in image_paths:
        os.remove(path)
    print("[INFO] all files are deleted")

def makeGrid(image_paths, gridSize, directory):
    output_path = directory + ".jpg"
    #images = [Image.open(path) for path in image_paths]
    images = []
    for path in image_paths:
        try:
            images.append(Image.open(path))
        except Exception:
            f = open("err.log","a")
            f.write(f"[ERR] {Exception}: something went wrong, we passed it")
            f.close()
            continue
    
    # adjust to max sizes no loss
    max_width = max(image.width for image in images)
    max_height = max(image.height for image in images)

    the_width = max_width
    the_height = max_height

    #margins
    width_margin = 0
    height_margin = 0

    numOfImages = len(images)
    gridHeight = (numOfImages // gridSize) + 1 if numOfImages % gridSize != 0 else (numOfImages // gridSize)

    combined_image = Image.new('RGB', ((the_width+width_margin)*gridSize,(the_height+height_margin)*gridHeight))
    #initials
    cur_width = 0
    cur_height = 0
    cnt = 0

    for image in images:
        new_image = Image.new('RGB', (the_width, the_height))
        if(cnt < gridSize):
            new_image.paste(image, (0,0))
            combined_image.paste(new_image, (cur_width, cur_height))
            cur_width += the_width
            cnt += 1
        else:
            new_image.paste(image, (0,0))
            cur_height += the_height + height_margin
            combined_image.paste(new_image, (0,cur_height))
            cnt = 1
            cur_width = the_width

    combined_image.save(output_path)
    delete_files(image_paths)
    print("done")





def dir_and_count(directory):
    dirs = list(filter(os.path.isdir, os.listdir(directory)))
    mydict = {}
    for dir in dirs:
        if len(os.listdir(dir)) != 0:
            mydict[f"{dir}"] = len(os.listdir(dir))
    
    return dict(sorted(mydict.items(), key=lambda x:x[1], reverse=True))


def refresh_listbox():
    #get the list
    listbox.delete(0,'end')
    result = dir_and_count(".")
    keysList = list(result.keys())
    for idx,key in enumerate(list(result.keys())):
        listbox.insert(idx, f"{key} - {result[key]}")
        listbox.pack()
    

def run():
    task = listbox.get('active')
    task = task.split(" - ")[0]
    print(task)
    dir = task
    #some work here
    image_paths = []
    for files in os.listdir(dir):
        if files.split(".")[-1] not in ["jpg","png","jpeg","tiff","webp","jfif"]:
            continue
        image_paths.append(os.path.join(dir,files))
    #print(image_paths)
    print("resizing images")
    resize_files(image_paths)
    print("trying to grid")
    makeGrid(image_paths, int(math.sqrt(len(image_paths))), dir)
    refresh_listbox()
    tk.messagebox.showinfo("showinfo", "done")
    return
    

def delete_empty_folders():
    empty_dirs = [file for file in os.listdir(".") if os.path.isdir(file) and len(os.listdir(file)) == 0]
    for dir in empty_dirs:
        os.rmdir(dir)
    refresh_listbox()
        
    
def runall():
    #get all elements in the list
    #for every element, run all
    mylist = listbox.get(0,END)
    names = list(map(lambda x:x.split(' - ')[0], mylist))
    for directory in names:
        image_paths = []
        for files in os.listdir(directory):
            if files.split(".")[-1] not in ["jpg","png","jpeg","tiff","webp","jfif"]:
                continue
            image_paths.append(os.path.join(directory,files))
        resize_files(image_paths)
        makeGrid(image_paths, int(math.sqrt(len(image_paths))), directory)
        image_paths = []
    print("all directories are done")
    tk.messagebox.showinfo("showinfo", "all dirs are done")
    
        


root = tk.Tk()
root.geometry('500x500')

btn_delete = tk.Button(root, text="Delete Empty", command=delete_empty_folders, width=15)
btn_delete.pack()

btn_refresh = tk.Button(root, text="Refresh", command=refresh_listbox, width=15)
btn_refresh.pack()

btn_run = tk.Button(root, text="Run", command=run, width=15)
btn_run.pack()

btn_makeall = tk.Button(root, text="Run all", command=runall, width=15)
btn_makeall.pack()


root.title("Make Grid")
listbox = tk.Listbox()
listbox.pack(side=LEFT, fill=BOTH)
listbox.config(width=150, height=200)


refresh_listbox() #fill in the listbox
listbox.pack()
root.mainloop()



