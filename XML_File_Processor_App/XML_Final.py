import pyfiglet

from XML_GUI import *

# Compression Decompression
from compress import *
from decompress import *

# XML to JSON
from xml_editor_json import xml_editor_json

# Consistency (Check and Fix)
from consistency_cmd import *

# Minfying
from minify import *

# Formatting
from Formatting_cmd import *

# ParsingToGraph
from ParsingToGraph import *

# Network Analysis
from Network_Analysis_cmd import *

# PostSearch
from PostSearch import *

import sys
import argparse

# Command handlers
def xml_editor_json_main(args):
    print(f"Processing 'xml_editor json' command...")
    xml_editor_json(args.input, args.output)

def xml_editor_compress_main(args):
    if not args.input.endswith('.xml'):
        print("Unsupported file format. Please use .xml files.")
        return
    compress_xml(args.input, args.output)

def xml_editor_decompress_main(args):
    if not args.input.endswith('.comp'):
        print("Unsupported file format. Please use .comp files for input.")
        return
    if not args.output.endswith('.xml'):
        print("Unsupported file format for output. Please use .xml files.")
        return
    decompress_xml(args.input, args.output)

def xml_editor_verify_main(args):
    try:
        with open(args.input, "r") as file:
            xml_lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{args.input}' was not found.")
        return

    is_valid, errors = check_xml_consistency(xml_lines)
    if is_valid is None:
        return

    if is_valid:
        print("Output: valid, no error found")
    else:
        print(f"Output: invalid ({len(errors)} errors)")
        for line_num, error in errors:
            print(f"Error on line {line_num}: {error}")

    if args.fix:
        fixed_lines, error_log = fix_xml_consistency(xml_lines, errors)
        if error_log:
            print("\nFixes applied:")
            for log in error_log:
                print(log)
        if args.output:
            with open(args.output, "w") as output_file:
                output_file.writelines(fixed_lines)
            print(f"\nFixed XML saved to {args.output}")
        else:
            print("\nFixed XML (printed below):")
            print("".join(fixed_lines))

def xml_editor_format_main(args):
    """
    Handles the 'xml_editor format' command.
    """
    print("Processing 'xml_editor format' command...")
    try:
        data = formatting(args.input)
        with open(args.output, "w") as output_file:
            for line in data:
                output_file.writelines(line)
                output_file.writelines("\n")
        print(f"Formatted XML saved to {args.output}")
    except FileNotFoundError:
        print(f"Error: The file '{args.input}' was not found.")
    except Exception as e:
        print(f"An error occurred while formatting: {e}")

def xml_editor_mini_main(args):
    """
    Handles the 'xml_editor mini' command for minification.
    """
    print("Processing 'xml_editor mini' command...")
    xml_editor_mini(args.input, args.output)

def xml_editor_draw_main(args):
    """
    Handles the 'xml_editor draw' command for visualizing a social network graph.
    """
    print("Processing 'xml_editor draw' command...")
    input_file = args.input
    output_file = args.output

    # Parse the XML to graph
    graph, posts, user_topics, post_topics, names = parse_xml_to_graph(input_file)

    # Visualize the graph
    visualize_graph(output_file, graph)

def xml_editor_search_main(args):
    """
    Handles the 'xml_editor search' command to search by word or topic.
    """
    print(f"Processing 'xml_editor search' command...")
    xml_file_name = args.input
    results = parse_xml_to_graph(xml_file_name)
    graph = results[0]
    posts = results[1]
    user_topics = results[2]
    post_topics = results[3]

    if args.word:
        wordSearch(args.word, posts)
    elif args.topic:
        topicSearch(args.topic, post_topics)
    else:
        print("Please provide either a word (-w) or a topic (-t) to search.")

def xml_editor_suggest_main(args):
    """
    Handles the 'xml_editor suggest' command to suggest users based on a target user.
    """
    print(f"Processing 'xml_editor suggest' command...")
    target_id = args.id
    xml_file_name = args.input

    graph, posts, user_topics, post_topics, names = parse_xml_to_graph(xml_file_name)
    suggestions = suggest_users(graph, target_id)
    print(f"Suggested users for user {target_id}:")
    for user_id, user_name in suggestions:
        print(f"ID: {user_id}, Name: {user_name}")

def xml_editor_mutual_main(args):
    """
    Handles the 'xml_editor mutual' command to find mutual followers among a group of users.
    """
    print(f"Processing 'xml_editor mutual' command...")

    # Convert the comma-separated string to a list
    user_ids = [uid.strip() for uid in args.ids.split(",")]  # Adjust to int or str based on your requirements

    xml_file_name = args.input

    # Parse the XML to graph
    graph, posts, user_topics, post_topics, names = parse_xml_to_graph(xml_file_name)

    # Find mutual followers
    mutual_users = mutual_followers(graph, user_ids)
    
    # Output results
    if mutual_users:
        print("Mutual users who follow all specified users:")
        for user_id in mutual_users:
            print(f"ID: {user_id}")
    else:
        print("No mutual users found.")

def xml_editor_most_influencer_main(args):
    """
    Handles the 'xml_editor most_influencer' command to find the most influential user.
    """
    print(f"Processing 'xml_editor most_influencer' command...")
    xml_file_name = args.input

    graph, posts, user_topics, post_topics, names = parse_xml_to_graph(xml_file_name)
    influencer_name, influencer_id = most_influencer(graph, names)
    print(f"Most Influencer: ID = {influencer_id}, Name = {influencer_name}")

def xml_editor_most_active_main(args):
    """
    Handles the 'xml_editor most_active' command to find the most active user.
    """
    print(f"Processing 'xml_editor most_active' command...")
    xml_file_name = args.input

    graph, posts, user_topics, post_topics, names = parse_xml_to_graph(xml_file_name)
    username, user_id = most_active_user(graph, names)
    print(f"Most Active User: ID = {user_id}, Name: {username}")

# Unified entry point for the program
def run_cli():
    
    parser = argparse.ArgumentParser(description="Unified command-line tool.")
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(title="commands", dest="command")
    
    # Define the 'xml_editor json' command
    json_parser = subparsers.add_parser(
        "json",
        help="Handle XML to JSON conversions."
    )
    json_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    json_parser.add_argument("-o", "--output", required=True, help="Output JSON file.")
    json_parser.set_defaults(func=xml_editor_json_main)
    
    # Define the 'xml_editor compress' command
    compress_parser = subparsers.add_parser(
        "compress",
        help="Compress XML files."
    )
    compress_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    compress_parser.add_argument("-o", "--output", required=True, help="Output compressed file.")
    compress_parser.set_defaults(func=xml_editor_compress_main)
    
    # Define the 'xml_editor decompress' command
    decompress_parser = subparsers.add_parser(
        "decompress",
        help="Decompress files to XML."
    )
    decompress_parser.add_argument("-i", "--input", required=True, help="Input compressed file.")
    decompress_parser.add_argument("-o", "--output", required=True, help="Output XML file.")
    decompress_parser.set_defaults(func=xml_editor_decompress_main)
    
    # Define the 'xml_editor verify' command
    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify and fix XML files."
    )
    verify_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    verify_parser.add_argument("-f", "--fix", action="store_true", help="Attempt to fix errors in the XML file.")
    verify_parser.add_argument("-o", "--output", help="Output file for the fixed XML.")
    verify_parser.set_defaults(func=xml_editor_verify_main)
    
    # Define the 'xml_editor format' command
    format_parser = subparsers.add_parser(
        "format",
        help="Format an XML file."
    )
    format_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    format_parser.add_argument("-o", "--output", required=True, help="Output formatted XML file.")
    format_parser.set_defaults(func=xml_editor_format_main)
    
    # Define the 'xml_editor mini' command for minification
    mini_parser = subparsers.add_parser(
        "mini",
        help="Minify an XML file."
    )
    mini_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    mini_parser.add_argument("-o", "--output", required=True, help="Output minified XML file.")
    mini_parser.set_defaults(func=xml_editor_mini_main)

    # Define the 'xml_editor draw' command for drawing a social network graph
    draw_parser = subparsers.add_parser(
        "draw",
        help="Draw a social network graph from XML data."
    )
    draw_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    draw_parser.add_argument("-o", "--output", required=True, help="Output file for the graph visualization.")
    draw_parser.set_defaults(func=xml_editor_draw_main)

    # Define the 'xml_editor search' command for searching posts by word or topic
    search_parser = subparsers.add_parser(
        "search",
        help="Search for posts in the XML file."
    )
    search_parser.add_argument("-w", "--word", help="Word to search for in post bodies", type=str)
    search_parser.add_argument("-t", "--topic", help="Topic to search for", type=str)
    search_parser.add_argument("-i", "--input", required=True, help="Input XML file", type=str)
    search_parser.set_defaults(func=xml_editor_search_main)   
    
    # Define the 'xml_editor suggest' command for user suggestions
    suggest_parser = subparsers.add_parser(
        "suggest",
        help="Suggest users based on target user."
    )
    suggest_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    suggest_parser.add_argument("-id", "--id", required=True, help="Target user ID for suggestions.")
    suggest_parser.set_defaults(func=xml_editor_suggest_main)
    
    # Define the 'xml_editor mutual' command for mutual followers
    mutual_parser = subparsers.add_parser(
        "mutual",
        help="Find mutual followers."
    )
    mutual_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    mutual_parser.add_argument("-ids", "--ids", required=True, help="Comma-separated list of user IDs.")
    mutual_parser.set_defaults(func=xml_editor_mutual_main)
    
    # Define the 'xml_editor most_influencer' command
    influencer_parser = subparsers.add_parser(
        "most_influencer",
        help="Find the most influential user."
    )
    influencer_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    influencer_parser.set_defaults(func=xml_editor_most_influencer_main)
    
    # Define the 'xml_editor most_active' command
    active_parser = subparsers.add_parser(
        "most_active",
        help="Find the most active user."
    )
    active_parser.add_argument("-i", "--input", required=True, help="Input XML file.")
    active_parser.set_defaults(func=xml_editor_most_active_main)
    
    # Parse the arguments and call the appropriate function
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

def show_cli_commands():
    print("""
Available CLI Commands:

1. (Converting XML to JSON): 
    python XML_Final.py --cli json -i input_file.xml -o output_file.json

2. (Compressing XML Files): 
    python XML_Final.py --cli compress -i input_file.xml -o output_file.comp

3. (Decompressing Files to XML): 
    python XML_Final.py --cli decompress -i input_file.comp -o output_file.xml

4. (Verifying and Fixing XML Files): 
    python XML_Final.py --cli verify -i input_file.xml -f [optional: to fix errors] -o output_file.xml

5. (Formatting XML): 
    python XML_Final.py --cli format -i input_file.xml -o output_file_formatted.xml

6. (Minifying XML): 
    python XML_Final.py --cli mini -i input_file.xml -o output_file_minified.xml

7. (Drawing Social Network Graph): 
    python XML_Final.py --cli draw -i input_file.xml -o output_graph.png

8. (Searching Posts in XML): 
    python XML_Final.py --cli search -w "word" -t "topic" -i input_file.xml

9. (User Suggestions): 
    python XML_Final.py --cli suggest -i input_file.xml -id target_user_id

10. (Finding Mutual Followers): 
    python XML_Final.py --cli mutual -i input_file.xml -ids user_id1,user_id2

11. (Finding Most Influential User): 
    python XML_Final.py --cli most_influencer -i input_file.xml

12. (Finding Most Active User): 
    python XML_Final.py --cli most_active -i input_file.xml
""")



def show_welcome_message():
    # Generate styled text for the header
    header = pyfiglet.figlet_format("Welcome to the XML File Processor!", font="slant") 

    print(header)  # Print the fancy header

    # Regular instructions
    print("""
This script supports both GUI and CLI modes. Follow the instructions below to get started:

1. **Run in GUI Mode:**
    python XML_Final.py --gui

2. **Run in CLI Mode:**
    python XML_Final.py --cli
""")

if __name__ == "__main__":
    # Check if arguments are provided
    if len(sys.argv) == 1:
        # No arguments provided; show the welcome message
        show_welcome_message()
    elif "--gui" in sys.argv:
        run_gui()
    elif "--cli" in sys.argv and len(sys.argv)== 2:
        show_cli_commands()
    elif "--cli" in sys.argv:
        sys.argv.remove("--cli")  # Remove the flag before passing to argparse
        run_cli()
    else:
        print("Invalid arguments! Please run the script without arguments for instructions.")


