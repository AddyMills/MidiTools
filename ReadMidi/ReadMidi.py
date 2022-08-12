from mido import MidiFile, MidiTrack
import os
import sys



path = os.getcwd()
directory = []
for x in os.listdir(path):
    names = os.path.splitext(os.path.basename(x))
    if names[1] == ".mid":
        directory.append(x)
    #print(names)

print("Reading MIDI files...")

finalList = ""

original_stdout = sys.stdout # Save a reference to the original standard output

for x in directory:
    finalList += os.path.splitext(x)[0]
    midi = MidiFile(x, clip = True)
    trackNames = ": "
    for z,y in enumerate(midi.tracks):
        if z == 0:
            pass
        else:
            if z != 1:
                trackNames += ", "
            trackNames += y.name
    finalList += trackNames + "\n"

with open("Midi Tracks.txt", 'w') as f:
    f.write(finalList)