# Salta Services

Project by: Ain Bolaños Cortés A01660732

### Provide and extensible project in Python to work with Google's API of Google Sheets though the use of a Service Account. 

Previous steps to implement inside a session of Google Cloud and creating a Service Account found on [here](https://developers.google.com/sheets/api/quickstart/python).

---
## manage_sheets.py
An Object-Oriented module that allows the developer create a `GoogleSheets` object and execute commands of edit simpler, mantaaining the modular philosophy of Python and also to reduce possible verbose as the API uses different layers in the Google Projects to allow make changes.

## Introduction to the project and the IA: 

This repository is for anyone that is trying to find a way to manage the production and sales of a company in the production of goods. With the help of Google Sheets and a terminal based (cli) application that runs a simple but rather fast way to edit the Manager Sheets. The Internal Assesment is initially aimed for *Salta Shoes* a shoe production company, but with addaptations over the `backend_main.py` module, the cli-program will be able to fit intoother similar projects or for any company that currently uses Google Sheets as a tool for their lean production. 
The repository and documentation around the algorithms developed fullfil the Criteria C: Development, and will be continiously improved as the project gets bigger and bigger. 

*Considerations*: The project is working only on Python, different addaptations should be made to use it on another language. The project is using Python 3.10 or upper and takes advantage of the free access modules inside the *pip* library of modules created by Google themselfs. 

## Installation:
To install the program in your computer using your own Google Sheets follow the appropiate guide for your OS: 

### Linux 
`cd` to the directory where you want to install the program and run: 
```
$ git clone https://github.com/0kron/SaltaServices
```
Replace the `key.json` file in the project to your's. And simply run the program using
```
$ python3 $HOME/path/to/the/git_clone/pomodoro/main.py
```
Or assaign an `alias` to the command on `.bashrc`: 
```
alias pomodoro='python3 $HOME/path/to/the/git_clone/SaltaServices/backend_main_salta.py
```

### MacOS
Open the Terminal application and use the comand `cd` to go into the chosen directory, for example dir *programs*: 
```
cd Desktop/programs/
```

Then, make sure Python is working on your Mac with the following: 
```
python -V
python3 -V
```
And follow [this](https://developers.google.com/sheets/api/guides/concepts) guide to install the mandatory `pip` modules in the virtual enviroment of your computer. 
*if necessary: allow the development tools of Xcode in MacOs, it is not necessary that you install the complete Xcode IDE*

Finally, you are ready to follow the same steps as in the Linux section. 

### Windows
Copy the files in this repository to a folder of your combenience and make sure you have Python in your PATH by running: 
```
python --version
Python 3.10.X
```
Note that this program works with some new features just included on Python 3.10, an update version of Python can be located [here](https://www.python.org/downloads/). 

To run the program follow the following command: 
```
> python3 C:\Users\user\path\of\the\folder\main.py
```
Or create and alias using the `DOSKEY` command like: 
```
> DOSKEY pomodoro=python3 C:\Users\user\path\of\the\folder\main.py
```
To that last option follow [this](https://shivamethical.medium.com/create-command-line-alias-in-windows-76684635b4c4) guide for creating a `*.bat` file.


**Note:** this program is for free use, recommendations and questions may be asked through this repository.


jalas?
