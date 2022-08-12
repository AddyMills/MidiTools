# MidiTools
Scripts that modify MIDI files in some way

## LyricsNotes

Add notes to lyrics events. Open the script and modify the "toAdd" variable to add your own track names.

Usage: Run the script with a MIDI file as its only variable.

## MergeMidi

Combines two MIDI tracks for the purposes of merging Rock Band MIDIs with on-disc upgrades. Deletes any tracks from the first MIDI that are shared between the input and replaces them with the tracks from the second MIDI.

Usage: Run the script with the main MIDI as the first argument and the upgrades midi as the second argument. It will insert the merged MIDI into a folder named "output" found in the same folder as the script.

## ReadMidi

Reads all MIDI files in the same folder as the script and creates a text file containing all tracks in each MIDI file.