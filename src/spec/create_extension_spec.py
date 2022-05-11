# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBDatasetSpec, NWBAttributeSpec
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
            )
        ],
    )

    new_data_types = [acoustic_waveform_series]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'spec'))
    export_spec(ns_builder, new_data_types, output_dir)
    print('Spec files generated. Please make sure to rerun `pip install .` to load the changes.')


if __name__ == '__main__':
    # usage: python create_extension_spec.py
    main()
