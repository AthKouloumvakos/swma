# Space Weather Monitor Application (SWMA)

An open-source app framework built specifically for visualizing realtime space weather related data. An online preview of this tool is available at [https://athkouloumvakos.github.io/swma](https://athkouloumvakos.github.io/swma) .

## Installation

To run localy this application you have to create a virtual enviroment in python, install the required python packages, and then run the application with streamlit. The package requirements are listed in the requirements.txt. So in your terminal:

```python
# You can create a virtual environment in Python inside the project folder.
# see https://docs.python.org/3/library/venv.html
python3 -m venv env

# Activate the enviroment
source env/bin/activate

# install the required packages using pip3
pip3 install -r requirements.txt

# When you are done you can deactivate a virtual environment
deactivate
```
The application should now open in the default browser!

## Run localy the SWMA application

After installing the required Python packages and activating the enviroment as shown above, run the application with streamlit.
```python
# In the terminal:
streamlit run swma.py
```

The application should  open in the default browser.

## Availiable realtime monitors 🖵:

- Soft x-ray flux (NOAA-GOES)
- Proton flux (NOAA-GOES)
- Solar Propabilities (NOAA)
- EUV Images (SDO/AIA)
- Coronagraphic Images (SoHO/LASCO)

### About the monitors:

**Soft x-ray flux (NOAA-GOES)**: Visualize real-time measurements of **X-ray flux** from GOES satelites. The SXR data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated every 1-minute.

**Proton flux (NOAA-GOES)**: Visualize real-time measurements of **proton flux** from GOES satelites. The proton flux data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated every 1-minute.

**Solar Events Forecast (NOAA)**: Visualize near-real-time **forecasts** of the likelihood (probability) of the occurrence of a solar event. the flare and the solar proton event foracast data are provided from the NOAA Solar Weather Prediction Center (SWPC) in JSON format and are updated daily. The flare forecasts are daily probabilistic forecasts, ranging from 1% to 99%, of the likelihood of a given class x-ray flare to occur within a time interval.

**EUV Images (SDO/AIA)**: Show near-real-time images of the solar chromosphere and corona from observations of the Atmospheric Imaging Assembly (AIA) on board the Solar Dynamics Observatory (SDO) in extreme ultraviolet (EUV). SDO is a NASA mission which has been observing the Sun since 2010. The AIA provides continuous near-real-time observations of the solar chromosphere and corona in seven channels in EUV. The images are provided from NASA/SDO in .png format.

**Coronagraphic Images (SoHO/LASCO)**: Show near-real-time images of the solar corona in white light from observations of the Large Angle and Spectrometric Coronagraph (LASCO) on board the Solar and Heliospheric Observatory satellite (SoHO). The coronagraphic images are provided from NASA/nascom in .jpg format.

## Usefull python packages 📦:
        
- [SunPy](https://sunpy.org/): The community-developed, free and open-source solar data analysis environment for Python.
- [AstroPy](https://www.astropy.org/): The Astropy Project is a community effort to develop a single core package for Astronomy in Python.
