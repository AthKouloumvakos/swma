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

import inspect
import textwrap
from collections import OrderedDict

import streamlit as st
from streamlit.logger import get_logger
import tools

LOGGER = get_logger(__name__)

def img_to_bytes(img_path):
    from pathlib import Path
    import base64
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def current_conditions():
    import urllib.request
    import json
    from pandas import json_normalize
    st.sidebar.markdown("""---""")
    st.sidebar.markdown("""## Current Space Weather Conditions ☂: """)
    
    with urllib.request.urlopen('https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json') as fp:
        data = json.loads(fp.read().decode())
    latest_flares = json_normalize(data)
    max_class = latest_flares['max_class'][0]
    if max_class is not None:
        max_time = latest_flares['max_time'][0][0:16]
        if "B" in max_class:
            color = 'Lime'
        elif "C" in max_class:
            color = 'yellow'
        elif "M" in max_class:
            color = 'orange'
        elif "X" in max_class:
            color = 'red'
    else:
        max_class = 'None'
        max_time = 'Now'
        color = 'None'
    st.sidebar.markdown(f"""Latest X-ray solar flare: <br />
                                     ➠ <span style="color:black; background:{color}">{max_class}</span> @{max_time}""", unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    #solar_wind_plasma = json_normalize(data)
    density = data[-1][1]
    time  = data[-1][0][0:16]
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    #solar_wind_plasma = json_normalize(data)
    speed = data[-1][2]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""Solar Wind: @{time} <br />
                                     ➠ Density: {density} protons/cm3 <br />
                                     ➠ Speed: {speed} km/s  <br />""", unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    #solar_wind_plasma = json_normalize(data)
    mag_tot = data[-1][6]
    mag_z = data[-1][3]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""IP Mag. Field: @{time} <br />
                                     ➠ Btot: {mag_tot} nT &nbsp;
                                     ➠ Bz: {mag_z} nT """, unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json') as fp:
        data = json.loads(fp.read().decode())
    #solar_wind_plasma = json_normalize(data)
    kp = data[-1][1]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""Planetary K-index: <br />
                                     ➠ Kp: {kp} @{time}""", unsafe_allow_html=True)
    
    
# Dictionary of
# demo_name -> (demo_function, demo_description)
TOOLS = OrderedDict(
    [
        ("—", (tools.intro, None)),
        (
            "Soft x-ray flux (NOAA-GOES)",
            (
                tools.goes_sxr,
                """
Visualize real-time measurements of **X-ray flux** from GOES satelites. The SXR data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated every 1-minute. Select to plot data among four different time intervals and also select to overplot the latest solar flares identifications.
""",
            ),
        ),
        (
            "Proton flux (NOAA-GOES)",
            (
                tools.goes_proton,
                """
Visualize real-time measurements of **proton flux** from GOES satelites. The proton flux data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated every 1-minute. Select to plot data among four different time intervals.
""",
            ),
        ),
        
        (
            "Solar Events Forecast (NOAA)",
            (
                tools.noaa_forecast,
                """
Visualize near-real-time measurements of forecasts of the likelihood (probability) of the occurrence of a solar event. the flare and the solar proton event foracast data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated daily. The flare forecasts are daily probabilistic forecasts, ranging from 1% to 99%, of the likelihood of a given class x-ray flare to occur within a time interval.
""",
            ),
        ),
        (
            "Extreme Ultraviolet Images (SDO/AIA)",
            (
                tools.aia_realtime,
                """
Show near-real-time images of the solar chromosphere and corona from observations of the Atmospheric Imaging Assembly (AIA) on board the Solar Dynamics Observatory (SDO) in extreme ultraviolet (EUV). The near-real-time EUV images are provided from NASA/SDO in .png format. Select between different wavelengths. Individual images are processed from .fits files. Select to overplot features from the Heliophysics Events Knowledgebase (HEK).
""",
            ),
        ),
        (
            "Coronagraphic Images (SoHO/LASCO)",
            (
                tools.lasco_realtime,
                """
Show near-real-time images of the solar corona in white light from observations of the Large Angle and Spectrometric Coronagraph (LASCO) on board the Solar and Heliospheric Observatory satellite (SoHO). The near-real-time coronagraphic images are provided from NASA/nascom in .jpg format.
""",
            ),
        ),
    ]
)


def run():
    # set page config
    st.set_page_config(page_title='SWMA',
                       page_icon=":rocket:",
                       #layout="wide",
                       initial_sidebar_state="expanded",
                       )

    st.sidebar.title('Space Weather Monitor Application 🚀')
    tool_name = st.sidebar.selectbox("Choose a Tool from the list", list(TOOLS.keys()), 0)
    tool = TOOLS[tool_name][0]

    # Hide the menu button
    st.markdown(""" <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style> """, unsafe_allow_html=True)

    # Do some css styling tricks here (e.g. remove the padding)
    # https://medium.com/ssense-tech/streamlit-tips-tricks-and-hacks-for-data-scientists-d928414e0c16
    padding = 1
    st.markdown(f""" <style>
                .reportview-container .main .block-container{{
                padding-top: {padding}rem;
                margin-top: -1.5rem;
                padding-right: {padding}rem;
                padding-left: {padding}rem;
                padding-bottom: {padding}rem;
                }} </style> """, unsafe_allow_html=True)
    st.markdown(f""" <style>
                .reportview-container .css-1lcbmhc .block-container{{
                margin-top: -1.0rem;
                }} </style> """, unsafe_allow_html=True)
    # Reduce the space in horizontal component
    st.markdown(f""" <style>
                hr {{
                margin: 10px 0px;
                }} </style> """, unsafe_allow_html=True)

    if tool_name == "—":
        show_code = False
        st.write("# Welcome to Space Weather Monitor Application!")
    else:
        # show_code = st.sidebar.checkbox("Show code", True)
        show_code = False
        st.markdown("# %s" % tool_name)
        description = TOOLS[tool_name][1]
        if description:
            st.write(description)
        # Clear everything from the intro page.
        # We only have 4 elements in the page so this is intentional overkill.
        for i in range(90):
            st.empty()

    tool()

    if show_code:
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(tool)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


    current_conditions()

    # Make the footer         
    footer="""<style>
.footer {
position: fixed;
bottom: 0;
max-width: 100%;
height: auto;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<a href="https://www.buymeacoffee.com/akouloumvako">
<img src='data:image/png;base64,""" + """{}' class='img-fluid' width=300 height=45>
<a/>
</div>
""".format(
    img_to_bytes("buy_me_a_coffee.png")
    )
    st.sidebar.markdown(footer,unsafe_allow_html=True)

if __name__ == "__main__":
    run()
