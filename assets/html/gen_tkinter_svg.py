"""Licence :  Julien Tayon (2018)
If you find me a job in GIS or BigData I will change this license to a full
2 clauses BSD

Licence proprietaire sur un fichier a code source ouvert
ca me laissera le plaisir de poursuivre ceux qui le reutilisent sans mon accord

Proprietary licence with opened source. This a bait for all the newbies
that copy paste from the internet without taking attention of the licenses.


This code is BSD licensed only for :
    Wikimedia
    Wikipedia
    all the BSD projects
    Ligue des Droits de L'Homme
    Public highschools as long it is not reused out of the schools usage

PS bug probable autour du seek/write du aux IO de windows, symptome en tete magane autour de la balise svg/ViewBox
"""
### STDLIB ONLY
from sys import argv
from csv import DictReader
from sys import exit
from json import loads, dumps
from functools import reduce
from time import sleep
from matplotlib import pyplot as plt

if len(argv) < 1:
    print("""Generateur de carte SVG depuis donnees INSEE
Arg1 : donnees issue de https://data.opendatasoft.com/explore/dataset/code-postal-code-insee-2015@public/
""")
    exit(0)

import csv
from archery.bow import Daikyu as mdict, ExpDict as edict
filename = argv[1]
f = open(filename, encoding="utf8")
csv = DictReader(f, delimiter=";")

initial = "Code INSEE;Code Postal;Commune;Département;Région;Statut;Altitude Moyenne;Superficie;Population;geo_point_2d;ID Geofla;Code Commune;Code Canton;Code Arrondissement;Code Département;Code Région".split(";")

dest = "insee;code_postal;commune;departement;region;statut;altitude;superficie;population;geo_point_2d;geo_flaid;code_commune;code_canton;code_arrondissement;code_departement;code_region".split(";")

translate = { s:d for s,d in zip(initial, dest) }




minc = lambda a,b: complex(min(a.real, b.real), min(b.imag, a.imag))
maxc = lambda a,b: complex(max(a.real, b.real), max(b.imag, a.imag))
FACTOR = 100

dec="\n" + " "*4 * 3
decp="\n" + " "*4 * 4

cmap=plt.get_cmap(len(argv) >= 3 and argv[3] or "magma")
maxd=0
MARKER = object()
upper = lower = MARKER

import collections

def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

for l in csv:
    if l["Code Département"] in { "96", "97" }:
        continue
    coord = loads(l["geo_shape"])["coordinates"]
    for i,polygon in enumerate(coord):
        try:
            coords= list(map(lambda x:complex(*x) * FACTOR, polygon))
        except TypeError:
            ### Lol Multipolygon
            coords= list(map(lambda x:complex(*x) * FACTOR, polygon[0]))
        if lower is MARKER:
            lower = upper = coords[0]
        lower = minc(reduce(minc, coords), lower)
        upper = maxc(reduce(maxc, coords), upper)

boundary = dict( ymin = lower.imag, xmin=lower.real, width = (upper - lower).real, height=(upper - lower).imag)
print( boundary)
print(lower)
print(upper)

print("done")
from tkinter import *
master = Tk()

w = Canvas(master, 
           width=int((upper - lower).real) *40,
           height=int((upper - lower).imag) * 40,
           )

f = open(filename, encoding="utf8")
from pdb import set_trace
csv = DictReader(f, delimiter=";")
w.pack()
for j,l in enumerate(csv):
    coord = loads(l["geo_shape"])["coordinates"]
    coords=[]
    if l["Code Département"] in { "96", "97"}:
        continue
    for i,polygon in enumerate(coord):
        try:
            coords= list(map(lambda x:(complex(*x) * FACTOR) - lower, polygon ))
        except TypeError:
            ### Lol Multipolygon
            coords= list(map(lambda x:(complex(*x) * FACTOR) -lower, polygon[0]))
    polygon = list(flatten([ [int(pt.real), int(pt.imag)] for pt in coords ]))

    w.create_polygon(polygon, fill="#0000" + l["Code Département"])
w.update()
w.postscript(file="~/file_name.ps", colormode='color')
mainloop()
