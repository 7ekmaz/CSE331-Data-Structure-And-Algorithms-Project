import argparse
import xml.etree.ElementTree as ET
import sys
import re


# 1. Parsing Command-Line Arguments
def parse_arguments():
    """
    For command line use

    """
    parser = argparse.ArgumentParser(description="XML Verifier and Repairer")
    parser.add_argument(
        "verify", help="Verify the XML file, Checking Consistency", choices=["verify"]
    )
    parser.add_argument("-i", "--input", required=True, help="Input XML file ")
    parser.add_argument(
        "-f", "--fix", action="store_true", help="Fix errors found in the input file"
    )
    parser.add_argument("-o", "--output", help="Output file for fixed XML")
    return parser.parse_args()

    # sooooooooon
    # def detect_malformed_tag(tag_content):
    """
    Detects if a tag contains a malformed XML tag and classifies the error.
    Returns a string describing the error type or None if the tag is valid.
    """
    tag_content = tag_content.strip()

    # Case 1: Opening tag missing '>'
    if tag_content.startswith("<") and not tag_content.endswith(">"):
        return "Missing_closing_angle"

    # Case 2: Closing tag missing '>'
    if tag_content.startswith("</") and not tag_content.endswith(">"):
        return "Missing_closing_angle"

    # Case 3: Opening tag missing '<'
    if (
        tag_content.endswith(">")
        and not tag_content.startswith("<")
        and not tag_content.startswith("</")
    ):
        return "Missing_opening_angle"

    # Case 4: Closing tag missing '<'
    if (
        tag_content.endswith(">")
        and tag_content.startswith("/")
        and not tag_content.startswith("</")
    ):
        return "Missing_opening_angle"

    # If none of the cases match, the tag is valid
    return None


def detect_invalid_tag(tag_content, line_num):
    """
    Checks if a tag has a valid name based on XML standards.
    Returns an error message if invalid, otherwise None.

    """
    tag_pattern = re.compile(r"[a-zA-Z_][\w.-]*")  # Valid XML tag name pattern

    is_closing = tag_content.startswith("/")
    is_self_closing = tag_content.endswith("/")

    # Remove leading '/' for closing tags or trailing '/' for self-closing tags
    if is_closing:
        tag_name = tag_content[1:]
    elif is_self_closing:
        tag_name = tag_content[:-1].strip()
    else:
        tag_name = tag_content.split()[0]

    if not tag_pattern.fullmatch(tag_name):
        return f"Invalid tag name detected: <{tag_content}>. Tag names must be valid identifiers."

    return None


# XML Consistency validator
def check_xml_consistency(xml_lines):
    stack = []  # Stack to track opened tags
    unclosed_opening_tags = {}  # Dictionary to track line numbers for each opening tag
    errors = []  # storing errors

    for line_num, line in enumerate(xml_lines, start=1):
        line = line.strip()

        start = line.find("<")
        while start != -1:
            end = line.find(">", start)
            if end == -1:  # Malformed tag detected
                errors.append(
                    (
                        line_num,
                        "Malformed tag detected. Tag is incomplete or improperly formatted.",
                    )
                )
                stack.pop()
                break  # Stop further processing for this line

            tag_content = line[start + 1 : end].strip()

            invalid_tag_error = detect_invalid_tag(tag_content, line_num)
            if invalid_tag_error:
                errors.append((line_num, invalid_tag_error))
                break  # Skip further processing of this malformed tag

            is_closing = tag_content.startswith("/")
            is_self_closing = tag_content.endswith("/")
            comment_tag = tag_content.startswith("!")

            if is_closing:
                tag_name = tag_content[1:].split()[0]
                matched = False
                for i in range(len(stack) - 1, -1, -1):
                    stack_tag_name = stack[i]
                    if stack_tag_name == tag_name:
                        stack.pop(i)  # Remove matched opening tag from stack
                        matched = True
                        break

                if not matched:
                    # If no match found, error with the current closing tag line
                    errors.append(
                        (
                            line_num,
                            f"Unexpected closing tag: </{tag_name}>. There is no matching opening tag.",
                        )
                    )

            elif is_self_closing:
                # Pass it as it is self closing
                pass
            elif comment_tag:
                pass
            else:
                #  opening tag
                tag_name = tag_content.split()[0]
                stack.append(tag_name)

                # Track all opening tags and their line numbers
                if tag_name not in unclosed_opening_tags:
                    unclosed_opening_tags[tag_name] = []
                unclosed_opening_tags[tag_name].append(line_num)

            # next tag in line
            start = line.find("<", end)

    # if stack is not empty
    while stack:
        tag_name = stack.pop()
        if tag_name in unclosed_opening_tags:

            errors.append(
                (
                    unclosed_opening_tags[tag_name].pop(),
                    f"<{tag_name}> has no closing tag",
                )
            )  # to be modifiedddddddd

    # return if their exist any errors, and the errors
    return len(errors) == 0, errors


def main():
    # Checking command-line arguments
    if len(sys.argv) > 1:
        args = parse_arguments()
        xml_path = args.input
    else:
        print("No command-line arguments provided.")
        xml_path = input("Enter the path to the XML file: ")

    # Validate XML file
    with open(xml_path, "r") as file:
        xml_lines = file.readlines()

    is_valid, errors = check_xml_consistency(xml_lines)
    if is_valid is None:
        return

    # Display results
    if is_valid:
        print("Output: valid, no error found")
    else:
        print(f"Output: invalid ({len(errors)} errors)")
        for line_num, error in errors:
            print(f"Error on line {line_num}: {error}")


if __name__ == "__main__":
    main()

    # This idiom is essential for writing modular, reusable, and testable Python code. It separates the script's reusable logic from its executable logic


"""
Iterating over n lines: O(n).
Processing t tags:
-Tag parsing and stack operations: O(t).
-Regex matching for invalid tags: O(t⋅l).
Cleanup for unmatched tags: O(k), which is at most O(t).
Total complexity is: O(n+t⋅l)
n: Number of lines in the input.
t: Total number of tags across all lines.
l: Average length of tags.

"""
