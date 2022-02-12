from mido import MidiFile, MidiTrack, merge_tracks
import os
import sys

toImport = ("PART REAL_GUITAR", "PART REAL_BASS", "PART REAL_GUITAR_22", "PART REAL_BASS_22", "PART KEYS", "PART REAL_KEYS_X", "PART REAL_KEYS_H", "PART REAL_KEYS_M", "PART REAL_KEYS_E", "PART KEYS_ANIM_RH", "PART KEYS_ANIM_LH")

toDelete = ("MARKUP")

try:
    midRB4 = MidiFile(sys.argv[1])
except IndexError:
    print("No Midi file found.")
    exit()
try:
    midRBHP = MidiFile(sys.argv[2])
except:
    print(f'RBHP file not found for {os.path.basename(sys.argv[1])}')
    exit()

saveFile = os.path.basename(sys.argv[1])
tempRB4 = MidiFile()

for x in midRB4.tracks:
    if x.name in toDelete:
        pass
    else:
        tempRB4.add_track()
        tempRB4.tracks[-1] = x.copy()

midRB4 = tempRB4

for x in midRBHP.tracks:
    if x.name in toImport:
        midRB4.add_track()
        midRB4.tracks[-1] = x.copy()

try:
    os.mkdir("output")
except:
    pass

midRB4.save(filename = f"output/{saveFile}")