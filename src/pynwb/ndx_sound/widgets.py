from typing import Tuple

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import Audio
from ipywidgets import Output, VBox
from matplotlib.gridspec import GridSpec
from nwbwidgets import default_neurodata_vis_spec
from nwbwidgets.base import fig2widget
from nwbwidgets.utils.timeseries import get_timeseries_tt
from pynwb.file import TimeSeries

from . import AcousticWaveformSeries


def plot_spectrogram(
    time_series: TimeSeries,
    n_fft: int = 1024,
    ax: plt.Axes = None,
    figsize: Tuple[int] = (8, 4),
    cax: plt.Axes = None,
    stft_kwargs: dict = None,
    specshow_kwargs: dict = None,
):
    """
    Plot spectrogram of sound.

    Parameters
    ----------
    time_series: pynwb.file.TimeSeries
    n_fft: int, optional
        Default is 1024
    ax: plt.Axes
    figsize: tuple
    cax: plt.Axes
    stft_kwargs: dict
        kwargs passed to librosa.stft
    specshow_kwargs: dict
        kwargs passed to librosa.display.specshow

    Returns
    -------
    plt.Axes

    """

    if stft_kwargs is None:
        stft_kwargs = dict()

    if specshow_kwargs is None:
        specshow_kwargs = dict()

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    y = time_series.data[:].astype(float)
    sr = time_series.rate

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft, **stft_kwargs)))

    tt = np.arange(len(D.T)) / time_series.rate * n_fft / 4 + time_series.starting_time

    img = librosa.display.specshow(
        D,
        y_axis="log",
        x_axis="time",
        sr=sr,
        cmap="plasma",
        ax=ax,
        x_coords=tt,
        **specshow_kwargs,
    )

    ax.set_xlabel("time (s)")

    fig.colorbar(img, ax=ax, format="%+2.f dB", cax=cax)

    return ax


def plot_waveform(time_series: TimeSeries, ax=None, figsize=(8, 4)):
    """
    Plot waveform of sound

    Parameters
    ----------
    time_series
    ax
    figsize

    Returns
    -------

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    y = time_series.data[:]
    tt = get_timeseries_tt(time_series)

    ax.plot(tt, y, "k")

    ax.axis("off")
    ax.autoscale(enable=True, axis="x", tight=True)

    return ax


def plot_sound(time_series: TimeSeries, figsize=None, **kwargs):
    """
    Figure for waveform and spectrogram

    Parameters
    ----------
    time_series
    figsize
    kwargs

    Returns
    -------

    """

    gs = GridSpec(
        nrows=2,
        ncols=2,
        hspace=0.04,
        wspace=0.04,
        height_ratios=[1, 5],
        width_ratios=[25, 1],
    )

    fig = plt.figure(figsize=figsize)

    ax1 = fig.add_subplot(gs[0, 0])

    plot_waveform(time_series, ax=ax1)

    ax2 = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])

    plot_spectrogram(time_series, ax=ax2, cax=cax, **kwargs)

    return fig


def play_sound_widget(time_series: TimeSeries):
    """
    Widget for playing sound.

    Parameters
    ----------
    time_series

    Returns
    -------

    """

    y = time_series.data[:].astype(float)
    sr = time_series.rate

    out = Output()
    out.append_display_data(Audio(y, rate=sr))

    return out


def acoustic_waveform_widget(time_series: TimeSeries, **kwargs):
    """
    Entire widget, with waveform, spectrogram, and sound.

    Parameters
    ----------
    time_series
    kwargs

    Returns
    -------

    """

    return VBox(
        [
            fig2widget(plot_sound(time_series, **kwargs)),
            play_sound_widget(time_series),
        ]
    )


default_neurodata_vis_spec.update({AcousticWaveformSeries: acoustic_waveform_widget})
