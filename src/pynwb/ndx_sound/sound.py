from hdmf.utils import docval, popargs
from pynwb import get_class

MicrophoneTable = get_class("MicrophoneTable", "ndx-sound")
SpeakerTable = get_class("SpeakerTable", "ndx-sound")


@docval(
    {"name": "region", "type": list, "doc": "the indices of the MicrophoneTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_microphone_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "microphone_table_region"
    return super(MicrophoneTable, self).create_region(name=name, region=region, description=description)


@docval(
    {"name": "region", "type": list, "doc": "the indices of the SpeakerTable"},
    {"name": "description", "type": str, "doc": "a brief description of what these table entries represent"},
)
def create_speaker_table_region(self, **kwargs):
    region, description = popargs("region", "description", kwargs)
    name = "speaker_table_region"
    return super(SpeakerTable, self).create_region(name=name, region=region, description=description)


MicrophoneTable.create_microphone_table_region = create_microphone_table_region
SpeakerTable.create_speaker_table_region = create_speaker_table_region