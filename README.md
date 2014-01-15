translation-cloud
=================

Visualizing word translations as clouds.
https://github.com/alvations/translation-cloud

The translation-cloud provides a word-cloud visualization of a
source words and its possible translations given a parallel corpus
and an optional list of possible translations.

Dependencies
============
The tcloud.py script requires Pillow, a friendly fork of Python Imaging Library.
(see http://pillow.readthedocs.org/en/latest/installation.html)

Pillow install for Debian/Ubuntu:
```
 $ sudo apt-get install python-pip python-dev build-essential 
 $ sudo apt-get pip pillow
```

Usage
======

You will need 2 seperate files as input for the parallel corpus.
and a wordlist in .csv format where the first column is the 
source word that you are interested in and the follwing columns are
possible translations of that source word.
```
 $ wget https://github.com/alvations/translation-cloud
 $ unzip translation-cloud-master.zip
 $ cd translation-cloud-master
 $ python tcloud.py galechurch/ntumc.eng galechurch/ntumc.jpn wordlist.txt
```

