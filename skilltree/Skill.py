# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 11:32:18 2024

@author: funky
"""

import drawsvg as dw
import math


class Skill:
    """
    Class to handle the drawing of an SVG for a skill.
    """
    def __init__(self, svg, name, position):
        self.svg = svg
        self.name = name
        self.pos_x = position[0]
        self.pos_y = position[1]
        self.initialised = False
        
        # Hard coded params
        self.outer_radius = 30
        self.inner_radius = 22
        self.outer_text_size = 8
        self.inner_text_size = 12
        
    
    def initialise(self, info_dict):
        """
        Does some validation of parameters passed, then sets them if fine.
        """
        status = info_dict['status']
        level = info_dict['level']
        
        allowed_statuses = ['locked', 'unlocked', 'completed']
        if status not in allowed_statuses:
            print(f'Status must be one of {allowed_statuses}')
            return
        
        if level < 0:
            print('Level provided must be a positive integer')
            return
        
        if status in ['locked', 'unlocked'] and level > 0:
            print('The level of a skill cannot be greater than 0 if it is not completed')
            return
        
        self.upper_text = info_dict['upper_text']
        self.lower_text = info_dict['lower_text']
        self.status = status
        self.color = info_dict['color']
        self.complete_inner_text_color = info_dict['complete_inner_text_color']
        self.unlocked_outer_text_color = info_dict['unlocked_outer_text_color']
        self.background_color = info_dict['background_color']
        self.locked_color = info_dict['locked_color']
        self.incomplete_inner_text_color = info_dict['incomplete_inner_text_color']
        self.locked_outer_text_color = info_dict['locked_outer_text_color']
        self.level = level
        
        self.initialised = True
    
    def draw(self):
        if self.initialised == False:
            print('Skill is not yet initialised, cannot draw it')
            return
        
        self.draw_base_shape()
        self.write_center_text()
        self.write_upper_text()
        self.write_lower_text()
        self.draw_stars()
    
    def draw_base_shape(self):
        # Draw base circle
        if self.status == 'locked':
            shape_color = self.locked_color
        else:
            shape_color = self.color
        
        # print(self.status, shape_color)
        
        circle = dw.Circle(self.pos_x, self.pos_y, self.outer_radius, fill=shape_color)
        self.svg.append(circle)
        
        # Add center for donut if not completed
        if self.status in ['locked', 'unlocked']:
            inner_circle = dw.Circle(self.pos_x, self.pos_y, self.inner_radius, fill=self.background_color)
            self.svg.append(inner_circle)
    
    def write_center_text(self):
        text = self.name.replace('|', '\n')
        lines = text.count('\n') + 1
        
        if self.status == 'complete':
            text_color = self.complete_inner_text_color
        else:
            text_color = self.incomplete_inner_text_color
        
        x = self.pos_x
        y = self.pos_y
            
        self.svg.append(dw.Text(text, x=x, y=y, font_size=self.inner_text_size, text_anchor="middle", 
                       alignment_baseline="middle", fill=text_color))
    
    def write_outer_text(self, position, text, color):
        """
        Goal is to write text along the the ring, at the top or bottom,
        curving around the circle, starting at the top/bottom and autoscaling.
        """
        if self.status == 'locked':
            text_color = self.locked_outer_text_color
        else:
            text_color = self.unlocked_outer_text_color

        num_chars = len(text)

        # Set the maximum angle between characters
        max_angle = 8  # Maximum angle per character in degrees

        max_angle_radians = math.radians(max_angle)  # Convert max angle to radians
        # Calculate the total angle needed to fit the text, max 180 degrees (π radians)
        total_angle_needed = min(math.radians(180), max_angle_radians * num_chars)

        # If the text is short, adjust the angle per character to fit within the max angle
        angle_step = total_angle_needed / num_chars if num_chars > 1 else 0  # If only one character, no angle spread

        # Adjust for the center
        if position == 'top':
            position_angle = 270
        elif position == 'bottom':
            position_angle = 90
            text = text[::-1]
        else:
            print(f'Position must be top or bottom, not: {position}')
            return
        start_angle = math.radians(position_angle) - (total_angle_needed / 2)  # Start at the top and spread outwards

        for i, char in enumerate(text):
            # Calculate the angle for each character along the top half
            angle = start_angle + i * angle_step
            # Calculate x, y positions for the character along the outer edge
            x = self.pos_x + (self.outer_radius+self.inner_radius)/2 * .95 * math.cos(angle)
            y = self.pos_y + (self.outer_radius+self.inner_radius)/2 * .95 * math.sin(angle)

            # Calculate the rotation angle for the text (tangent to the circle)
            if position == 'top':
                rotation_angle = angle + math.pi / 2  # Rotate by 90 degrees to align text perpendicular to radius
            elif position == 'bottom':
                rotation_angle = angle - math.pi / 2
                y += self.outer_text_size * 0.2

            # Add text element at calculated position with rotation and color
            text = dw.Text(char,
                           x=x,
                           y=y,
                           font_size=self.outer_text_size,
                           text_anchor="middle", 
                           alignment_baseline="middle",
                           transform=f"rotate({math.degrees(rotation_angle)}, {x}, {y})", 
                           fill=text_color)
            self.svg.append(text)

    def write_upper_text(self):
        """
        Goal is to write text along the top, curving around the circle, starting at the top and autoscaling.
        """
        if self.status == 'locked':
            text_color = self.locked_outer_text_color
        else:
            text_color = self.unlocked_outer_text_color

        self.write_outer_text('top', self.upper_text, text_color)

    def write_lower_text(self):
        """
        Goal is to write text along the top, curving around the circle, starting at the top and autoscaling.
        """
        if self.status == 'locked':
            text_color = self.locked_outer_text_color
        else:
            text_color = self.unlocked_outer_text_color

        self.write_outer_text('bottom', self.lower_text, text_color)
    
    def draw_stars(self):
        """
        Draws up to 5 stars above the center text to represent the skill's level.
        The stars will follow the shape of the donut, located above the text.
        Bronze stars for levels 1-4, Silver stars for level 5.
        """
        star_radius = 3  # Radius of each star
        star_distance = self.inner_radius * .8 # Trying to get it just inside the donut
        bronze_color = '#cd7f32'
        silver_color = '#c0c0c0'
        gold_color = '#ffd700'
        
        level_to_show = min(self.level, 15)
               
        # Determine how many stars get drawn and what their colors are
        if level_to_show < 6:
            # up to 5 bronze stars
            num_stars = level_to_show
            color = bronze_color
        elif 5 < level_to_show < 11:
            # up to 5 silver stars
            num_stars = level_to_show - 5
            color = silver_color
        elif 10 < level_to_show <= 15:
            # up to 5 old stars
            num_stars = level_to_show - 10
            color = gold_color
        else:
            print('Something happened in calculating number of stars to draw')
        
        angle_separation = 25
        total_angle_span = (num_stars - 1) * angle_separation
        start_angle = math.radians(270) - math.radians(total_angle_span / 2)
        
        for i in range(num_stars):
                        
            # Calculate the angle for the current star
            angle = start_angle + math.radians(i * angle_separation)
    
            # Calculate the (x, y) position for each star
            x = self.pos_x + star_distance * math.cos(angle)
            y = self.pos_y + star_distance * math.sin(angle)
            
            # Draw the star, which is actually just a circle
            star = dw.Circle(x, y, star_radius, fill=color)
            self.svg.append(star)


# width, height = 400, 400
# svg = dw.Drawing(width, height)

# bkg_col = '#394b5a'
# lok_col = '#b5bdc4'
# incomplete_i_txt_col = '#b5bdc4'
# lok_o_txt_col = '#ffffff'
# complete_i_txt_col = '#ffffff'
# unlok_o_txt_col = '#ffffff'


# # """
# locked_skill = Skill(svg, 'locked', bkg_col, lok_col, incomplete_i_txt_col, lok_o_txt_col)
# locked_skill.initialise([width//2, height//2], 'locked '*3, 'locked '*4, 'locked', 'red', complete_i_txt_col, unlok_o_txt_col, 0)
# locked_skill.draw()
# # """
# """
# unlocked_skill = Skill(svg, 'unlocked', bkg_col, lok_col, incomplete_i_txt_col, lok_o_txt_col)
# unlocked_skill.initialise([width//2, height//2], 'unlocked '*3, 'unlocked', 'unlocked', 'red', complete_i_txt_col, unlok_o_txt_col, 0)
# unlocked_skill.draw()
# # """
# """
# completed_skill = Skill(svg, 'completed', bkg_col, lok_col, incomplete_i_txt_col, lok_o_txt_col)
# completed_skill.initialise([width//2, height//2], 'completed '*3, 'completed', 'completed', 'red', complete_i_txt_col, unlok_o_txt_col, 0)
# completed_skill.draw()
# # """