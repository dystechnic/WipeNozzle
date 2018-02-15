
BlenderGcodeImport

Python script to load gcode files produced by Slic3r into Blender

his script is inspired by a post on Ian Deckingman's website somei3deas.wordpress.com.
The post (https://somei3deas.wordpress.com/2017/12/06/5-colour-printing-with-a-purge-bucket/)
showed a way to print multicolor without the need of a purge/wipe tower.
I wrote this script because I own a different hotend and Ian did not have a script in his original post.

The script adds the needed code to a Gcode file. I use it with a switching three color extruder. (THC-01)

The script takes a file as input on the command-line but it's intended use is as a postprocessing
script in Slic3r.

This script is a work in progress and comes without any warranty whatsoever and is for my testing
purposes only.
