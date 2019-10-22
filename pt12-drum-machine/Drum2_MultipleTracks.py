import time
import simpleaudio as sa
import sys

bass_wave = sa.WaveObject.from_wave_file("beats/bass.wav")
snare_wave = sa.WaveObject.from_wave_file("beats/snare.wav")
hh_closed_wave = sa.WaveObject.from_wave_file("beats/hh_closed.wav")

tracks = [
    (bass_wave, "X...X...X...X..."),
    (snare_wave, "....X.......X..."),
    (hh_closed_wave, "X.X.X.X.XX.XXXXX")
]

bpm = 120
beatsPerMeasure = 4
beat = 60 / bpm / beatsPerMeasure  # 16th note expressed in seconds

start=time.time()
barsToPlay = 16
step = 1
adjustment = -4/1000 # millisecs
while step < barsToPlay * beatsPerMeasure:
    beatStart = time.time()
    for track in tracks:
        wave = track[0]
        playNote = track[1][step % 16] == 'X'
        if playNote:
            wave.play()
    startBeatTime = time.time() - beatStart
    time.sleep(beat - startBeatTime + adjustment)
    step = step + 1
end=time.time()
print("Music length: ", end - start)