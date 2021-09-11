from mido import MidiFile

mid = MidiFile('daftPunk.mid', clip=True)
print(mid)
for msg in mid.tracks[0]:
    print(msg)
