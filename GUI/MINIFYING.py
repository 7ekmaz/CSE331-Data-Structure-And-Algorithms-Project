def parse_xml(file_content):
    """
    Parses XML content and generates a simplified representation.
    Time Complexity O(N), where N is the number of characters.
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
    Time Complexity O(M), where M is the number of elements.
    """
    minified = ''
    for element_type, content in elements:
        if element_type == 'tag':
            minified += content
        elif element_type == 'text':
            minified += content
    return minified


def minify_xml(input_xml):
    """
    Minifies an XML string by removing unnecessary whitespace.
    Time Complexity O(N), where N is the number of characters.
    """
    try:
        # Parse the XML content
        elements = parse_xml(input_xml)

        # Generate the minified XML
        minified_content = generate_minified_xml(elements)

        return minified_content
    except Exception as e:
        raise ValueError(f"Error during minification: {e}")
