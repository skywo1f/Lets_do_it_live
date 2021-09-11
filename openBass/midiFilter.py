from mido import MidiFile

mid = MidiFile('zelda-simple.mid', clip=True)
#print(mid)
#for msg in mid.tracks[0]:
#    print(msg)
addTime = 0
singleTrack = []
singleTime = []
for i in range(len(mid.tracks[0])):
    addTime = addTime + mid.tracks[0][i].time
    if str(mid.tracks[0][i]).startswith("note_on"):
        if mid.tracks[0][i].channel == 0:
            singleTrack.append(int(int(mid.tracks[0][i].note)))
            singleTime.append(int(int(addTime)/50))
#print(singleTime)
print(singleTrack)
