from pyo import *
from typing import Union, List
from Synth.utils.SoundObject import SoundObject


class MusicHandler:
    def __init__(self, nchannel, dur, filename: str):
        self.nchannel = nchannel
        self.dur = dur
        self.server = Server(audio="offline", nchnls=self.nchannel).boot()
        self.server.recordOptions(filename=filename, dur=self.dur, quality=0.1)

        self.channels = {
            idx: []
            for idx in range(self.nchannel)
        }

    def add_to_channel(self, channel: int, sounds: Union[SoundObject, List[SoundObject]]):
        if isinstance(sounds, list):
            self.channels[channel].extend(sounds)
        else:
            self.channels[channel].append(sounds)

    def compile(self):
        listos = []
        for channel, list_of_sounds in self.channels.items():
            delay = 0
            for sound in list_of_sounds:
                listos.append(sound.__copy__())
                listos[-1].sound.out(channel, delay=delay, dur=sound.duration)
                delay += sound.duration

        self.server.start()
        self.server.shutdown()
