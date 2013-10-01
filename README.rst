==========================================================
 Création d'une page web simple pour un album photo
==========================================================

Le script ``album-creator.py`` génère des vignettes des images qui sont dans le dossier $FOLDER, puis construit une page web à partir de ``index_stub.html``


Pré-requis
==========
- python
- imagemagick

Pour tout installer, sur une distribution de type Debian/Ubuntu :

    sudo apt-get install python imagemagick

Utilisation
===========

    python album-creator.py $FOLDER $TITLE