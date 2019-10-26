import time
import simpleaudio as sa


def waveOf(file):
    return sa.WaveObject.from_wave_file(file)


bass_wave = sa.WaveObject.from_wave_file("beats/bass.wav")
snare_wave = sa.WaveObject.from_wave_file("beats/snare.wav")
hh_closed_wave = sa.WaveObject.from_wave_file("beats/hh_closed.wav")


def playTracks(bpm, tracks, barsToPlay):
    quartersPerBar = 4
    beat = 60 / bpm / quartersPerBar  # 16th note expressed in seconds
    step = 0
    while step < barsToPlay * quartersPerBar:
        beatStart = time.time()
        for track in tracks:
            wave = track[0]
            playNote = track[1][step % 16] == 'X'
            if playNote:
                wave.play()
        playTime = time.time() - beatStart
        time.sleep(beat - playTime)
        step = step + 1


verse = [
    (waveOf("beats/bass.wav"), "X...X...X...X..."),
    (waveOf("beats/snare.wav"), "....X.......X..."),
    (waveOf("beats/hh_closed.wav"), "X.X.X.X.XX.XXXXX")
]

chorus = [
    (waveOf("beats/bass.wav"), "XXXXXXXXXXXXX..."),
    (waveOf("beats/snare.wav"), "....X.......X..."),
    (waveOf("beats/hh_closed.wav"), "X.X.X.X.XX.XXXXX"),
    (waveOf("beats/conga_low.wav"), "X.....X.X..X...."),
    (waveOf("beats/conga_high.wav"), "....X....X......"),
    (waveOf("beats/cowbell_high.wav"), "...............X")
]

bpm = 120
playTracks(bpm, verse, 16)
playTracks(bpm, chorus, 16)
playTracks(bpm, verse, 16)
playTracks(bpm, chorus, 16)
