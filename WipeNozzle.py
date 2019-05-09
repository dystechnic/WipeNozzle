#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

# TODO: Create DocString

#some variables used in the usage comment
copyright = "(C) 2017-2019"
author = 'Dystechnic (dystechnic@gmail.com)'
license = 'Attribution-NonCommercial-ShareAlike 4.0 https://creativecommons.org/licenses/by-nc-sa/4.0/'

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

# default retraction length before tool change.
# I use a 3-color THC-01 head. For this head the minimalretract length is 45mm
# and the minimal extrusion length for priming is 55mm.
# But I guess these are chinese mm's because my printer tells me different ;-)
retract1 = '5'
retract2 = '75'
extrude1 = '60'
extrude2 = '55'
ooze = '16'

# Usable keys from dict:
# rel_mov   # Relative moves for extruder
# fil_res   # Set the current filament position to E=0
# retr1     # Quickly retract 'retract1' mm to prevent oozing
# home      # Home X and Y axis leave Z at current height
# res_ext   # Set the current filament position to E=0
# reins_1   # Reinsert 5mm to prevent stringing
# res_ext   # Set the current filament position to E=0
# retr2     # Quickly retract 'retract2' mm to free the splitter
# rel_ext   # Release extruder stepper motor from 'holding' position
#
#             # Now change the tool to T0.
# extr1     # Extrude 'extrude1'mm to fill the splitter
# noz_mv1   # Move the nozzle before purging
# extr2     # Extrude 'extrude2' mm to purge the nozzle
# wipe1     # Wipe the nozzle, first pass
# wipe2     # Wipe the nozzle, second pass
# cur_ann   # Compensate for the annoying Cura G1 F1200 E16


gcode = {'rel_mov': 'M83', 'fil_res': 'G92 E0', 'retr1': ('G1 F1300 E-' + retract1), 'home': 'G1 X0.000000 Y0.000000 F21000',
         'res_ext': 'G92 E0', 'reins_1': 'G1 F25 E5.000000', 'retr2': ('G1 F1300 E-' + retract2), 'rel_ext': 'M84 E',
         'extr1': ('G1 F700 E-' + extrude1), 'noz_mv1': 'G1 F5000 X20.000000 Y0.000000',
         'extr2': ('G1 F200 E-' + extrude2), 'wipe1': 'G1 F5000 X25.000000 Y10.000000',
         'wipe2': 'G1 F5000 X0.000000 Y0.000000', 'cur_ann': ('G1 F1300 E-' + ooze)}


# Show usage information
def usage():
    print("Usage:")
    print()
    print("  ", sys.argv[0], " gcodeFile")
    print(copyright + " Licensed under CC BY-NC-SA 4.0 by " + author)
    print()
    sys.exit()


# Create the outputfile, open source for reading output for writing and add the needed Gcode
def wipenozzle(filename):
    prefix = filename[:-6]
    suffix = '.gcode'
    addition = '-modded'
    ofile = prefix + addition + suffix
    # checker to see if it is the first toolchange in the G-Code file
    Firsttime = True
    with open(filename, 'r') as infile, open(ofile, 'w+') as outfile:
        while 1:                                                # Main loop to find tool changes and insert code"
            ln = infile.readline()                              # Read input file line by line
            if (ln == ''):                                      # check for end of file
                break
            if ln[0] == ';':                                    # skip comment lines
                outfile.write(ln)
                continue
            if ln[:12] == '; ' + EOGmarker:                     # Check for End Gcode marker
                outfile.write('; =====> Reached the end of Gcode marker' + '\n')
                outfile.write(gcode['rel_mov'] + '\n')          # relative moves for extruder
                outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                outfile.write(gcode['retr1'] + '\n')            # Quickly retract 'Retract1' mm to prevent oozing
                outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                outfile.write(gcode['retr2'] + '\n')            # Quickly retract 'Retract2' mm to free the splitter
                outfile.write(gcode['rel_ext'] + '\n')          # release extruder from 'holding' position
            if ln[0] == ';':                                    # skip comment lines
                outfile.write(ln)
                continue
            if ln[:2] == 'T0' or ln[:2] == 'T1' or ln[:2] == 'T2':    # replace T* with code
                nozzle = ln[:2]
                if not Firsttime:  			                    # If it is not the first time a toolchange occurred, apply the changes
                    outfile.write('; =====> Editted by WipeNozzle.py (was ' + nozzle + ')' + '\n')
# TODO: G60 feature request Marlin
#                fout.write('G60 S0' + '\n')                         # Save current position to memory slot S0
                    outfile.write(gcode['rel_mov'] + '\n')          # relative moves for extruder
                    outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                    outfile.write(gcode['retr1'] + '\n')            # Quickly retract 'Retract1' mm to prevent oozing
                    outfile.write(gcode['home'] + '\n')             # Home X and Y axis leave Z at current height
                    outfile.write(gcode['res_ext'] + '\n')          # Set the current filament position to E=0
                    outfile.write(gcode['reins_1'] + '\n')          # Reinsert 5mm to prevent stringing
                    outfile.write(gcode['res_ext'] + '\n')          # Set the current filament position to E=0
                    outfile.write(gcode['retr2'] + '\n')            # Quickly retract 'Retract2' mm to free the splitter
                    outfile.write(gcode['rel_ext'] + '\n')          # release extruder from 'holding' position
                    outfile.write(nozzle + '\n')                    # Now change the tool to T0.
                    #
                    # Load the next extruder, prime it with fillament and prepare it for printing
                    #
                    outfile.write(gcode['rel_mov'] + '\n')          # relative moves for extruder
                    outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                    outfile.write(gcode['extr1'] + '\n')            # Extrude 'Extrude1' mm to fill the splitter
                    outfile.write(gcode['noz_mv1'] + '\n')          # Move the Nozzle before purging
                    outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                    outfile.write(gcode['extr2'] + '\n')            # Extrude 'Extrude2' mm to purge the nozzle
                    outfile.write(gcode['wipe1'] + '\n')            # Wipe the Nozzle
                    outfile.write(gcode['wipe2'] + '\n')            # Wipe the Nozzle
                    outfile.write(gcode['res_ext'] + '\n')          # set the current filament position to E=0
                    outfile.write(gcode['cur_ann'] + '\n')          # Compensate fot the annoying Cura G1 F1200 E16
                    outfile.write(gcode['res_ext'] + '\n')          # Set the current filament position to E=0
# TODO: G61 feature request Marlin
#                fout.write('G61 S0 X Y F20000' + '\n')              # Return to saved X and Y position
                    outfile.write('; =====> Editted by WipeNozzle.py' + '\n')
                else:
                    outfile.write(ln)
                    Firsttime = False
                    continue
            else:
                outfile.write(ln)

# Main function to check if input is given and start rewriting the Gcode file
def main():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        name = sys.argv
        usage()

    wipenozzle(filename)


main()
