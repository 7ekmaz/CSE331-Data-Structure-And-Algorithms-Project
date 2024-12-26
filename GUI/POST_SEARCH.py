
#Word search function
def wordSearch (word , posts):

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
    found = False
    for post in post_topics:
        if topic in post['topics']:
            desired_post = post['body']
            print(desired_post)
            found = True
    if not found:
        print("The topic is not found")

