"""
NOAA GOES X-ray Sensor (XRS) soft X-ray (SXR) flux in near-real-time.

The NOAA Solar Weather Prediction Center (SWPC) provides near-real-time measurements
of the proton flux from GOES satelites.
The proton as a function of time is used to track the solar activity and solar energetic particles.
The near-real-time proton data are provided from <https://services.swpc.noaa.gov/json/goes/>
in JSON format (updated every 1-minute).
The solar proton measurements are made in five different integral chanels.
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
* `SWPC GOES proton flux description <https://www.swpc.noaa.gov/products/goes-proton-flux>`_
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
import pandas as pd
import streamlit as st
from pandas import json_normalize
from sunpy.time import parse_time
from sunpy.util.metadata import MetaDict

url_sxr = 'https://services.swpc.noaa.gov/json/goes/primary/integral-protons-?.json'


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
    # Convoluted time index handling
    result = result.set_index('time_tag')
    result.index = pd.DatetimeIndex(result.index.values)
    result.index = pd.DatetimeIndex(parse_time(
        [x for x in result.index.values]).isot.astype('datetime64'))
    # Add the units on data.
    units = OrderedDict([('satellite', u.dimensionless_unscaled),
                         ('flux', u.W/u.m**2),
                         ('energy', u.MeV)])
    return result, MetaDict(
        {'comments': 'Merged time serie for 0.1-0.8nm & 0.05-0.4nm wavelengths'}), units


def _split_to_data(result, type_):
    dataframe_ = result[0]
    dataframe = dataframe_[dataframe_['energy'] == type_]
    return dataframe


def plot_(result, mode='1-day', type_='GOES-Long_and_Short', outfile='', in_app=False,
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

    GOES_1MeV = _split_to_data(result, '>=1 MeV')
    axes.plot(GOES_1MeV.index, GOES_1MeV['flux'],
              marker='', color='orange', linewidth=1, label='GOES->1MeV')

    GOES_10MeV = _split_to_data(result, '>=10 MeV')
    axes.plot(GOES_10MeV.index, GOES_10MeV['flux'],
              marker='', color='red', linewidth=1, label='GOES->10MeV')

    GOES_50MeV = _split_to_data(result, '>=50 MeV')
    axes.plot(GOES_50MeV.index, GOES_50MeV['flux'],
              marker='', color='blue', linewidth=1, label='GOES->50MeV')

    GOES_100MeV = _split_to_data(result, '>=100 MeV')
    axes.plot(GOES_100MeV.index, GOES_100MeV['flux'],
              marker='', color='green', linewidth=1, label='GOES->100MeV')

    GOES_500MeV = _split_to_data(result, '>=500 MeV')
    axes.plot(GOES_500MeV.index, GOES_500MeV['flux'],
              marker='', color='black', linewidth=1, label='GOES->500MeV')

    axes.set_title('NOAA - GOES Proton Flux (1-minute average)')
    axes.set_xlabel('Time [UT]')
    axes.set_ylabel(r'Flux [$Particles \cdot cm^{-2} s^{-1} sr^{-1} $]')
    plt.yscale('log')
    plt.ylim([1e-2, 1e4])
    axes.set_xlim([GOES_1MeV.index[0], GOES_1MeV.index[-1]])
    axes.grid(True, which='minor', linewidth=0.5)
    axes.grid(True, which='major', linewidth=0.5)
    ymin, ymax = axes.get_ylim()
    axes.legend(fontsize=8)

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

    # Here it needs some attention of the limits and the class labels
    ax2 = plt.gca().twinx()
    ax2.set_yscale('log')
    ax2.set_ylim(axes.get_ylim())
    ax2.set_yticklabels(['', '', '', 'N \u2192', 'SEP', '\u2190 Y', ''], rotation=270, va='center')
    ax2.set_ylabel('Alert Thresshold', rotation=270, va='bottom')

    plt.tight_layout()

    # ax2.annotate('@Last Update:' + datetime.now().strftime("%d/%m/%Y %H:%M"),
    #              xy=(10, 15), xycoords='figure pixels',fontsize=8, color=(0,0,0,0.5))
    # plt.show()

    if outfile != '':
        save_path = os.path.join(outfile, f'GOES_PROTONS_latest_{mode}.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=150)

    if in_app:
        st.pyplot(fig)
    else:
        plt.show()

    return plt


def produce_plot(mode='1-day', in_app=False):
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
    plt = plot_(result, mode, in_app=in_app)

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
