## Final Project for Spring 2024 Math 242 at Duke University

from mido import MidiFile, MidiTrack, Message
import random
def get_mappings(song, n):
    mapping = {}
    i = 0
    while i < len(song) - n:
        sequence = tuple(song[i:i+n])
        if sequence not in mapping:
            mapping[sequence] = []
        mapping[sequence].append(tuple(song[i+1:i+n+1]))
        i += 1
    return mapping
#print(get_mappings(song, 2))
# Load the MIDI file
midi_path = "/Users/johnbloch/Desktop/songs.mid"
midi_file = MidiFile(midi_path)

# Extracting notes from the MIDI file
song = []
for track in midi_file.tracks:
    for msg in track:
        if msg.type == 'note_on' and msg.velocity > 0:
            song.append(msg.note)
print(song)

markov_chain = get_mappings(song, 2)

# Initialize MIDI composition
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Start with a random state
starting_state = random.choice(list(markov_chain.keys()))
time = 0  # Initialize time for the  first note
for note in starting_state:
    track.append(Message("note_on", note=note, velocity=64, time=0))  # Start immediately
    track.append(Message("note_on", note=note, velocity=0, time=100))  # Note off after 100 ticks

current_state = starting_state
while time < 50000:
    if current_state not in list(markov_chain.keys()):
        current_state = random.choice(list(markov_chain.keys()))
    current_state = random.choice(markov_chain[current_state])
    note = current_state[-1]
    # Note on right after the last note off
    track.append(Message("note_on", note=note, velocity=64, time=0))
    # Note off 100 ticks later
    track.append(Message("note_on", note=note, velocity=0, time=100))
    time += 100  # Increment total time by the duration of the note

mid.save('/Users/johnbloch/Desktop/output.mid')
