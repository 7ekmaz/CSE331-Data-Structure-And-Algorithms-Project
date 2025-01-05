import pyfiglet

from XML_GUI import *

from CLI_XML import *


def show_welcome_message():
    # Generate styled text for the header
    header = pyfiglet.figlet_format("Welcome to the XML File Processor!", font="slant") 

    print(header)  # Print the fancy header

    # Regular instructions
    print("""
This script supports both GUI and CLI modes. Follow the instructions below to get started:

1. **Run in GUI Mode:**
    python XML_Final.py --gui

2. **Run in CLI Mode:**
    python XML_Final.py --cli
""")
    # Wait for user input to proceed
    choice = input("Enter '--gui' to start GUI or '--cli' for CLI mode: ").strip().lower()

    # Handle the input to run GUI or CLI
    if choice == '--gui':
        run_gui()
    elif choice == '--cli':
        run_cli()
    else:
        print("Invalid input! Please run the script with '--gui' or '--cli'.")


if __name__ == "__main__":
    # Check if arguments are provided
    if len(sys.argv) == 1:
        # No arguments provided; show the welcome message
        show_welcome_message()
    elif "--gui" in sys.argv:
        run_gui()
    elif "--cli" in sys.argv:
        run_cli() 
    else:
        print("Invalid arguments! Please run the script without arguments for instructions.")


