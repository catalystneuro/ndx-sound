# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBAttributeSpec, NWBLinkSpec
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
            NWBDatasetSpec(
                name="location",
                doc="Location of the speaker",
                dtype="text",
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
            NWBDatasetSpec(
                name="location",
                doc="Location of the microphone",
                dtype="text",
            ),
        ]
    )

    acoustic_stimulus_series = NWBGroupSpec(
        neurodata_type_def='AcousticStimulusSeries',
        neurodata_type_inc='AcousticWaveformSeries',
        doc="Waveform of acoustic stimulus",
        links=[
            NWBLinkSpec(
                name="speaker",
                target_type="Speaker",
                doc="Link to the speaker device used for the stimulus.",
            )
        ]
    )

    acoustic_recording_series = NWBGroupSpec(
        neurodata_type_def='AcousticRecordingSeries',
        neurodata_type_inc='AcousticWaveformSeries',
        doc="Waveform of acoustic recording",
        links=[
            NWBLinkSpec(
                name="microphone",
                target_type="Microphone",
                doc="Link to the microphone device used for the recording.",
            )
        ]
    )

    new_data_types = [speaker, microphone, acoustic_waveform_series, acoustic_stimulus_series, acoustic_recording_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
