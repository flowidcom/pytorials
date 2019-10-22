import time
import simpleaudio as sa

def playSound(file):
    wave_obj = sa.WaveObject.from_wave_file(file)
    play_obj = wave_obj.play()

def debug(*args):
    print(args)


phrase = "X...X...X...X..."

bpm = 120
beatsPerMeasure = 4
beat = 60 / bpm / beatsPerMeasure  # 16th note expressed in seconds

barsToPlay = 2
step = 1
while step < barsToPlay * len(phrase):
    playNote = phrase[step % 16] == 'X'
    if playNote:
        playSound("beats/bass.wav")
    time.sleep(beat)
    step = step + 1
