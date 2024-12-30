'''
AUTHORS
Ahmed Haitham Ismail El-Ebidy   -   2101629
Mohamed Khaled Elsayed Goda     -   2100675
Marwan Ahmed Hassen Ali         -   2100902
'''

from ParsingToGraph import parse_xml_to_graph, Graph, visualize_graph

def most_influencer(graph, names):
    followers = {}
    for node in graph.get_all_nodes():
        followers[node] = graph.get_in_degree(node)
    most = max(followers, key=followers.get)
    return names[most], most 

def most_active_user(graph, names): 
    activity = {}
    for node in graph.get_all_nodes():
        followers = set(graph.get_followers(node))
        followees = set(graph.get_neighbors(node))
        activity[node] = graph.get_in_degree(node) + graph.get_out_degree(node) - len(followers.intersection(followees))
    most_active = max(activity, key=activity.get)
    return names[most_active], most_active

def mutual_followers(graph, users):
    mutual = []
    for user in users:
        mutual.append(graph.get_followers(user))
    result = list(set.intersection(*map(set, mutual)))
    if not result:
            print("No Mutual Followers")
    return result

def suggest_users(graph, target_user):
    """
    Suggests users for the given user ID based on their followers' connections.

    :param graph: The Graph object representing the social network.
    :param target_user: The user ID for whom to suggest new users.
    :return: A list of tuples with IDs and names of suggested users.
    """
    # Get the direct followers of the target user
    direct_followers = graph.get_followers(target_user)
    suggested_users = set()

    # For each direct follower of the target user
    for follower in direct_followers:
        # Get the second-degree neighbors (followers of the follower)
        second_degree_neighbors = graph.get_followers(follower)
        
        # Suggest a user if they are not the target user, not already a direct follower, and not the follower itself
        for second_degree_user in second_degree_neighbors:
            if second_degree_user != target_user:
                suggested_users.add(second_degree_user)

    # Return the list of suggested users along with their names
    return [(user, user) for user in suggested_users]  # Assuming user names are the same as user IDs
