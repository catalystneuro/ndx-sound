"""Mock implementations for testing ndx-sound."""

from typing import Optional, Tuple, Union

import numpy as np

from ndx_sound import AcousticWaveformSeries


def mock_AcousticWaveformSeries(
    name: str = "AcousticWaveformSeries",
    data_shape: Union[Tuple[int], Tuple[int, int]] = (100,),
    rate: float = 42000.0,
    description: str = "acoustic stimulus description",
    seed: int = 0,
    data: Optional[np.ndarray] = None,
    add_random_nans: bool = False,
    **kwargs
) -> AcousticWaveformSeries:
    """
    Generate a mock AcousticWaveformSeries object with specified parameters or from given data.

    Parameters
    ----------
    name : str, optional
        The name of the AcousticWaveformSeries. Default is "AcousticWaveformSeries".
    data_shape : tuple, optional
        The shape of the data to generate. Can be (time,) or (time, channels).
        Default is (100,).
    rate : float, optional
        The sampling rate in Hz. Default is 42000.0.
    description : str, optional
        A description of the acoustic waveform. Default is "acoustic stimulus description".
    seed : int, optional
        Seed for the random number generator to ensure reproducibility. Default is 0.
    data : np.ndarray, optional
        The data to use. If provided, it overrides the generation of mock data based on other parameters.
    add_random_nans : bool, optional
        If True, random NaN values will be added to the data. Default is False.
    **kwargs
        Additional keyword arguments to pass to the AcousticWaveformSeries constructor.

    Returns
    -------
    AcousticWaveformSeries
        A mock AcousticWaveformSeries object populated with the provided or generated data and parameters.
    """
    if data is not None:
        if len(data.shape) == 1:
            data_shape = (data.shape[0],)
        else:
            data_shape = (data.shape[0], data.shape[1])
    else:
        rng = np.random.default_rng(seed=seed)
        data = rng.integers(low=0, high=1000, size=data_shape, dtype="int16")

    # Add random nans if requested
    if add_random_nans:
        data = data.astype("float32")
        rng = np.random.default_rng(seed=seed)
        nan_mask = rng.choice([True, False], size=data.shape, p=[0.1, 0.9])
        data[nan_mask] = np.nan

    acoustic_waveform_series = AcousticWaveformSeries(
        name=name,
        data=data,
        rate=rate,
        description=description,
        **kwargs
    )
    return acoustic_waveform_series
