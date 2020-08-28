## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Contact](#contact)

 


## About The Project

This project allows any individual to connect to any number of machines on a LAN and get access to their folder structure and files remotely via HTTP.

Overview of How it Works
* Connect to the networks IP via the browser
* Login into the server via credentials established on setup
* Gain access to any connected PC on the remote network to get access to their files and folders

![](https://i.imgur.com/s0ayhd4.png=300x300)
![](https://i.imgur.com/4ZtGohZ.png=300x300)

This project supports both Unix (Mac OSX and Linux) as well as Windows systems.

### Built With
Major frameworks and tools used in this project. Please note that a lot of complimentary libraries were also significant.
* [Python](https://www.python.org/download/releases/3.0/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Bootstrap](https://getbootstrap.com/)

 

## Getting Started
To get a local copy up and running follow these simple example steps.

### Prerequisites

* Must have Python3, Pip3, and venv.
* Example of how to setup venv and start the virtual environment

-Unix (Mac and Linux & Windows WSL Terminal)
```sh
python3 -m venv ./rfawt_env && cd ./rfawt_env && source bin/activate && cd ..
```
-Windows
```sh
python3 -m -venv ./rfawt_env && cd ./rfawt_env && cd scripts && activate && cd ..
```
### Installation

1. Clone the repo
```sh
git clone https://github.com/MikePresman/RFAWT.git
```
2. Cd into RFAWT and Install the Requirements.txt
```sh
cd RFAWT && pip3 -r requirements.txt
```
3. Setup the Flask Server
* Unix (Linux and OSX)
```sh
export FLASK_APP=run.py
export FLASK_ENV=production
```
* Windows
```sh
set FLASK_APP=run.py
set FLASK_ENV=production
```
4. Start the server
```sh
flask run
```

 


## Usage
Login with the default credentials. <br/>
Username: Admin<br/>
Password: 1234


## Roadmap
* Continue working on Unix support
* Implement Upload feature (have to be security aware)

 

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

 


 

## Contact

Michael Presman - mikepresman@gmail.com

 

 

 




