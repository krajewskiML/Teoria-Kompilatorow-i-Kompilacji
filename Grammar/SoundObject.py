from pyo import *


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


dicto = {
    "type": "Sine",
    "properties": {
        "freq": 100,
        "mul": 3,
        "add": 9,
    }
}
dicto2 = {
    "filename": "proba.wav"
}
s = Server().boot()
a = SoundObject(**dicto2)
b =- 0

