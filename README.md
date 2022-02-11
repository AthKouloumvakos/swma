# Space Weather Monitor Application (SWMA)

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Version](https://img.shields.io/github/v/release/AthKouloumvakos/swma)](https://github.com/AthKouloumvakos/swma/releases)
[![Release Date](https://img.shields.io/github/release-date/AthKouloumvakos/swma)](https://github.com/AthKouloumvakos/swma/releases)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![flake8](https://github.com/AthKouloumvakos/swma/actions/workflows/flake8.yml/badge.svg)
![pytest](https://github.com/AthKouloumvakos/swma/actions/workflows/pytest.yml/badge.svg)

Space Weather Monitor Application (SWMA) is an open-source software package that can be used to visualize realtime space weather related data. An online preview of this tool is available at [https://athkouloumvakos.github.io/swma](https://athkouloumvakos.github.io/swma).

## 💾 Installation

_SWMA_ is written in Python >=3.8 and has some package requirements, which are listed in the requirements.txt and environment.yml files.
To run localy this application we recomend to create its own virtual enviroment in Python.

**Recomended (conda)**

Because of a range of dependencies that packages have, the simplest way to work with _SWMA_
is in conda and to create its own environment using the ```conda env create```.
If you already have conda installed, then ```cd``` the root directory of _SWMA_ and in your terminal do:

```python
# Create a virtual environment in python using conda
#  see https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html
conda env create -f environment.yml
conda info --envs

# Activate the enviroment
conda activate swma

# When you are done you can deactivate a virtual environment
conda deactivate
```

**Alternative (pip)**

```python
# You can create a virtual environment in Python inside the project folder.
#  see https://docs.python.org/3/library/venv.html
python3 -m venv env

# Activate the enviroment
source env/bin/activate

# install the required packages using pip3
pip3 install -r requirements.txt

# When you are done you can deactivate a virtual environment
deactivate
```

Now you can run any part of the _SWMA_ (see Usage section).

You may also add your _SWMA_ directory to the environment variable ```PYTHONPATH```. This is usefull if you need to run _SWMA_ tests or when you need to run some of the package modules out of streamlit.

In the terminal use the following and change the \<SWMARootDir\> with your path.

```
export PYTHONPATH="${PYTHONPATH}:<SWMARootDir>/SWMA"
```

For a premanent solution, if you're using bash (on a Mac or GNU/Linux distribution), add the above line to your ```~/.bashrc``` file (changing the \<SWMARootDir\> with your path first).

## 🐾 Run localy the _SWMA_ application

Install the required Python packages, activate the enviroment as shown above, and then run the application with streamlit.
```
# cd into the package directory and run,
streamlit run swma.py
```
The application should now open in the default browser!

The application should  open in the default browser.

## 🖵 Availiable realtime monitors:

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
