from mido import Message, MetaMessage, MidiFile, MidiTrack, merge_tracks
import os
import sys

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
        output = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), os.path.splitext(os.path.basename(os.path.abspath(sys.argv[1])))[0]) + "_RB.mid"
    mid_dict = {}
    for x in mid.tracks:
        mid_dict[x.name.lower()] = x

    # Define a new midi and put the tempo map from the first midi in it
    new_midi = MidiFile()
    new_midi.add_track()
    new_midi.tracks[0] = mid.tracks[0]

    # Set up the RB tracks. Each is a list containing the event and total time
    PART_GUITAR_NOTES = mid_dict["plastic guitar"]
    PART_GUITAR_ANIM_NOTES = MidiTrack()
    PART_GUITAR_ANIM_EVENTS = MidiTrack()
    PART_BASS_NOTES = mid_dict["plastic bass"]
    PART_BASS_ANIM_NOTES = MidiTrack()
    PART_BASS_ANIM_EVENTS = MidiTrack()
    PART_DRUMS_NOTES = mid_dict["plastic drums"]
    PART_DRUMS_ANIM_NOTES = MidiTrack()
    PART_DRUMS_ANIM_EVENTS = MidiTrack()
    PART_VOCALS = mid_dict["part vocals"]
    EVENTS = mid_dict["events"]
    SECTIONS = MidiTrack()
    BEAT = mid_dict["beat"]

    # Move events from old PART x to PLASTIC x, which is now a new PART x

    for inst in ["GUITAR", "BASS", "DRUMS"]:
        total_time = 0
        last_note = 0
        last_event = 0
        part = f"part {inst.lower()}"
        anim_notes = globals()[f"PART_{inst}_ANIM_NOTES"]
        anim_events = globals()[f"PART_{inst}_ANIM_EVENTS"]
        for x in mid_dict[part]:
            total_time += x.time
            if x.type == "text":
                if x.text == "[guitar]" or x.text == "[keytar]":
                    continue
                if x.text == "[idle_mellow]":
                    x.text = "[idle]"
                append_event(anim_events, x.text, total_time - last_event)
                last_event = total_time
            elif x.type == "note_on" or x.type == "note_off":
                if x.note < 60:
                    append_note(anim_notes, x.note, x.type, x.velocity, total_time - last_note)
                    last_note = total_time

    # Make sections
    total_time = 0
    last_event = 0
    section_count = {}
    for x in mid_dict["section"]:
        total_time += x.time
        if x.type == "text":
            if x.text.startswith("[") and x.text.endswith("]"):
                text_event = x.text[1:-1]
                if text_event not in section_count:
                    section_count[text_event] = 1
                else:
                    section_count[text_event] += 1
                append_event(SECTIONS, f"[section {text_event}_{section_count[text_event]}]", total_time - last_event)
                last_event = total_time

    # Merge MIDI Tracks and add to new_midi
    PART_GUITAR = merge_tracks([PART_GUITAR_NOTES, PART_GUITAR_ANIM_EVENTS, PART_GUITAR_ANIM_NOTES])
    PART_GUITAR.name = "PART GUITAR"
    new_midi.add_track()
    new_midi.tracks[-1] = PART_GUITAR

    PART_BASS = merge_tracks([PART_BASS_NOTES, PART_BASS_ANIM_NOTES, PART_BASS_ANIM_EVENTS])
    PART_BASS.name = "PART BASS"
    new_midi.add_track()
    new_midi.tracks[-1] = PART_BASS

    PART_DRUMS = merge_tracks([PART_DRUMS_NOTES, PART_DRUMS_ANIM_NOTES, PART_DRUMS_ANIM_EVENTS])
    PART_DRUMS.name = "PART DRUMS"
    new_midi.add_track()
    new_midi.tracks[-1] = PART_DRUMS

    new_midi.add_track()
    new_midi.tracks[-1] = PART_VOCALS

    NEW_EVENTS = merge_tracks([EVENTS, SECTIONS])
    NEW_EVENTS.name = "EVENTS"
    new_midi.add_track()
    new_midi.tracks[-1] = NEW_EVENTS

    new_midi.add_track()
    new_midi.tracks[-1] = BEAT

    if not output.endswith(".mid"):
        output = os.path.join(output, os.path.splitext(os.path.basename(os.path.abspath(sys.argv[1])))[0] + "_RB.mid")

    new_midi.save(output)
    # raise Exception
    """for x in new_midi.tracks[0]:
        print(x)"""
