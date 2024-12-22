from ParsingToGraph import *
from Network_Analysis import *
import sys

def main():
    # Parse command-line arguments
    if len(sys.argv) < 3:
        print("Usage:")
        print("  xml_editor mutual -i input_file.xml -ids id1,id2,id3")
        print("  xml_editor suggest -i input_file.xml -id target_id")
        print("  xml_editor most_influencer -i input_file.xml")
        sys.exit(1)

    command = sys.argv[1]
    input_file = None
    user_ids = []
    target_id = None

    for i in range(2, len(sys.argv)):
        if sys.argv[i] == "-i":
            input_file = sys.argv[i + 1]
        elif sys.argv[i] == "-ids":
            user_ids = list(map(str.strip, sys.argv[i + 1].split()))
        elif sys.argv[i] == "-id":
            target_id = sys.argv[i + 1]

    if not input_file:
        print("Error: Input file must be specified with -i.")
        sys.exit(1)

    # Parse the XML file into a graph
    graph, posts, user_topics, names = parse_xml_to_graph(input_file)

    if command == "mutual":
        if not user_ids:
            print("Error: User IDs must be specified with -ids for mutual command.")
            sys.exit(1)
        mutual_users = mutual_followers(graph, user_ids)
        print("Mutual users who follow all specified users:")
        for user_id in mutual_users:
            print(f"ID: {user_id}")

    elif command == "suggest":
        if not target_id:
            print("Error: Target user ID must be specified with -id for suggest command.")
            sys.exit(1)
        suggestions = suggest_users(graph, target_id)
        print(f"Suggested users for user {target_id}:")
        for user_id, user_name in suggestions:
            print(f"ID: {user_id}, Name: {user_name}")

    elif command == "most_influencer":
        influencer_name, influencer_id = most_influencer(graph, names)
        print(f"Most Influencer: ID = {influencer_id}, Name = {influencer_name}")

    elif command == "most_active":
        username, userID = most_active_user(graph,names)
        print(f"Most Connected User: ID = {userID}, Name: {username}")

    else:
        print("Error: Unknown command.")
        sys.exit(1)

if __name__ == "__main__":
    main()
