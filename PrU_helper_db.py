# PrU_helper_db.py
# Database settings that can be edited by the user

# global settings for the database, all other modules import this one
# this module can't import any of the other modules

J_DB_FOLDER = "json"   # define a subfolder where to store the json files

# list the tables, the data files will share the same name as set here

my_db_tables = [
    'patient',
    'doctor',
    'appointment_join'
]

# the schema for each element in your database records
# the value type of each key must be indicated as a string
# the value types indicate here are recognised by printDict(), putDict(), getUserInput()

my_db_schema = {
    'patient': {
        "id": ("int", None),
        "name": ("text", None),
        "date_of_birth": ("date", None),
        "status": ("set", ('Active', 'Innactive'))
    },
    'doctor': {
        "id": ("int", None),
        "name": ("text", None),
        "salary": ("int", None),
        "status": ("set", ('Available', 'Unavailable'))
    },
    'appointment_join': {
        "id": ("int", None),
        "booking_date": ("date", None),
        "patient_id": ("FK", ('patient', 'name')),
        "doctor_id": ("FK", ('doctor', 'name')),
        "price": ("int", None),
        "status": ("set", ('Booked', 'Canceled', 'Done'))
    }
}

##################
# this.is(the_end)