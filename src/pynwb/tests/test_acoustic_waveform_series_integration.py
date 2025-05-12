"""Integration tests for AcousticWaveformSeries."""

import numpy as np
import pytest
from pynwb import NWBHDF5IO

from ndx_sound.testing.mock import mock_AcousticWaveformSeries
from pynwb.testing.mock.file import mock_NWBFile


def test_add_to_acquisition(tmp_path):
    """Test adding an AcousticWaveformSeries to the acquisition field of an NWBFile."""
    # Create NWBFile
    nwbfile = mock_NWBFile()
    
    # Create test data
    acoustic_waveform_series = mock_AcousticWaveformSeries()
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


def test_add_to_acquisition_with_float(tmp_path):
    """Test adding an AcousticWaveformSeries to the acquisition field of an NWBFile."""
    # Create NWBFile
    nwbfile = mock_NWBFile()
    
    # Create test data
    rng = np.random.default_rng(seed=0)
    data = rng.random(size=(100,), dtype="float32")
    acoustic_waveform_series = mock_AcousticWaveformSeries(data=data)
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
        assert read_acoustic_waveform_series.data.dtype == "float32"
        np.testing.assert_array_equal(read_acoustic_waveform_series.data, data)


def test_add_to_stimulus(tmp_path):
    """Test adding an AcousticWaveformSeries to the stimulus field of an NWBFile."""
    # Create NWBFile
    nwbfile = mock_NWBFile()
    
    # Create test data
    acoustic_waveform_series = mock_AcousticWaveformSeries()
    nwbfile.add_stimulus(acoustic_waveform_series)

    # Write to file
    test_path = tmp_path / "test.nwb"
    with NWBHDF5IO(test_path, mode="w") as io:
        io.write(nwbfile)

    # Read from file and verify
    with NWBHDF5IO(test_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        read_acoustic_waveform_series = read_nwbfile.stimulus[acoustic_waveform_series.name]
        # Check key attributes
        assert read_acoustic_waveform_series.name == acoustic_waveform_series.name
        assert read_acoustic_waveform_series.description == acoustic_waveform_series.description
        assert read_acoustic_waveform_series.rate == acoustic_waveform_series.rate
        np.testing.assert_array_equal(read_acoustic_waveform_series.data, acoustic_waveform_series.data)


def test_add_to_processing_module(tmp_path):
    """Test adding an AcousticWaveformSeries to a processing module of an NWBFile."""
    # Create NWBFile
    nwbfile = mock_NWBFile()
    
    # Create test data
    acoustic_waveform_series = mock_AcousticWaveformSeries()
    processing_module = nwbfile.create_processing_module(
        name="test_module",
        description="Test module",
    )
    processing_module.add(acoustic_waveform_series)

    # Write to file
    test_path = tmp_path / "test.nwb"
    with NWBHDF5IO(test_path, mode="w") as io:
        io.write(nwbfile)

    # Read from file and verify
    with NWBHDF5IO(test_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        read_acoustic_waveform_series = read_nwbfile.processing["test_module"][acoustic_waveform_series.name]
        # Check key attributes
        assert read_acoustic_waveform_series.name == acoustic_waveform_series.name
        assert read_acoustic_waveform_series.description == acoustic_waveform_series.description
        assert read_acoustic_waveform_series.rate == acoustic_waveform_series.rate
        np.testing.assert_array_equal(read_acoustic_waveform_series.data, acoustic_waveform_series.data)


def test_multiple_acoustic_waveform_series(tmp_path):
    """Test adding multiple AcousticWaveformSeries to an NWBFile."""
    # Create NWBFile
    nwbfile = mock_NWBFile()
    
    # Add to acquisition
    aws1 = mock_AcousticWaveformSeries(name="aws1")
    nwbfile.add_acquisition(aws1)

    # Add to stimulus
    aws2 = mock_AcousticWaveformSeries(name="aws2")
    nwbfile.add_stimulus(aws2)

    # Add to processing module
    aws3 = mock_AcousticWaveformSeries(name="aws3")
    processing_module = nwbfile.create_processing_module(
        name="test_module",
        description="Test module",
    )
    processing_module.add(aws3)

    # Write to file
    test_path = tmp_path / "test.nwb"
    with NWBHDF5IO(test_path, mode="w") as io:
        io.write(nwbfile)

    # Read from file and verify
    with NWBHDF5IO(test_path, mode="r", load_namespaces=True) as io:
        read_nwbfile = io.read()
        
        # Check acquisition
        read_aws1 = read_nwbfile.acquisition["aws1"]
        assert read_aws1.name == aws1.name
        assert read_aws1.description == aws1.description
        assert read_aws1.rate == aws1.rate
        np.testing.assert_array_equal(read_aws1.data, aws1.data)
        
        # Check stimulus
        read_aws2 = read_nwbfile.stimulus["aws2"]
        assert read_aws2.name == aws2.name
        assert read_aws2.description == aws2.description
        assert read_aws2.rate == aws2.rate
        np.testing.assert_array_equal(read_aws2.data, aws2.data)
        
        # Check processing module
        read_aws3 = read_nwbfile.processing["test_module"]["aws3"]
        assert read_aws3.name == aws3.name
        assert read_aws3.description == aws3.description
        assert read_aws3.rate == aws3.rate
        np.testing.assert_array_equal(read_aws3.data, aws3.data)
