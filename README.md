# EasyCNC 

[![pyqt6](https://img.shields.io/badge/pyqt6-6.7.0-blue?style=flat-square&logo=qt)](https://pypi.org/project/PyQt6/)
[![sqlalchemy](https://img.shields.io/badge/sqlalchemy-2.0.30-blue?style=flat-square&logo=sqlalchemy)](https://pypi.org/project/sqlalchemy/)
[![opencv-python](https://img.shields.io/badge/opencv--python-4.9.0.80-blue?style=flat-square&logo=opencv)](https://pypi.org/project/opencv-python/)
[![numpy](https://img.shields.io/badge/numpy-1.26.4-blue?style=flat-square&logo=numpy)](https://pypi.org/project/numpy/)
[![matplotlib](https://img.shields.io/badge/matplotlib-3.9.0-blue?style=flat-square&logo=matplotlib)](https://pypi.org/project/matplotlib/)
[![pytest](https://img.shields.io/badge/pytest-8.2.1-blue?style=flat-square&logo=pytest)](https://pypi.org/project/pytest/)

<img src="src/app/resources/images/app%20logo.png" alt="App Logo" width="1200"/>

EasyCNC is a free, platform-independent solution for effectively managing CNC inventories and routers.
It can easily be integrated into an existing workflow and leverages computer vision for digitizing used stock, and is capable of automatically generating highly optimal layouts for machining new parts. 
EasyCNC is intended for machining 2D parts on 3-axis CNC routers. 

Supported Languages:
- English (UK, US) 🇬🇧 🇺🇸
- Chinese (Simplified, Traditional) 🇨🇳 🇹🇼
- Russian 🇷🇺
- Japanese 🇯🇵

# Table of Contents

- Installation
- App Structure and Functionality
- Optimization Algorithm
- FAQ

# Installation

1. Make sure that you have Python version 3.10.4 or higher installed on your system.

2. Download ZIP file containing GitHub source code.

3. Extract all files to a directory of your choice.

4. Run the following commands to execute the program:

``` 
cd <TARGET_DIR>\easycnc-main
pip install -r requirements.txt
python run.py
```

## Running Locally

The app is ready to run locally out of the box. By default, it is configured to create a SQLite3 database titled app_data.db in the src\data directory.

## Database Hosting

# App Structure and Functionality

## App Architecture

The app follows a traditional MVC structure. 

## CAD File Conversion

## Plate Image Conversion

## Placement Optimization

# FAQ
