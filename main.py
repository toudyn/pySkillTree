# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 13:45:11 2024

@author: funky
"""
import datetime
import drawsvg as dw
from skilltree.SkillTree import SkillTree

st = SkillTree('test.csv')


# Create the SVG drawing of the skill tree and save it
drawing = st.render()
dt = datetime.datetime.now().isoformat().split('.')[0].replace(':','')
drawing.save_svg(f'diagrams/skills_{dt}.svg')

