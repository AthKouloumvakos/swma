"""
NOAA GOES X-ray Sensor (XRS) soft X-ray (SXR) flux in near-real-time.

The NOAA Solar Weather Prediction Center (SWPC) provides near-real-time measurements
of the X-ray flux from GOES satelites.
The SXR flux as a function of time is used to track the solar activity and solar flares.
The near-real-time SXR data are provided from <https://services.swpc.noaa.gov/json/goes/>
in JSON format (updated every 1-minute).
The solar SXR measurements are made in the 1-8 Angstrom (0.1-0.8 nm, long channel)
and 0.5-4.0 Angstrom (0.05-0.4 nm, short channel) passbands.
SWPC designates a Primary and a Secondary GOES Satellite (e.g. GOES-16/17) for each instrument,
the satellite from which the SXR measurement is made can be found in
<https://services.swpc.noaa.gov/json/goes/instrument-sources.json>.
Data from the SWPC Primary and Secondary GOES X-ray satellite are provided from two separate sub-directories.
The final products should be used for preview purposes of the current space weather conditions.
Use the GOES XRS `~sunpy.timeseries.TimeSeries` source to process GOES/XRS FITS file.

Examples
--------
>>>

References
----------
* `SWPC provided observations from <https://www.swpc.noaa.gov/observations>`_
* `SWPC GOES soft X-ray flux description <https://www.swpc.noaa.gov/products/goes-x-ray-flux>`_
* `SWPC's data service for GOES SXR JSON files <https://services.swpc.noaa.gov/json/goes/>`_
"""

import argparse
import json
import os
import urllib.request
from collections import OrderedDict

import astropy.units as u
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
# from datetime import datetime
import numpy as np
import pandas as pd
import streamlit as st
from pandas import json_normalize
from sunpy.time import parse_time
from sunpy.util.metadata import MetaDict

url_sxr = 'https://services.swpc.noaa.gov/json/goes/primary/xrays-?.json'


def _parse_json_file(mode):
    """
    Parses an NOAA GOES SXR JSON file.
    Parameters
    ----------
    filepath : `str`
        The path or url to the file you want to parse.
    """
    url = (url_sxr).replace('?', mode)
    with urllib.request.urlopen(url) as fp:
        data = json.loads(fp.read().decode())
    return data


def _to_dataframe(data):
    # Convert the json data to Dataframe
    result = json_normalize(data)
    rename = {'energy': 'wavelength'}
    result = result.rename(columns=rename)
    # Convoluted time index handling
    result = result.set_index('time_tag')
    result.index = pd.DatetimeIndex(result.index.values)
    result.index = pd.DatetimeIndex(parse_time(
        [x for x in result.index.values]).isot.astype('datetime64'))
    # Add the units on data.
    units = OrderedDict([('satellite', u.dimensionless_unscaled),
                         ('flux', u.W/u.m**2),
                         ('wavelength', u.nm)])
    return result, MetaDict(
        {'comments': 'Merged time serie for 0.1-0.8nm & 0.05-0.4nm wavelengths'}), units


def _split_to_data(result, type_):
    dataframe_ = result[0]
    if type_ == 'GOES-Long':
        dataframe = dataframe_[dataframe_['wavelength'] == '0.1-0.8nm']
    elif type_ == 'GOES-Short':
        dataframe = dataframe_[dataframe_['wavelength'] == '0.05-0.4nm']
    else:
        raise ValueError(f'Got unknown _split type "{type}"')
    return dataframe


def plot_(result, mode='1-day', type_='GOES-Long_and_Short', plot_flares=False, outfile='', in_app=False,
          **plot_args):
    """
    Plot the data from the GOES SXR JSON file.
    Parameters
    ----------
    result: dataframe
    mode : `str`
        The mode of json file you want to process
    """
    # plt.figure(dpi=150)
    fig, axes = plt.subplots()
    fig.set_size_inches(5.5, 5)
    if type_ == 'GOES-Long_and_Short':
        dataframe_long = _split_to_data(result, type_='GOES-Long')
        axes.plot(dataframe_long.index, dataframe_long['flux'],
                  marker='', color='red',
                  linewidth=1, label='0.1-0.8nm', **plot_args)
        dataframe_sort = _split_to_data(result, type_='GOES-Short')
        axes.plot(dataframe_sort.index, dataframe_sort['flux'],
                  marker='', color='blue',
                  linewidth=1, label='0.05-0.4nm', **plot_args)
    elif type_ == 'GOES-Long':
        dataframe_long = _split_to_data(result, type_='GOES-Long')
        axes.plot(dataframe_long.index, dataframe_long['flux'],
                  marker='', color='red',
                  linewidth=1, label='0.1-0.8nm', **plot_args)
    elif type_ == 'GOES-Short':
        dataframe_sort = _split_to_data(result, type_='GOES-Short')
        axes.plot(dataframe_sort.index, dataframe_sort['flux'],
                  marker='', color='blue',
                  linewidth=1, label='0.05-0.4nm', **plot_args)
    else:
        raise ValueError(f'Got unknown plot type "{type}"')

    tstart, tend = result[0].index[0], result[0].index[-1]
    axes.set_title('NOAA - GOES Soft X-Ray Flux (1-minute average)')
    axes.set_xlabel('Time [UT]')
    axes.set_ylabel('Flux [W/m$^2$]')
    axes.set_yscale('log')
    axes.set_ylim([1e-9, 1e-3])
    axes.set_xlim([tstart, tend])

    axes.grid(True, which='minor', linewidth=0.5)
    axes.grid(True, which='major', linewidth=0.5)
    ymin, ymax = axes.get_ylim()
    xmin, xmax = axes.get_xlim()
    axes.legend(loc='upper left')

    if plot_flares is True:
        # url = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json"
        url = 'https://services.swpc.noaa.gov/json/goes/primary/xray-flares-7-day.json'
        with urllib.request.urlopen(url) as url:
            data_flare = json.loads(url.read().decode())
        # If we want to add flare information:
        # Convert the json data to Dataframe
        result_flare = json_normalize(data_flare)

        for index, flare in result_flare.iterrows():
            Time_Flare = pd.to_datetime(flare['max_time'], format='%Y-%m-%dT%H:%M:%SZ')
            if (Time_Flare is not None):
                if (Time_Flare > tstart):
                    axes.plot([Time_Flare, Time_Flare], [1e-9, flare['max_xrlong']], marker='',
                              color='black', linestyle='dashed', linewidth=1, label='Flare')
                    axes.text(Time_Flare, 1.5*flare['max_xrlong'], flare['max_class'],
                              horizontalalignment='center',
                              verticalalignment='center')

    # Add a color to the classes limits
    ygrid = axes.get_ygridlines()
    ygrid[2].set_color('blue')
    ygrid[2].set_linewidth(1)
    ygrid[3].set_color('green')
    ygrid[3].set_linewidth(1)
    ygrid[4].set_color('yellow')
    ygrid[4].set_linewidth(1)
    ygrid[5].set_color('orange')
    ygrid[5].set_linewidth(1)
    ygrid[6].set_color('red')
    ygrid[6].set_linewidth(1)

    locator = mdates.AutoDateLocator(minticks=4, maxticks=8)
    formatter = mdates.ConciseDateFormatter(locator)
    axes.xaxis.set_major_locator(locator)
    axes.xaxis.set_major_formatter(formatter)
    fig.autofmt_xdate(bottom=0, rotation=0, ha='center')

    # Add a label at the classes lines
    ax2 = axes.twinx()
    ax2.set_yscale('log')
    ax2.set_ylim(ymin, ymax)
    labels = ['A', 'B', 'C', 'M', 'X']
    centers = np.logspace(-7.5, -3.5, len(labels))
    ax2.yaxis.set_minor_locator(mticker.FixedLocator(centers))
    ax2.set_yticklabels(labels, minor=True)
    ax2.set_yticklabels([])
    plt.tight_layout()
    # ax2.annotate('@Last Update:' + datetime.now().strftime("%d/%m/%Y %H:%M"),
    #        xy=(10, 15), xycoords='figure pixels',fontsize=8, color=(0,0,0,0.5))
    # plt.show()
    if outfile != '':
        save_path = os.path.join(outfile, f'GOES_SXR_latest_{mode}.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=150)

    if in_app:
        st.pyplot(fig)
    else:
        plt.show()

    return plt


def produce_plot(mode='1-day', plot_flares=False, in_app=False):
    """
    Downloads an NOAA GOES SXR NRT JSON file and process it
    into a plot.
    Parameters
    ----------
    mode : `str`
        The mode of json file you want to process
    """
    data = _parse_json_file(mode)
    result = _to_dataframe(data)
    plt = plot_(result, mode, plot_flares=plot_flares, in_app=in_app)

    return plt

# Check to see if this file is being executed as the "Main" python
# script instead of being used as a module by some other python script
# This allows us to use the module which ever way we want.


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-mode', '--mode', default='1-day',
                        choices=['6-hour', '1-day', '3-day', '7-day'])
    args = parser.parse_args()
    produce_plot(mode=args.mode)
