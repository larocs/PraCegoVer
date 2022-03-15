import json

from post_class import Post


def append(post, file):
    if isinstance(post, Post):
        post = post.get_dict()
    json.dump(post, file)
    file.write('\n')


def read_posts(filepath):
    try:
        with open(filepath) as file:
            posts = [Post.from_dict(json.loads(line)) for line in file]
        return posts
    except FileNotFoundError:
        return []