import argparse
import matplotlib.pyplot as plt
import networkx as nx


class Graph:
    """
    add_node(node): Adds a node to the graph if it doesn’t already exist.
    add_edge(from_node, to_node): Adds a directed edge from from_node to to_node. It adds both nodes if they don’t already exist in the adjacency list.
    get_neighbors(node): Returns the neighbors of a given node.
    get_in_degree(node): Returns the in-degree (number of incoming edges) for a node.
    get_out_degree(node): Returns the out-degree (number of outgoing edges) for a node.
    get_degree(node): Returns the total degree (sum of in-degree and out-degree).
    get_all_nodes(): Returns a list of all nodes in the graph.
    """

    def __init__(self):
        self.adjacency_list = {}

    def add_node(self, node):
        if node not in self.adjacency_list:
            self.adjacency_list[node] = []

    def add_edge(self, from_node, to_node):
        if from_node not in self.adjacency_list:
            self.add_node(from_node)
        if to_node not in self.adjacency_list:
            self.add_node(to_node)
        self.adjacency_list[from_node].append(to_node)

    def get_neighbors(self, node):
        return self.adjacency_list.get(node, [])

    def get_in_degree(self, node):
        in_degree = 0
        for neighbors in self.adjacency_list.values():
            in_degree += neighbors.count(node)
        return in_degree

    def get_followers(self, node):
        list_of_in_degree = []
        for nodes, neighbors in self.adjacency_list.items():
            if neighbors.count(node) != 0:
                list_of_in_degree.append(nodes)
        return list_of_in_degree

    def get_out_degree(self, node):
        return len(self.adjacency_list.get(node, []))

    def get_degree(self, node):
        return self.get_in_degree(node) + self.get_out_degree(node)

    def get_all_nodes(self):
        return list(self.adjacency_list.keys())


def parse_xml_to_graph(input_file):
    """
    Parses the input XML file, creating a social network graph where each user is a node, and edges represent followers.
    Posts and Topics: As the XML is parsed, the posts and topics for each user are stored in the posts and user_topics dictionaries .
    Additionally, The topics for each post are mentioned in list "post_topics" to be used in search.
    The graph is built by adding nodes for users and edges for follower relationships.

    """

    graph = Graph()
    names = {}
    posts = {}
    user_topics = {}
    post_topics = []

    lines = input_file.splitlines()

    current_user = None
    inside_body = False
    body_content = ""
    inside_topic = False
    topic_content = ""

    for line in lines:
        line = line.strip()

        if line.startswith("<user>"):
            followers = []
            current_posts = []
            current_topics = []

        elif line.startswith("<id>") and current_user is None:
            current_user = line.replace("<id>", "").replace("</id>", "").strip()
            graph.add_node(current_user)
        
        elif line.startswith("<post>"):
            body_content = ""
            curr_topics = []

        elif line.startswith("<name>") :
            names[current_user] = line.replace("<name>", "").replace("</name>", "").strip()

        elif line.startswith("<body>"):
            inside_body = True
            body_content = ""

        elif line.startswith("</body>") and inside_body:
            inside_body = False
            current_posts.append(body_content.strip())

        elif line.startswith("<topic>"):
            inside_topic = True
            topic_content = ""


        elif line.startswith("</topic>") and inside_topic:
            inside_topic = False
            current_topics.append(topic_content.strip())
            curr_topics.append(topic_content.strip())
        #Store the topics as list for each post
        elif line.startswith("</post>"):
            if curr_topics:
                post_topics.append({
                'body': body_content.strip(),
                'topics': curr_topics
            })

        elif inside_topic:
            topic_content += line + " "

        elif inside_body:
            body_content += line + " "

        elif line.startswith("<id>") and current_user is not None:
            follower_id = line.replace("<id>", "").replace("</id>", "").strip()
            followers.append(follower_id)
        

        elif line.startswith("</user>"):
            for follower in followers:
                graph.add_edge(follower, current_user)
            if current_posts:
                posts[current_user] = current_posts
            if current_topics:
                user_topics[current_user] = current_topics
            current_user = None

    return graph, posts, user_topics , post_topics, names



import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(graph, output_file=None):
    G = nx.DiGraph()

    for node in graph.get_all_nodes():
        G.add_node(node)
        for neighbor in graph.get_neighbors(node):
            G.add_edge(node, neighbor)

    pos = nx.circular_layout(G)
    
    # Create a matplotlib figure and axis
    fig, ax = plt.subplots(figsize=(8, 8))
    nx.draw(
        G,
        pos,
        ax=ax,
        with_labels=True,
        node_color="lightblue",
        node_size=2000,
        font_size=10,
        font_weight="bold",
    )
    ax.set_title("Social Network Graph", fontsize=16)
    if output_file:
        fig.savefig(output_file)
        plt.close(fig)  # Close the figure after saving to avoid duplication in GUI
    return fig

