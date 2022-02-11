import json
import urllib.request

from pandas import json_normalize


def current_conditions(st):
    st.sidebar.markdown("""---""")
    st.sidebar.markdown("""## Space Weather Conditions ☂: """)

    with urllib.request.urlopen('https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json') as fp:
        data = json.loads(fp.read().decode())
    latest_flares = json_normalize(data)
    max_class = latest_flares['max_class'][0]
    if max_class is not None:
        max_time = latest_flares['max_time'][0][0:16]
        if 'B' in max_class:
            color = 'Lime'
        elif 'C' in max_class:
            color = 'yellow'
        elif 'M' in max_class:
            color = 'orange'
        elif 'X' in max_class:
            color = 'red'
    else:
        max_class = 'None'
        max_time = 'Now'
        color = 'None'
    st.sidebar.markdown(f"""Latest X-ray solar flare: <br />
                                     ➠ <span style="color:black; background:{color}">{max_class}</span> @{max_time}""", unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    # solar_wind_plasma = json_normalize(data)
    density = data[-1][1]
    time  = data[-1][0][0:16]
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/plasma-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    # solar_wind_plasma = json_normalize(data)
    speed = data[-1][2]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""Solar Wind: @{time} <br />
                                     ➠ Density: {density} protons/cm3 <br />
                                     ➠ Speed: {speed} km/s  <br />""", unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/solar-wind/mag-1-day.json') as fp:
        data = json.loads(fp.read().decode())
    # solar_wind_plasma = json_normalize(data)
    mag_tot = data[-1][6]
    mag_z = data[-1][3]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""IP Mag. Field: @{time} <br />
                                     ➠ Btot: {mag_tot} nT &nbsp;
                                     ➠ Bz: {mag_z} nT """, unsafe_allow_html=True)
    with urllib.request.urlopen('https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json') as fp:
        data = json.loads(fp.read().decode())
    # solar_wind_plasma = json_normalize(data)
    kp = data[-1][1]
    time  = data[-1][0][0:16]
    st.sidebar.markdown(f"""Planetary K-index: <br />
                                     ➠ Kp: {kp} @{time}""", unsafe_allow_html=True)
