"""
Space Weather Monitor Application (SWMA)
An open-source app framework built specifically for visualizing
realtime space weather related data.

Copyright (C) 2021  Athanasios Kouloumvakos

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import io
import datetime
import streamlit as st
from PIL import Image
import requests
from packages.noaa_goes import goes_sxr_json
from packages.noaa_goes import goes_protons_json
from packages.noaa_goes import goes_prop_json
from buttons import download_button

def intro():
    """
    This is the intro function used for the first page.
    """
    st.sidebar.success("Select a space weather monitor from the list above.")

    st.markdown(
        """
        _Space Weather Monitor Application (SWMA)_ is an open-source app framework
        built specifically for visualizing realtime space weather related data
        from different sources.

        ** ⏻ Start this application selecting a monitor from the dropdown list
        on the left**

        ----------------------------------------------------------------------

        ### Availiable (near-)real-time monitors 🖵:

        - Soft x-ray flux (NOAA-GOES)
        - Proton flux (NOAA-GOES)
        - Solar Propabilities (NOAA)
        - EUV Images (SDO/AIA)
        - Coronagraphic Images (SoHO/LASCO)

        ----------------------------------------------------------------------

        ### Usefull python packages 📦:

        - [SunPy](https://sunpy.org/): The community-developed, free and
          open-source solar data analysis environment for Python.
        - [AstroPy](https://www.astropy.org/): The Astropy Project
          is a community effort to develop a single core package for
          Astronomy in Python.

    """
    )


# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off
def goes_sxr():
    """
    PLot the real-time soft x-rays.
    """
    option = st.sidebar.selectbox(
                              'Select a mode for realtime data:',
                              ('1-day', '3-day', '7-day', '6-hour'))
    plt_flare = st.sidebar.checkbox('Plot Latest Flares', value = True)
    st.sidebar.button("Refresh")

    plt = goes_sxr_json.produce_plot(mode=option,
                                     plot_flares=plt_flare,
                                     in_app=True)
    # Download button
    plot2 = io.BytesIO()
    plt.savefig(plot2, format='png', bbox_inches='tight')
    download_button_str = download_button(plot2.getvalue(), 
                           'NOAA_GOES_SXR_flux.png', 
                           'Download figure as .png file',
                           pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
    st.markdown(
        """
        ----------------------------------------------------------------------------------
        ### Instrument/Data Details:
        The solar SXR measurements are made in the 1-8 Angstrom (0.1-0.8 nm, long channel)
        and 0.5-4.0 Angstrom (0.05-0.4 nm, short channel) passbands.
        SWPC designates a Primary and a Secondary GOES Satellite (e.g.
        GOES-16/17) for each instrument. In the above data visualization
        only the observations from the primary satelite are considered.
        The satellite from which the SXR measurement is made can be found in
        <https://services.swpc.noaa.gov/json/goes/instrument-sources.json>.
        Data from the SWPC Primary and Secondary GOES X-ray satellite are
        provided from two separate sub-directories.
        """
    )

# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off

def goes_proton():
    """
    PLot the real-time proton flux.
    """
    option = st.sidebar.selectbox(
                              'Select a mode for realtime data:',
                              ('1-day', '3-day', '7-day', '6-hour'))
    st.sidebar.button("Refresh")

    plt = goes_protons_json.produce_plot(mode=option, in_app=True)
    # Download button
    plot2 = io.BytesIO()
    plt.savefig(plot2, format='png', bbox_inches='tight')
    download_button_str = download_button(plot2.getvalue(), 
                           'NOAA_GOES_Proton_flux.png', 
                           'Download figure as .png file',
                           pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)
    st.markdown(
        """
        ----------------------------------------------------------------------------------
        ### Instrument/Data Details:
        The solar proton measurements are made in five different integral
        chanels from 1 MeV to 500 MeV. SWPC designates a Primary and a
        Secondary GOES Satellite (e.g. GOES-16/17) for each instrument.
        In the above data visualization only the observations from the
        primary satelite are considered. The satellite from which the
        SXR measurement is made can be found in
        <https://services.swpc.noaa.gov/json/goes/instrument-sources.json>.
        Data from the SWPC Primary and Secondary GOES X-ray satellite are
        provided from two separate sub-directories.
        """
    )
# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off

def noaa_forecast():
    """
    PLot the real-time NOAA forecast.
    """
    st.sidebar.button("Refresh")

    data = goes_prop_json._parse_json_file()
    result = goes_prop_json._to_dataframe(data)
    # First Plot
    plt = goes_prop_json.plot_latest_prop_all(result, in_app=True)
    # Download button
    plot2 = io.BytesIO()
    plt.savefig(plot2, format='png', bbox_inches='tight')
    download_button_str = download_button(plot2.getvalue(), 
                           'NOAA_GOES_Timeline_flux.png', 
                           'Download figure as .png file',
                           pickle_it=False)
    st.markdown(download_button_str, unsafe_allow_html=True)

    option = st.selectbox(
                          'Select a mode for timeline data:',
                          ('c_class', 'm_class', 'x_class', '10mev_protons'))
    # Second Plot
    goes_prop_json.plot_prop_timeline(result, mode=option, in_app=True)
# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off

def aia_realtime():
    """
    View real-time EUV images from SDO/AIA.
    """
    option = st.sidebar.selectbox('Select wavelength:',
                                  ['Overview'])

    if option == 'Overview':
        pfss_mode = st.sidebar.checkbox('View PFSS', value = False)
        if pfss_mode is True:
            pfss = 'pfss'
        else:
            pfss = ''
        left_column, right_column = st.beta_columns(2)
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           'assets/img/latest/f_211_193_171pfss_1024.jpg',
                           stream=True).raw
                           )
        left_column.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_HMIB{pfss}.jpg',
                           stream=True).raw
                           )
        right_column.image(image, caption='')

        one_, two_, three_, four_ = st.beta_columns(4)
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0171{pfss}.jpg',
                           stream=True).raw
                           )
        one_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0193{pfss}.jpg',
                           stream=True).raw
                           )
        two_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0211{pfss}.jpg',
                           stream=True).raw
                           )
        three_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0304{pfss}.jpg',
                           stream=True).raw
                           )
        four_.image(image, caption='')

        one_, two_, three_, four_ = st.beta_columns(4)
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0094{pfss}.jpg',
                           stream=True).raw
                           )
        one_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0131{pfss}.jpg',
                           stream=True).raw
                           )
        two_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_0335{pfss}.jpg',
                           stream=True).raw
                           )
        three_.image(image, caption='')
        image = Image.open(
                           requests.get('https://sdo.gsfc.nasa.gov/'
                           f'assets/img/latest/latest_1024_1700{pfss}.jpg',
                           stream=True).raw
                           )
        four_.image(image, caption='')

    st.sidebar.button("Refresh")

    st.markdown('_Images Courtesy of NASA/SDO and the AIA, EVE, and HMI science teams._')
    st.markdown(
        """
        ----------------------------------------------------------------------------------
        ### Instrument/Data Details:
        SDO is a NASA mission which has been observing the Sun since 2010.
        The AIA is a sophisticated extreme ultraviolet (EUV) telescope suite
        that provides continuous full-disk observations of the solar chromosphere
        and corona in seven channels in EUV. The image candence is around twelve
        seconds; AIA captures high-definition (4096×4096) images of the Sun with a
        resolution of 0.6 arcsec/pixel. Observations of the solar corona in EUV helps
        in the early detection of eruptive phenomena such as solar flares, coronal mass
        ejections (CMEs), EUV waves and other phenomena affecting space weather.
    """
    )
# fmt: on

# Turn off black formatting for this function to present the user with more
# compact code.
# fmt: off

def lasco_realtime():
    """
    View real-time coronagraphic images from SoHO/LASCO.
    """
    left_column, right_column = st.beta_columns(2)
    image = Image.open(
                       requests.get('https://sohowww.nascom.nasa.gov/'
                       'data/realtime/c2/1024/latest.jpg',
                       stream=True).raw
                       )
    left_column.image(image, caption='SOHO/LASCO-C2 near-real-time coronagraphic image')
    image = Image.open(
                       requests.get('https://sohowww.nascom.nasa.gov/'
                       'data/realtime/c3/1024/latest.jpg',
                       stream=True).raw
                       )
    right_column.image(image, caption='SOHO/LASCO-C3 near-real-time coronagraphic image')
    st.markdown(
        """
        ----------------------------------------------------------------------------------
        ### Instrument/Data Details:
        LASCO consists of two solar coronagraphs that are still operational
        and observe the solar corona since 1996. The white light coronagraphs
        C2 and C3 produce images of the corona over much of the visible spectrum.
        C2 coronagraph images the solar corona from 1.5 to 6 solar radii and C3
        from 3.7 to 30 solar radii. The three LASCO cameras have a resolution
        of one megapixel and the candence is around 4 to 5 images per hour.
    """
    )
