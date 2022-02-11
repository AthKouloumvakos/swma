import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import streamlit as st
from sunpy import timeseries as ts
from sunpy.net import Fido
from sunpy.net import attrs as a


def plot(tstart='2021-05-01 00:00', tend='2021-05-03 00:00',
         sat_num=17, in_app=False, outfile=''):
    Fido.search(a.Time(tstart, tend), a.Instrument('XRS'))
    result_goes = Fido.search(a.Time(tstart, tend), a.Instrument('XRS'), a.goes.SatelliteNumber(17))
    file_goes = Fido.fetch(result_goes)
    goes_ = ts.TimeSeries(file_goes, concatenate=True)

    fig, axes = plt.subplots()
    fig.set_size_inches(5.5, 5)

    axes.plot(goes_.index, goes_.quantity('xrsb'), marker='', color='red',
              linewidth=1, label='0.1-0.8nm')
    axes.plot(goes_.index, goes_.quantity('xrsa'), marker='', color='blue',
              linewidth=1, label='0.05-0.4nm')

    axes.set_title('NOAA - GOES Soft X-Ray Flux')
    axes.set_ylabel('Flux [W/m$^2$]')
    axes.set_xlabel('Time [UT]')
    axes.set_yscale('log')
    axes.set_ylim([1e-9, 1e-3])
    axes.set_xlim([goes_.index[0], goes_.index[-1]])
    axes.grid(True, which='minor', linewidth=0.5)
    axes.grid(True, which='major', linewidth=0.5)
    ymin, ymax = axes.get_ylim()
    axes.legend()

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

    axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y\n%b-%d\n%H:%M'))
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
    axes.get_shared_x_axes().join(axes, ax2)
    plt.tight_layout()
    if outfile != '':
        save_path = os.path.join(outfile, f'GOES_SXR_latest_{mode}.png')
        fig.savefig(save_path, bbox_inches='tight', dpi=150)

    if in_app:
        st.pyplot(fig)
    else:
        plt.show()
