# GameOfLife_DropTables


![LOGO](assets/img/logo.jpg)

## Live
Grab your OS version from [Releases Page](https://github.com/Madiocre/GameOfLife_DropTables/releases)

## Screenshots
![s1](.res/s1.png)
![s2](.res/Carosel1.png)
![s3](.res/Carosel2.png)
![s4](.res/Movie.png)
![s5](.res/Register.png)
![s6](.res/Map.png)

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Setup and Installation](#setup-and-installation)
6. [Running the Application](#running-the-application)
7. [API Endpoints](#api-endpoints)
9. [Database Schema](#database-schema)
10. [Configuration](#configuration)
11. [License](#license)

## Introduction

...........................

## Features

- Responsive design for various screen sizes

## Technology Stack

- Backend: Flask (Python)

## Project Structure

```text
.
├── Dockerfile
├── LICENSE
├── README.md
├── assets
│   └── img
│       └── logo.jpg
├── gol.py
├── main.py
├── main.spec
├── requirments.txt
└── whdog.py

2 directories, 9 files
```

## Development
- Set up python3-tk `sudo apt install python3-tk`
- install requirments `pip3 install -r requirments.txt`
- Run `python3 whdog.py` For hot reloads

## Setup and Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Madiocre/GameOfLife_DropTables/
   cd GameOfLife_DropTables
   ```
2. Set up python3-tk:
   - `sudo apt install python3-tk`

3. Install requirments:
   - `pip3 install -r requirments.txt`

4. Run
   - `python3 main.py`

## Building
- make sure you have all requirments installed (See last section)
- On linux run `pyinstaller --onefile --add-data "./assets:assets"  --hidden-import "PIL._tkinter_finder" --windowed main.py`
- On windows run `pyinstaller --onefile --add-data "assets;assets"  --hidden-import "PIL._tkinter_finder" --windowed main.py`
- Your build should be in `dist/` folder

## Running the Application (Still under progress)

```sh
docker run -p 5000:5000 remyrecipex
```

Enjoy :D

## Configuration

................

## Authors

- Noor Amjad - [GitHub](https://github.com/Justxd22) / [Twitter](https://twitter.com/_xd222) / [LinkedIn](https://www.linkedin.com/in/noor-amjad-xd)
- Amr Abdelfattah - [GitHub](https://github.com/0x3mr) / [Twitter](https://twitter.com/an0n_amr) / [LinkedIn](https://www.linkedin.com/in/amrabdelfattah/)
- Ahmed Shalaby - [GitHub](https://github.com/Madiocre) / [Twitter](https://twitter.com/Ahmed_K_Shalaby) / [LinkedIn](https://www.linkedin.com/in/ahmed-shalaby-31a03a235/)
- Ahmed Aboalesaad - [GitHub](https://github.com/Ahmed-Aboalasaad) / [Twitter](https://x.com/Aboalesaad_) / [LinkedIn](https://www.linkedin.com/in/ahmed-aboalesaad/)
- Abdelrahman Mohamed - [GitHub](https://github.com/hackerSa3edy) / [Twitter](https://x.com/hackersa3edy) / [LinkedIn](https://linkedin.com/abdelrahmanm0)
- Kedir Jabir - [GitHub](https://github.com/IbnuJabir) / [Twitter](https://x.com/Ibnu_J1) / [LinkedIn](https://www.linkedin.com/in/ibnu-jabir/)

## License

Copyright (C) 2024
Licensed under the GPLv3 License
