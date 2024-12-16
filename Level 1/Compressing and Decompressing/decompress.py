'''
AUTHOR: AHMED HAITHAM ISMAIL EL-EBIDY
'''

import xml.etree.ElementTree as ET
import json
import sys


def reverse_bpe(data, mapping):
    """
    Reverse the Byte Pair Encoding (BPE) compression to recover the original data.

    This function takes a compressed string and the mapping dictionary used for BPE and replaces encoded characters with their original pairs.

    Parameters:
    -----------
    data : str
        The compressed string to be decompressed.
    mapping : dict
        The dictionary mapping encoded characters to the original pairs.

    Returns:
    --------
    str
        The decompressed string after reversing BPE.
    """
    for new_char, pair in reversed(mapping.items()):
        data = data.replace(new_char, ''.join(pair))
    return data

def decompress_xml(input_file, output_file):
    """
    Decompress an XML file that was previously compressed using a Byte Pair Encoding (BPE) technique.

    The input file is expected to have two parts:
      1. The compressed XML data.
      2. A JSON mapping that contains the dictionary used for compression.
    These two parts are separated by a line with the delimiter `===JSON_MAP===`.

    This function reverses the compression using the provided mapping and writes the decompressed XML content to the output file.

    Parameters:
    -----------
    input_file : str
        Path to the input file containing the compressed XML data and JSON mapping.
    output_file : str
        Path to the output file where the decompressed XML content will be saved.

    Raises:
    -------
    Exception
        If there is any error during the file operations, parsing, or decompression process, an exception will be raised with an error message.

    How to Use:
    -----------
    1. Ensure the input file is formatted correctly with the compressed data followed by `===JSON_MAP===` and the JSON mapping.
    2. Call the function with the path to the input file and the desired output file.
    3. The decompressed XML content will be written to the specified output file.

    Example:
    --------
    Suppose you have a compressed XML file `compressed.xml` with the following content:

    ```
    <xml>@@ </xml>===JSON_MAP===
    {"@@": "data"}
    ```

    Call the function as:
    ```python
    decompress_xml('compressed.xml', 'decompressed.xml')
    ```
    After execution, `decompressed.xml` will contain:
    ```
    <xml>data</xml>
    ```
    """
    try:
        # Open the input file and read its contents
        with open(input_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Split the file into compressed data and JSON mapping
        delimiter_index = lines.index("===JSON_MAP===\n")
        compressed_data = ''.join(lines[:delimiter_index]).strip()
        mapping_json = ''.join(lines[delimiter_index + 1:]).strip()
        
        # Parse the JSON mapping
        mapping = json.loads(mapping_json)

        # Reverse the compression
        decompressed_data = reverse_bpe(compressed_data, mapping)

        # Write the decompressed XML content to the output file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(decompressed_data)
    except Exception as e:
        print(f"Error decompressing XML file: {e}")