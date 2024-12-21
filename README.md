# pySkillTree
Skill tree SVG generator using Python

# How it works

The generator generates a SVG of a skill tree that is defined in a CSV file.

Skills can have up to one dependency (or None).
Each skill can be in one of three statuses:

* locked (will show up as a donut shape with the 'locked' color)
* unlocked (will show up as a donut shape with the skill's color)
* completed (will show up as a filled circle with the skill's color)

Each skill has a name (to keep relatively short - as it is written on the node). You can use a '|' in the name, which will convert to a line break when text is added to the skill.
Slightly more detail can be added in the upper and lower text of the donut/circle.

Skills that have dependencies are connected with a line to that skill (the color of which depends on the status of the skill).

To aid in positioning the nodes, an editor is included, which crudely helps position nodes, though as of right now the dependencies do not show.
Just run the editor on the CSV file you want and click and drag skill nodes. It saves automatically.

A sample CSV for running goals is included.

# Note

This is quite crude and rudimental, so a lot may not work well, but it should work to generate the SVG skill tree.

