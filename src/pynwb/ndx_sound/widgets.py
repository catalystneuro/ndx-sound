import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from nwbwidgets import default_neurodata_vis_spec
from nwbwidgets.utils.timeseries import get_timeseries_tt
from pynwb.file import TimeSeries

from . import AcousticWaveformSeries


def plot_spectrogram(
    time_series: TimeSeries, n_fft: int = 1024, ax=None, figsize=(8, 4), cax=None
):

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else:
        fig = ax.figure

    y = time_series.data[:].astype(float)
    sr = time_series.rate

    D = librosa.amplitude_to_db(np.abs(librosa.stft(y, n_fft=n_fft)))

    img = librosa.display.specshow(
        D, y_axis="log", x_axis="time", sr=sr, cmap="plasma", ax=ax
    )
    fig.colorbar(img, ax=ax, format="%+2.f dB", cax=cax)

    return ax


def plot_waveform(time_series: TimeSeries, ax=None, figsize=(8, 4)):
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    y = time_series.data[:]
    tt = get_timeseries_tt(time_series)

    ax.plot(tt, y, "k")

    ax.axis("off")
    ax.autoscale(enable=True, axis="x", tight=True)


def plot_acoustic_waveform(time_series: TimeSeries, figsize=None, **kwargs):

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

    plot_spectrogram(time_series, ax=ax2, cax=cax)

    return fig


default_neurodata_vis_spec.update({AcousticWaveformSeries: plot_acoustic_waveform})
