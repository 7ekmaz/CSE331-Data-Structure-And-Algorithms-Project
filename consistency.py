import argparse
import xml.etree.ElementTree as ET
import sys


# 1. Parsing Command-Line Arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="XML Verifier and Repairer")
    parser.add_argument("verify", help="Verify the XML file, Checking Consistency", choices=["verify"])
    parser.add_argument("-i", "--input", required=True, help="Input XML file ")
    parser.add_argument("-f", "--fix", action="store_true", help="Fix errors found in the input file")
    parser.add_argument("-o", "--output", help="Output file for fixed XML")
    return parser.parse_args()


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
            if end == -1:  # Distorted tag detected
                errors.append((line_num,"Malformed tag detected. Tag is incomplete or improperly formatted.",))
                break

            tag_content = line[start + 1 : end].strip()
            is_closing = tag_content.startswith("/")
            is_self_closing = tag_content.endswith("/")

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
                    errors.append((line_num,f"Unexpected closing tag: </{tag_name}>. There is no matching opening tag.",))

            elif is_self_closing:
                # to be modifiedddddddd
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

            errors.append((unclosed_opening_tags[tag_name].pop(),f"<{tag_name}> has no closing tag",))  # to be modifiedddddddd

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
    main()  # This idiom is essential for writing modular, reusable, and testable Python code. It separates the script's reusable logic from its executable logic
