# doctorsrus
An appointment booking system built on JSON files

## Overview

The Doctors 'R' Us Appointment Booking System is a console-based application designed for educational purposes.

This program demonstrates how to update JSON files, use dictionaries and lists, and build menus in a console application.

It is a simple booking system that allows users to manage and manipulate data related to doctor appointments.

## Features

- Initialize database tables (JSON files)
- Print records from tables
- Update records in tables
- Print various reports
- Manage appointments
- Reset tables
- User-friendly console menus

## Purpose

This program is intended solely for educational purposes. 
It serves as a practical example for learning the following concepts while programming in Python:

	- Updating and managing JSON files
	- Utilizing dictionaries and lists in Python, retriving input from users and checking it for data validation
	- Utilizing functions and Python modules to manage your code
	- Building and navigating menus in console applications using libraries such as beaupy, rich and art

## Installation

Clone this repository.

Navigate to the project directory.

Install the required dependencies:

	pip install -r requirements.txt

Run the main program:

	python PrU_main.py

Main Menu Options:

	- Print the records in a table: Select and display records from a chosen table.
	- Update the records in a table: Choose a table to update and modify its records.
	- Print Reports: Generate and display various reports.
	- Manage appointments: Edit and manage appointment data.
	- Reset a table: Reset the chosen table to an empty state.
	- Exit: Exit the program.

## Program Structure
	- PrU_main.py: Main program file containing the core logic and menu system.
	- PrU_helper_json.py: Helper functions for JSON file operations.
	- PrU_helper_db.py: Helper functions for database (JSON files) management.
	- PrU_helper_menus.py: Helper functions for menu operations.

## Dependencies
	- beaupy: For enhanced menu navigation.
	- rich: For rich text formatting in the console.
	- art: For ASCII art generation.

You can install these dependencies using the requirements.txt file provided.

## License
This project is licensed under the MIT License.

## Disclaimer: 
This program is not intended for real-world use and should only be used as a learning tool.
I wrote this program as a project for a Python larning class, as such, I don't plan on making any further changes or improvements to this code nor to offer any support in running or troubleshooting it, but please feel free to use it and change it as you seem fit for your purposes.
