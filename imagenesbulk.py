'''
Created on 27 mar. 2021

@author: Patxi Juaristi
'''
from tkinter import Tk, Frame, Text, Scrollbar, Label, Button, filedialog, \
    PhotoImage, Radiobutton, IntVar, StringVar, Entry
from tkinter.constants import END

import requests
import os
import sys
from urllib.parse import urlparse
from threading import Thread

def resource_path(relative_path):
    """ To get resources path for creating the .exe with PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

raiz = Tk()
icono = PhotoImage(file = resource_path('imagenes.png'))
raiz.iconphoto(False, icono)
raiz.title("Bulk Image Downloader")

ancho= 600
alto = 500

miFrame=Frame(raiz, width=ancho, height=alto)
miFrame.pack()

nombreImg=StringVar()
directorioPath=StringVar()
tieneNombre=False

opcionesFrame=Frame(miFrame)
opcionesFrame.grid(row=0, column=0, columnspan=3, padx=20, pady=15, sticky='w')

def selec():
    global tieneNombre
    if(opcion.get()==2):
        nameKeywords.grid_forget()
        scrollVertK.grid_forget()
        kwLabel.grid_forget()
        tieneNombre = False
        nombreImgEntry.pack_forget()
        nombreImg.set('')
        nameKeywords.delete(1.0,"end")
    elif(opcion.get() == 3):
        nameKeywords.grid(row=2, column=4, sticky="w", padx=1, pady=5)
        scrollVertK.grid(row=2, column=5, sticky="nsew")
        kwLabel.grid(row=2, column=3, sticky="w", pady=10)
        nombreImgEntry.pack_forget()
        nombreImg.set('')
    else:
        nameKeywords.grid_forget()
        scrollVertK.grid_forget()
        kwLabel.grid_forget()
        tieneNombre = True
        nombreImgEntry.pack(side='left')
        nameKeywords.delete(1.0,"end")

opcion = IntVar()
opcion.set(2)

nombreLabel=Label(opcionesFrame, text="Expecific name: ", font=('Arial', 12 ))
nombreLabel.pack(side='left')

nombreImgEntry=Entry(opcionesFrame, textvariable=nombreImg, width=50, font=('Arial', 12 ))
nombreImgEntry.pack_forget()

named = Radiobutton(opcionesFrame, text="Yes", variable=opcion, value=1, command=selec, font=('Arial', 12 )).pack(side='left')
withoutname = Radiobutton(opcionesFrame, text="No", variable=opcion, value=2, command=selec, font=('Arial', 12 )).pack(side='left')
keywordsname = Radiobutton(opcionesFrame, text="Keywords", variable=opcion, value=3, command=selec, font=('Arial', 12 )).pack(side='left')

############

def establecerDirectorio():
    path = filedialog.askdirectory(initialdir="/", title="Select file")
    directorioPath.set(path)

folderFrame=Frame(miFrame)
folderFrame.grid(row=1, column=0, columnspan=5, padx=20, pady=15, sticky='w')

folderFrameLabel=Label(folderFrame, text="Output folder path: ", font=('Arial', 12 ))
folderFrameLabel.pack(side='left')

folderFrameEntry=Entry(folderFrame, textvariable=directorioPath, width=50, font=('Arial', 12 ))
folderFrameEntry.pack(side='left')

botonDir=Button(folderFrame, text="Folder", font=('Arial', 12 ), command=establecerDirectorio)
botonDir.pack(side='left')

#######

urlImagenes=Text(miFrame, width=63, height=10)
urlImagenes.grid(row=2, column=1, sticky="w", padx=1, pady=5)

scrollVert=Scrollbar(miFrame, command=urlImagenes.yview)
scrollVert.grid(row=2, column=2, sticky="nsew")

urlImagenes.config(yscrollcommand=scrollVert.set)

comentariosLabel=Label(miFrame, text="Image URL-s: ", font=('Arial', 12 ))
comentariosLabel.grid(row=2, column=0, sticky="w", padx=(10,0), pady=10)

#######

nameKeywords=Text(miFrame, width=60, height=10)
nameKeywords.grid_forget()

scrollVertK=Scrollbar(miFrame, command=nameKeywords.yview)
scrollVertK.grid_forget()

nameKeywords.config(yscrollcommand=scrollVertK.set)

kwLabel=Label(miFrame, text="Keyword list: ", font=('Arial', 12 ))
kwLabel.grid_forget()

####################################

resultadosText=Text(miFrame, width=63, height=10)
resultadosText.grid(row=3, column=1, sticky="w", padx=1, pady=5)

scrollVert2=Scrollbar(miFrame, command=resultadosText.yview)
scrollVert2.grid(row=3, column=2, sticky="nsew")

resultadosText.config(yscrollcommand=scrollVert2.set)

comentariosLabel2=Label(miFrame, text="Results: ", font=('Arial', 12 ))
comentariosLabel2.grid(row=3, column=0, sticky="w", padx=(10,0), pady=10)

####################################

def downloadWithName(urlsImagenes, nombre):
    i = 1
    for url in urlsImagenes:
            try:
                ficheroN = directorioPath.get() + '/' + nombre + '-' + str(i)+'.jpg'
                with open(ficheroN, 'wb') as f:
                    f.write(requests.get(url).content)
                resultadosText.insert(float(i), ficheroN + ' Downloaded OK\n')
                i = i + 1
            except:
                resultadosText.insert(float(i), 'Error\n')

def quitarTildes(s):
    replacements = (("á", "a"), ("é", "e"), ("í", "i"), ("ó", "o"), ("ú", "u"),)
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def getKeywordList(texto):
    texto = quitarTildes(texto.lower().replace(' ','-').replace('.',''))
    listaImagenes = texto.split('\n')
    
    return listaImagenes

def downloadFromKeywords(urlsImagenes):
    texto2 = nameKeywords.get("1.0", END)
    namessImagenes = getKeywordList(texto2)
    i = 1
    for url in urlsImagenes:
            try:
                ficheroN = directorioPath.get() + '/' + namessImagenes[i-1] +'.jpg'
                with open(ficheroN, 'wb') as f:
                    f.write(requests.get(url).content)
                resultadosText.insert(float(i), ficheroN + ' Downloaded OK\n')
                i = i + 1
            except:
                resultadosText.insert(float(i), 'Error\n')

def downloadWithoutName(urlsImagenes):
    i = 1
    for url in urlsImagenes:
            try:
                a = urlparse(url)
                nombre = os.path.basename(a.path)
                ficheroN = directorioPath.get() + '/' + nombre
                with open(ficheroN, 'wb') as f:
                    f.write(requests.get(url).content)
                resultadosText.insert(float(i), ficheroN + ' Downloaded OK\n')
                i = i + 1
            except:
                resultadosText.insert(float(i), 'Error\n')    

def descargarImagenes():
    texto = urlImagenes.get("1.0", END)
    urlsImagenes = texto.split()
    
    if(directorioPath.get() != ''):
        if(opcion.get()==2):
            Thread(target = downloadWithoutName, args=(urlsImagenes,)).start()
        elif(opcion.get() == 3):
            Thread(target = downloadFromKeywords, args=(urlsImagenes,)).start()
        else:
            Thread(target = downloadWithName, args=(urlsImagenes, nombreImg.get(),)).start()
    else:
        resultadosText.delete(1.0,"end")
        resultadosText.insert(1.0, 'Introduce the output folder path for the images')

botonBuscar=Button(raiz, text="Download", command=descargarImagenes, bg='red', fg='white', font=('Arial', 14 ))
botonBuscar.pack(pady=20)

raiz.mainloop()