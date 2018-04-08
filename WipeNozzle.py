#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Print with a multicolor hotend without the need of a purge/wipe tower.

This script is inspired by a post on Ian Deckingman's website somei3deas.wordpress.com.
The post (https://somei3deas.wordpress.com/2017/12/06/5-colour-printing-with-a-purge-bucket/)
showed a way to print multicolor without the need of a purge/wipe tower. I've used the info
and created this script. It adds the needed code to a Gcode file. I use it with a switching
three color extruder.
The script takes a file as input on the command-line but it's intended use is as a postprocessing
script in Slic3r.
"""

import sys
import re
import os


# Position of rubber wipe strip
# Mine is at the front-left corner of the bed (0,0)

xpos = 0
ypos = 0

# default retraction length before tool change.
# I use a 3-color THC-01 head. For this head the minimalretract length is 45mm
# and the minimal extrusion length for priming is 55mm

DefRetract = 55
DefExtrude = 55

# I noticed that some fillament neededmore extrusion length to reach a solid color than others
# I guess not all fillament are created equally ;-)
# Therefore I made it possible to define extrusion length in mm per fillament typr you have

RedPLA = 80
WhitePLA = 105
BluePLA = 80
BlackPLA = 100
DarkGreyPLA = 100
LightGreyPLA = 100

# Define wich fillament is loaded into wich extruder Ext0 = T0 etc.

Ext0 = DarkGreyPLA
Ext1 = RedPLA
Ext3 = BluePLA


# Get input file from cli and define input and output file variables

infile = sys.argv[1]
outfile = sys.argv[1] + '.postproc'

with open(infile, 'rt') as fin:
    with open(outfile, 'w') as fout:
        while 1:  					# loop to find tool changes and insert code"
            ln = fin.readline()
            if ln == '':  				# check for end of file
                break
            if ln[0] == ';':  				# skip comment lines
                fout.write(ln)
                continue
            if ln[:2] == 'T0':  			# replace T0 with code
                fout.write('; =====> Editted by WipeNozzle.py (T0)' + '\n')
                fout.write('M401' + '\n')  # Use M401 to store and M402 to move to the stored position(it´s not in EEprom)
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F21000' + '\n')  	# move quickly to wipe position
                fout.write('G1 E-' + str(DefRetract) + ' F300' + '\n')  # retract before tool change
                fout.write('T0' + '\n')  		# change tool.
                fout.write('G1 E' + str(Ext0) + ' F300' + '\n')  # extrude fillament specific amount at 5mm/sec
                fout.write('G1 X' + str(xpos + 40) + ' Y' + str(ypos + 12) + ' F1000' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F1000' + '\n')  # move back to the start position (0,0)
                fout.write('G1 E-6.5 F1800' + '\n')  # Retract to prevent oozing
                fout.write('M402 F10000' + '\n')  # Go back to where the nozzle was before the wipe
                fout.write('G1 E6.5 F1800' + '\n')   # Re-prime the nozzle before printing
                fout.write('; =====> Editted by WipeNozzle.py' + '\n')
                continue
            if ln[:2] == 'T1':  # replace T1 with code
                fout.write('; =====> Editted by WipeNozzle.py (T1)' + '\n')
                fout.write('M401' + '\n')  # Use M401 to store and M402 to move to the stored position(it´s not in EEprom)
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F21000' + '\n')  	# move quickly to wipe position
                fout.write('G1 E-' + str(DefRetract) + ' F300' + '\n')  # retract before tool change
                fout.write('T1' + '\n')  		# change tool.
                fout.write('G1 E' + str(Ext1) + ' F300' + '\n')  # extrude fillament specific amount at 5mm/sec
                fout.write('G1 X' + str(xpos + 40) + ' Y' + str(ypos + 12) + ' F1000' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F1000' + '\n')  # move slowly back to the start position (0,0)
                fout.write('G1 E-6.5 F1800' + '\n')  # Retract to prevent oozing
                fout.write('M402 F10000' + '\n')  # Go back to where the nozzle was before the wipe
                fout.write('G1 E6.5 F1800' + '\n')   # Re-prime the nozzle before printing
                fout.write('; =====> Editted by WipeNozzle.py' + '\n')
                continue
            if ln[:2] == 'T2':  # replace T2 with code
                fout.write('; =====> Editted by WipeNozzle.py (T2)' + '\n')
                fout.write('M401' + '\n')  # Use M401 to store and M402 to move to the stored position(it´s not in EEprom)
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F21000' + '\n')  	# move quickly to wipe position
                fout.write('G1 E-' + str(DefRetract) + ' F300' + '\n')  # retract before tool change
                fout.write('T2' + '\n')  		# change tool.
                fout.write('G1 E' + str(Ext2) + ' F300' + '\n')  # extrude fillament specific amount at 5mm/sec
                fout.write('G1 X' + str(xpos + 40) + ' Y' + str(ypos + 12) + ' F1000' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
                fout.write('G1 X' + str(xpos) + ' Y' + str(ypos) + ' F1000' + '\n')  # move slowly back to the start position (0,0)
                fout.write('G1 E-6.5 F1800' + '\n')  # Retract to prevent oozing
                fout.write('M402 F10000' + '\n')  # Go back to where the nozzle was before the wipe
                fout.write('G1 E6.5 F1800' + '\n')   # Re-prime the nozzle before printing
                fout.write('; =====> Editted by WipeNozzle.py T2' + '\n')
            else:
                fout.write(ln)

# close the files

fin.close()
fout.close()

# Delete the original input file

os.remove(sys.argv[1])

# Rename the output file to be what the input file was called

os.rename(sys.argv[1] + '.postproc', sys.argv[1])
