"""
Aaron Whitaker
10/22/2022
CRN: 10235
Class name: CIS 226: Advanced Python Programming
Aprox time to complete: 8 hours
"""

import sqlite3

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def setup():
    # builds database
    c.execute("CREATE TABLE IF NOT EXISTS vegetable (name text, quantity integer)")
    conn.commit()
    print("\nVegetable table created!")

def insert_vegetable( name, quantity):
    # inserts a vegetable and quantity into the database
    c.execute("INSERT INTO vegetable VALUES (?, ?)", [name, quantity])
    print(f"\nAdded {name} as a new vegetable.")

def select_vegetable(name, quantity) -> bool:
    # finds vegetable in database or notify user if not found
    c.execute("SELECT quantity, name FROM vegetable WHERE name=?", [name, ])
    row = c.fetchone() 
    if row is None:
        print(f"\n{name} not found!")
        return False
    else:
        print(f"\n{name} found!\n{quantity} in stock.")
        return True

def update_vegetable( name, quantity):
    # updates vegetable name and/or quantity in database
    found = select_vegetable(name, quantity)
    if found:
        c.execute("UPDATE vegetable SET quantity=? WHERE name=?", [quantity, name])
    else:
        print(f"\nAdding {name} as a new vegetable.")
        insert_vegetable(name, quantity)
        c.execute("UPDATE vegetable SET quantity=? WHERE name=?", [quantity, name])
        select_vegetable(name, quantity)

def delete_vegetable(name, quantity):
    # deletes vegetable from database
    if select_vegetable(name, quantity):
        found = c.execute("SELECT quantity, name FROM vegetable WHERE name=?", [name, ])
        c.execute("DELETE FROM vegetable WHERE name=?", [name])
        conn.commit()
        print(f"\n{name} deleted!")
        
def show_all():
    # prints all vegetables in database
    print("\nAll vegetables: quantities")
    for row in c.execute("SELECT * FROM vegetable"):
        print(f"{row[0]}: {row[1]}")

def close():
    # closes database
    conn.close()
    exit()
def input_check( go) -> bool:
    # verifies quantity input is an integer
    try:
        go = int(go)
        go in range (0,8)
        return True
    except:
        print("\nInvalid option!\n")
        return False

def vegi_name() -> str:
    # requests vegetable name from user
    name = input("Enter the vegetable name: ")
    return name

def vegi_quantity() -> int:
    # requests vegetable quantity from user
    try: 
        quantity = input("Enter the quantity: ")
        try:
            quantity = int(quantity.strip())
        except:
            print("\nInvalid quantity!\n")
            menu()
    except:
        print("\nInvalid quantity!\nPlease renter vegetable and a valid quantity.\n")
        main()
    return quantity

def db_check() -> bool:
    # checks if database has been created
    try:
        c.execute("SELECT * FROM vegetable")
        return True
    except:
        return False

def select(go):
    # calls selected function based on user input from menu
    if go == 7:
        close()
    elif go == 1:
        setup()
        menu()
    elif db_check():
        if go == 2:
            name = vegi_name()
            quantity = vegi_quantity()
            insert_vegetable(name, quantity)
            menu()
        elif go == 3:
            name = vegi_name()
            select_vegetable(name, quantity)
            menu()
        elif go == 4:
            name = vegi_name()
            quantity = vegi_quantity()
            update_vegetable(name, quantity)
            menu()
        elif go == 5:
            name = vegi_name()
            delete_vegetable(name)
            menu()
        elif go == 6:
            show_all()
            menu()
        else:
            print("\nInvalid option!\n")
            menu()
    elif go in range (1,7):
        print("\nDatabase has not been created!\nPlease select option 1 to create the database.\n")
        menu()

def menu():
    # displays menu and requests user input
    print("\nPlease select an option:\n"\
        "1: Create the vegetable table\n"\
        "2: Insert a vegetable\n"\
        "3: Select a vegetable\n"\
        "4: Update a vegetable\n"\
        "5: Delete a vegetable\n"\
        "6: Show all \n"\
        "7: Exit")
    go = input("")
    if input_check(go):
        go = int(go)
        select(go)
    else:
        print("\nInvalid option!\n")
        menu()


def main():
    # prints welcome and calls menu function
    print("Welcome to the Vegetable Stand!\n")
    menu()

if __name__ == "__main__":
    main()

"""
Design: I intended to use the example from DB Part 1 but ran into errors about the database not being created when trying to use class Vegetables. 
Develop: I ended up not using a classes in this program due to the errors, but it still operates as intended.
Test: I tested the program by running it and selecting each option in the menu manually, and by running the included test_main.py pytest.
Document: The above program prompts the user for input to select a menu option, and requests that option 1 is selected if a database has not been
    built yet unless the user selects 7 to exit the program. Each menu option from 2-6 calls a function that performs the desired CRUD action.
"""