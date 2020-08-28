## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

 


## About The Project

This project was inspired by a problem that I wanted to solve as a CS student who likes to develop on his desktop PC but then needs transfer/have files available on his laptop. A lot of the times transferring files either requires an account to a reputable service such as Dropbox, or it requires a USB key (which may not be readily accessible). But even with a Dropbox or USB you have to remember to upload the proper files; which can only become apparent at a later date. As a result I began RFAWT in order to easily and quickly transfer files from anyone of my PC's to a remote machine while anywhere in the world, (primarily at school) while having access to my entire PC file structure.

Overview of How it Works
* Setup a Flask server on your main machine at home with port forwarding enabled on your network
* Setup any node children servers on any other pc's in your home which will connect to your main pc. (This allows you to grab files from more than one PC without having to install requirements on each)
* Create an account for login authentication.

![](https://i.imgur.com/s0ayhd4.png)


This project was initially created for windows as back in the day I mainly used Windows. But now I have made changes to the codebase in order to support Mac OSX as well as Linux. Full support for UNIX (OSX and Linix) is still in progress as I am still looking for potential bugs but nevertheless RFAWT is fully usuable on all platforms.

### Built With
Major frameworks and tools used in this project. Please note that a lot of compliemntary libraries were also significant.
* [Python](https://www.python.org/download/releases/3.0/)
* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Bootstrap](https://getbootstrap.com/)

 

## Getting Started
This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* Must have Python3, Pip3, and Virtualenv.
* Example of how to setup venv and start the virtual environment
```sh
python3 -m venv ./rfawt/env && source bin/activate
```

### Installation

1. Clone the repo
```sh
git clone https://github.com/MikePresman/RFAWT.git
```
2. Cd into RFAWT and Install the Requirements.txt
```sh
pip3 -r requirements.txt
```
3. Setup the Flask Server
```sh
// Unix : export FLASK_APP=run.py
// Unix : export FLASK_ENV=development

// Windows : set FLASK_APP=run.py
// Windows : set FLASK_ENV=development
```
4. Start the server
```sh
flask run
```

 


## Usage
Login with the default credentials. 
Username: Admin
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

 

## License

Distributed under the MIT License. See `LICENSE` for more information.

 

## Contact

Michael Presman - mikepresman@gmail.com

 

 

 


![](https://i.imgur.com/o2dOuJo.png)
2 visits · 2 online