import numpy as np

from pynwb.testing import TestCase

from ndx_sound import AcousticWaveformSeries


class TestAcousticWaveformSeriesConstructor(TestCase):

    def test_constructor(self):
        """Test that the constructor for TetrodeSeries sets values as expected."""

        valid_shapes = (
            (100,),
            (100, 1),
            (100, 2),
        )
        for data in (np.random.randint(1000, size=size) for size in valid_shapes):
            acoustic_waveform_series = AcousticWaveformSeries(
                name="acoustic_stimulus",
                data=data,
                rate=42000.,
                description="acoustic_stimulus",
            )

            self.assertEqual(acoustic_waveform_series.name, 'acoustic_stimulus')
            self.assertEqual(acoustic_waveform_series.description, 'acoustic_stimulus')
            np.testing.assert_array_equal(acoustic_waveform_series.data, data)
            self.assertEqual(acoustic_waveform_series.rate, 42000.)
            self.assertEqual(acoustic_waveform_series.unit, "n.a.")