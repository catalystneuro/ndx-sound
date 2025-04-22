import numpy as np
from pynwb.testing import AcquisitionH5IOMixin, TestCase
import pytest

from ndx_sound import AcousticWaveformSeries
from ndx_sound.testing.mock import mock_AcousticWaveformSeries


class TestAcousticWaveformSeriesConstructor(TestCase):
    def test_constructor(self):
        """Test that the constructor for AcousticWaveformSeries sets values as expected."""

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


class TestAcousticWaveformSeriesRoundtripPyNWB(AcquisitionH5IOMixin, TestCase):
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
        nwbwidgets = pytest.importorskip("nwbwidgets", reason="nwbwidgets not installed")
        librosa = pytest.importorskip("librosa", reason="librosa not installed")
        from nwbwidgets.controllers import StartAndDurationController
        from ndx_sound.widgets import AcousticWaveformWidget

        data = np.random.randint(1000, size=(10000,))
        acoustic_waveform_series = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=data,
            rate=42000.0,
            description="acoustic stimulus description",
        )

        controller = StartAndDurationController(tmin=0.1, tmax=0.3)
        AcousticWaveformWidget(acoustic_waveform_series, controller)


def test_constructor_with_custom_unit():
    """Test that the constructor accepts a custom unit."""
    data = np.random.randint(1000, size=(100,))
    custom_unit = "mV"
    
    acoustic_waveform_series = AcousticWaveformSeries(
        name="acoustic_stimulus",
        data=data,
        rate=42000.0,
        description="acoustic stimulus description",
        unit=custom_unit,
    )
    
    assert acoustic_waveform_series.unit == custom_unit


def test_constructor_with_starting_time():
    """Test that the constructor accepts a custom starting time."""
    data = np.random.randint(1000, size=(100,))
    starting_time = 10.5
    
    acoustic_waveform_series = AcousticWaveformSeries(
        name="acoustic_stimulus",
        data=data,
        rate=42000.0,
        description="acoustic stimulus description",
        starting_time=starting_time,
    )
    
    assert acoustic_waveform_series.starting_time == starting_time


def test_mock_acoustic_waveform_series():
    """Test the mock_AcousticWaveformSeries function."""
    # Test with default parameters
    aws = mock_AcousticWaveformSeries()
    assert aws.name == "AcousticWaveformSeries"
    assert aws.description == "acoustic stimulus description"
    assert aws.rate == 42000.0
    assert aws.unit == "n.a."
    assert aws.data.shape == (100,)
    
    # Test with custom parameters
    custom_name = "custom_name"
    custom_shape = (200, 2)
    custom_rate = 48000.0
    custom_description = "custom description"
    
    aws = mock_AcousticWaveformSeries(
        name=custom_name,
        data_shape=custom_shape,
        rate=custom_rate,
        description=custom_description,
    )
    
    assert aws.name == custom_name
    assert aws.description == custom_description
    assert aws.rate == custom_rate
    assert aws.data.shape == custom_shape