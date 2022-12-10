from mido import Message, MetaMessage, MidiFile, MidiTrack, merge_tracks
import os
import sys

triggers_swap = {
    # Global events
    "verse": "[verse]",
    "solo": "[solo]",
    "chorus": "[chorus]",
    "end": "[end]",
    # Guitar events
    "gtr_on": "[play]",
    "gtr_off": "[idle]",
    "solo_on": "[solo_on]",
    "solo_off": "[solo_off]",
    "wail_on": "[wail_on]",
    "wail_off": "[wail_off]",
    "ow_face_on": "[ow_face_on]",
    "ow_face_off": "[ow_face_off]",
    # Misc Events
    "sing_on": "[play]",
    "bass_on": "[play]",
    "drum_on": "[play]",
    "sing_off": "[idle]",
    "bass_off": "[idle]",
    "drum_off": "[idle]",
    "drum_double": "[double_time]",
    "drum_normal": "[play]",
    "drum_half": "[half_time]",
    "drum_allbeat": "[allbeat]",
    "gtr_half_tempo": "[half_tempo]",
    "bass_half_tempo": "[half_tempo]",
    "drum_half_tempo": "[half_tempo]",
    "crowd_half_tempo": "[crowd_half_tempo]",
    "sing_half_tempo": "[half_tempo]",
    "gtr_normal_tempo": "[normal_tempo]",
    "bass_normal_tempo": "[normal_tempo]",
    "drum_normal_tempo": "[normal_tempo]",
    "crowd_normal_tempo": "[crowd_normal_tempo]",
    "sing_normal_tempo": "[normal_tempo]",
    "gtr_double_tempo": "[double_tempo]",
    "bass_double_tempo": "[double_tempo]",
    "drum_double_tempo": "[double_tempo]",
    "crowd_double_tempo": "[crowd_double_tempo]",
    "sing_double_tempo": "[double_tempo]",
    # Hand and Strum Maps
    "HandMap_Default": "[map HandMap_Default]",
    "HandMap_Linear": "[map HandMap_Linear]",
    "HandMap_NoChords": "[map HandMap_NoChords]",
    "HandMap_AllChords": "[map HandMap_AllChords]",
    "HandMap_DropD": "[map HandMap_DropD]",
    "HandMap_DropD2": "[map HandMap_DropD2]",
    "HandMap_Solo": "[map HandMap_Solo]",
    "StrumMap_Default": "[map StrumMap_Default]",
    "StrumMap_punk": "[map StrumMap_punk]",
    "StrumMap_softpick": "[map StrumMap_softpick]",
}

def append_event(track, event, event_time):
    track.append(MetaMessage("text", text = event, time = event_time))
    return

def append_note(track, note, note_type, velocity, event_time):
    track.append(Message(type = note_type, note = note, time = event_time, velocity = velocity, channel = 1))
    return

if __name__ == "__main__":
    # Read the MIDI and put all the tracks in a dict for easy access
    mid = MidiFile(sys.argv[1])
    # print(mid.ticks_per_beat)
    if len(sys.argv) > 2:
        output = sys.argv[2]
    else:
        output = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), os.path.splitext(os.path.basename(os.path.abspath(sys.argv[1])))[0]) + "_GH2.mid"
    mid_dict = {}
    for x in mid.tracks:
        mid_dict[x.name.lower()] = x

    # Define a new midi and put the tempo map from the first midi in it
    new_midi = MidiFile()
    new_midi.add_track()
    new_midi.tracks[0] = mid.tracks[0]

    # Since T1 GEMS is essentially PART GUITAR, I'll just add it to the new midi and add the other events later
    t1_gems = mid_dict["T1 GEMS".lower()]

    # Set up the GH2 tracks. Each is a list containing the event and total time
    PART_GUITAR_ANIM_NOTES = MidiTrack()
    PART_GUITAR_ANIM_EVENTS = MidiTrack()
    PART_GUITAR_EVENTS = MidiTrack()
    BAND_BASS_EVENTS = MidiTrack()
    BAND_BASS_NOTES = MidiTrack()
    BAND_DRUMS_EVENTS = MidiTrack()
    BAND_DRUMS_NOTES = MidiTrack()
    BAND_SINGER = MidiTrack()
    TRIGGERS = MidiTrack()
    EVENTS = MidiTrack()
    EVENTS.append(MetaMessage("text", text = "[lighting ()]", time = 0))
    # [["[lighting ()]", 0]]
    # print(len(EVENTS))

    # Make Band and Guitar text events
    total_time = 0
    last_drum = 0
    last_bass = 0
    last_sing = 0
    last_gtr = 0
    last_else = 0
    for x in mid_dict["events"]:
        total_time += x.time
        if x.type == "text":
            if x.text.startswith("drum"):
                append_event(BAND_DRUMS_EVENTS, triggers_swap[x.text], total_time - last_drum)
                last_drum = total_time
            elif x.text.startswith("sing"):
                append_event(BAND_SINGER, triggers_swap[x.text], total_time - last_sing)
                last_sing = total_time
            elif x.text.startswith("bass"):
                append_event(BAND_BASS_EVENTS, triggers_swap[x.text], total_time - last_bass)
                last_bass = total_time
            elif x.text.startswith("gtr") or x.text.endswith("on") or x.text.endswith("off"):
                append_event(PART_GUITAR_EVENTS, triggers_swap[x.text], total_time - last_gtr)
                last_gtr = total_time
            else:
                if len(EVENTS) != 1:
                    append_event(EVENTS, triggers_swap[x.text], total_time - last_else)
                else:
                    append_event(EVENTS, "[music_start]", total_time - last_else)
                    append_event(EVENTS, triggers_swap[x.text], 0)
                last_else = total_time

    # Speaker cone and kick drum anims
    total_time = 0
    last_drum = 0
    last_bass = 0
    for x in mid_dict["triggers"]:
        total_time += x.time
        if x.type == "note_on" or x.type == "note_off":
            if x.note == 61:
                append_note(BAND_BASS_NOTES, 36, x.type, x.velocity, total_time - last_bass)
                last_bass = total_time
                # BAND_BASS_NOTES.append([36, total_time, x.type])
            elif x.note == 60:
                append_note(BAND_DRUMS_NOTES, 36, x.type, x.velocity, total_time - last_drum)
                last_drum = total_time

    # Hand map and fret map anims
    total_time = 0
    last_gtr_note = 0
    last_gtr_event = 0
    for x in mid_dict["anim"]:
        total_time += x.time
        if x.type == "note_on" or x.type == "note_off":
            append_note(PART_GUITAR_ANIM_NOTES, x.note, x.type, x.velocity, total_time - last_gtr_note)
            last_gtr_note = total_time
        elif x.type == "text":
            append_event(PART_GUITAR_ANIM_EVENTS, triggers_swap[x.text], total_time - last_gtr_event)
            last_gtr_event = total_time

    # Key frames for lights
    total_time = 0
    last_gtr_note = 0
    for x in t1_gems:
        total_time += x.time
        if x.type == "note_on" or x.type == "note_off":
            if x.note in range(60, 63):
                append_note(TRIGGERS, x.note - 12, x.type, x.velocity, total_time - last_gtr_note)
                last_gtr_note = total_time

    # Merge MIDI Tracks and add to new_midi
    PART_GUITAR = merge_tracks([t1_gems, PART_GUITAR_ANIM_EVENTS, PART_GUITAR_ANIM_NOTES, PART_GUITAR_EVENTS])
    PART_GUITAR.name = "PART GUITAR"
    new_midi.add_track()
    new_midi.tracks[-1] = PART_GUITAR

    BAND_BASS = merge_tracks([BAND_BASS_EVENTS, BAND_BASS_NOTES])
    BAND_BASS.name = "BAND BASS"
    new_midi.add_track()
    new_midi.tracks[-1] = BAND_BASS

    BAND_DRUMS = merge_tracks([BAND_DRUMS_EVENTS, BAND_DRUMS_NOTES])
    BAND_DRUMS.name = "BAND DRUMS"
    new_midi.add_track()
    new_midi.tracks[-1] = BAND_DRUMS

    BAND_SINGER.name = "BAND SINGER"
    new_midi.add_track()
    new_midi.tracks[-1] = BAND_SINGER

    EVENTS.name = "EVENTS"
    new_midi.add_track()
    new_midi.tracks[-1] = EVENTS

    TRIGGERS.name = "TRIGGERS"
    new_midi.add_track()
    new_midi.tracks[-1] = TRIGGERS

    if not output.endswith(".mid"):
        output = os.path.join(output, os.path.splitext(os.path.basename(os.path.abspath(sys.argv[1])))[0] + "_GH2.mid")

    new_midi.save(output)
    # raise Exception
    """for x in new_midi.tracks[0]:
        print(x)"""
