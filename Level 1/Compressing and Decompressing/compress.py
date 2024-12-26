'''
AUTHOR: Mohamed Khaled Elsayed Goda
''' 

import xml.etree.ElementTree as ET
import json
import sys
from collections import Counter


def byte_pair_encoding(data):

    """
    Perform Byte Pair Encoding (BPE) on the input data.

    This function compresses a string by iteratively replacing the most frequent adjacent character pairs with a new character.
    It returns the compressed data and the mapping of replacements used during compression.

    Parameters:
    -----------
    data : str
        The input string to be compressed.

    Returns:
    --------
    tuple : (str, dict)
        - Compressed string after applying BPE.
        - Dictionary mapping new characters to the replaced pairs.
    """

    mapping = {}
    step_count = 0
    initial_size = len(data)
    current_dict_size = 0
    current_size = len(data)

    def get_pairs(data):
        pairs = Counter(zip(data, data[1:]))  # Generate pairs and count them
        unique_pairs = len(pairs) == len(data) - 1  # Check if all pairs are unique
        number_of_pairs = len(pairs)  # Total unique pairs
        return pairs, unique_pairs, number_of_pairs
    
    for i in range(0,10):
        pairs,unique_pairs,number_of_pairs = get_pairs(data)
        step_count += 1
        if not pairs or unique_pairs:
            break
        
        most_frequent = max(pairs, key=pairs.get)
        most_frequent_value = pairs[most_frequent]

        if(most_frequent_value < initial_size*1/100):
            break

        new_char = chr(len(mapping) + 256)
        mapping[new_char] = most_frequent
        data = data.replace(''.join(most_frequent), new_char)

        if((current_size - len(data) - (sys.getsizeof(mapping) - current_dict_size)) < initial_size/100):
            break

        else:
            current_dict_size = sys.getsizeof(mapping)
            current_size = len(data)

    return data, mapping


def compress_xml(input_file, output_file):

    """
    Compress an XML file using a Byte Pair Encoding (BPE) technique.

    This function reads an XML file, compresses its content using BPE, and saves the compressed data and the BPE mapping to the output file.
    The output file will have two parts:
      1. The compressed XML data.
      2. A JSON mapping that contains the dictionary used for compression.
    These two parts are separated by a line with the delimiter `===JSON_MAP===`.

    Parameters:
    -----------
    input_file : str
        Path to the input XML file to be compressed.
    output_file : str
        Path to the output file where the compressed XML data and mapping will be saved.

    Raises:
    -------
    Exception
        If there is any error during the file operations, XML parsing, or compression process, an exception will be raised with an error message.

    How to Use:
    -----------
    1. Ensure the input file contains valid XML content.
    2. Call the function with the path to the input file and the desired output file.
    3. The output file will contain the compressed XML data and the JSON mapping.

    Example:
    --------
    Suppose you have an XML file `input.xml` with the following content:

    ```
    <xml>data</xml>
    ```

    Call the function as:
    ```python
    compress_xml('input.xml', 'compressed.xml')
    ```
    After execution, `compressed.xml` will contain:
    ```
    <xml>@@</xml>
    ===JSON_MAP===
    {"@@": "data"}
    ```
    """

    try:
        # Parse the XML file
        tree = ET.parse(input_file)
        root = tree.getroot()
        xml_data = ET.tostring(root, encoding='unicode')

        # Perform Byte Pair Encoding (BPE) compression
        compressed_data, mapping = byte_pair_encoding(xml_data)

        # Write the compressed data and mapping to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(compressed_data + '\n')
            file.write("===JSON_MAP===\n")
            file.write(json.dumps(mapping))
    except Exception as e:
        print(f"Error compressing XML file: {e}")