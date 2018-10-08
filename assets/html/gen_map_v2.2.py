#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""Licence :  Julien Tayon (2018) WTFPL 2.0

Générateur de carte méthodologie "GoodEnough" depuis les données de communnes INSEE

Argument 1 : le CSV avec les données à jour
Argument 2 : le nom de la carte HTML en sortie
Argument 3 (optionnel) le gradient de couleur à utiliser
Argumnet 4 (cheat code) pour sortir du nawakolor par défaut

"""
### STDLIB ONLY
from sys import argv
from csv import DictReader
from archery.bow import Daikyu as mdict, ExpDict as edict

from sys import exit
from json import loads, dumps
from functools import reduce
from time import sleep
from matplotlib import pyplot as plt

if len(argv) < 2:
    print(__doc__)
    exit(0)

import csv
#next(csvr, None)
from archery.bow import Daikyu as mdict, ExpDict as edict
#color = brutal = mdict({ k:float(v) for k,v in csvr })
#color= mdict({ 
#            e : i for i, d in enumerate(
#                reduce(
#                    mdict.__add__,
#                    (mdict({v:(k,)}) for k,v in sorted(
#                        edict(color), key =lambda e:e[1]
#                    ))
#                ).values()) for e in d 
#        })
#color /= max(color.values())
filename = argv[1]
map_name = len(argv) > 2 and argv[2] or "carte_insee_v2.html"

out = open(map_name, "w" )
f = open(filename)
csv = DictReader(f, delimiter=";")

initial = "Code INSEE;Code Postal;Commune;Département;Région;Statut;Altitude Moyenne;Superficie;Population;geo_point_2d;ID Geofla;Code Commune;Code Canton;Code Arrondissement;Code Département;Code Région".split(";")

dest = "insee;code_postal;commune;departement;region;statut;altitude;superficie;population;geo_point_2d;geo_flaid;code_commune;code_canton;code_arrondissement;code_departement;code_region".split(";")

translate = { s:d for s,d in zip(initial, dest) }

TEMPLATE_BEGIN_1 = """
<html>
<header>
<script
			  src="https://code.jquery.com/jquery-3.3.1.slim.js"
			  integrity="sha256-fNXJFIlca05BIO2Y5zh1xrShK3ME+/lYZ0j+ChxX2DA="
			  crossorigin="anonymous"></script>
    
    <script>
$(document).ready(function(){
    $( "polygon" ).hover(function() {

           for( prop of [ "commune", "population", "altitude" ] ) {
           var val = $(this.attributes[prop]).val();
           $("#" + prop).html("" + val);
           }
           //$("#population").html(this.attributes["population"]);
           
  });  
});    </script>
    <style>
        polygon {
            stroke:rgba(60,60,60,.4);
            stroke-width:1;
        }
        polygon:hover {
            stroke:yellow;
            stroke-width:2;
            z-index:2;
filter: drop-shadow( -8px -8px 5px #333 );
        }
        #status {
            position:fixed;
            bottom:0;
            width:60em;
            height:3em;
            color:black;
            background-color:white;
            font-size:20px;
            }
        body{ background-color: #ccc; }
    </style>
</header>
<body>
    <table id=status style='z-index:1000' >
        <tr>
            <td style="width:50%" >Commune</td>
            <td id=commune >&nbsp;</td>
        </tr>
        <tr>
        <td 
            style="background-color:#ccc"
            >Population</td>
        <td 
            style="background-color:#ccc"
            id=population >&nbsp;</td>
        </tr>
        <tr>
        <td >Altitude</td>
        <td id=altitude >&nbsp;</td>
        </tr>
    </table>
<center>
    <svg 
    """

TEMPLATE_BEGIN_2 ="\n" + (" " * 160) + """
            preserveAspectRatio="xMidYMid meet"
            style='position:relative'
        >
        <g fill="red" stroke="blue" stroke-width="0" >

"""
TEMPLATE_BEGIN = TEMPLATE_BEGIN_1 + TEMPLATE_BEGIN_2

TEMPLATE_END = """
        </g>
        </svg>
        <center>
</body>
</html>
"""

minc = lambda a,b: complex(min(a.real, b.real), min(b.imag, a.imag))
maxc = lambda a,b: complex(max(a.real, b.real), max(b.imag, a.imag))
FACTOR = 800
upper = lower = complex(4.6667,43.8472) * FACTOR

dec="\n" + " "*4 * 3
decp="\n" + " "*4 * 4
out.write(TEMPLATE_BEGIN )

cmap=plt.get_cmap(len(argv) >= 3 and argv[3] or "magma")
maxd=0

def rounded_dict(a_dict, round_by=0):
    maxv = max(a_dict.values())
    return mdict({
        k : round(v, round_by) for k,v in a_dict.items() 
    }) / maxv


        
def ranged_dict(a_dict, level=50):
    val_to_rank = { val:rank for rank, val in  enumerate(sorted(set(a_dict.values()))) }
    scale=int(len(val_to_rank)/level)
    val_to_rank = { val:int(rank/scale) for val, rank in val_to_rank.items()}
    return mdict({ k:val_to_rank[v] for k,v in a_dict.items() })/ level
color = mdict()

def ignore_line(l):
    return l["Code Département"] not in { "59", "02", "60", "95", "80", "62" }

for l in csv:
    if ignore_line(l):
        #carte france metropolitaine
        # pour les DOMTOMs, faite l'oppose
        continue
    color[l["Code INSEE"]]= float(l.get("Population", 1.0))

no_corr = len(argv) > 4
print len(argv)
if no_corr:
    color /= max(color.values())
    print "linear"

else:
    #color = rounded_dict(color,-0)
    color = ranged_dict(color)
    print  "non linear"

f = open(filename)
csv = DictReader(f, delimiter=";")
for l in csv:
    if ignore_line(l):
        #carte france metropolitaine
        # pour les DOMTOMs, faite l'oppose
        continue
    coord = loads(l["geo_shape"])["coordinates"]

    for i,polygon in enumerate(coord):
        try:
            coords= list(map(lambda x:complex(*x) * FACTOR, polygon))
        except TypeError:
            ### Lol Multipolygon
            coords= list(map(lambda x:complex(*x) * FACTOR, polygon[0]))

        lower = minc(reduce(minc, coords), lower)
        upper = maxc(reduce(maxc, coords), upper)
        data = decp.join( ["%s=\"%s\"" % (translate[k], l[k]) for k in initial ])
        data += decp 
        #just for fun
        data += decp + "style='fill:rgb(%d, %d, %d)'" % tuple(list([ int(x*256) for x in cmap(color[l["Code INSEE"]])])[:3])

        points = " ".join(["%.4f,%.4f" % (c.real,c.imag) for c in coords ])
        el = """%s<polygon
               id="%s_%d"
                points="%s"
                %s />""" % (dec, color[l["Code INSEE"]], i, points, data)
        out.write(el)
print(maxd)
boundary = dict( ymin = lower.imag, xmin=lower.real, width = (upper - lower).real, height=(upper - lower).imag)
out.write(TEMPLATE_END)
out.close()

out = open(map_name, "rb+")
out.seek(len(bytearray( TEMPLATE_BEGIN_1,encoding="utf8")))
tow = """            transform="scale(1,-1)"
            ViewBox="%(xmin)f %(ymin)f %(width)f %(height)f"\n""" % boundary
out.write(bytearray(tow,encoding="utf8"))

out.close()
