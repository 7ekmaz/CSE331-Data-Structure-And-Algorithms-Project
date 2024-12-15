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


''' 
                             COMMENT FROM THE AUTHORS 
    This part is for test purposes only. A person tasked with connecting the project parts
    should remove this main function and devise his own test file.
'''
def main():
    operation = sys.argv[1]
    input_file = sys.argv[3]
    output_file = sys.argv[5]

    if operation == 'compress':
        if input_file.endswith('.xml'):
            compress_xml(input_file, output_file)
        else:
            print("Unsupported file format. Please use .xml files.")
    elif operation == 'decompress':
        if input_file.endswith('.comp'):
            if output_file.endswith('.xml'):
                decompress_xml(input_file, output_file)
            else:
                print("Unsupported file format for output.")
    else:
        print("Invalid operation. Use 'compress' or 'decompress'.")


if __name__ == "__main__":
    main()

