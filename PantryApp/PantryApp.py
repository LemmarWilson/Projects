pantry = {}

def add_item():
    item = input("Enter the item name: ")
    quantity = int(input("Enter the quantity: "))
    pantry[item.title()] = quantity
    print(f"{item.title()} added to the pantry.")

def check_item():
    print_pantry()
    item = input("Enter the item name: ")
    if item.title() in pantry:
        quantity = pantry[item.title()]
        print(f"{item.title()} quantity: {quantity}")
    else:
        print(f"{item.title()} is not found in the pantry.")

def remove_item():
    item = input("Enter the item name: ")
    if item.title() in pantry:
        del pantry[item.title()]
        print(f"{item.title()} removed from the pantry.")
    else:
        print(f"{item.title()} is not found in the pantry.")

def print_pantry():
    print("Pantry contents:")
    if not pantry:
        print("Pantry is empty.")
    else:
        for item, quantity in pantry.items():
            print(f"{item.title()}: {quantity}")

def main():
    while True:
        print("\nPantry App")
        print("1. Add Item")
        print("2. Check Item")
        print("3. Remove Item")
        print("4. Print Pantry")
        print("5. Quit")
        choice = input("Enter your choice: ")
        if "ADD" in choice.upper() or choice == "1":
            add_item()
        elif "CHECK" in choice.upper() or choice == "2":
            check_item()
        elif "REMOVE" in choice.upper() or choice == "3":
            remove_item()
        elif "PRINT" in choice.upper() or choice == "4":
            print_pantry()
        elif "QUIT" in choice.upper() or choice =="5":
            print("Thank you for using the Pantry App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
