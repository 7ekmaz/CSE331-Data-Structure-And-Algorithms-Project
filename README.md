# CSE331-Project:-XML-Editor-Program 
This project provides a comprehensive platform for managing and analyzing XML data. With a dual-interface design, users can seamlessly switch between a command-line interface (CLI) for power and precision, and a graphical user interface (GUI) for ease of use. The system is equipped with advanced capabilities

Built with a focus on versatility and user experience, this project is for Data Structure And Algorthims Course (CSE311s) in Ain Shams university.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [SetUP](#setup)
3. [Repository Structure](#repository-structure)
4. [CMD Commands](#cmd-commands)
5. [License](#license)

---

## Overview
  The XML Editor Project is a versatile tool built to simplify the management and manipulation of XML files. **With a dual-interface design** , users can seamlessly switch between a Command-Line Interface (CLI) for quick command-based operations and a Graphical User Interface (GUI) for an intuitive, user-friendly experience.

The project is structured into two levels:

- Level 1: Basic XML Operations
    Provides fundamental functionalities for handling a wide range of XML files.
- Level 2: Advanced Network Analysis
    Specializes in XML processing tailored for network-related analysis and applications.
By combining both interface options with comprehensive features, this project ensures a robust and flexible solution for XML file operations, catering to diverse user needs.

---

## Features

- Validation and Detection:
Ensures all opening tags have corresponding closing tags to maintain proper nesting.
Detects unexpected or unmatched closing tags.

- Error Correction:
Automatically corrects mismatched tags and improper nesting.

- Formatting:
Formats XML files to improve readability.

- Minification:
Minifies XML files to reduce their size without altering their structure or content.

- Compression and Decompression:
Compresses XML files for efficient storage and includes a reverse function to restore the files to their original form.

- JSON Conversion:
Converts XML files into JSON format for compatibility with other systems.

- Graph Representation:
Provides visual representation of XML structures and dependencies through graphs.

- Network Analysis:
This analysis involves examining XML structures to identify relationships and connections within the data. It includes functions that allow the user to identify the most active user and the most influential user based on network analysis. Additionally, it provides a list of mutual users to help analyze shared connections.
also searches for specific words within posts and performs topic-based searches to classify and filter data inside posts.

---

### Setup

Follow these steps to set up and run the application:

1. **Ensure Python Installation**
   - Make sure you have Python version 3.6 or higher installed on your system.

2. **Clone the Repository**
   ```bash
   git clone https://github.com/7ekmaz/CSE331-Data-Structure-And-Algorithms-Project/
   ```

3. **Install Required Libraries**
   Run the following commands to install the necessary dependencies:
   ```bash
   pip install pyfiglet
   pip install PyQt5
   pip install matplotlib
   pip install networkx
   ```

4. **Move the Main File**
   - Move the `XML_Final.py` file to the `Requirements` folder.


5. **Navigate to the Required Directory**
   ```bash
   cd CSE331-Data-Structure-And-Algorithms-Project/XML_File_Processor_App/Requirements/
   ```

6. **Run the Application**
   ```bash
   python XML_Final.py
   ```
 
---

## Repository Structure

```markdown
CSE331-Data-Structure-And-Algorithms-Project/
├── XML_File_Processor_App/   # Dual interface code
│   ├── Requirements.zip/
│   ├── XML_Final.py/     
│   └── sample.xml/           
├── Level 1/                  # Source code
│   ├── Compressing and Decompressing/
│   ├── Consistency Check/
│   ├── Formatting XML/
│   ├── Minifying The XML File/     
│   └── Converting XML to JSON/
├── Level 2/                  # Source code
│   ├── Network Analysis/
│   ├── ParsingToGraph.py/
│   ├── PostSearch.py/     
│   └── Social-network-graph.jpg/ 
├──GUI/                       # Gui implementation
│   ├── COMPRESSION.py/
│   ├── CONSISTENCY.py/
│   ├── CONVERT_TO_JSON.py/
│   ├── DECOMPRESSION.py/  
│   ├── FORMATTING.py/
│   ├── MINIFYING.py/
│   ├── POST_SEARCH.py/
│   ├── XMLGRAPH.py/
│   ├── json_utils.py/
│   ├── main_GUI.py/    
│   └── s.xml/ 
│ 
├──CMD/                     # CLI implementation
│   └── main_CMD.py/        
├── LICENSE         # License file
└── README.md       # Readme file
```

---

## CMD Commands

The application supports two modes of operation: GUI (Graphical User Interface) and CLI (Command-Line Interface). Below are the specific commands to help you get started:

### Commands

- command_1: To get started with the app  
  ```markdown
    python XML_Final.py
  ```
- command_2: To choose GUI  
  ```markdown
    python XML_Final.py --gui
  ```
- command_3: To choose CLI 
  ```markdown
    python XML_Final.py --cli
  ```
---

## License

This project is licensed under the [License Name](LICENSE).
