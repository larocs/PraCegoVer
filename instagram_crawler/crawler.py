import random
import time

from constants import constants
from instagram_api import InstagramAPI
from instagram_crawler.constants.user_credentials import get_user_credentials
from utils import file_handler


def create_dict(posts):
    profile_dict = dict()
    for p in posts:
        if profile_dict.get(p.owner, None):
            profile_dict[p.owner] = max(p.post_date, profile_dict[p.owner])
        else:
            profile_dict[p.owner] = p.post_date
    return profile_dict


if __name__ == '__main__':
    posts = file_handler.read_posts(constants.POST_FILE_PATH)
    profile_dict = create_dict(posts)
    shortcodes = set([p.shortcode for p in posts])
    credentials = get_user_credentials()
    profile_username = credentials['username']
    profile_password = credentials['password']

    instagram_API = InstagramAPI(profile_username, profile_password)
    usernames = instagram_API.get_users_from_hashtag(constants.HASHTAG)
    print("PROFLES:", len(usernames))

    with open(constants.POST_FILE_PATH, "a") as post_file:
        for i, (username, user_id) in enumerate(usernames):
            if username is not None:
                print("---------------")
                print("|     " + str(i) + "       |")
                print("---------------")
                print("*****username: " + str(username))
                last_date = profile_dict.get(user_id, 0)
                profile_dict[user_id] = instagram_API.collect_posts_from_user(user_id, post_file,
                                                                              shortcodes=shortcodes,
                                                                              last_saved_post_date=last_date)
                time.sleep(4 + random.random())
