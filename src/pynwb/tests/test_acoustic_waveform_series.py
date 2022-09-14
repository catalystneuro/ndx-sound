import numpy as np
from pynwb.testing import AcquisitionH5IOMixin, TestCase
from nwbwidgets.controllers import StartAndDurationController

from pynwb.testing import TestCase

from ndx_sound import AcousticWaveformSeries
from ndx_sound.widgets import AcousticWaveformWidget


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


class TestAcousticWaveformSeriesWidget(TestCase):
    def test_AcousticWaveformWidget_with_time_window_controller(self):
        data = np.random.randint(1000, size=(10000,))
        acoustic_waveform_series = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=data,
            rate=42000.0,
            description="acoustic stimulus description",
        )

        controller = StartAndDurationController(tmin=0.1, tmax=0.3)
        AcousticWaveformWidget(acoustic_waveform_series, controller)
