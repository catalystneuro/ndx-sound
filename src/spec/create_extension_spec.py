# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBAttributeSpec, NWBLinkSpec, NWBRefSpec
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec, NWBAttributeSpec


def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        doc="""Represent acoustic stimuli and responses""",
        name="""ndx-sound""",
        version="""0.1.0""",
        author=list(map(str.strip, """Ben Dichter""".split(','))),
        contact=list(map(str.strip, """ben.dichter@catalystneuro.com""".split(',')))
    )

    # as in which namespace they are found.
    # this is similar to specifying the Python modules that need to be imported
    # to use your new data types.
    # all types included or used by the types specified here will also be
    # included.
    ns_builder.include_type('TimeSeries', namespace='core')
    ns_builder.include_type('Device', namespace='core')
    ns_builder.include_type('DynamicTable', namespace='core')
    ns_builder.include_type('DynamicTableRegion', namespace='core')
    ns_builder.include_type('LabMetaData', namespace='core')

    # see https://pynwb.readthedocs.io/en/latest/extensions.html#extending-nwb
    # for more information
    acoustic_waveform_series = NWBGroupSpec(
        neurodata_type_def='AcousticWaveformSeries',
        neurodata_type_inc='TimeSeries',
        doc="single or multi-channel acoustic series",
        datasets=[
            NWBDatasetSpec(
                name="data",
                doc="acoustic waveform",
                dtype='int16',
                shape=((None,), (None, 1), (None, 2)),
                dims=(("time",), ("time", "channel"), ("time", "channels")),
                attributes=[
                    NWBAttributeSpec(
                        name="unit",
                        doc="SI unit of data",
                        dtype="text",
                        value="n.a.",
                    )
                ]
            ),
            NWBDatasetSpec(
                name="starting_time",
                default_value=0.,
                quantity=1,
                dtype="float",
                doc="starting time of acoustic waveform.",
                attributes=[
                    NWBAttributeSpec(
                        name="rate",
                        required=True,
                        dtype="float",
                        doc="sampling frequency of acoustic waveform.",
                    )
                ]
            )
        ],
    ) 

    speaker = NWBGroupSpec(
        neurodata_type_def='Speaker',
        neurodata_type_inc='Device',
        doc="Speaker device used for acoustic stimuli",
        datasets=[
            NWBDatasetSpec(
                name="frequency_range_in_hz",
                doc="Frequency range of the speaker in Hz",
                dtype="float",
                shape=(2,),
            ),
            NWBDatasetSpec(
                name="sensitivity_in_db",
                doc="Sensitivity of the speaker in dB at 1m",
                dtype="float",
            ),
        ]
    )

    microphone = NWBGroupSpec(
        neurodata_type_def='Microphone',
        neurodata_type_inc='Device',
        doc="Microphone device used for acoustic recordings",
        datasets=[
            NWBDatasetSpec(
                name="frequency_range_in_hz",
                doc="Frequency range of the microphone in Hz",
                dtype="float",
                shape=(2,),
            ),
            NWBDatasetSpec(
                name="sensitivity_in_mv_per_pa",
                doc="Sensitivity of the microphone in mV/Pa",
                dtype="float",
            ),
        ]
    )

    audio_interface = NWBGroupSpec(
        neurodata_type_def='AudioInterface',
        neurodata_type_inc='Device',
        doc="Audio interface device used for acoustic recordings",
        datasets=[
            NWBDatasetSpec(
                name="signal_to_noise_ratio_in_db",
                doc="Signal-to-noise ratio of the audio interface in dB",
                dtype="float",
            ),
            NWBDatasetSpec(
                name="channel_separation_in_db",
                doc="Channel separation of the audio interface in dB",
                dtype="float",
            ),
        ]
    )

    microphone_table = NWBGroupSpec(
        neurodata_type_def="MicrophoneTable",
        neurodata_type_inc="DynamicTable",
        doc="Extends DynamicTable to hold metadata on the auditory recording system.",
        datasets=[
            NWBDatasetSpec(
                name="location",
                doc="Location of microphone.",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="microphone",
                doc="Link to microphone object.",
                dtype=NWBRefSpec(target_type='Device', reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="audio_interface",
                doc="Link to audio interface object.",
                dtype=NWBRefSpec(target_type='Device', reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
        ],
    )

    speaker_table = NWBGroupSpec(
        neurodata_type_def="SpeakerTable",
        neurodata_type_inc="DynamicTable",
        doc="Extends DynamicTable to hold metadata on the auditory stimulus system.",
        datasets=[
            NWBDatasetSpec(
                name="location",
                doc="Location of speaker.",
                dtype="text",
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="speaker",
                doc="Link to speaker object.",
                dtype=NWBRefSpec(target_type='Device', reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
            NWBDatasetSpec(
                name="audio_interface",
                doc="Link to audio interface object.",
                dtype=NWBRefSpec(target_type='Device', reftype="object"),
                shape=(None,),
                neurodata_type_inc="VectorData",
            ),
        ],
    )

    acoustic_stimulus_series = NWBGroupSpec(
        neurodata_type_def='AcousticStimulusSeries',
        neurodata_type_inc='AcousticWaveformSeries',
        doc="Waveform of acoustic stimulus",
        datasets=[
            NWBDatasetSpec(
                name="speaker_table_region",
                doc="References row(s) of SpeakTable.",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            )
        ]
    )

    acoustic_recording_series = NWBGroupSpec(
        neurodata_type_def='AcousticRecordingSeries',
        neurodata_type_inc='AcousticWaveformSeries',
        doc="Waveform of acoustic recording",
        datasets=[
            NWBDatasetSpec(
                name="microphone_table_region",
                doc="References row(s) of MicrophoneTable.",
                neurodata_type_inc="DynamicTableRegion",
                quantity="?",
            )
        ]   
    )

    acoustic_lab_meta_data = NWBGroupSpec(
        neurodata_type_def="AcousticLabMetaData",
        neurodata_type_inc="LabMetaData",
        doc="Extends LabMetaData to hold all acoustic metadata.",
        groups=[
            NWBGroupSpec(
                neurodata_type_inc="MicrophoneTable",
                doc="Table of microphones used for acoustic recordings.",
                quantity="?",
            ),
            NWBGroupSpec(
                neurodata_type_inc="SpeakerTable",
                doc="Table of speakers used for acoustic stimuli.",
                quantity="?",
            ),
        ],
    )

    new_data_types = [
        speaker,
        microphone,
        audio_interface,
        microphone_table,
        speaker_table,
        acoustic_lab_meta_data,
        acoustic_waveform_series,
        acoustic_stimulus_series,
        acoustic_recording_series,
    ]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
