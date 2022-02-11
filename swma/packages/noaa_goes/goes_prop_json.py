import argparse
import json
import os
import urllib.request

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from pandas import json_normalize
from sunpy.time import parse_time

url = 'https://services.swpc.noaa.gov/json/solar_probabilities.json'


def _parse_json_file():
    """
    Parses an NOAA solar_probabilities JSON file.
    Parameters
    ----------
    filepath : `str`
        The path or url to the file you want to parse.
    """
    with urllib.request.urlopen(url) as fp:
        data = json.loads(fp.read().decode())
    return data


def _to_dataframe(data):
    # Convert the json data to Dataframe
    result = json_normalize(data)
    result = result.set_index('date')
    result.index = pd.DatetimeIndex(result.index.values)
    result.index = pd.DatetimeIndex(parse_time(
        [x for x in result.index.values]).isot.astype('datetime64'))
    return result


def autolabel(ax, bars, hbar=True):
    # attach some text labels
    for bar in bars:
        width = bar.get_width()
        height = bar.get_height()
        if hbar is True:
            width = bar.get_width()
            if width < 10:
                pivot = 7
            else:
                pivot = -1
            ax.text(width+pivot, bar.get_y() + height/2,
                    '%d %%' % int(width),
                    ha='right', va='center')
        else:
            pivot = 1
            ax.text(bar.get_x() + width/2, height+pivot,
                    '%d%%' % int(height),
                    ha='center', va='bottom', rotation=90)


def plot_latest_prop_all(result, outfile='', in_app=False, **plot_args):
    """
    Plot the data from the solar_probabilities JSON file.
    Parameters
    ----------
    result: dataframe
    mode : `str`
        The mode of json file you want to process
    """
    fig = plt.figure()
    fig.set_size_inches(5.5, 5)
    ax = fig.add_subplot(111)
    y = (result['c_class_1_day'][0],
         result['c_class_2_day'][0],
         result['c_class_3_day'][0],
         result['m_class_1_day'][0],
         result['m_class_2_day'][0],
         result['m_class_3_day'][0],
         result['x_class_1_day'][0],
         result['x_class_2_day'][0],
         result['x_class_3_day'][0],
         result['10mev_protons_1_day'][0],
         result['10mev_protons_2_day'][0],
         result['10mev_protons_3_day'][0])
    x = (1, 2, 3, 5, 6, 7, 9, 10, 11, 13, 14, 15)
    abar = plt.barh(x, y, color=('lightgreen', 'lightblue', 'lightcoral',
                                 'lightgreen', 'lightblue', 'lightcoral',
                                 'lightgreen', 'lightblue', 'lightcoral',
                                 'lightgreen', 'lightblue', 'lightcoral'))
    autolabel(ax, abar, hbar=True)
    plt.axhline(y=4, color='k', linestyle='-', linewidth=1)
    plt.axhline(y=8, color='k', linestyle='-', linewidth=1)
    plt.axhline(y=12, color='k', linestyle='-', linewidth=1)
    plt.title('NOAA - Daily Solar Propabilities:')
    plt.xlabel('Propability %')
    # plt.ylabel('')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 16)
    labels = [item.get_text() for item in ax.get_yticklabels()]
    labels[1] = 'C-class'
    labels[3] = 'M-class'
    labels[5] = 'X-class'
    labels[7] = 'Protons'
    ax.set_yticklabels(labels, rotation=90, ha='right', va='center')
    ax.legend((abar[0], abar[1], abar[2]), ['1-day', '2-days', '3-days'], loc='upper right')
    plt.tight_layout()

    if outfile != '':
        save_path = os.path.join(outfile, f'NOAA_latest_prop_all.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=150)

    if in_app:
        st.pyplot(fig)
    else:
        plt.show()

    return plt


def plot_prop_timeline(result, mode='c_class', outfile='', in_app=False, **plot_args):
    fig = plt.figure()
    fig.set_size_inches(5.5, 4.5)
    ax = fig.add_subplot(111)
    abar = ax.bar(result.index, result[f'{mode}_1_day'], color='lightblue')
    autolabel(ax, abar, hbar=False)
    plt.ylabel('Propability %')
    ax.set_ylim(0, 100)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%b-%d'))
    fig.autofmt_xdate(bottom=0, rotation=25, ha='center')
    ax.legend((abar), [f'{mode}'], loc='upper right')
    plt.tight_layout()

    if outfile != '':
        save_path = os.path.join(outfile, f'NOAA_prop_timeline_{mode}.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=150)

    if in_app:
        st.pyplot(fig)
    else:
        plt.show()

    return plt


def produce_plot(in_app=False):
    """
    Downloads an NOAA GOES SXR NRT JSON file and process it
    into a plot.
    Parameters
    ----------
    mode : `str`
        The mode of json file you want to process
    """
    data = _parse_json_file()
    result = _to_dataframe(data)
    plt = plot_latest_prop_all(result, in_app=in_app)

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
