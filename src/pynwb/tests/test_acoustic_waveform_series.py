import numpy as np
from pynwb.testing import AcquisitionH5IOMixin, TestCase

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
                rate=42000.0,
                description="acoustic stimulus description",
            )

            self.assertEqual(acoustic_waveform_series.name, "acoustic_stimulus")
            self.assertEqual(
                acoustic_waveform_series.description, "acoustic stimulus description"
            )
            np.testing.assert_array_equal(acoustic_waveform_series.data, data)
            self.assertEqual(acoustic_waveform_series.rate, 42000.0)
            self.assertEqual(acoustic_waveform_series.unit, "n.a.")


class TestAcousticWaveforSeriesRoundtripPyNWB(AcquisitionH5IOMixin, TestCase):
    def setUpContainer(self):
        """Return the test AcousticWaveformSeries to read/write"""
        acoustic_waveform_series = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=np.random.randint(1000, size=(100, 2)),
            rate=42000.0,
            description="acoustic stimulus description",
        )
        return acoustic_waveform_series
