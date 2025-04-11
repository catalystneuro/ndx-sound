import os
from pynwb import load_namespaces, get_class

# Set path of the namespace.yaml file to the expected install location
ndx_sound_specpath = os.path.join(
    os.path.dirname(__file__), "spec", "ndx-sound.namespace.yaml"
)

# If the extension has not been installed yet but we are running directly from
# the git repo
if not os.path.exists(ndx_sound_specpath):
    ndx_sound_specpath = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "..",
            "spec",
            "ndx-sound.namespace.yaml",
        )
    )

# Load the namespace
load_namespaces(ndx_sound_specpath)

# new_data_types = [speaker, microphone, acoustic_waveform_series, acoustic_stimulus_series, acoustic_recording_series]
# Make them accessible at the package level
AcousticWaveformSeries = get_class("AcousticWaveformSeries", "ndx-sound")
Speaker = get_class("Speaker", "ndx-sound")
Microphone = get_class("Microphone", "ndx-sound")
AudioInterface = get_class("AudioInterface", "ndx-sound")
AcousticLabMetaData = get_class("AcousticLabMetaData", "ndx-sound")
AcousticStimulusSeries = get_class("AcousticStimulusSeries", "ndx-sound")
AcousticRecordingSeries = get_class("AcousticRecordingSeries", "ndx-sound")

from .sound import MicrophoneTable, SpeakerTable


# set default value for data_unit
for i, arg in enumerate(AcousticWaveformSeries.__init__.__docval__["args"]):
    if arg["name"] == "unit":
        AcousticWaveformSeries.__init__.__docval__["args"][i].update(default="n.a.")
        continue
