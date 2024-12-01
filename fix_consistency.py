 import argparse
import xml.etree.ElementTree as ET
import sys


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

            # Locate content before the closing tag
            closing_tag_line = line_num - 1
            content = fixed_lines[closing_tag_line].strip()
            content_without_tag = content.replace(f"</{tag_name}>", "").strip()

            if content_without_tag:  # Case with content
                # Add an opening tag before the content
                fixed_lines[closing_tag_line] = (
                    f"<{tag_name}>{content_without_tag}</{tag_name}>"
                )
                error_log.append(
                    f"Added missing opening tag <{tag_name}> on line {line_num} for existing closing tag."
                )
            else:  # Case without content
                # Comment out the redundant closing tag
                fixed_lines[closing_tag_line] = (
                    f"<!-- {content} --><!-- Error fixed: Removed unexpected closing tag -->\n"
                )
                error_log.append(
                    f"Removed redundant closing tag </{tag_name}> on line {line_num} with no associated content."
                )

        elif "Malformed" in error_msg:
    # Identify the malformed tag
            line = fixed_lines[line_num - 1]
            if "<" in line and not line.strip().endswith(">"):
        # Add the closing angle bracket
                fixed_lines[line_num - 1] = line.rstrip() + ">\n"
                error_log.append(
            f"Fixed malformed tag on line {line_num}: Added missing '>'."
        )


    return fixed_lines, error_log
