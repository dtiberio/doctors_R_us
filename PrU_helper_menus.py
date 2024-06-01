# PrU_helper_menus.py
# helper functions for the menus

import beaupy
from PrU_helper_json import *
from PrU_helper_db import *
from rich.console import Console

console = Console()

def printMenuSelectTable(list_of_all_tables):
    """
    Displays a menu to select a table from a list.
    
    Args:
    - list_of_all_tables (list): A list of table names.
    
    Returns:
    - str: The selected table name in lowercase, or None if 'Go Back' is selected.
    """
    list_of_all_tables.append("Go Back")
    while True:
        op = beaupy.select(list_of_all_tables, cursor="->", cursor_style='green')
        if op == "Go Back":
            break   # returns None
        else:
            return op.lower()

def printMenuSelectRecord(my_table):
    """
    Displays a menu to select a record from a table.
    
    Args:
    - my_table (list): A list of records in the table.
    
    Returns:
    - The selected record.
    """

    while True:
        console.clear()
        printDictsAsTable(my_table)
        try:
            op = int(input('Type the ID number for the record you want to update: '))
        except ValueError:
            console.print(f"Error: Type a number between 1 and {len(my_table)}", style="bold green")
            pause()
        else:
            if 1 <= op <= len(my_table):
                break
            else:
                console.print(f"Error: Type a number between 1 and {len(my_table)}", style="bold green")
                pause()
    
    my_record = my_table[op-1] # get the corresponding record
    return my_record

def printMenuEditTable(my_table_name):
    """
    Displays a menu to add or update records in a table.
    
    Args:
    - my_table_name (str): The name of the table to edit.
    
    Returns:
    - None
    """
    menu_edit_table = ["Add data records", "Update data records", "Go back"]
    while True:
        console.clear()
        console.print(f"Table selected: {my_table_name}", style="bold green")
        
        op = beaupy.select(menu_edit_table, cursor="->", cursor_style='green', return_index=True) + 1
        match op:
            case 1:  # Add records
                console.clear()
                console.print(f"Table selected: {my_table_name}", style="bold green")   # shows table name while adding record
                if addJRecord(my_table_name, putDict(my_db_schema[my_table_name])):
                    console.print("Record added successfully.", style="bold green")
                    # add print record
                    pause()
                else:
                    console.print("Adding record failed.", style="bold green")
                    pause()

            case 2:  # Update Records
                if not loadJTable(my_table_name):
                    console.print(f"[bold red]Error: there's no records[/bold red]")
                    pause()
                    continue   # exit match, stay inside while loop, if the user wants to add records
                console.clear()
                console.print(f"Table selected: {my_table_name}", style="bold green")
                console.print(f"Select a record:", style="bold blue") 
                my_record = printMenuSelectRecord(loadJTable(my_table_name))  # select record from the table
                console.clear()
                console.print("Record selected:", style="bold green")
                printDict(my_record)
                if beaupy.confirm("Update this record?"):
                    if patchDict(my_table_name, my_record):
                        console.print("Record updated successfully.", style="bold green")
                        # add print record
                        pause()
                    else:
                        console.print("Update failed.", style="bold red")
                        pause()
                else:
                    console.print("Record update cancelled.", style="bold yellow")
                    pause()

            case 3:  # Go back
                console.clear()
                console.print("Returning to main menu.", style="bold blue")
                break   # returns None

def printMenuEditJoinTable(menu_list=['Book Appointment', 'Edit Appointment', 'Go Back'], join_table_name='appointment_join'):
    """
    Display a menu for managing join tables, such as booking or editing appointments.

    Args:
    - menu_list (list): A list of three menu options in the following order:
        1. Create a new join (e.g., book an appointment)
        2. Edit an existing join (e.g., edit an appointment)
        3. Go back to the previous menu
      Defaults to ['Book Appointment', 'Edit Appointment', 'Go Back'].
    - join_table_name (str): The name of the join table to be managed. Defaults to 'appointment_join'.

    """
    
    while True:
        console.clear()
        console.print(f"Table selected: {join_table_name}", style="bold green")
        op = beaupy.select(menu_list, cursor="->", cursor_style='green', return_index=True) + 1
        match op:
            
            case 1:  # (1) Create a new join --> book appointment
                appointment = bookAppointment()  # no args required, uses defaults
                if beaupy.confirm("Book this appointment?"):
                    if addJRecord(join_table_name, appointment):
                        console.print("Appointment booked successfully.", style="bold green")
                    else:
                        console.print("Booking failed.", style="bold red")
                else:
                    console.print("Booking cancelled.", style="bold red")
                pause()
            
            case 2:  # (2) Edit an existing join --> update appointment
                updateAppointment()

            case 3:  # (3) Go Back --> Go back to the main loop
                break  # return None

##################
# nothing more to see