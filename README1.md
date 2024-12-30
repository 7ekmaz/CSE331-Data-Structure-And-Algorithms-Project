# CSE331-Project:-XML-Editor-Program 
This project provides a comprehensive platform for managing and analyzing XML data. With a dual-interface design, users can seamlessly switch between a command-line interface (CLI) for power and precision, and a graphical user interface (GUI) for ease of use. The system is equipped with advanced capabilities

Built with a focus on versatility and user experience, this project is for Data Structure And Algorthims Course (CSE311s) in Ain Shams university.

---

## Table of Contents

1. [Overview](#CSE331-Project:-XML-Editor-Program)
2. [Features](#features)
3. [Repository Structure](#repository-structure)
4. [CLI Commands](#cli-commands)
5. [GUI Usage](#gui-usage)
6. [License](#license)

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

## Repository Structure

```markdown
CSE331-Data-Structure-And-Algorithms-Project/
├── GUI/           # Graphical user interface related code
├── Level 1/            # Source code
│   ├── Compressing and Decompressing/
│   ├── Consistency Check/
│   ├── Formatting XML/
│   ├── Minifying The XML File/     
│   └── Converting XML to JSON/
├── Level 2/            # Source code
│   ├── Network Analysis/
│   │   ├── Network_Analysis.py/    
│   │   └── main.py/
│   ├── _pycache__/
│   ├── ParsingToGraph.py/
│   ├── PostSearch.py/     
│   └── Social-network-graph.jpg/ 
│   
│
├──CMD/
│
│
│
│
├── tests/          
├── LICENSE         # License file
└── README.md       # Readme file
```

---

## CLI Commands

List the commands available in the command-line interface :

### Example Commands

- `command_1`: Minifying the XML file  
  ```markdown
    python XML_Final.py --cli mini -i input_file.xml -o output_file.xml
  ```
- `command_2`: Prettifying the XML file  
  ```markdown
    python XML_Final.py --cli format -i input_file.xml -o output_file.xml
  ```
- `command_3`: Checking the XML file consistency  
  ```markdown
    python XML_Final.py --cli verify -i input_file.xml
  ```
- `command_4`: Fixing the XML file  
  ```markdown
    python XML_Final.py --cli verify -i input_file.xml -f -o fixed_file.xml
  ```
- `command_5`: Converting the XML file to JSON  
  ```markdown
    python XML_Final.py --cli json -i input_file.xml -o output_file.json
  ```
- `command_6`: Compressing the XML file
  ```markdown
    python XML_Final.py --cli compress -i input_file.xml -o output_file.comp
  ```
- `command_7`: Decompressing the XML file  
  ```markdown
    python XML_Final.py --cli decompress -i input_file.comp -o output_file.xml
  ```

---

## GUI Usage

Provide instructions for using the graphical user interface:

1. **Installation**: Steps to set up the GUI application.
2. **Launching**: How to start the GUI.
3. **Features**: All functions available in the CLI are also present in the GUI, ensuring a simple user experience.e.
 
---


## License

This project is licensed under the [License Name](LICENSE).

