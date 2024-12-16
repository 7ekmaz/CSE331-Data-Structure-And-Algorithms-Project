import argparse
import ParsingToGraph # type: ignore
graph, posts , user_topics ,post_topics = ParsingToGraph.parse_xml_to_graph(xml_file_name)
#Word search function
def wordSearch (word , posts):
    """
    Word search through all the posts and returns the post and the user who wrote it
    parameters:
    word    : the string to be found
    posts   : dictionary {key (user) , value (posts)}
    O(N*L)  : where the L is the length of post and the N is the number of posts 

    """
    #insenstive search
    for key in posts:
        posts[key] = [item.lower() for item in posts[key]]
    word = word.lower()
    found = False
    for key , values in posts.items():
        for value in values:
            if word in value:
             print(f"Found '{word}'in post: '{value}' by user :'{key}'")
             found = True
        if not found:
         print(f"'{word}'is not found in any post")
#Topic search function
def topicSearch(topic , post_topics):
    """
    Topic search through each post's topics and returns the post that mention the specified topic.
    topic       : the string to be found .
    post_topics : A list contians [body:(post content),topics:(topics are mentioned in the post)] .
    O(k)        : where k is the number of topics mentioned in the file .

    """
    found = False
    for post in post_topics:
        if topic in post['topics']:
            desired_post = post['body']
            print(desired_post)
            found = True
    if not found:
        print("The topic is not found")

def main():
    parser = argparse.ArgumentParser(description='xml_editor')
    subparsers = parser.add_subparsers(dest='command')
    search_parser = subparsers.add_parser('search', help='Search for posts')

    # Add arguments for the search command
    search_parser.add_argument('-w', '--word', help='Word to search in post bodies', type=str)
    search_parser.add_argument('-t', '--topic', help='Topic to search for', type=str)
    search_parser.add_argument('-i', '--input', help='Input XML file', type=str, required=True)

    args = parser.parse_args()

    # Check which command was called
    if args.command == 'search':
        xml_file_name = args.input
        graph, posts, user_topics,post_topics = parse_xml_to_graph(xml_file_name)
        if args.word:
            wordSearch(args.word, posts)
        elif args.topic:
            topicSearch(args.topic, post_topics)
        else:
            print("Please provide either a word (-w) or a topic (-t) to search.")

if __name__ == '__main__':
    main()