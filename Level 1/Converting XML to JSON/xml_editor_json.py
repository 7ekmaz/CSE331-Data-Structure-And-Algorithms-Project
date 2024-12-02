import argparse
from json_utils import custom_dumps, parse

# Main function to convert input XML file to output JSON file
def xml_editor_json(input_file, output_file):
    # Read the input XML file
    with open(input_file, 'r') as xml_file:
        xml_data = xml_file.read()
    
    # Parse the XML data to a dictionary
    data_dict = parse(xml_data)
    
    # Convert the dictionary to JSON
    json_data = custom_dumps(data_dict, indent=4)
    
    # Write the JSON data to the output file
    with open(output_file, 'w') as json_file:
        json_file.write(json_data)

def main():
    parser = argparse.ArgumentParser(description="Convert XML to JSON.")
    parser.add_argument('-i', '--input', required=True, help="Input XML file")
    parser.add_argument('-o', '--output', required=True, help="Output JSON file")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Call the function to convert XML to JSON
    xml_editor_json(args.input, args.output)
    
if __name__ == "__main__":
    main()