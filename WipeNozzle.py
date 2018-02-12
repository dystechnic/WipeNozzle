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
# import os

# Repetier-Host sends only the file name, Slic3r sends path and file name
sourcename = sys.argv[1]
if sourcename[1] != ':':
    sourcename = sourcename	 # source file passed from Slic3r

tmpname = 'tmpfile.gcode'    # temp file name

with open(sourcename, 'rt') as fin, open(tmpname, 'w') as fout:
    while 1:  # loop to find tool changes and insert code"
        ln = fin.readline()
        if (ln == ''):	 # check for end of file
            break
        if ln[0] == ';':  # skip comment lines
            fout.write(ln)
            continue
        if ln[:2] == 'T0':  # replace T0 with code
            fout.write('T0			; Editted by WipeNozzle.py' + '\n')
#           fout.write('G10 ; Inserted by WipeNozzle.py' + '\n') 			# retract (not necessary when using slic3r
            fout.write('G1 E-45 F300		; Inserted by WipeNozzle.py' + '\n') 	# retract 45mm of filament at 5mm/sec
            fout.write('G1 X50 Y430 F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to rear of bed and X=50
#            fout.write('G11			; Inserted by WipeNozzle.py' + '\n') 	# un-retrcat (replace with E moves when not using firmware retract)
            fout.write('G1 E100 F300		; Inserted by WipeNozzle.py' + '\n') 	# extrude 100mm of filament at 5mm/sec	
            fout.write('G10			; Inserted by WipeNozzle.py' + '\n') 	# retract (replace with E moves when not using firmware retract)
            fout.write('G1 X70 Y410 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X90 Y430 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T0 command.
            continue
        if ln[:2] == 'T1':  # replace T1 with code
            fout.write('T1 			; Editted by WipeNozzle.py' + '\n')
#           fout.write('G10 ; Inserted by WipeNozzle.py' + '\n') 			# retract (not necessary when using slic3r
            fout.write('G1 E-45 F300		; Inserted by WipeNozzle.py' + '\n') 	# retract 45mm of filament at 5mm/sec
            fout.write('G1 X50 Y430 F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to rear of bed and X=50
#            fout.write('G11			; Inserted by WipeNozzle.py' + '\n') 	# un-retrcat (replace with E moves when not using firmware retract)
            fout.write('G1 E100 F300		; Inserted by WipeNozzle.py' + '\n') 	# extrude 100mm of filament at 5mm/sec	
            fout.write('G10			; Inserted by WipeNozzle.py' + '\n') 	# retract (replace with E moves when not using firmware retract)
            fout.write('G1 X70 Y410 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X90 Y430 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T1 command.
            continue
        if ln[:2] == 'T2':  # replace T2 with code
            fout.write('T2 			; Editted by WipeNozzle.py' + '\n')
#           fout.write('G10 ; Inserted by WipeNozzle.py' + '\n') 			# retract (not necessary when using slic3r
            fout.write('G1 E-45 F300		; Inserted by WipeNozzle.py' + '\n') 	# retract 45mm of filament at 5mm/sec
            fout.write('G1 X50 Y430 F21000	; Inserted by WipeNozzle.py' + '\n') 	# move quickly to rear of bed and X=50
#            fout.write('G11			; Inserted by WipeNozzle.py' + '\n') 	# un-retrcat (replace with E moves when not using firmware retract)
            fout.write('G1 E100 F300		; Inserted by WipeNozzle.py' + '\n') 	# extrude 100mm of filament at 5mm/sec	
            fout.write('G10			; Inserted by WipeNozzle.py' + '\n') 	# retract (replace with E moves when not using firmware retract)
            fout.write('G1 X70 Y410 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly forward past the rubber strip and 20mm to the right
            fout.write('G1 X90 Y430 F1000	; Inserted by WipeNozzle.py' + '\n')  # move slowly backwards and right another 20mm
            fout.write('G1 R2 X0 Y0 Z0 F21000   ; Inserted by WipeNozzle.py' + '\n')  # move quickly to where the print head was at the T2 command.
        else:
            fout.write(ln)
fin.close()	 # close the files
fout.close()
shutil.move(tmpname, sourcename)  # replace orginal file with modified file
# os.remove(sourcename + '~') 
