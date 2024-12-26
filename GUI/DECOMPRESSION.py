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

def decompress_xml_content(compressed_data):
    """
    Decompress XML content using the reverse Byte Pair Encoding (BPE) mapping.
    
    The input string must contain:
      1. Compressed XML data.
      2. The JSON mapping, separated by ===JSON_MAP===.

    Parameters:
    -----------
    compressed_data : str
        The compressed XML data and mapping.

    Returns:
    --------
    str
        The decompressed XML content.

    Raises:
    -------
    ValueError:
        If the input format is invalid or an error occurs during decompression.
    """
    try:
        # Split the input into compressed data and JSON mapping
        if "===JSON_MAP===" not in compressed_data:
            raise ValueError("Invalid compressed data format. Missing '===JSON_MAP===' delimiter.")

        compressed_data_part, mapping_json = compressed_data.split("===JSON_MAP===")
        compressed_data_part = compressed_data_part.strip()
        mapping_json = mapping_json.strip()

        # Parse the JSON mapping
        mapping = json.loads(mapping_json)

        # Reverse the compression
        decompressed_data = reverse_bpe(compressed_data_part, mapping)
        return decompressed_data
    except Exception as e:
        raise ValueError(f"Error during decompression: {e}")