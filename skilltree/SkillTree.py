# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:04:06 2024

@author: funky
"""

from skilltree.Skill import Skill
import drawsvg as dw
import csv


class SkillTree:
    def __init__(self, skills_file):
        self.csv_file = skills_file
        self.skills = self.load_skills_from_csv()
        self.dependency_map = {skill['name']: skill['dependency'] for skill in self.skills}
        
        self.background_color = '#003153'
    
    def load_skills_from_csv(self):
        skills = []
        try:
            with open(self.csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    skill = {
                        "name": row['name'],
                        "x": int(row['x']),
                        "y": int(row['y']),
                        "dependency": row['dependency'],
                        "upper_text": row['upper_text'],
                        "lower_text": row['lower_text'],
                        "status": row['status'],
                        "color": row['color'],
                        "complete_inner_text_color": row['complete_inner_text_color'],
                        "unlocked_outer_text_color": row['unlocked_outer_text_color'],
                        "background_color": row['background_color'],
                        "locked_color": row['locked_color'],
                        "incomplete_inner_text_color": row['incomplete_inner_text_color'],
                        "locked_outer_text_color": row['locked_outer_text_color'],
                        "level": int(row['level']),
                        'dependency_color': row['dependency_color']}
                    skills.append(skill)
        except FileNotFoundError:
            print("No CSV file found")
            return
        return skills

    def render(self):
        # Create the drawing object
        size = 2400
        drawing = dw.Drawing(size, size, origin='top-left')
        drawing.append(dw.Rectangle(0, 0, size, size, fill=self.background_color))
 
        # print(self.skills)
        
        # Draw dependencies
        for skill in self.skills:
            name = skill['name']
            x, y = skill.get('x', 100), skill.get('y', 100)  # Default to (100, 100) if not set
            # print(skill)
            if skill['status'] == 'locked':
                dependency_color = skill.get('locked_color', 'grey')
            else:
                dependency_color = skill.get('dependency_color', '#ffffff')
            # print(dependency_color)
            # Draw lines to dependencies
            dependency = skill.get('dependency', None)
            if dependency:
                dependency_skill = next(s for s in self.skills if s['name'] == dependency)
                dep_x, dep_y = dependency_skill.get('x', 100), dependency_skill.get('y', 100)

                # Draw a line between the skill and its dependency
                drawing.append(dw.Line(x, y, dep_x, dep_y, stroke=dependency_color, stroke_width=15))
        
        # Draw actual skill nodes on top
        for skill in self.skills:
            name = skill['name']
            x, y = skill.get('x', 100), skill.get('y', 100)  # Default to (100, 100) if not set
            
            # Create a Skill instance and draw it
            skill_instance = Skill(drawing, name, [x, y])
            
            info_dict = {'upper_text': skill.get('upper_text'),
                         'lower_text': skill.get('lower_text'),
                         'status': skill.get('status'),
                         'color': skill.get('color'),
                         'complete_inner_text_color': skill.get('complete_inner_text_color'),
                         'unlocked_outer_text_color': skill.get('unlocked_outer_text_color'),
                         'background_color': skill.get('background_color'),
                         'locked_color': skill.get('locked_color'),
                         'incomplete_inner_text_color': skill.get('incomplete_inner_text_color'),
                         'locked_outer_text_color': skill.get('locked_outer_text_color'),
                         'level': skill.get('level')}

            skill_instance.initialise(info_dict)
            skill_instance.draw()

        return drawing
           