#!/usr/bin/env python
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
import shutil

# Repetier-Host sends only the file name, Slic3r sends path and file name
sourcename = sys.argv[1]
if sourcename[1] != ':':
    sourcename = sourcename	 # source file passed from Slic3r

tmpname = 'tmpfile.gcode'    # temp file name

# position of rubber wipe strip
xpos = 50
ypos = 430

# default retraction length before tool change.
# I use a 3-color THC-01 head. For this head the minimalretract length is 45mm
# and the minimal extrusion length for priming is 55mm
DefRetract = 45
DefExtrude = 55

# I noticed that some fillament neededmore extrusion length to reach a solid color than others
# I guess not all fillament are created equally ;-)
# Therefore I made it possible to define extrusion length in mm per fillament typr you have
RedPLA = 75
WhitePLA = 100
BluePLA = 80
BlackPLA = 100
DarkGreyPLA = 100
LightGreyPLA = 100

# Define wich fillament is loaded into wich extruder Ext0 = T0 etc.
Ext0 = RedPLA
Ext1 = WhitePLA
Ext3 = BluePLA

with open(sourcename, 'rt') as fin, open(tmpname, 'w') as fout:
    while 1:  # loop to find tool changes and insert code"
        ln = fin.readline()
        if (ln == ''):	 # check for end of file
            break
        if ln[0] == ';':  # skip comment lines
            fout.write(ln)
            continue
        if ln[:2] == 'T0':  # replace T0 with code
            fout.write('G1 E-' + (str(DefRetract)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# retract before tool change
            fout.write('T0			; Editted by WipeNozzle.py' + '\n')  # change tool
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to wipe position
            fout.write('G1 E' + (str(Ext0)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# extrude fillament specific amount at 5mm/sec
            fout.write('G1 X' + (str(xpos+20)) + ' Y' + (str(ypos-20)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T0 command.
            continue
        if ln[:2] == 'T1':  # replace T1 with code
            fout.write('G1 E-' + (str(DefRetract)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# retract before tool change
            fout.write('T1			; Editted by WipeNozzle.py' + '\n')  # change tool
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to wipe position
            fout.write('G1 E' + (str(Ext0)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# extrude fillament specific amount at 5mm/sec
            fout.write('G1 X' + (str(xpos+20)) + ' Y' + (str(ypos-20)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T1 command.
            continue
        if ln[:2] == 'T2':  # replace T2 with code
            fout.write('G1 E-' + (str(DefRetract)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# retract before tool change
            fout.write('T2			; Editted by WipeNozzle.py' + '\n')  # change tool
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to wipe position
            fout.write('G1 E' + (str(Ext0)) + ' F300		; Editted by WipeNozzle.py' + '\n') 	# extrude fillament specific amount at 5mm/sec
            fout.write('G1 X' + (str(xpos+20)) + ' Y' + (str(ypos-20)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X' + (str(xpos)) + ' Y' + (str(ypos)) + ' F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T1 command.
        else:
            fout.write(ln)
fin.close()	 # close the files
fout.close()
shutil.move(tmpname, sourcename)  # replace orginal file with modified file
