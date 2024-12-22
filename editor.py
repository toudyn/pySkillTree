# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 14:48:06 2024

@author: funky
"""

import csv
import tkinter as tk

class SkillEditor:
    def __init__(self, csv_file, grid_size=10, multiplier=2):
        # Hard coded node radius
        self.radius = 15
        self.size = 800
        self.grid_size = grid_size
        self.multiplier = multiplier
        
        self.csv_file = csv_file
        self.skills = self.load_skills_from_csv()

        # Setup Tkinter
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, width=self.size, height=self.size, bg="white")
        self.canvas.pack()

        # Draw grid and skills
        self.draw_grid()
        self.draw_skills()

        # List to track selected nodes
        self.selected_skills = []

        # Create Save button
        self.save_button = tk.Button(self.root, text="Save", command=self.save_skills)
        self.save_button.pack()

        # Bind mouse click, drag events, and key press for movement
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.root.bind("<KeyPress-Left>", self.move_selected_nodes)
        self.root.bind("<KeyPress-Right>", self.move_selected_nodes)
        self.root.bind("<KeyPress-Up>", self.move_selected_nodes)
        self.root.bind("<KeyPress-Down>", self.move_selected_nodes)

        # Focus on root to listen to key presses
        self.root.focus_set()

        self.root.mainloop()

    def load_skills_from_csv(self):
        """Load skills from CSV and apply multiplier when reading coordinates."""
        skills = []
        try:
            with open(self.csv_file, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    skill = {
                        "name": row['name'],
                        "x": int(row['x']) / self.multiplier,  # Apply multiplier
                        "y": int(row['y']) / self.multiplier,  # Apply multiplier
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
            # Draw with no multiplier applied for visual representation in editor
            x, y = skill['x'], skill['y']
            radius = self.radius
            circle = self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="gray")
            text = self.canvas.create_text(x, y, text=skill['name'], fill="black", font=("Arial", font_size))
            self.skill_circles[skill['name']] = (circle, text)

    def on_click(self, event):
        """Handles clicking on skills to initiate selection or deselection."""
        for skill in self.skills:
            x, y = skill['x'], skill['y']
            radius = self.radius
            if (event.x - x) ** 2 + (event.y - y) ** 2 <= radius ** 2:
                # If Ctrl is pressed, toggle selection
                if event.state == 0x0004:  # Ctrl is pressed
                    if skill in self.selected_skills:
                        self.selected_skills.remove(skill)
                    else:
                        self.selected_skills.append(skill)
                else:
                    # Select single node without Ctrl
                    self.selected_skills = [skill]  # Deselect others
                self.update_selection_visuals()

    def on_drag(self, event):
        """Handles dragging of the selected skills."""
        if len(self.selected_skills) == 1:  # Only allow drag if one node is selected
            skill = self.selected_skills[0]
            new_x = self.snap_to_grid(event.x)  # Snap to grid
            new_y = self.snap_to_grid(event.y)  # Snap to grid
            skill['x'] = new_x
            skill['y'] = new_y

            # Update visuals (positions)
            circle, text = self.skill_circles[skill['name']]
            self.canvas.coords(circle, new_x - self.radius, new_y - self.radius, new_x + self.radius, new_y + self.radius)
            self.canvas.coords(text, new_x, new_y)

    def move_selected_nodes(self, event):
        """Moves all selected nodes based on arrow key pressed."""
        move_distance = 20
        dx = 0
        dy = 0

        if event.keysym == 'Left':
            dx = -move_distance
        elif event.keysym == 'Right':
            dx = move_distance
        elif event.keysym == 'Up':
            dy = -move_distance
        elif event.keysym == 'Down':
            dy = move_distance

        # Move all selected nodes and snap to grid
        for skill in self.selected_skills:
            skill['x'] += dx
            skill['y'] += dy

            # Snap to grid after movement
            skill['x'] = self.snap_to_grid(skill['x'])
            skill['y'] = self.snap_to_grid(skill['y'])

            # Update visuals (positions)
            circle, text = self.skill_circles[skill['name']]
            self.canvas.coords(circle, skill['x'] - self.radius, skill['y'] - self.radius, skill['x'] + self.radius, skill['y'] + self.radius)
            self.canvas.coords(text, skill['x'], skill['y'])

    def snap_to_grid(self, value):
        """Snaps a coordinate value to the nearest grid multiple."""
        return round(value / self.grid_size) * self.grid_size

    def save_skills(self):
        """Saves the updated skills with their new positions back to the CSV with multiplier."""
        with open(self.csv_file, 'w', newline='') as csvfile:
            fieldnames = ['name', 'x', 'y', 'dependency', 'upper_text', 'lower_text', 'status', 'color', 'complete_inner_text_color', 
                          'unlocked_outer_text_color', 'background_color', 'locked_color', 'incomplete_inner_text_color', 
                          'locked_outer_text_color', 'level', 'dependency_color']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for skill in self.skills:
                write_dict = {}
                for field in fieldnames:
                    if field in ['x', 'y']:
                        write_dict[field] = int(skill[field] * self.multiplier)  # Apply multiplier for saving
                    else:
                        write_dict[field] = skill[field]
                writer.writerow(write_dict)

    def update_selection_visuals(self):
        """Updates visuals of selected skills (highlighting)."""
        # First clear all current highlights
        for circle, text in self.skill_circles.values():
            self.canvas.itemconfig(circle, fill="gray")
        
        # Then highlight selected nodes with a lighter blue for better readability
        for skill in self.selected_skills:
            circle, text = self.skill_circles[skill['name']]
            self.canvas.itemconfig(circle, fill="#66b3ff")  # Light blue for selected nodes
            self.canvas.itemconfig(text, fill="black")  # Ensure text remains black

editor = SkillEditor('test.csv')