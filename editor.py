# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:48:06 2024

@author: funky
"""

import csv
import tkinter as tk

class SkillEditor:
    def __init__(self, csv_file, grid_size=5):
        # Hard coded node radius
        self.radius = 15
        self.size = 800
        self.multiplier = 2
        
        self.csv_file = csv_file
        self.grid_size = grid_size
        self.skills = self.load_skills_from_csv()
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg="white")
        self.canvas.pack()
        self.draw_grid()  # Draw the grid for visual reference
        self.draw_skills()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)  # Detect drag motion
        self.root.mainloop()
        
       

    def load_skills_from_csv(self):
        skills = []
        try:
            with open(self.csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    skill = {
                        "name": row['name'],
                        "x": int(row['x'])/self.multiplier,
                        "y": int(row['y'])/self.multiplier,
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
                        "dependency_color": row['dependency_color']}
                    skills.append(skill)
        except FileNotFoundError:
            print("No CSV file found, starting with empty skill set.")
        return skills

    def draw_grid(self):
        """Draws a grid on the canvas for visual feedback."""
        width, height = self.canvas.winfo_width(), self.canvas.winfo_height()
        for x in range(0, width, self.grid_size):
            self.canvas.create_line(x, 0, x, height, fill="lightgray", dash=(2, 2))
        for y in range(0, height, self.grid_size):
            self.canvas.create_line(0, y, width, y, fill="lightgray", dash=(2, 2))

    def draw_skills(self):
        """Draws all skills as circles with text labels."""
        font_size = 8
        self.skill_circles = {}
        for skill in self.skills:
            x, y = skill['x'], skill['y']
            radius = self.radius
            circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="gray")
            text = self.canvas.create_text(x, y, text=skill['name'], fill="black", font=("Arial", font_size))
            self.skill_circles[skill['name']] = (circle, text)

    def on_click(self, event):
        """Handles clicking on skills to initiate drag."""
        for skill in self.skills:
            x, y = skill['x'], skill['y']
            radius = self.radius
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= radius ** 2:
                self.selected_skill = skill
                break

    def on_drag(self, event):
        """Handles dragging of the selected skill, snapping to the grid."""
        if hasattr(self, 'selected_skill'):
            # Snap the dragged position to the grid
            new_x = self.snap_to_grid(event.x)
            new_y = self.snap_to_grid(event.y)

            # Update the skill's position on the canvas
            self.selected_skill['x'] = new_x
            self.selected_skill['y'] = new_y
            circle, text = self.skill_circles[self.selected_skill['name']]
            self.canvas.coords(circle, new_x - self.radius, new_y - self.radius, new_x + self.radius, new_y + self.radius)
            self.canvas.coords(text, new_x, new_y)

            self.save_skills_to_csv()

    def snap_to_grid(self, value):
        """Snaps a coordinate value to the nearest grid multiple."""
        return round(value / self.grid_size) * self.grid_size

    def save_skills_to_csv(self):
        """Saves the updated skills with their new positions back to the CSV."""
        with open(self.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['name',
                          'x',
                          'y',
                          'dependency',
                          'upper_text',
                          'lower_text',
                          'status',
                          'color',
                          'complete_inner_text_color',
                          'unlocked_outer_text_color',
                          'background_color',
                          'locked_color',
                          'incomplete_inner_text_color',
                          'locked_outer_text_color',
                          'level',
                          'dependency_color']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for skill in self.skills:
                write_dict = {}
                for field in fieldnames:
                    if field in ['x', 'y']:
                        write_dict[field] = int(skill[field] * self.multiplier)
                    else:
                        write_dict[field] = skill[field]
                writer.writerow(write_dict)


editor = SkillEditor('test.csv')
