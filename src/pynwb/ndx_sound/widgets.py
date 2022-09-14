from typing import Tuple

from librosa import amplitude_to_db, stft
from librosa import display as librosa_display
import matplotlib.pyplot as plt
import numpy as np
from IPython.core.display_functions import clear_output, display
from IPython.display import Audio
from ipywidgets import Output, VBox
from ipywidgets.widgets.interaction import show_inline_matplotlib_plots
from matplotlib.gridspec import GridSpec
from matplotlib.ticker import FormatStrFormatter
from nwbwidgets.base import fig2widget
from nwbwidgets.controllers import StartAndDurationController
from nwbwidgets.timeseries import AbstractTraceWidget
from nwbwidgets.utils.timeseries import (
    get_timeseries_tt,
    timeseries_time_to_ind,
    get_timeseries_in_units,
)
from pynwb.file import TimeSeries

from . import AcousticWaveformSeries


class AcousticWaveformWidget(AbstractTraceWidget):
    def __init__(
            self,
            acoustic_waveform_series: AcousticWaveformSeries,
            foreign_time_window_controller: StartAndDurationController = None,
            **kwargs
    ):
        super().__init__(
            timeseries=acoustic_waveform_series,
            foreign_time_window_controller=foreign_time_window_controller,
            **kwargs,
        )

    def set_out_fig(self):
        time_series = self.controls["timeseries"].value
        time_window = self.controls["time_window"].value

        self.out_fig = acoustic_waveform_widget(time_series, time_window)

        def on_change(change):
            time_window = self.controls["time_window"].value

            with self.out_fig.children[0]:
                clear_output(wait=True)
                plot_sound(time_series, time_window)
                show_inline_matplotlib_plots()

            with self.out_fig.children[1]:
                clear_output(wait=True)
                display(play_sound(time_series, time_window))

        self.controls["time_window"].observe(on_change)


def plot_spectrogram(
        time_series: TimeSeries,
        time_window=None,
        n_fft: int = 1024,
        ax: plt.Axes = None,
        figsize: Tuple[int] = (8, 4),
        cax: plt.Axes = None,
        stft_kwargs: dict = None,
        specshow_kwargs: dict = None,
        **kwargs,
):
    """
    Plot spectrogram of sound.

    Parameters
    ----------
    time_series: pynwb.file.TimeSeries
    time_window: tuple, optional
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

    if time_window is not None:
        istart = timeseries_time_to_ind(time_series, time_window[0])
        istop = timeseries_time_to_ind(time_series, time_window[1])
        data, units = get_timeseries_in_units(time_series, istart, istop)
    else:
        data = time_series.data[:].astype(float)
    sr = time_series.rate
    starting_time = time_series.starting_time if time_window is None else time_window[0]

    D = amplitude_to_db(np.abs(stft(data, n_fft=n_fft, **stft_kwargs)))

    tt = np.arange(len(D.T)) / sr * n_fft / 4 + starting_time

    img = librosa_display.specshow(
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
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    ax.tick_params(axis='x', labelrotation=45)

    fig.colorbar(img, ax=ax, format="%+2.f dB", cax=cax)

    return ax


def plot_waveform(time_series: TimeSeries, time_window=None, ax=None, figsize=(8, 4)):
    """
    Plot waveform of sound

    Parameters
    ----------
    time_series
    time_window
    ax
    figsize

    Returns
    -------

    """
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    if time_window is not None:
        istart = timeseries_time_to_ind(time_series, time_window[0])
        istop = timeseries_time_to_ind(time_series, time_window[1])
        data, units = get_timeseries_in_units(time_series, istart, istop)
        tt = get_timeseries_tt(time_series, istart, istop)
    else:
        data = time_series.data[:]
        tt = get_timeseries_tt(time_series)

    ax.plot(tt, data, "k")

    ax.axis("off")
    ax.autoscale(enable=True, axis="x", tight=True)

    return ax


def plot_sound(time_series: TimeSeries, time_window=None, figsize=None, **kwargs):
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

    plot_waveform(time_series, time_window=time_window, ax=ax1)

    ax2 = fig.add_subplot(gs[1, 0])
    cax = fig.add_subplot(gs[1, 1])

    plot_spectrogram(time_series, time_window=time_window, ax=ax2, cax=cax, **kwargs)

    return fig


def play_sound(time_series: TimeSeries, time_window=None):
    """Returns the Audio widget."""

    if time_window is not None:
        istart = timeseries_time_to_ind(time_series, time_window[0])
        istop = timeseries_time_to_ind(time_series, time_window[1])
        data, units = get_timeseries_in_units(time_series, istart, istop)
    else:
        data = time_series.data[:].astype(float)
    sr = time_series.rate

    return Audio(data, rate=sr)


def play_sound_widget(time_series: TimeSeries, time_window=None):
    """
    Widget for playing sound.

    Parameters
    ----------
    time_series
    time_window

    Returns
    -------

    """
    out = Output()
    with out:
        display(play_sound(time_series, time_window))
    return out


def acoustic_waveform_widget(time_series: TimeSeries, time_window=None, **kwargs):
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
            fig2widget(plot_sound(time_series, time_window, **kwargs)),
            play_sound_widget(time_series, time_window),
        ]
    )


def load_widgets():
    """Load AcousticWaveformWidget into nwbwidgets, to use as default visualization
    for AcousticWaveformSeries data."""
    from nwbwidgets import default_neurodata_vis_spec

    default_neurodata_vis_spec.update({AcousticWaveformSeries: AcousticWaveformWidget})
