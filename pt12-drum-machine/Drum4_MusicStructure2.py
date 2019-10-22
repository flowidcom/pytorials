from DrumMachine import waveOf, playTracks

verse = [
    (waveOf("beats/bass.wav"), "X...X...X...X..."),
    (waveOf("beats/snare.wav"), "..............X."),
    (waveOf("beats/hh_closed.wav"), "X.XXX.XXX.X.X.X."),
    (waveOf("beats/agogo_high.wav"), "..............XX")
]

chorus = [
    (waveOf("beats/bass.wav"), "X...X...X...X..."),
    (waveOf("beats/snare.wav"), "....X.......X..."),
    (waveOf("beats/hh_closed.wav"), "X.XXX.XXX.XX..X."),
    (waveOf("beats/tom4.wav"), "...........X...."),
    (waveOf("beats/tom2.wav"), "..............X."),
]

bpm = 120
playTracks(bpm, verse, 8)
playTracks(bpm, chorus, 16)
playTracks(bpm, verse, 8)
playTracks(bpm, chorus, 16)
