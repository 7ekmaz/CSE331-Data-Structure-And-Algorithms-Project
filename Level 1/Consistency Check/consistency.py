import argparse
import xml.etree.ElementTree as ET
import sys


# Parsing Command-Line Arguments
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


def check_xml_consistency(xml_lines):
    tag_list = []  # List to track opened tags with line numbers
    errors = []  # List to store errors

    for line_num, line in enumerate(xml_lines, start=1):
        line = line.strip()

        start = line.find("<")
        while start != -1:
            end = line.find(">", start)

            # Extract the tag content
            tag_content = line[start + 1 : end].strip()

            is_closing = tag_content.startswith("/")
            is_self_closing = tag_content.endswith("/")
            comment_tag = tag_content.startswith("!")

            if is_closing:
                # Extract the tag name for closing tag
                tag_name = tag_content[1:].split()[0]
                matched = False

                # Search for matching opening tag in the stack
                for i in range(len(tag_list) - 1, -1, -1):
                    list_tag_name, opening_line = tag_list[i]
                    if list_tag_name == tag_name:
                        tag_list.pop(i)  # Remove the matched opening tag from the stack
                        matched = True
                        break

                if not matched:
                    # If no matching opening tag, log the error
                    errors.append(
                        (
                            line_num,
                            f"Unexpected closing tag: </{tag_name}>. There is no matching opening tag.",
                        )
                    )

            elif is_self_closing or comment_tag:
                # Ignore self-closing or comment tags as they don't affect xml structure
                pass

            else:
                # opening tag, track it with its line number
                tag_name = tag_content.split()[0]
                tag_list.append(
                    (tag_name, line_num)
                )  # used in order to track opening tag line number in case of many tags with the same name

            # Look for the next tag in the line
            start = line.find("<", end)

    #  check if any opening tags are left unclosed
    while tag_list:
        tag_name, opening_line = tag_list.pop()
        errors.append(
            (
                opening_line,
                f"<{tag_name}> has no closing tag.",
            )
        )

    # return errors if exist and the list of errors
    return len(errors) == 0, errors


def fix_xml_consistency(xml_lines, errors):
    fixed_lines = xml_lines[:]
    error_log = []

    for line_num, error_msg in errors:
        if "has no closing tag" in error_msg:
            # Extract the tag name from the error message
            tag_name = error_msg.split("<")[1].split(">")[0]

            # Locate the line with the opening tag
            open_tag_line = line_num - 1
            for i in range(open_tag_line, len(fixed_lines)):
                if f"<{tag_name}" in fixed_lines[i]:
                    open_tag_line = i
                    break

            # Find the appropriate position to insert the closing tag
            insertion_point = open_tag_line + 1
            for i in range(open_tag_line + 1, len(fixed_lines)):
                if (
                    fixed_lines[i].strip().startswith("</")
                    or "<" in fixed_lines[i].strip()
                ):
                    break
                insertion_point = i + 1

            fixed_lines.insert(
                insertion_point,
                f"</{tag_name}><!-- Error fixed: Added missing closing tag for <{tag_name}> -->\n",
            )
            error_log.append(
                f"Added closing tag </{tag_name}> for <{tag_name}> starting on line {line_num}"
            )

        elif "Unexpected closing tag" in error_msg:
            # Extract the tag name from the error message
            tag_name = error_msg.split("</")[1].split(">")[0]

            # Locate the line with the closing tag
            closing_tag_line = line_num - 1
            content = fixed_lines[closing_tag_line].strip()

            # Set how many lines to check before the closing tag for content
            lines_to_check = 2

            # Search up to 'lines_to_check' lines before the closing tag for content
            for i in range(1, lines_to_check + 1):
                previous_line = closing_tag_line - i
                if previous_line < 0:
                    break  # Don't go beyond the first line

                content = fixed_lines[previous_line].strip()
                if content:  # Found non-empty content
                    # Add the opening tag before the found content
                    fixed_lines[previous_line] = f"<{tag_name}> {content}"
                    fixed_lines[closing_tag_line] = f"</{tag_name}>"
                    break  # Stop once content is found and fixed
            else:
                # If no content found in the range, insert opening tag before closing tag
                fixed_lines.insert(closing_tag_line, f"<{tag_name}>")

            # Log the error fix
            error_log.append(
                f"Added missing opening tag <{tag_name}> on line {line_num} for existing closing tag."
            )
            
    return fixed_lines, error_log


def main():
    # Checking command-line arguments
    args = parse_arguments()  # Parse arguments from command line
    xml_path = args.input  # Get the input XML file path

    # Validate XML file
    try:
        with open(xml_path, "r") as file:
            xml_lines = file.readlines()  # Read XML file into lines
    except FileNotFoundError:
        print(f"Error: The file '{xml_path}' was not found.")
        return

    # Check XML consistency
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

    # If the --fix flag (-f) is set, attempt to fix the errors
    if args.fix:
        fixed_lines, error_log = fix_xml_consistency(xml_lines, errors)

        # Display applied fixes if any
        if error_log:
            print("\nFixes applied:")
            for log in error_log:
                print(log)

        # If --output is specified, write the fixed XML to the output file
        if args.output:
            with open(args.output, "w") as output_file:
                output_file.writelines(fixed_lines)
            print(f"\nFixed XML saved to {args.output}")
        else:
            print("\nFixed XML (printed below):")
            print("".join(fixed_lines))


if __name__ == "__main__":
    main()

    # This idiom is essential for writing modular, reusable, and testable Python code. It separates the script's reusable logic from its executable logic


# Time Complexity Explanation:
#
# The time complexity of the `check_xml_consistency` function depends on the operations
# performed within the loops and the use of the stack.
#
#  Outer Loop (Line Iteration):
#    The function iterates through each line in `xml_lines` using `enumerate`, which runs in O(n) time
#    where `n` is the number of lines in the XML input. This loop processes each line once.
#
#  Inner Loop (Tag Parsing):
#    Inside the outer loop, there is a while loop that scans for each tag within the current line.
#    For each line, the `find` function is used to locate the positions of tags. In the worst case,
#    the line could contain multiple tags, and the while loop will process each tag one by one. For
#    a line with `m` tags, the `find` operation will be performed `m` times. However, we can simplify
#    the complexity of the inner loop to O(L), where `L` is the maximum line length.
#
#
#    For each closing tag (`</tag>`), the function looks for a matching opening tag in the list.
#    In the worst case, the list may contain all previously encountered opening tags, so finding
#    a match involves iterating through the list in reverse order, which can be as large as the number
#    of tags processed so far.
#
# Remaining list Check:
#    After processing all the lines, any remaining opening tags in the list are checked for unclosed
#    tags. This operation contributes O(k) time, where `k` is the number of tags.
#
# Overall Time Complexity:
#    The outer loop runs O(n), where `n` is the number of lines. For each line, the inner loop operates
#    in O(L) for tag parsing, and the stack operations contribute O(k) time.
#
# Final Big O Complexity:
#    O(n * L)
#    Where `n` is the number of lines in the XML, and `L` is the length of the longest line.


# Time Complexity Explanation for fix_xml_consistency:

# Iteration Over Errors:
#    The function iterates through each error in the `errors` list. If there are `k` errors, this part will take O(k) time.

# Finding and Inserting Closing Tags:
#    For errors where a closing tag is missing, the function locates the appropriate line to insert the closing tag.
#    This scan of the lines takes O(n) time, where `n` is the number of lines in the XML file. Inserting a closing tag
#    into a list takes O(n) time, resulting in an O(n) time complexity for this operation.

# Fixing Unexpected Closing Tags:
#    For errors involving unexpected closing tags, the function searches for the content associated with the tag
#    and either adds an opening tag or comments out a redundant closing tag. This scan also takes O(n) in the worst case.

# Error Log Construction:
#    Building the error log involves appending to a list, which is O(1) per operation and does not significantly affect
#    the overall time complexity.

# Overall Time Complexity:
#    The function has a time complexity of O(k * n), where:
#    - `k` is the number of errors.
#    - `n` is the number of lines in the XML file.
