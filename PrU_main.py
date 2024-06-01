# PrU_main.py
# the main program

from PrU_helper_json import *
from PrU_helper_db import *
from PrU_helper_menus import *
import beaupy
from rich.console import Console
from art import text2art

console = Console()

def initializeProgramSettings():
    """
    Initialize program settings by creating the database files.
    If the file already exists, do nothing.
    """
    for table in my_db_tables:
        success = initJTable(table)
        match success:
            case -1:
                console.print(f"--- Error initializing {table} table", style="bold red")
                console.print(f"--- Unfortunately, must exit now.", style="bold red")
                raise SystemExit(0)  # Exit with status 0 (successful termination)
            case 0:
                console.print(f"--- The {table} table already exists, keeping it as-is, no changes", style="bold green")
            case 1:
                console.print(f"--- The {table} table was initialized with an empty table", style="bold green")

def mainLoop():
    """
    Main loop of the program, displaying the home menu and handling user selections.
    """
    # Set the Home Menu
    menu_home = ["Print the records in a table", "Update the records in a Table", "Print Reports", "Manage appointments", "Reset a table", "Exit"]

    # The main loop starts here
    while True:
        console.clear()
        console.print("Doctors 'R' Us - Booking system", style="bold blue")
        console.print("Main Menu", style="bold green")
        op = beaupy.select(menu_home, cursor="->", cursor_style='green', return_index=True) + 1  # Returns index of the menuList

        match op:

            case 1:     # Print Table
                console.clear()
                console.print("Select the table to read:", style="bold blue")
                op = printMenuSelectTable(my_db_tables.copy())  # Pass list as a copy, it will be changed
                if op:
                    console.clear()
                    console.print(f"Table selected: {op}", style="bold green")
                    #for my_record in loadJTable(op):
                        # printDict(my_record)
                    printDictsAsTable(loadJTable(op))
                    pause()

            case 2:     # Edit Table
                console.clear()
                console.print("Select the table to edit:", style="bold blue")
                op = printMenuSelectTable(my_db_tables.copy())  # Pass list as a copy, it will be changed
                if op:
                    console.clear()
                    if '_join' in op:           # join tables require this menu
                        printMenuEditJoinTable(join_table_name=op)
                    else:
                        printMenuEditTable(op)      # all other tables use this menu

            case 3:     # Select a report to print
                console.clear()
                console.print("Select the report to print:", style="bold blue")
                menu_list = ['All the appointments for a date', 'Sum of total revenue for a range of dates', 'Appointment history for a patient']
                op = beaupy.select(menu_list, cursor="->", cursor_style='green')
                match op:

                    case 'All the appointments for a date': # must match the menu string
                        printAppointmentsForDate()

                    case 'Sum of total revenue for a range of dates':
                        printRevenueForDateRange()

                    case 'Appointment history for a patient':
                        printAppointmentsForPatient()

            case 4:     # manage join tables, in this case the 'appointment_join' table
                console.clear()
                printMenuEditJoinTable()        # safe to call function with default args

            case 5:     # reset a table, make it an empty table
                console.clear()
                console.print("Select the table to reset:", style="bold blue")
                op = printMenuSelectTable(my_db_tables.copy())  # Pass list as a copy, it will be changed
                if op:
                    console.clear()
                    if beaupy.confirm(f"Reset this table: {op}?"):
                        initJTable(op, True)
                        console.print("The table was reset.", style="bold green")
                        pause()
                    else:
                        console.print("Table reset is cancelled.", style="bold yellow")
                        pause()

            case 6:     # exit the program
                console.clear()
                if beaupy.confirm("Are you sure you want to exit the program?"):
                    break       # exit the main loop
                else:
                    console.print("Taking you back to the main menu", style="bold blue")
                    pause()
            
            case _:
                console.print("Try again", style="bold yellow") # just in case something goes wrong
                pause()

###
# Initialize program settings
###
console.clear()
console.print(text2art("Doctors 'R' Us", font='small'))
console.print("Doctors 'R' Us", style="bold blue")
initializeProgramSettings()
console.print("Welcome to the appoitment booking system", style="bold blue")
pause()

###
# Start the main loop
###
mainLoop()

# exit the main loop
console.print(text2art("Doctors 'R' Us", font='small'))
console.print("Thank you for using our booking system.", style="bold blue")
console.print("Bye :)", style="bold yellow")

##################
# You've reached the end of the file, well done!