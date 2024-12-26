from json_utils import custom_dumps, parse   # Convert XML to JSON  format


# JSON Conversion Function
def xml_to_json(xml_text):
    try:
        data_dict = parse(xml_text)  # Parse XML to dictionary
        json_data = custom_dumps(data_dict, indent=4)  # Convert dictionary to JSON
        return json_data
    except Exception as e:
        raise ValueError(f"Error during conversion: {e}")