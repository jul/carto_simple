===================
Cartographie simple
===================

Ce micro projet est constitué de 2 composantes :

`Un code «GoodEnough» <./gen_map_v2.2.py>`_ (© Joueur du Grenier) pour tracer des cartes
et une `présentation narrative <./carto.rst>`_)

Ce projet une introduction à la cartographie qui a vocation à être enrichie par ceux et ceussent qui veulent.


Gen_map
=======

Code de démonstration (ne gérant correctement ni les polygons, ni les 
multi polygons) permettant de tracer des cartes de la France à partir
des données de correspondances INSEE

Dépendances (à réduire) dans *requirements.gen_map.txt*

Dépendance de données

https://public.opendatasoft.com/explore/dataset/correspondance-code-insee-code-postal/


Prendre le fichier CSV

carto.rst
=========

Le makefile sert à le générer sous forme html et si j'utilise gh-pages elle devrait être `ici <./hover/>`_
Faut pas que j'ai oublié de faire::

   make with_notes #pour avoir la version avec les notes

ou pour la version de présentation::

   make wo_notes # la version à présenter en conf

Dépendances (à réduire) dans *requirements.txt* installable dans un virtualenv python avec::

   pip install -r requirements.txt

.. TODO::
   rajouter un make pdf ou latex dans le makefile


