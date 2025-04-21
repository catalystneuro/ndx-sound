"""Tests for error cases in AcousticWaveformSeries."""

import numpy as np
import pytest

from ndx_sound import AcousticWaveformSeries


def test_constructor_invalid_data_type():
    """Test that the constructor raises an error for invalid data types."""
    # Test with a string instead of a numpy array
    with pytest.raises(Exception):
        AcousticWaveformSeries(
            name="acoustic_stimulus",
            data="not a numpy array",
            rate=42000.0,
            description="acoustic stimulus description",
        )


def test_constructor_data_shape_validation():
    """Test that the constructor accepts only valid data shapes."""
    # Test with a 3D array - this should not raise an exception
    # but we should verify the data is correctly stored
    data_3d = np.random.randint(1000, size=(10, 10, 10))
    
    # This test verifies that the constructor doesn't raise an exception
    # but we should check that the data is correctly stored
    aws = AcousticWaveformSeries(
        name="acoustic_stimulus",
        data=data_3d,
        rate=42000.0,
        description="acoustic stimulus description",
    )
    
    # Verify the data is stored correctly
    np.testing.assert_array_equal(aws.data, data_3d)


def test_constructor_rate_validation():
    """Test that the constructor handles different rate values."""
    # Test with a negative rate - this should raise a ValueError
    negative_rate = -42000.0
    with pytest.raises(ValueError):
        AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=np.random.randint(1000, size=(100,)),
            rate=negative_rate,
            description="acoustic stimulus description",
        )
    
    # Test with a zero rate - this should not raise an exception
    # but it should generate a warning
    zero_rate = 0.0
    with pytest.warns(UserWarning):
        aws_zero_rate = AcousticWaveformSeries(
            name="acoustic_stimulus",
            data=np.random.randint(1000, size=(100,)),
            rate=zero_rate,
            description="acoustic stimulus description",
        )
    
    # Verify the rate is stored correctly
    assert aws_zero_rate.rate == zero_rate


def test_constructor_starting_time_validation():
    """Test that the constructor handles different starting time values."""
    # Test with a negative starting time - this should not raise an exception
    # but we should verify the starting time is correctly stored
    negative_starting_time = -10.0
    aws = AcousticWaveformSeries(
        name="acoustic_stimulus",
        data=np.random.randint(1000, size=(100,)),
        rate=42000.0,
        description="acoustic stimulus description",
        starting_time=negative_starting_time,
    )
    
    # Verify the starting time is stored correctly
    assert aws.starting_time == negative_starting_time
