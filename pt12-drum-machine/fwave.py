import copy
import math
import numpy as np
import warnings
import subprocess
from wave import open as open_wave
import os
import logging as logger

import matplotlib.pyplot as pyplot

FRAMERATE = 44100

try:
    from IPython.display import Audio
except Exception:
    logger.debug("Can't import Audio from IPython.display Wave.make_audio() will not work.")


class FWave:
    def __init__(self, ys, ts=None, framerate=None):
        """Initializes the wave.

        ys: wave array
        ts: array of times
        framerate: samples per second
        """
        self.ys = np.asanyarray(ys)
        self.framerate = framerate if framerate is not None else FRAMERATE

        if ts is None:
            self.ts = np.arange(len(ys)) / self.framerate
        else:
            self.ts = np.asanyarray(ts)

    def copy(self):
        """Makes a copy.

        Returns: new Wave
        """
        return copy.deepcopy(self)

    def __len__(self):
        return len(self.ys)

    @property
    def duration(self):
        """Duration (property).

        returns: float duration in seconds
        """
        return len(self.ys) / self.framerate

    def __add__(self, other):
        """Adds two waves elementwise.

        other: Wave

        returns: new Wave
        """
        if other == 0:
            return self

        assert self.framerate == other.framerate

        # make an array of times that covers both waves
        start = min(self.start, other.start)
        end = max(self.end, other.end)
        n = int(round((end - start) * self.framerate)) + 1

        # initially set to 0
        ys = np.zeros(n)
        ts = start + np.arange(n) / self.framerate

        newWave = FWave(ys, ts, self.framerate);
        newWave.addWave(self)
        newWave.addWave(other)

        return newWave

    def addWave(self, other):
        # internal method that assumes that the self has a larger time span than the other
        logger.debug("Adding wave. Current: start: %0.3f, end: %0.3f, New: start: %0.3f",
                     self.start * 1000, self.end * 1000, other.start * 1000)
        i = findIndex(other.start, self.ts)
        diff = self.ts[i] - other.start
        if diff > 0.1:  # at most 0.1 secs apart
            logger.info("Time does not line up. Self timestamp is %0.3f, new wave start is: %0.3f",
                        self.ts[i], other.start)
        j = i + len(other)
        self.ys[i:j] += other.ys

    def __or__(self, other):
        """Concatenates two waves.

        other: Wave

        returns: new Wave
        """
        if self.framerate != other.framerate:
            raise ValueError('Wave.__or__: framerates do not agree')

        ys = np.concatenate((self.ys, other.ys))
        return FWave(ys, framerate=self.framerate)

    def normalize(self, amp=1.0):
        """Normalizes the signal to the given amplitude.

        amp: float amplitude
        """
        high, low = abs(max(self.ys)), abs(min(self.ys))
        self.ys = amp * self.ys / max(high, low)

    @property
    def start(self):
        return self.ts[0] if len(self.ts) > 0 else 0

    @property
    def end(self):
        return self.ts[-1] if len(self.ts > 0) else 0

    def find_index(self, t):
        """Find the index corresponding to a given time."""
        n = len(self)
        start = self.start
        end = self.end
        i = round((n - 1) * (t - start) / (end - start))
        return int(i)

    def plot(self, style='', **options):
        pyplot.plot(self.ts, self.ys, style, **options)

    def shift(self, shift):
        """Shifts the wave left or right in time.

        shift: float time shift
        """
        self.ts += shift

    def write(self, filename='sound.wav'):
        """Write a wave file.

        filename: string
        """
        nchannels = 1
        sampwidth = 2  # 16 bits
        bits = sampwidth * 8;
        bound = 2 ** (bits - 1) - 1

        fp = open_wave(filename, 'w')
        fp.setnchannels(nchannels)
        fp.setsampwidth(sampwidth)
        fp.setframerate(self.framerate)

        zs = quantize(self.ys, bound, np.int16)
        fp.writeframes(zs.tostring())
        fp.close()

    def play(self, filename='sound.wav', player='afplay'):
        """Plays a wave file.

        filename: string
        """
        self.write(filename)
        playWave(filename, player)

    def __str__(self):
        return "Time: " + str(list(map(lambda t: "%0.3f" % t, self.ts))) \
               + os.linesep \
               + "Vals: " + str(list(map(lambda y: "%0.3f" % y, self.ys)));


### Class Ends

def readWave(filename='sound.wav'):
    """Reads a wave file.

    filename: string

    returns: Wave
    """
    fp = open_wave(filename, 'r')

    nchannels = fp.getnchannels()
    nframes = fp.getnframes()
    sampwidth = fp.getsampwidth()
    framerate = fp.getframerate()

    z_str = fp.readframes(nframes)

    fp.close()

    dtype_map = {1: np.int8, 2: np.int16, 3: 'special', 4: np.int32}
    if sampwidth not in dtype_map:
        raise ValueError('sampwidth %d unknown' % sampwidth)

    if sampwidth == 3:
        xs = np.fromstring(z_str, dtype=np.int8).astype(np.int32)
        ys = (xs[2::3] * 256 + xs[1::3]) * 256 + xs[0::3]
    else:
        ys = np.fromstring(z_str, dtype=dtype_map[sampwidth])

    # if it's in stereo, just pull out the first channel
    if nchannels == 2:
        ys = ys[::2]

    # ts = np.arange(len(ys)) / framerate
    wave = FWave(ys, framerate=framerate)
    wave.normalize()
    return wave


def writeWave(wave, filename):
    wave.write(filename)


def playWave(filename='sound.wav', player='afplay'):
    """Plays a wave file.

    filename: string
    player: string name of executable that plays wav files
    """

    cmd = '%s %s' % (player, filename)
    popen = subprocess.Popen(cmd, shell=True)
    popen.communicate()


def findIndex(x, xs):
    """Find the index corresponding to a given value in an array."""
    n = len(xs)
    start = xs[0]
    end = xs[-1]
    i = round((n - 1) * (x - start) / (end - start))
    return int(i)


def quantize(ys, bound, dtype):
    """Maps the waveform to quanta.

    ys: wave array
    bound: maximum amplitude
    dtype: numpy data type of the result

    returns: quantized signal
    """
    if max(ys) > 1 or min(ys) < -1:
        ys = normalize(ys)

    zs = (ys * bound).astype(dtype)
    return zs


def initWave(duration=1):
    return FWave(np.zeros(int(duration * FRAMERATE)))


def normalize(ys, amp=1.0):
    """Normalizes a wave array so the maximum amplitude is +amp or -amp.

    ys: wave array
    amp: max amplitude (pos or neg) in result

    returns: wave array
    """
    high, low = abs(max(ys)), abs(min(ys))
    return amp * ys / max(high, low)


def makeBeat(file, phrase, bpm, beatsPerMeasure=4):
    beatLength = 60 / bpm / beatsPerMeasure
    track = initWave(beatLength * len(phrase))

    bip = readWave(file)

    for step in range(len(phrase)):
        logger.debug("Step %d, adding bip %s with duration: %d", step, file, bip.duration)

        playNote = phrase[step % 16] == 'X'
        if playNote:
            # copy the bit to the track
            stepWave = bip.copy()
            stepWave.shift(step * beatLength);
            logger.debug("Bip start: %0.3f, duration %0.3f", stepWave.start, bip.duration)
            track = track + stepWave

    return track


def repeatWave(wave, n):
    result = wave;
    for i in range(n - 1):
        result = result | wave;
    return result;


def makeAudio(wave):
    """Makes an IPython Audio object.
    """
    audio = Audio(data=wave.ys.real, rate=wave.framerate)
    return audio
