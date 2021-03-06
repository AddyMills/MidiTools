from mido import MidiFile, MidiTrack, merge_tracks
import os
import sys

toDelete = ("MARKUP")
toIgnore = ("VENUE", "BEAT", "EVENTS")

try:
    midRB4 = MidiFile(sys.argv[1], clip = True)
except IndexError:
    print("No Midi file found.")
    exit()
try:
    midRBHP = MidiFile(sys.argv[2], clip = True)
except:
    print(f'Upgrade file not found for {os.path.basename(sys.argv[1])}')
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
        if x.name in toIgnore:
            tempRB4.add_track()
            tempRB4.tracks[-1] = x.copy()
        else:
            pass
    else:
        tempRB4.add_track()
        tempRB4.tracks[-1] = x.copy()

midRB4 = tempRB4

for y, x in enumerate(midRBHP.tracks):
    if x.name in toIgnore:
        pass
    elif x.name in toDelete:
        pass
    elif y == 0:
        pass
    else:
        midRB4.add_track()
        midRB4.tracks[-1] = x.copy()
        
tempRB4 = MidiFile()

try:
    os.mkdir("output")
except:
    pass

midRB4.save(filename = f"output/{saveFile}")