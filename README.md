# Salta Services

Project by: Ain Bolaños Cortés A01660732

### Provide and extensible project in Python to work with Google's API of Google Sheets though the use of a Service Account. 

Previous steps to implement inside a session of Google Cloud and creating a Service Account found on [here](https://developers.google.com/sheets/api/quickstart/python).

---
## manage_sheets.py
An Object-Oriented module that allows the developer create a `GoogleSheets` object and execute commands of edit simpler, mantaaining the modular philosophy of Python and also to reduce possible verbose as the API uses different layers in the Google Projects to allow make changes. The module uses a service account made with Google Cloud, if suitable, check put the module on `SaltaServicesSrc/manage_sheets.py`.

## Introduction to the project and the IA: 

This repository is for anyone that is trying to find a way to manage the production and sales of a company in the production of goods. With the help of Google Sheets and a terminal based (cli) application that runs a simple but rather fast way to edit the Manager Sheets. The Internal Assesment is initially aimed for *Salta Shoes* a shoe production company, but with addaptations over the `backend_main.py` module, the cli-program will be able to fit intoother similar projects or for any company that currently uses Google Sheets as a tool for their lean production. 
The repository and documentation around the algorithms developed fullfil the Criteria C: Development, and will be continiously improved as the project gets bigger and bigger. 

*Considerations*: The project is working only on Python, different addaptations should be made to use it on another language. The project is using Python 3.10 or upper and takes advantage of the free access modules inside the *pip* library of modules created by Google themselfs. 

## Implementation
The project connects directly with the following Google Sheets: [Salta Services Sheets](https://docs.google.com/spreadsheets/d/1UGu1bBWuS-J6lmuxuCMwv_GL8LUPlpXzTZ3VGR4Nyz0/edit?usp=sharing), this link provides a *read only* mode access in order to keep certain order in the project while allowing any possible user to interact with the solution. 

In addition, you can also check the Criterion D video [here](https://youtu.be/HFa2AMmqrrc) with an example of full use of the system.

## Installation:
To install the program in your computer using your own Google Sheets follow the appropiate guide for your OS: 

### Linux or MacOS
Firstly, make sure Python is working on your Mac with the following: 

```
python -V
python3 -V
```

`cd` to the directory where you want to install the program and run: 
```
$ git clone https://github.com/0kron/SaltaServices
```
> If you have your own Google Sheets, replace the `key.json` file in the project to your's. 

And simply run the program using: 
```
$ python3 $HOME/path/to/the/git_clone/SaltaServicesSrc/main.py
```
On **Linux** you may also assaign an `alias` to the command on `.bashrc`: 
```
alias pomodoro='python3 $HOME/path/to/the/git_clone/SaltaServices/backend_main_salta.py
```
To do something similar on **MacOS** follow [this](https://developers.google.com/sheets/api/guides/concepts) guide to install the mandatory `pip` modules in the virtual enviroment of your computer. 
*if necessary: allow the development tools of Xcode in MacOs, it is not necessary that you install the complete Xcode IDE*
