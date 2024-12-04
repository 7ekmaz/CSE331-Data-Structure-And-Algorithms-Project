def parse_xml(file_content):
    """
    Parses XML content and generates a simplified representation.
    Time Complexity O(N) where N:No of character

    """
    elements = []
    tag = ''
    text = ''
    inside_tag = False
    
    for char in file_content:
        if char == '<':  # Start of a tag
            if text.strip():  # If there's meaningful text before this tag, add it
                elements.append(('text', text.strip()))
            text = ''
            inside_tag = True
            tag = '<'
        elif char == '>':  # End of a tag
            tag += '>'
            elements.append(('tag', tag))
            tag = ''
            inside_tag = False
        elif inside_tag:  # Inside a tag
            tag += char
        else:  # Outside a tag, accumulating text
            text += char
    
    if text.strip():  # Capture any remaining text
        elements.append(('text', text.strip()))
    
    return elements


def generate_minified_xml(elements):
    """
    Generates minified XML content from parsed elements.
    Time Complexity O(M) where M:No of elements
    """
    minified = ''
    for element_type, content in elements:
        if element_type == 'tag':
            minified += content
        elif element_type == 'text':
            minified += content
    return minified


def  xml_editor_mini(input_file, output_file):
    """
    Minifies an XML file by removing unnecessary whitespace.
    Time Complexity O(N) where N:No of character
    """
    try:
        # Step 1: Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # Step 2: Parse the XML content
        elements = parse_xml(file_content)
        
        # Step 3: Generate the minified XML
        minified_content = generate_minified_xml(elements)
        
        # Step 4: Write the minified content to the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(minified_content)
        
        print(f"Minified XML written to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    """
    Main function to handle input/output paths and run the minification process.
    """
    # Replace these paths with your actual file paths
    input_file = "sample2.xml"
    output_file = "output.xml"

    print("Minifying XML file...")
    xml_editor_mini(input_file, output_file)


if __name__ == "__main__":
    main()

