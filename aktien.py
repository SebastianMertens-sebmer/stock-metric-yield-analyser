# -*- coding: utf-8 -*-

from app.soft import *

# set c to False or True in soft.py
#
#
# if c is True
# the programm will start a interface
#
# if c is False
# the programm will assume aktien.csv is in path .app
#


stop()
link_generator()
stockanalysis(
    analysis_stockreturn=True,
    analysis_kgv=True,
    analysis_gewinnwachstum=True,
    analysis_divineuro=True,
    analysis_divinprozent=True,
)
output(c)
