from mido import MidiFile, MidiTrack, merge_tracks
import os
import sys

toDelete = ("MARKUP")

try:
    midRB4 = MidiFile(sys.argv[1], clip = True)
except IndexError:
    print("No Midi file found.")
    exit()
try:
    midRBHP = MidiFile(sys.argv[2], clip = True)
except:
    print(f'RBHP file not found for {os.path.basename(sys.argv[1])}')
    exit()

saveFile = os.path.basename(sys.argv[1])
tempRB4 = MidiFile()

upgradeNames = []

for y, x in enumerate(midRBHP.tracks):
    if y != 0:
        upgradeNames.append(x.name)

for x in midRB4.tracks:
    if x.name in toDelete:
        pass
    elif x.name in upgradeNames:
        pass
    else:
        tempRB4.add_track()
        tempRB4.tracks[-1] = x.copy()

midRB4 = tempRB4

for y, x in enumerate(midRBHP.tracks):
    if y != 0:
        midRB4.add_track()
        midRB4.tracks[-1] = x.copy()

try:
    os.mkdir("output")
except:
    pass

midRB4.save(filename = f"output/{saveFile}")