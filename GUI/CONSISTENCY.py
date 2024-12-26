

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