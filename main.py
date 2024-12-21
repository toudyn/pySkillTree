# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 13:45:11 2024

@author: funky
"""
import drawsvg as dw
from skilltree.SkillTree import SkillTree

st = SkillTree('test.csv')


# Create the SVG drawing of the skill tree and save it
drawing = st.render()
drawing.save_svg('test.svg')

