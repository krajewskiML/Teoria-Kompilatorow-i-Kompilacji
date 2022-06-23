from pyo import *

SINE = "Sine"
LFO = "Lfo"
SUPERSAW = "SuperSaw"
FASTSINE = "FastSine"
RCOSC = "RCOsc"
PAUSE = "Pause"
SYNTH_NAMES = [SINE, LFO, SUPERSAW, FASTSINE, RCOSC, PAUSE]
SOUND = "sound"
SYNTH = "synth"
SOUND_TYPES = [SOUND, SYNTH]


class SoundObject:
    def __init__(self, **kwargs):
        # from file -> filename
        if "filename" in kwargs:
            filename = kwargs["filename"]
            self.sound = SfPlayer(filename)
        # synth -> type, parameters
        else:
            synth_type = kwargs["type"]
            synth_class = eval(synth_type)
            synth_properties = kwargs["properties"]
            self.sound = synth_class(**synth_properties)

#
# dicto = {
#     "type": "Sine",
#     "properties": {
#         "freq": 100,
#         "mul": 3,
#         "add": 9,
#     }
# }
# # dicto2 = {
# #     "filename": "proba.wav"
# # }
s = Server().boot()
# a = SoundObject(**dicto)
#
# b = 9
# # b =- 0

