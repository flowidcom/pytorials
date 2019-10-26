from fwave import FWave, readWave, playWave, makeBeat, writeWave, repeatWave, makeAudio, initWave
import matplotlib.pyplot as plt

import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

def test1():
    w = readWave("beats/bass.wav")
    w.plot()

    w2 = w.copy()
    w2.shift(2)
    w2.plot()

    song = w + w2
    song.normalize()

    plt.show()

    song.write("song.wav")
    playWave("song.wav", 'afplay')


test1()


def test2():
    song = makeBeat("beats/bass.wav", "X...X...X...X...", 120);
    song.play(player='afplay')


test2()


def test4():
    bpm = 120
    beat1 = makeBeat("beats/bass.wav", "X...X...X...X...", bpm)
    beat2 = makeBeat("beats/snare.wav", "....X.......X...", bpm)
    beat3 = makeBeat("beats/hh_closed.wav", "X.X.X.X.XX.XXXXX", bpm)
    verse = beat1 + beat2 + beat3

    verse2 = repeatWave(verse, 2);

    writeWave(verse2, "sound.wav");
    playWave("sound.wav")


# test4()

verse = {
    "bpm": 120,
    "beats": [
        ("beats/bass.wav", "X...X...X...X..."),
        ("beats/snare.wav", "....X.......X..."),
        ("beats/hh_closed.wav", "X.X.X.X.XX.XXXXX")
    ],
    "times": 2
}

# Chorus:
#   - bass.wav:         XXXXXXXXXXXXX...|XXXXXXXXXXXXX...
#   - snare.wav:        ....X.......X...|....X.......X...
#   - hh_closed.wav:    XXXXXXXXXXXXX...|XXXXXXXXXXXXX...
#   - conga_low.wav:    X.....X.X..X....|X.X....XX.X.....
#   - conga_high.wav:   ....X....X......|................
#   - cowbell_high.wav: ................|..............X.
#

chorus = {
    "bpm": 120,
    "beats": [
        ("beats/bass.wav", "XXXXXXXXXXXXX..."),
        ("beats/snare.wav", "....X.......X..."),
        ("beats/hh_closed.wav", "XXXXXXXXXXXXX..."),
        ("beats/conga_low.wav", "X.....X.X..X...."),
        ("beats/conga_high.wav", "....X....X......"),
        ("beats/cowbell_high.wav", "..............X.")
    ],
    "times": 2
}


def makeBeat2(songdef):
    if isinstance(songdef, list):
        result = initWave()
        for song in songdef:
            result = result | makeBeat2(song)
        return result;
    else:
        bpm = songdef['bpm']
        song = initWave()
        for beatdef in songdef['beats']:
            song = song + makeBeat(beatdef[0], beatdef[1], bpm)
        song = repeatWave(song, int(songdef['times']))
        return song;


s = makeBeat2([verse, chorus, verse, chorus])
s.play()
