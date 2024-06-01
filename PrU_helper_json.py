# PrU_helper_json.py
# helper functions for json file handling

import json
import os
import beaupy
from datetime import datetime, date
from PrU_helper_db import *
from rich.console import Console
from rich.table import Table

# initialize the console from the rich library
console = Console()

##################
# helper functions

def pause(message="Press any key to continue..."):
    """
    Pauses the program and waits for the user to press any key.
    
    Args:
    - message (str): The message to display to the user.
    """
    console.print(message, style="bold yellow")
    console.input()

def calculateAge(date_str):
    """
    Calculates the age based on the given birth date.
    
    Args:
    - date_str (str): The birth date string in the format 'YYYY-MM-DD'.
    
    Returns:
    - int: The calculated age.
    """
    today = date.today()
    try:
        birth_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except (ValueError, TypeError) as e:
        console.print(f"Error: {e}", style="bold red")
        return 0
    else:
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

def daysFromToday(date_str):
    """
    Calculate the number of days the given date is from today.
    
    :param date_str: A date in the format 'YYYY-MM-DD'.
    :return: Number of days from today. Positive for future dates, negative for past dates, 0 for today.
    :raises ValueError: If the date_str is not in the valid format 'YYYY-MM-DD'.
    """
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today = datetime.today().date()
        delta = (date - today).days
        return delta
    except ValueError:
        raise ValueError("Invalid date format. Please use 'YYYY-MM-DD'.")

def isListOfDicts(data):
    """
    Check if the provided data is a list of dictionaries.

    :param data: The data to check.
    :return: True if the data is a list of dictionaries, False otherwise.
    """
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        return True
    return False

##################
# functions to manage files

def loadJTable(table_name):
    """
    Load a JSON file and return the data.
    
    :param table_name: The name of the table (file) to load.
    :return: The data in the file as a list of dictionaries, or an empty list if the file is not found or invalid.
    """
    file_path = os.path.join(J_DB_FOLDER, table_name) + ".json"
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        console.print(f"Error: JSON decoding error in file {file_path}", style="bold red")
        return []
    except Exception as err:
        console.print(f"Error loading table {table_name}: {err}", style="bold red")
        return []
    else:
        if isListOfDicts(data):
            return data
        else:
            return []

def saveJTable(table_name, my_table):
    """
    Save a list to a JSON file.
    
    :param table_name: The name of the table (file) to save.
    :param my_table: The list of dictionaries to save.
    :return: 1 on success, or 0 on failure.
    """
    if isListOfDicts(my_table):
        file_path = os.path.join(J_DB_FOLDER, table_name) + ".json"
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(my_table, f, indent=4)
                return 1
        except Exception as e:
            console.print(f"Error saving table {table_name}: {e}", style="bold red")
            return 0
    else:
        return 0

def initJTable(table_name, overwrite=False):
    """
    Initialize a JSON table file with an empty list.
    
    :param table_name: The name of the table (file) to initialize.
    :param overwrite: Boolean indicating whether to overwrite the file if it exists.
    :return: 1 if the table is initialized or overwritten, 0 if the file exists and is not overwritten, or -1 on failure.
    """
    file_path = os.path.join(J_DB_FOLDER, table_name) + ".json"
    
    try:
        if os.path.exists(file_path) and not overwrite:
            return 0  # file exists, keep it as-is, no changes
        
        success = saveJTable(table_name, [])
        return success if success == 1 else -1  # return result of saveJTable (if success) or -1 on failure
    except Exception as e:
        console.print(f"Error initializing table {table_name}: {e}", style="bold red")
        return -1

##################
# functions to manage json records

def addJRecord(table_name, record):
    """
    Add a new record to the JSON table, assigning a new ID.
    
    :param table_name: The name of the table (file) to add the record to.
    :param record: The dictionary representing the new record.
    :return: 1 on success, or 0 on failure.
    """
    data = loadJTable(table_name)
    record['id'] = max([r['id'] for r in data]) + 1 if data else 1
    data.append(record)
    success = saveJTable(table_name, data)
    if success:
        printDict(record)
    return success

def getKeyMatch(data, **kwargs):
    """
    Find a dictionary in the list where the specified key matches the given value.
    
    :param data: The list of dictionaries to search.
    :**kwargs: as a named key:value pairs
    :return: The matching dictionary on success, or None on failure.
    """
    if not data:
        return []
    its_a_match = []
    for key, value in kwargs.items():
        for item in data:
            if item.get(key) == value:
                its_a_match.append(item)
    return its_a_match

def updateJRecord(table_name, record_id, update_info):
    """
    Update a record in the JSON table.
    
    :param table_name: The name of the table (file) to update.
    :param record_id: The ID of the record to update.
    :param update_info: A dictionary of fields to update with their new values.
    :return: 1 on success, or 0 on failure.
    """
    data = loadJTable(table_name)
    update_info.pop('id', None)  # Ensure the 'id' key is removed, if present
    my_record = getKeyMatch(data, id=record_id)[0] # Get the first matching record from the list returned
    if my_record:
        my_record.update(update_info)   # put update_info on my_record
        success = saveJTable(table_name, data)
        if success:
            printDict(my_record)
        return success
    else:
        return 0

def getUserInput(key, value_type):
    """
    Prompts the user for a value of a specified type and casts it to that type.
    
    Args:
    - key (str): The key to be displayed in the prompt.
    - value_type (tuple): value_type[0] holds the type of value expected ('int', 'text', 'date' or 'set').
    
    Returns:
    - The value cast to the specified type if valid, otherwise None.
    """
    while True:
        match value_type[0]:
            case 'int':
                user_input = console.input(f"[bold blue]Please enter a value for[/bold blue][bold yellow] {key} (integer): [/bold yellow]")
                try:
                    return int(user_input)
                except ValueError:
                    console.print("[bold red]Invalid input. Please enter a valid integer.[/bold red]")
            
            case 'text' | 'str':
                user_input = console.input(f"[bold blue]Please enter a value for[/bold blue][bold yellow] {key} (text): [/bold yellow]")
                if user_input:      # must not be an empty string
                    return user_input
                else:
                    console.print("[bold red]Invalid input. Please enter valid text.[/bold red]")

            case 'set':
                console.print(f"[bold blue]Please enter a value for[/bold blue][bold yellow] {key} (one of {value_type[1]}): [/bold yellow]")
                user_input = beaupy.select(list(value_type[1]), cursor="->", cursor_style='green')
                return user_input.title()
                    
            case 'date':
                user_input = console.input(f"[bold blue]Please enter a value for[/bold blue][bold yellow] {key} (date in YYYY-MM-DD format): [/bold yellow]")
                try:
                    parsed_date = datetime.strptime(user_input, '%Y-%m-%d').date()
                    today = datetime.today().date()

                    if key == 'date_of_birth' and parsed_date > today:
                        console.print("[bold red]Invalid input. Date of birth cannot be in the future.[/bold red]")
                    elif key == 'booking_date' and parsed_date < today:
                        console.print("[bold red]Invalid input. Booking date cannot be in the past.[/bold red]")
                    else:
                        return parsed_date.strftime('%Y-%m-%d')
                except ValueError:
                    console.print("[bold red]Invalid input. Please enter a valid date in the format YYYY-MM-DD.[/bold red]")
            
            case 'FK':
                return None    # placeholder for future use case

            case _:
                console.print(f"[bold red]Unsupported type: {value_type[0]}[/bold red]")
                return None

def putDict(dict_schema):
    """
    Collects user inputs based on the structure of a dictionary schema.
    
    Args:
    - dict_schema (dict): A dictionary where keys are field names and values are types (or descriptions).

    Returns:
    - dict: A new dictionary filled with user input values.
    """
    new_dict = {}
    for key, value_type in dict_schema.items():  # get one key at a time
        match key:
            case 'id':  # don't ask the user for an 'id'
                new_dict[key] = 0  # added as a placeholder, it will be re-assigned by addJRecord()

            case 'patient_id' | 'doctor_id':
                # Load the corresponding table and present the options to the user
                table_name, display_key = value_type[1]
                table_data = loadJTable(table_name)

                if not table_data:
                    console.print(f"No data found in the {table_name} table.", style="bold red")
                    new_dict[key] = None
                    continue

                options = {item['id']: item[display_key] for item in table_data}
                console.print(f"Select a {key.replace('_id', '')} from the list below:", style="bold blue")
                for id, name in options.items():
                    console.print(f"{id}: {name}", style="bold green")

                while True:
                    selected_id = console.input(f"[bold blue]Please enter the ID for {key.replace('_id', '')}: [/bold blue]")
                    try:
                        selected_id = int(selected_id)
                        if selected_id in options:
                            new_dict[key] = selected_id
                            break
                        else:
                            console.print("[bold red]Invalid ID. Please enter a valid ID from the list.[/bold red]")
                    except ValueError:
                        console.print("[bold red]Invalid input. Please enter a valid integer ID.[/bold red]")

            case _:
                user_input = getUserInput(key, value_type)
                new_dict[key] = user_input

    return new_dict

def patchDict(my_table_name, my_record):
    """
    Patch a dictionary record in a table by updating its fields while respecting update restrictions.
    
    Args:
    - my_table_name (str): The name of the table containing the record.
    - my_record (dict): The dictionary record to be patched.
    
    Returns:
    - int: 1 on success, 0 on failure.
    """

    new_record = putDict(my_db_schema[my_table_name])  # calls putDict with the schema
    success = updateJRecord(my_table_name, my_record['id'], new_record)
    
    return success

def printDict(data_dict):
    """
    Prints each key-value pair in the dictionary.
    
    Args:
    - data_dict (dict): The dictionary to be printed.
    """
    if not data_dict:
        console.print(f"[bold red]Error: there's no records[/bold red]")
        return
    
    for key, value in data_dict.items():
        match key.lower():
            case 'id':
                console.print(f"[bold blue]ID Number[/bold blue] : [bold green]{value}[/bold green]")
            
            case 'name' | 'status':
                console.print(f"[bold blue]{key.title()}[/bold blue] : [bold green]{value.title()}[/bold green]")
            
            case 'date_of_birth':
                console.print(f"[bold blue]Age[/bold blue] : [bold green]{calculateAge(data_dict[key])} years old[/bold green]")
            
            case 'salary' | 'price':
                console.print(f"[bold blue]{key}[/bold blue] = [bold green]{value} EUR[/bold green]")
            
            case 'patient_id' | 'doctor_id':
                console.print(f"[bold blue]{key}[/bold blue] : [bold green]{value}[/bold green]")

            case 'booking_date':
                try:
                    result = daysFromToday(data_dict[key])
                    if result > 0:
                        console.print(f"[bold blue]Booking date[/bold blue] : [bold green]{data_dict[key]} is {result} days in the future.[/bold green]")
                    elif result < 0:
                        console.print(f"[bold blue]Booking date[/bold blue] : [bold green]{data_dict[key]} is {-result} days in the past.[/bold green]")
                    else:
                        console.print(f"[bold blue]Booking date[/bold blue] : [bold green]{data_dict[key]} is today.[/bold green]")
                except ValueError as err:
                    console.print(f"[bold red]Error: {err}[/bold red]")
                    console.print(f"[bold blue]{key}[/bold blue] : [bold green]{value}[/bold green]")

            case _:
                console.print(f"[bold blue]{key}[/bold blue] = [bold green]{value}[/bold green]")

def printDictsAsTable(dict_list):
    """
    Prints a list of dictionaries as a formatted table.
    
    Args:
    - dict_list (list of dict): The list of dictionaries to print.
    """
    if not dict_list:
        console.print("No data to display.", style="bold red")
        return

    # Load patient and doctor tables to support name resolution
    patient_data = {item['id']: item['name'] for item in loadJTable('patient')}
    doctor_data = {item['id']: item['name'] for item in loadJTable('doctor')}

    # Initialize the table
    table = Table(show_header=True, header_style="bold magenta")

    # Add columns to the table based on the keys of the first dictionary
    keys = list(dict_list[0].keys())
    for key in keys:
        if key == 'date_of_birth':
            table.add_column('Current Age', style="dim", justify="left")
        elif key == 'booking_date':
            table.add_column('Booking Date', style="dim", justify="left")
            table.add_column('Days from Today', style="dim", justify="left")
        elif key == 'patient_id':
            table.add_column('Patient Name', style="dim", justify="left")
        elif key == 'doctor_id':
            table.add_column('Doctor Name', style="dim", justify="left")
        else:
            table.add_column(key, style="dim", justify="left")

    # Add rows to the table, checks the keys to choose best printing options
    for item in dict_list:
        row = []
        for key in keys:
            if key == 'date_of_birth':
                age = calculateAge(item.get(key, ""))
                row.append(str(age) if age is not None else "Invalid Date")
            elif key == 'booking_date':
                booking_date = item.get(key, "")
                days = daysFromToday(booking_date)
                row.append(booking_date)
                row.append(str(days) if days is not None else "Invalid Date")
            elif key == 'patient_id':
                patient_name = patient_data.get(item.get(key), "Unknown Patient")
                row.append(patient_name)
            elif key == 'doctor_id':
                doctor_name = doctor_data.get(item.get(key), "Unknown Doctor")
                row.append(doctor_name)
            else:
                row.append(str(item.get(key, "")))
        table.add_row(*row)

    # Print the table
    console.print(table)

##################
# functions to manage appointments

def selectRecordByID(my_table, display_key='name'):
    """
    Presents a list of records for the user to select from and returns the selected record's ID.
    Expects the table to have matching keys for 'id' and display_key.
    
    Returns:
    - int: The ID of the selected record.
    """
    # Load table data
    my_data = loadJTable(my_table)

    if not my_data:
        console.print("No records found in the database.", style="bold red")
        pause()
        return None
    
    if not all('id' in d and display_key in d for d in my_data):
        console.print(f"The keys 'id' and {display_key} are not found in all the records.", style="bold red")
        pause()
        return None

    # Display the list of records
    console.print("Select a record from the list below:", style="bold blue")
    keys_list = [f"{d['id']} : {d[display_key]}" for d in my_data if 'id' in d and display_key in d]
    op = beaupy.select(keys_list, cursor="->", cursor_style='green', return_index=True) + 1
    return op
    
def bookAppointment(my_booking_table='appointment_join', booking1='patient_id', booking2='doctor_id'):
    """
    Books an appointment by creating a dictionary based on the schema defined in my_db_schema[my_booking_table].
    The returned 'id' is always set to 0.
    
    Args:
    - my_booking_table (str): The name of the booking table (default is 'appointment_join').
    - booking1 (str): The key for the first booking ID (default is 'patient_id').
    - booking2 (str): The key for the second booking ID (default is 'doctor_id').
    
    Returns:
    - dict: A dictionary representing the appointment.
    """
    # Clear the terminal
    console.clear()

    appointment_schema = my_db_schema[my_booking_table]
    appointment = {}

    # Set the 'id' to 0, as a placeholder for the key
    appointment['id'] = 0

    # Prompt the user for other fields
    for key, value_type in appointment_schema.items():
        if key == 'id':
            continue  # Skip 'id' as it's already set to 0
        
        # these two keys require loading values from additional tables
        elif key in (booking1, booking2):       
            # Load the corresponding table and present the options to the user
            table_name, display_key = value_type[1]   # gets the (table, attribute) tuple from the schema
            appointment[key] = selectRecordByID(table_name, display_key) # returns the 'id' selected by the user
        
        # all other keys are handled as default
        else:
            user_input = getUserInput(key, value_type)
            appointment[key] = user_input

    return appointment

def updateAppointment(my_booking_table='appointment_join', booking1='patient_id', booking2='doctor_id'):
    """
    Displays the appointment table, asks for an update, and applies the update with restrictions.
    Updates are restricted by status (Cancelada, Realizada) and booking date (set in the past).
    
    Args:
    - my_booking_table (str): The name of the booking table (default is 'appointment_join').
    - booking1 (str): The key for the first booking ID (default is 'patient_id').
    - booking2 (str): The key for the second booking ID (default is 'doctor_id').
    """

    def getUpdateInfo(record, booking1='patient_id', booking2='doctor_id'):
        """
        Prompts the user for update information based on the given record.
        This is a helper function specific for the appointment_join table and its restrictions.
        
        Args:
        - record (dict): The appointment record to update.
        - booking1 (str): The key for the first booking ID.
        - booking2 (str): The key for the second booking ID.
        
        Returns:
        - dict: A dictionary with the updated fields and their new values.
        """
        update_info = {}
        today = datetime.today().date()
        my_schema = my_db_schema[my_booking_table]
        
        for key, value in record.items():
            if key == booking1:     # patient_id can't be changed
                continue
            
            if key == booking2:     # display doctor_id
                table_name, display_key = my_schema[booking2][1] # get table name and field name from schema
                update_info[key] = selectRecordByID(table_name, display_key)
            
            if key == 'booking_date':
                booking_date = datetime.strptime(value, '%Y-%m-%d').date()   # get booking_data as date
                
                if booking_date < today:    # dates in the past can't be changed, but the status can be updated
                    console.print("The booking date is in the past.", style="bold yellow")
                    while True:
                        new_status = console.input("You can only change the status to 'Canceled' or 'Done'. Enter the new status: ")
                        if new_status.lower() in ['canceled', 'done']:
                            update_info['status'] = new_status.capitalize()
                            return update_info
                        else:
                            console.print("Invalid input. Please enter 'Canceled' or 'Done'.", style="bold red")
                else:
                    update_info[key] = getUserInput(key, my_schema[key]) # get new date

            if key == 'price' or key == 'status':
                update_info[key] = getUserInput(key, my_schema[key])
        
        return update_info

    # main function starts here
    appointments = loadJTable(my_booking_table)
    printDictsAsTable(appointments)
    
    while True:
        try:
            op = int(console.input("Type the ID number for the record you want to update: "))
        except ValueError:
            console.print(f"Error: Type a number between 1 and {len(appointments)}", style="bold green")
            continue
        else:
            if 1 <= op <= len(appointments):
                my_matches = getKeyMatch(appointments, id=op) # returns list
                my_record = my_matches[0] # gets first item in the list, the first match
                if my_record:
                    if my_record['status'].lower() in ['canceled', 'done']:
                        console.print(f"Record cannot be updated because the status is '{my_record['status']}'.", style="bold red")
                        pause()
                        return None
                    else:
                        update_info = getUpdateInfo(my_record, booking1, booking2)
                        if update_info is None:
                            return
                        console.print("Proposed changes:", style="bold blue")
                        # print new values
                        for key, value in update_info.items():
                            console.print(f"{key}: {value}", style="bold blue")
                        # get confirmation
                        if beaupy.confirm("Confirm changes?"):
                            success = updateJRecord(my_booking_table, my_record['id'], update_info)
                            if success:
                                console.print("Record updated successfully.", style="bold green")
                                pause()
                            else:
                                console.print("Failed to update the record.", style="bold red")
                                pause()
                else:
                    console.print("Record not found.", style="bold red")
                    pause()
                break   # didn't find it, my_record is empty, returns None
            else:
                console.print(f"Error: Type a number between 1 and {len(appointments)}", style="bold green")
                pause()

##################
# functions to print reports

def printAppointmentsForDate(my_appointments = 'appointment_join', table1='patient', table2='doctor'):
    """
    Prompts the user for a date and prints a table of appointments for that specific date.
    Supports joins inside my_appointments up to two tables, table1 and table2.
    
    """
    # Prompt user to input a date
    console.print("You must enter a date that exists in the database", style="bold blue")
    date_input = getUserInput("appointment_date", ("date", None))

    if date_input is None:
        console.print("Invalid date input. Exiting.", style="bold red")
        pause()
        return    # exit early

    # Load the appointments data
    appointments = loadJTable(my_appointments)

    # Filter appointments for the specified date
    filtered_appointments = [appointment for appointment in appointments if appointment.get('booking_date') == date_input]

    if not filtered_appointments:
        console.print(f"No appointments found for {date_input}.", style="bold yellow")
        pause()
        return  # exit early

    # Load patient and doctor data for name resolution, gets 'id' and 'name'
    patient_data = {item['id']: item['name'] for item in loadJTable(table1)}
    doctor_data = {item['id']: item['name'] for item in loadJTable(table2)}

    # Initialize the rich.table
    table = Table(show_header=True, header_style="bold magenta")

    # Define the rich.table columns
    keys = ['id', 'booking_date', 'patient_id', 'doctor_id', 'price', 'status']
    column_headers = {
        'id': 'ID',
        'booking_date': 'Booking Date',
        'patient_id': 'Patient Name',
        'doctor_id': 'Doctor Name',
        'price': 'Price',
        'status': 'Status'
    }
    for key in keys:
        table.add_column(column_headers[key], style="dim", justify="left")

    # Add rows to the table
    for appointment in filtered_appointments:
        row = []
        for key in keys:
            if key == 'patient_id':     # replace 'id' with name
                patient_name = patient_data.get(appointment.get(key), "Unknown Patient")
                row.append(patient_name)
            elif key == 'doctor_id':        # replace 'id' with name
                doctor_name = doctor_data.get(appointment.get(key), "Unknown Doctor")
                row.append(doctor_name)
            else:
                row.append(str(appointment.get(key, "")))
        table.add_row(*row)

    # Print the table
    console.print(table)
    pause()

def printAppointmentsForPatient():
    """
    Prints a table of all appointments for a specific patient selected by the user.
    """
    
    # Get the selected patient's ID
    patient_id = selectRecordByID('patient')  # safe to call with default args

    if patient_id is None:
        console.print("No valid patient selected. Exiting.", style="bold red")
        pause()
        return

    # Load the appointments data
    appointments = loadJTable('appointment_join')

    # Filter appointments for the selected patient
    filtered_appointments = [appointment for appointment in appointments if appointment.get('patient_id') == patient_id]

    if not filtered_appointments:
        console.print(f"No appointments found for patient ID {patient_id}.", style="bold yellow")
        pause()
        return

    # Load doctor data for name resolution
    doctor_data = {item['id']: item['name'] for item in loadJTable('doctor')}
    patient_data = {item['id']: item['name'] for item in loadJTable('patient')}

    # Initialize the table
    table = Table(show_header=True, header_style="bold magenta")

    # Define table columns
    keys = ['id', 'booking_date', 'patient_id', 'doctor_id', 'price', 'status']
    column_headers = {
        'id': 'ID',
        'booking_date': 'Booking Date',
        'patient_id': 'Patient Name',
        'doctor_id': 'Doctor Name',
        'price': 'Price',
        'status': 'Status'
    }
    for key in keys:
        table.add_column(column_headers[key], style="dim", justify="left")

    # Add rows to the table
    for appointment in filtered_appointments:
        row = []
        for key in keys:
            if key == 'patient_id':
                patient_name = patient_data.get(appointment.get(key), "Unknown Patient")
                row.append(patient_name)
            elif key == 'doctor_id':
                doctor_name = doctor_data.get(appointment.get(key), "Unknown Doctor")
                row.append(doctor_name)
            else:
                row.append(str(appointment.get(key, "")))
        table.add_row(*row)

    # Print the table
    console.print(table)
    pause()

def printRevenueForDateRange():
    """
    Prompts the user for two dates and prints a table of all appointments between those dates with individual prices and the total price.
    """
    # Prompt the user to input two dates
    start_date_str = getUserInput("start_date", ("date", None))
    end_date_str = getUserInput("end_date", ("date", None))

    if start_date_str is None or end_date_str is None:
        console.print("Invalid date input. Exiting.", style="bold red")
        pause()
        return

    # Convert strings to date
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    if start_date > end_date:
        start_date, end_date = end_date, start_date  # get them in right order

    # Load the appointments data
    appointments = loadJTable('appointment_join')

    # Filter appointments between the specified dates, where status = 'realizada'. 
    # Status must be updated after the appointment for revenue to be accounted for.
    filtered_appointments = [appointment for appointment in appointments 
        if start_date <= datetime.strptime(appointment.get('booking_date'), '%Y-%m-%d').date() <= end_date
        and appointment.get('status').lower() == 'realizada']

    if not filtered_appointments:
        console.print(f"No appointments found between {start_date_str} and {end_date_str}.", style="bold yellow")
        pause()
        return

    # Load patient and doctor data for name resolution
    patient_data = {item['id']: item['name'] for item in loadJTable('patient')}
    doctor_data = {item['id']: item['name'] for item in loadJTable('doctor')}

    # Initialize the table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Booking Date", style="dim", justify="left")
    table.add_column("Patient Name", style="dim", justify="left")
    table.add_column("Doctor Name", style="dim", justify="left")
    table.add_column("Price (EUR)", style="dim", justify="left")

    # Add rows to the table and calculate the total price
    total_price = 0
    for appointment in filtered_appointments:   # follows 'id' order, not the 'date order'
        booking_date = appointment.get('booking_date', "")
        patient_name = patient_data.get(appointment.get('patient_id'), "Unknown Patient")
        doctor_name = doctor_data.get(appointment.get('doctor_id'), "Unknown Doctor")
        price = appointment.get('price', 0)
        total_price += price
        table.add_row(booking_date, patient_name, doctor_name, str(price))

    # Add the total row
    table.add_row("", "", "Total = ", str(total_price), style="bold green on yellow")

    # Print the table
    console.print(table)
    pause()

##################
# What does the Python interpreter say to its friends when it reaches the end of a file?
#
# EOF