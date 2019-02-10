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

I use a 3-color THC-01 head wich is a 3 in, 1 out head. So I have three extruders feeding
one hotend. This script makes sure that all fillament in all three extruders is loaded
and unloaded without clogging the hotend when needed.

"""

import sys
import shutil

# checker to see if it is the first toolchange in the G-Code file
Firsttime = True

# default retraction length before tool change.
# I use a 3-color THC-01 head. For this head the minimalretract length is 45mm
# and the minimal extrusion length for priming is 55mm.
# But I guess these are chinese mm's because my printer tells me different ;-)
Retract1 = 5
Retract2 = 75
Extrude1 = 60
Extrude2 = 55

# Cura has an annoying G1 F1200 E-16 and G1 F1200 E16 before and after a tool change.
# This is a hardcoded setting and can not be changed. See issue #676.
# So before we restore the hotend to its position befor the tool change we have
# to compensate for this extrusion
Ooze = 16

# If you want to reset to reset the last active extruder after printing
# you can use a marker in the 'End-Gcode' field of your slicer. This script wil detect
# that marker and inserts the required code.
# Don't forget to change the length field on line 58 to match the length of the
# colun + a space + the length of your marker.
#
# Set a default extrusion for the initial extruder in the Start G-code settings of your
# slicer. The ideal length is Extrude1 + Etrude2
# If you don't want to use this, just leave this empty or set it to something that doesn't exist.
EOGmarker = 'G-Code-End'

# Now we finaly can go do something interesting
# First get the input file from cli and define input and output file variables

sourcename = sys.argv[1]
if sourcename[1] != ':':
    sourcename = sourcename	 # source file passed from Slic3r

tmpname = 'tmpfile.gcode'    # temp file name

with open(sourcename, 'rt') as fin, open(tmpname, 'w') as fout:
    while 1:                                                        # loop to find tool changes and insert code"
        ln = fin.readline()
        if (ln == ''):	                                            # check for end of file
            break
        if ln[:12] == '; ' + EOGmarker :                            # Check for End Gcode marker
            fout.write('; =====> Reached the end of Gcode marker' + '\n')
            fout.write('M83' + '\n')                                # relative moves for extruder
            fout.write('G92 E0' + '\n')                             # set the current filament position to E=0
            fout.write('G1 F1300 E-' + str(Retract1) + '\n')        # Quickly retract 'Retract1' mm to prevent oozing
            fout.write('G92 E0' + '\n')                             # set the current filament position to E=0
            fout.write('G1 F1300 E-' + str(Retract2) + '\n')        # Quickly retract 'Retract2' mm to free the splitter
            fout.write('M84 E' + '\n')                              # release extruder stepper motor from 'holding' position
            fout.write('; =====> Editted by WipeNozzle.py' + '\n')
        if ln[0] == ';':                                            # skip comment lines
            fout.write(ln)
            continue
        if ln[:2] == 'T0':                                          # replace T0 with code
            if not Firsttime:  			                            # If it is not the first time a toolchange occurred, apply the changes
                # First we extract the fillament fromthe active extruder in a way we can use
                # the extruder again later and there are no obstructions in the splitter
                fout.write('; =====> Editted by WipeNozzle.py (was T0)' + '\n')
                fout.write('G60 S0' + '\n')                         # Save current position to memory slot S0
                fout.write('M83' + '\n')                            # Relative moves for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract1) + '\n')    # Quickly retract 'Retract1' mm to prevent oozing
                fout.write('G1 X0.000000 Y0.000000 F21000' + '\n')  # Home X and Y axis leave Z at current height
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F25 E5.000000' + '\n')               # Reinsert 5mm to prevent stringing
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract2) + '\n')    # Quickly retract 'Retract2' mm to free the splitter
                fout.write('M84 E' + '\n')                          # Release extruder stepper motor from 'holding' position
                fout.write('T0' + '\n')                             # Now change the tool to T0.
                #
                # Load the next extruder, prime it with fillament and prepare it for printing
                #
                fout.write('M83' + '\n')                            # Relative movement for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F700 E' + str(Extrude1) + '\n')      # Extrude 'Extrude1'mm to fill the splitter
                fout.write('G1 F5000 X20.000000 Y0.000000' + '\n')  # Move the Nozzle before purging
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F200 E' + str(Extrude2) + '\n')      # Extrude 'Extrude2' mm to purge the nozzle
                fout.write('G1 F5000 X25.000000 Y10.000000' + '\n') # Wipe the Nozzle
                fout.write('G1 F5000 X0.000000 Y0.000000' + '\n')   # Wipe the Nozzle
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Ooze) + '\n')        # Compensate fot the annoying Cura G1 F1200 E16
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G61 S0 X Y F20000' + '\n')              # Return to saved X and Y position
                fout.write('; =====> Editted by WipeNozzle.py' + '\n')
            else:
                fout.write(ln)
                Firsttime = False
            continue
        if ln[:2] == 'T1':                                          # replace T1 with code
            if not Firsttime:  			                            # If it is not the first time a toolchange occurred, apply the changes
                # First we extract the fillament fromthe active extruder in a way we can use
                # the extruder again later and there are no obstructions in the splitter
                fout.write('; =====> Editted by WipeNozzle.py (was T1)' + '\n')
                fout.write('G60 S0' + '\n')                         # Save current position to memory slot S0
                fout.write('M83' + '\n')                            # Relative moves for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract1) + '\n')    # Quickly retract 'Retract1' mm to prevent oozing
                fout.write('G1 X0.000000 Y0.000000 F21000' + '\n')  # Home X and Y axis leave Z at current height
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F25 E5.000000' + '\n')               # Reinsert 5mm to prevent stringing
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract2) + '\n')    # Quickly retract 'Retract2' mm to free the splitter
                fout.write('M84 E' + '\n')                          # Release extruder stepper motor from 'holding' position
                fout.write('T1' + '\n')                             # Now change the tool to T1.
                #
                # Load the next extruder, prime it with fillament and prepare it for printing
                #
                fout.write('M83' + '\n')                            # Relative movement for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F700 E' + str(Extrude1) + '\n')      # Extrude 'Extrude1'mm to fill the splitter
                fout.write('G1 F5000 X20.000000 Y0.000000' + '\n')  # Move the Nozzle before purging
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F200 E' + str(Extrude2) + '\n')      # Extrude 'Extrude2' mm to purge the nozzle
                fout.write('G1 F5000 X25.000000 Y10.000000' + '\n') # Wipe the Nozzle
                fout.write('G1 F5000 X0.000000 Y0.000000' + '\n')   # Wipe the Nozzle
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Ooze) + '\n')        # Compensate fot the annoying Cura G1 F1200 E16
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G61 S0 X Y F20000' + '\n')              # Return to saved X and Y position
                fout.write('; =====> Editted by WipeNozzle.py' + '\n')
            else:
                fout.write(ln)
                Firsttime = False
            continue
        if ln[:2] == 'T2':                                          # replace T2 with code
            if not Firsttime:  			                            # If it is not the first time a toolchange occurred, apply the changes
                # First we extract the fillament fromthe active extruder in a way we can use
                # the extruder again later and there are no obstructions in the splitter
                fout.write('; =====> Editted by WipeNozzle.py (was T2)' + '\n')
                fout.write('G60 S0' + '\n')                         # Save current position to memory slot S0
                fout.write('M83' + '\n')                            # Relative moves for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract1) + '\n')    # Quickly retract 'Retract1' mm to prevent oozing
                fout.write('G1 X0.000000 Y0.000000 F21000' + '\n')  # Home X and Y axis leave Z at current height
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F25 E5.000000' + '\n')               # Reinsert 5mm to prevent stringing
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Retract2) + '\n')    # Quickly retract 'Retract2' mm to free the splitter
                fout.write('M84 E' + '\n')                          # Release extruder stepper motor from 'holding' position
                fout.write('T2' + '\n')                             # Now change the tool to T0.
                #
                # Load the next extruder, prime it with fillament and prepare it for printing
                #
                fout.write('M83' + '\n')                            # Relative movement for extruder
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F700 E' + str(Extrude1) + '\n')      # Extrude 'Extrude1'mm to fill the splitter
                fout.write('G1 F5000 X20.000000 Y0.000000' + '\n')  # Move the Nozzle before purging
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F200 E' + str(Extrude2) + '\n')      # Extrude 'Extrude2' mm to purge the nozzle
                fout.write('G1 F5000 X25.000000 Y10.000000' + '\n') # Wipe the Nozzle
                fout.write('G1 F5000 X0.000000 Y0.000000' + '\n')   # Wipe the Nozzle
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G1 F1300 E-' + str(Ooze) + '\n')        # Compensate fot the annoying Cura G1 F1200 E16
                fout.write('G92 E0' + '\n')                         # Set the current filament position to E=0
                fout.write('G61 S0 X Y F20000' + '\n')              # Return to saved X and Y position
                fout.write('; =====> Editted by WipeNozzle.py' + '\n')
            else:
                fout.write(ln)
                Firsttime = False
        else:
            fout.write(ln)
fin.close()	                                                        # close the files
fout.close()
shutil.move(tmpname, sourcename)                                    # replace orginal file with modified file
