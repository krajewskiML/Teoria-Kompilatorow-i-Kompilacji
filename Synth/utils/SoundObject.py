from pyo import *

SINE = "Sine"
LFO_NAME = "LFO"
SUPERSAW = "SuperSaw"
FASTSINE = "FastSine"
RCOSC = "RCOsc"
PAUSE = "Pause"
SYNTH_NAMES = [SINE, LFO_NAME, SUPERSAW, FASTSINE, RCOSC, PAUSE]
SOUND = "sound"
SYNTH = "synth"
SOUND_TYPES = [SOUND, SYNTH]


class SoundObject:
    def __init__(self, **kwargs):
        # from file -> filename
        self.params = kwargs
        if "filename" in kwargs:
            filename = os.path.join("source", kwargs["filename"][1:-1])
            self.sound = SfPlayer(filename)
        # synth -> type, parameters
        else:
            synth_type = kwargs["type"]
            synth_class = eval(synth_type)
            synth_properties = kwargs["properties"]
            self.sound = synth_class(**synth_properties)

        if kwargs["duration"] <= 0:
            raise ValueError("Length of sound must be greater then 0!")
        self.duration = kwargs["duration"]

    def __copy__(self):
        return SoundObject(**self.params)

    def __mul__(self, other):
        if other < 0:
            raise ValueError("You must multiply sound objects by non negative number")
        if isinstance(other, int):
            return [self] * other
        elif isinstance(other, float):
            whole = int(other)
            partial = other - whole
            partial_sound = self.__copy__()
            partial_sound.duration *= partial
            return (self * whole) + [partial_sound]

# dicto = {
#     "type": "Sine",
#     "properties": {
#         "freq": 100,
#         "mul": 3,
#         "add": 9,
#     },
#     "duration": 10
# }
# s = Server().boot()
# a = SoundObject(**dicto)

# b = a * 5.5
#
# c = 9
# b = 9
# # b =- 0

