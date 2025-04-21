import numpy as np
import pytest
import os
from pynwb import NWBHDF5IO, NWBFile
from datetime import datetime

from ndx_sound import AcousticWaveformSeries
from ndx_sound.testing.mock import mock_AcousticWaveformSeries


def test_constructor():
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

        assert acoustic_waveform_series.name == "acoustic_stimulus"
        assert acoustic_waveform_series.description == "acoustic stimulus description"
        np.testing.assert_array_equal(acoustic_waveform_series.data, data)
        assert acoustic_waveform_series.rate == 42000.0
        assert acoustic_waveform_series.unit == "n.a."


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


def test_roundtrip(tmp_path):
    """Test roundtrip serialization/deserialization."""
    # Create NWBFile
    nwbfile = NWBFile(
        session_description="Test session",
        identifier="TEST123",
        session_start_time=datetime.now(),
    )
    
    # Create test data
    acoustic_waveform_series = mock_AcousticWaveformSeries(
        data_shape=(100, 2),
    )
    nwbfile.add_acquisition(acoustic_waveform_series)
    
    # Write to file
    test_path = tmp_path / "test.nwb"
    with NWBHDF5IO(test_path, mode="w") as io:
        io.write(nwbfile)
    
    # Read from file and verify
    with NWBHDF5IO(test_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        read_acoustic_waveform_series = read_nwbfile.acquisition[acoustic_waveform_series.name]
        
        # Check key attributes
        assert read_acoustic_waveform_series.name == acoustic_waveform_series.name
        assert read_acoustic_waveform_series.description == acoustic_waveform_series.description
        assert read_acoustic_waveform_series.rate == acoustic_waveform_series.rate
        np.testing.assert_array_equal(read_acoustic_waveform_series.data, acoustic_waveform_series.data)


def test_acoustic_waveform_widget_with_time_window_controller():
    """Test the AcousticWaveformWidget with a time window controller."""
    # Skip test if nwbwidgets or librosa is not installed
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
