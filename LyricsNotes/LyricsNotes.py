from mido import MidiFile, MidiTrack, Message, merge_tracks
import os
import sys

toAdd = ("PART VOCALS", "HARM1", "HARM2", "HARM3")

try:
    mid = MidiFile(sys.argv[1], clip = True)
except IndexError:
    print("No Midi file found.")
    exit()

tempMid = MidiFile()
tempMid.add_track()
tempMid.tracks[0] = mid.tracks[0]

for x in mid.tracks:
    if x.name in toAdd:
        tempTrack = MidiTrack()
        voxTrack = x.copy()
        time = 0
        lastTime = 0
        noteCount = 0
        for msg in x:
            time += msg.time
            if msg.type == "lyrics":
                if noteCount == 0:
                    tempTrack.append(Message('note_on', note = 33, velocity = 100, time = time-lastTime))
                else:
                    tempTrack.append(Message('note_on', note = 33, velocity = 100, time = time-lastTime-30))
                tempTrack.append(Message('note_on', note = 33, velocity = 0, time = 30))
                lastTime = time
                noteCount += 1
            
        newTrack = merge_tracks((tempTrack, voxTrack))
        tempMid.add_track()
        tempMid.tracks[-1] = newTrack.copy()

tempMid.save(filename = "VoxUpdate.mid")