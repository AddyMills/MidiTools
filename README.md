# MidiTools
Scripts that modify MIDI files in some way

## Fortnite Festival to Rock Band

A script to move all the events from Fortnite standards to to Rock Band. This includes:
- Moving all animation notes from PART X to PLASTIC X
- Moving all text events from PART X to PLASTIC X
  - [idle_mellow] also gets renamed to [idle]
- Deleting the PART X tracks and renaming PLASTIC X to PART X
- Making sections based on the SECTION track. It currently reads the sections found in there and appends the current count of that event
- File will be saved in the same folder as the input with "_RB" appended to the name or a custom output

Usage:
- Run the script with a midi file as the first argument
- Optionally: Enter in a folder or file path for the output.
  - If a folder is entered, or a file that does not end in .mid, the output will be the input filename with "_RB" appended to it, but placed in the folder of the output argument

## LyricsNotes

Add notes to lyrics events. Open the script and modify the "toAdd" variable to add your own track names.

Usage: Run the script with a MIDI file as its only variable.

## MergeMidi

Combines two MIDI tracks for the purposes of merging Rock Band MIDIs with on-disc upgrades. Deletes any tracks from the first MIDI that are shared between the input and replaces them with the tracks from the second MIDI.

Usage: Run the script with the main MIDI as the first argument and the upgrades midi as the second argument. It will insert the merged MIDI into a folder named "output" found in the same folder as the script.

## ReadMidi

Reads all MIDI files in the same folder as the script and creates a text file containing all tracks in each MIDI file.
