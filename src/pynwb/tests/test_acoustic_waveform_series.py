import numpy as np
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
                rate=42000.,
                description="acoustic_stimulus",
            )

            self.assertEqual(acoustic_waveform_series.name, 'acoustic_stimulus')
            self.assertEqual(acoustic_waveform_series.description, 'acoustic_stimulus')
            np.testing.assert_array_equal(acoustic_waveform_series.data, data)
            self.assertEqual(acoustic_waveform_series.rate, 42000.)
            self.assertEqual(acoustic_waveform_series.unit, "n.a.")

    def test_AcousticWaveformWidget_without_time_window_controller(self):
        data = np.random.randint(1000, size=(10000,))
        acoustic_waveform_series = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=data,
            rate=42000.,
            description="acoustic_stimulus",
        )

        AcousticWaveformWidget(acoustic_waveform_series)

    def test_AcousticWaveformWidget_with_time_window_controller(self):
        data = np.random.randint(1000, size=(10000,))
        acoustic_waveform_series = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=data,
            rate=42000.,
            description="acoustic_stimulus",
        )

        controller = StartAndDurationController(tmin=0.1, tmax=0.3)
        AcousticWaveformWidget(acoustic_waveform_series, controller)
