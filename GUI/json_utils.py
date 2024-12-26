import re

def tokenize(xml_input):
    
    """
    Splits the XML string into tokens (tags and text).
    - Tags include <tag>, </tag>, and self-closing tags like <tag/>.
    - Text includes anything outside of tags.

    Args:
        xml_input (str): The XML string to tokenize.
    
    Returns:
        list: A list of tokens extracted from the XML string.
    
    Time Complexity: O(n), where n is the length of the input XML string.
    Space Complexity: O(n), as we store all tokens in a list.
    """
    return re.findall(r"<[^>]+>|[^<]+", xml_input)

def is_start_tag(token):
    """
    Checks if the token is a start tag (e.g., <tag>).
    
    Args:
        token (str): The XML token to check.
    
    Returns:
        bool: True if the token is a start tag, False otherwise.
    
    Time Complexity: O(1), constant for checking string properties.
    Space Complexity: O(1), no extra memory is used.
    """
    return token.startswith("<") and not token.startswith("</") and not token.endswith("/>")

def is_end_tag(token):
    """
    Checks if the token is an end tag (e.g., </tag>).
    
    Args:
        token (str): The XML token to check.
    
    Returns:
        bool: True if the token is an end tag, False otherwise.
    
    Time Complexity: O(1), constant for checking string properties.
    Space Complexity: O(1), no extra memory is used.
    """
    return token.startswith("</")

def is_text(token):
    """
    Checks if the token is plain text content (not a tag).
    
    Args:
        token (str): The XML token to check.
    
    Returns:
        bool: True if the token is text, False otherwise.
    
    Time Complexity: O(1), constant for checking string properties.
    Space Complexity: O(1), no extra memory is used.
    """
    return not token.startswith("<")

def get_tag_name(token):
    """
    Extracts the tag name from a start tag.
    
    Args:
        token (str): The XML token containing a tag.
    
    Returns:
        str: The name of the tag.
    
    Time Complexity: O(k), where k is the length of the token.
    Space Complexity: O(k), temporary memory used for stripping and splitting the tag.
    """
    return token.strip("<>").split()[0]

def get_text_value(token):
    """
    Extracts the plain text value from a text token.
    
    Args:
        token (str): The XML token containing text.
    
    Returns:
        str: The text content without leading/trailing whitespace.
    
    Time Complexity: O(k), where k is the length of the token.
    Space Complexity: O(k), temporary memory used for stripping the text.
    """
    return token.strip()

def is_sibling_tag(stack, current_tag):
    """
    Checks if a tag with the same name already exists in the current dictionary
    in a list format, indicating multiple sibling tags.
    
    Args:
        stack (list): The stack of nested dictionaries.
        current_tag (str): The tag name to check for siblings.
    
    Returns:
        bool: True if the tag is found and is a list, False otherwise.
    
    Time Complexity: O(1), dictionary lookup and list check are constant-time operations.
    Space Complexity: O(1), no extra memory is used.
    """
    return isinstance(stack[-1].get(current_tag), list)

def handle_multiple_siblings(stack, current_tag, new_element):
    """
    Handles the case where multiple sibling tags with the same name are encountered,
    converting the tag value into a list if necessary.
    
    Args:
        stack (list): The stack of nested dictionaries.
        current_tag (str): The tag name to check and handle.
        new_element (dict): The new dictionary element to add to the stack.
    
    Time Complexity: O(1), operations on dictionary and list are constant time.
    Space Complexity: O(1), no extra space required for this function.
    """
    if current_tag in stack[-1]:
        if isinstance(stack[-1][current_tag], list):
            stack[-1][current_tag].append(new_element)
        else:
            stack[-1][current_tag] = [stack[-1][current_tag], new_element]
    else:
        stack[-1][current_tag] = new_element

def replace_empty_dict_with_text(stack, current_tag, text_value):
    """
    Replaces an empty dictionary with a text value for the current tag.
    
    Args:
        stack (list): The stack of nested dictionaries.
        current_tag (str): The tag name where the text is to be assigned.
        text_value (str): The text value to assign to the tag.
    
    Time Complexity: O(1), dictionary check and assignment are constant-time operations.
    Space Complexity: O(1), no extra memory is used.
    """
    if isinstance(stack[-2][current_tag], dict) and not stack[-2][current_tag]:
        stack[-2][current_tag] = text_value

def assign_text_to_most_recent_sibling(stack, current_tag, text_value):
    """
    Assigns text to the most recent sibling element in a list.
    
    Args:
        stack (list): The stack of nested dictionaries.
        current_tag (str): The tag name where the text is to be assigned.
        text_value (str): The text value to assign to the tag.
    
    Time Complexity: O(1), list assignment is a constant-time operation.
    Space Complexity: O(1), no extra memory is used.
    """
    if isinstance(stack[-2][current_tag], list):
        stack[-2][current_tag][-1] = text_value


def parse(xml_input):
    """
    Parses an XML string into a nested Python dictionary.
    
    - Start tags create new nested dictionaries.
    - Text content is directly assigned to tags.
    - End tags close the current dictionary context.

    Args:
        xml_input (str): The XML string to parse.
    
    Returns:
        dict: A simplified dictionary representing the XML structure.
    
    Time Complexity:
        - Tokenizing: O(n), where n is the length of the XML string.
        - Iteration: O(t), where t is the number of tokens.
        - Dictionary operations: O(1) average per operation.
        - Total: O(n + t), approximately linear since t is proportional to n.
    
    Space Complexity:
        - Stack: O(d), where d is the maximum depth of the XML (stack size for nested tags).
        - Output Dictionary: O(k), where k is the size of the resulting dictionary.
        - Total: O(d + k).
    """
    
    # Tokenize the input XML string into tags and text
    tokens = tokenize(xml_input)

    # Initialize a stack with a root dictionary
    stack = [{}]  # Stack stores dictionaries for nested tags.
    tag_stack = []  # To track the current tag context.

    # Iterate through each token
    for token in tokens:
        if is_start_tag(token):
            # If it's a start tag, create a new dictionary for the element
            tag_name = get_tag_name(token)
            new_element = {}
            
            # Handle multiple sibling tags with the same name
            handle_multiple_siblings(stack, tag_name, new_element)
            
            # Add the new dictionary to the current top of the stack
            stack.append(new_element)
            tag_stack.append(tag_name)
        
        elif is_end_tag(token):
            # If it's an end tag, pop the stack to move out of the current element
            stack.pop()
            tag_stack.pop()
        
        elif is_text(token):
            # If it's text, add it directly to the current dictionary
            text_value = get_text_value(token)
            if text_value:  # Ignore empty or whitespace-only text nodes
                current_tag = tag_stack[-1]  # Get the current tag
                # Replace empty dictionary with text if necessary
                replace_empty_dict_with_text(stack, current_tag, text_value)
                # Assign text to the most recent sibling if in list format
                assign_text_to_most_recent_sibling(stack, current_tag, text_value)

    # Return the root dictionary (the only remaining element in the stack)
    return stack[0]


def custom_dumps(obj, indent=None, level=0):
    """
    Serializes a Python object into a JSON string.

    Args:
        obj: The Python object to serialize.
        indent: (Optional) Number of spaces for pretty-printing. Defaults to None.
        level: (Internal) Current depth of recursion for indentation. Defaults to 0.

    Returns:
        str: JSON-compliant string representation of the input object.

    Time Complexity: Depends on the structure:
       
         Overall: O(N), where N is the total number of elements (keys, values, or list items) in the input object.
             - Primitive types: O(k), where k is the length of the string or number of digits.
             - List: O(n * t), where n is the number of elements and t is the average time to serialize each element.
             - Dictionary: O(m * t), where m is the number of key-value pairs and t is the average time to serialize each pair.

 
 

    Space Complexity:
          Overall: O(S + d), where S is the size of the serialized JSON string, and d is the depth of nested objects.
               - Primitive types: O(k), where k is the size of the serialized result.
               - List/Dictionary: O(d) for stack recursion and O(S) for output size.
               - For a dictionary or list: O(n), where n is the number of elements in the object.
               - For strings or numbers: O(1).
    """
    # Check if the object is a dictionary
    if isinstance(obj, dict):
        # Handle dictionaries
        items = []  # List to hold serialized key-value pairs
        for key, value in obj.items():
            serialized_key = custom_dumps(key, indent)  # Serialize the key (must be string-like)
            serialized_value = custom_dumps(value, indent, level + 1)  # Serialize the value
            items.append(f"{serialized_key}: {serialized_value}")  # Add to the list
        # Time Complexity: O(n), iterating over n items in the dictionary.
        # Space Complexity: O(n) for the list of serialized items.

        # Format output based on indentation
        if indent is not None:
            spacing = " " * (level * indent)  # Current level's spaces
            inner_spacing = " " * ((level + 1) * indent)  # Inner level's spaces
            return f"{{\n{inner_spacing}" + f",\n{inner_spacing}".join(items) + f"\n{spacing}}}"
        return "{" + ", ".join(items) + "}"  # Compact representation
        # Space Complexity: O(d) stack and O(n) for serialized result.

    # Check if the object is a list
    elif isinstance(obj, list):
        # Handle lists
        items = [custom_dumps(item, indent, level + 1) for item in obj]  # Recursively serialize list items
        # Time Complexity: O(n), where n is the number of items in the list.
        # Space Complexity: O(n) for the serialized items list.

        # Format output based on indentation
        if indent is not None:
            spacing = " " * (level * indent)  # Current level's spaces
            inner_spacing = " " * ((level + 1) * indent)  # Inner level's spaces
            return f"[\n{inner_spacing}" + f",\n{inner_spacing}".join(items) + f"\n{spacing}]"
        return "[" + ", ".join(items) + "]"  # Compact representation
        # Space Complexity: O(d) stack and O(n) for serialized result.

    # Check if the object is a string
    elif isinstance(obj, str):
        # Handle strings
        return f'"{obj}"'  # Wrap the string in double quotes
        # Time Complexity: O(k), where k is the length of the string.
        # Space Complexity: O(k) for the result string.

    # Check if the object is a number (int or float)
    elif isinstance(obj, (int, float)):
        # Handle numbers
        return str(obj)  # Convert number to a string
        # Time Complexity: O(k), where k is the number of digits in the number.
        # Space Complexity: O(k) for the result string.

    # Check if the object is a boolean
    elif obj is True:
        return "true"  # Convert Python True to JSON true
        # Time Complexity: O(1).
        # Space Complexity: O(1).
    elif obj is False:
        return "false"  # Convert Python False to JSON false
        # Time Complexity: O(1).
        # Space Complexity: O(1).

    # Check if the object is None
    elif obj is None:
        return "null"  # Convert Python None to JSON null
        # Time Complexity: O(1).
        # Space Complexity: O(1).

    # If the object is not JSON-serializable
    else:
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
        # Time Complexity: O(1).
        # Space Complexity: O(1).
