import xml.etree.ElementTree as ET
import json
import sys
from collections import Counter

def byte_pair_encoding(data):
    """
    Performs Byte Pair Encoding (BPE) compression on the given data.
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
    
    for i in range(0, 10):
        pairs, unique_pairs, number_of_pairs = get_pairs(data)
        step_count += 1
        if not pairs or unique_pairs:
            break
        
        most_frequent = max(pairs, key=pairs.get)
        most_frequent_value = pairs[most_frequent]

        if most_frequent_value < initial_size * 1 / 100:
            break

        new_char = chr(len(mapping) + 256)
        mapping[new_char] = most_frequent
        data = data.replace(''.join(most_frequent), new_char)

        if (current_size - len(data) - (sys.getsizeof(mapping) - current_dict_size)) < initial_size / 100:
            break
        else:
            current_dict_size = sys.getsizeof(mapping)
            current_size = len(data)

    return data, mapping

def compress_xml_content(xml_data):
    """
    Compress the XML data using Byte Pair Encoding and return the compressed data and mapping.
    """
    try:
        # Perform Byte Pair Encoding (BPE) compression
        compressed_data, mapping = byte_pair_encoding(xml_data)

        # Format the output
        output = f"{compressed_data}\n===JSON_MAP===\n{json.dumps(mapping, indent=4)}"
        return output
    except Exception as e:
        raise ValueError(f"Error compressing XML data: {e}")