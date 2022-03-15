import json
import math
import random
import time
from datetime import datetime

import requests

from constants import urls, constants
from post_class import Post
from utils import date_handler, helper, file_handler


class InstagramAPI:
    def __init__(self, username, password):
        self.session = self.instagram_login(username, password)

    def __next_page_get_usernames_from_hashtag(self, response, url):
        cursor = response['data']['recent']['next_max_id']
        has_next_page = response['data']['recent']['more_available']
        response = None
        print("cursor:" + str(cursor) + " - hasMore:" + str(has_next_page))
        if has_next_page:
            try:
                response = self.get(url + urls.NEXT_PAGE.format(cursor))
            except Exception as e:
                raise e
        else:
            print("there is no more posts")

        return response, has_next_page

    def __parse_post(self, post_response):
        shortcode = post_response['node']['shortcode']
        is_video = post_response['node']["is_video"]
        caption = ''
        if len(post_response['node']['edge_media_to_caption']["edges"]) > 0:
            caption = post_response['node']['edge_media_to_caption']["edges"][0]['node']['text']
        image = post_response['node']['display_url']
        accessibility_caption = ''
        if 'accessibility_caption' in post_response['node']:
            accessibility_caption = post_response['node']['accessibility_caption']
        image_type = ''
        if '__typename' in post_response['node']:
            image_type = post_response['node']['__typename']
        number_likes = 0
        if 'edge_media_preview_like' in post_response['node']:
            number_likes = post_response['node']['edge_media_preview_like']['count']
        date = ''
        if 'taken_at_timestamp' in post_response['node']:
            date = post_response['node']['taken_at_timestamp']
        owner = -1
        if 'owner' in post_response['node']:
            owner = post_response['node']['owner']['id']
        width = 0
        height = 0
        if post_response['node']['dimensions'] is not None:
            width = post_response['node']['dimensions']['width']
            height = post_response['node']['dimensions']['height']

        obj_post = Post(image=image, accessibility_caption=accessibility_caption,
                        width=width, height=height, post_date=date,
                        caption=caption, owner=owner, image_type=image_type,
                        number_likes=number_likes, shortcode=shortcode)

        return obj_post, is_video

    def instagram_login(self, username, password):
        """Login on Instagram"""

        time = str(int(datetime.now().timestamp()))
        enc_password = "#PWD_INSTAGRAM_BROWSER:0:{}:{}".format(time, password)

        session = requests.Session()
        # set a cookie that signals Instagram the "Accept cookie" banner was closed
        session.cookies.set("ig_cb", "2")
        session.headers.update({'user-agent': urls.USER_AGENT})
        session.headers.update({'Referer': 'https://www.instagram.com'})
        res = session.get('https://www.instagram.com')

        csrftoken = None

        for key in res.cookies.keys():
            if key == 'csrftoken':
                csrftoken = session.cookies['csrftoken']

        session.headers.update({'X-CSRFToken': csrftoken})
        login_data = {'username': username, 'enc_password': enc_password}

        login = session.post('https://www.instagram.com/accounts/login/ajax/', data=login_data, allow_redirects=True)
        session.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        return session

    def get(self, url, return_json=True):
        """
        call a GET method for a given URL

        :param url: a URL for any Instagram's endpoint
        :param return_json: return a json or a response
        :return:
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError('Received non 200 status code: {}'.format(e))
        except requests.RequestException:
            raise requests.RequestException

        if return_json:
            return response.json()
        else:
            return response

    def __get_username(self, id):
        start = 'https://www.instagram.com/graphql/query/?query_hash=c' \
                '9100bf9110dd6361671f113dd02e7d6&variables={"user_id":"'

        end = '","include_chaining":false,"include_reel":true,' \
              '"include_suggested_users":false,"include_logged_out_extras":false,' \
              '"include_highlight_reels":false,"include_related_profiles":false}'

        return start + str(id) + end

    def get_username_from_userid(self, id):
        url = self.__get_username(id)
        try:
            response = self.get(url)
            return response["data"]["user"]["reel"]["owner"]["username"]
        except Exception as e:
            print(e)
            pass

        return None

    def get_users_from_hashtag(self, hashtag):
        if "#" in hashtag:
            hashtag = hashtag.replace("#", "")
        url = urls.HASHTAG_URL.format(hashtag)
        usernames = []

        try:
            response = self.get(url)
            has_next_page = True
            num_requests = 0
            while has_next_page:
                if num_requests % 5 == 4:
                    time.sleep(1)

                for section in response['data']['recent']['sections']:
                    for media in section['layout_content']['medias']:
                        username = media['media']['user']['username']
                        user_id = media['media']['user']['pk']
                        usernames.append((username, user_id))

                response, has_next_page = self.__next_page_get_usernames_from_hashtag(response, url)
                num_requests += 1
                if num_requests == 15:
                    break
        except Exception as e:
            print(e)

        return usernames

    def collect_posts_from_user(self, userid, post_file, shortcodes, last_saved_post_date=0):
        params = {"id": userid, "first": 30}
        url = urls.POST_URL.format(json.dumps(params))
        has_next_page = True
        min_post_date = math.inf
        max_post_date = 0
        num_requests = 0
        while has_next_page and min_post_date > last_saved_post_date:
            response = self.get(url)
            # loop over the post list
            for post_response in response["data"]["user"]["edge_owner_to_timeline_media"]["edges"]:
                obj_post, is_video = self.__parse_post(post_response)
                post_date = date_handler.string_to_timestamp(obj_post.post_date)

                min_post_date = min(post_date, min_post_date)

                # verify whether the hashtag is in the caption
                if constants.HASHTAG.upper() in obj_post.caption.upper() and \
                        not is_video and \
                        obj_post.shortcode not in shortcodes:
                    helper.download_image(obj_post.image_url, obj_post.shortcode + '.jpg',
                                          constants.IMAGES_DIR_PATH)
                    # save collected post
                    shortcodes.add(obj_post.shortcode)
                    file_handler.append(obj_post, post_file)
                    print(obj_post.caption, 'blue')
                    max_post_date = max(post_date, max_post_date)
                    time.sleep(random.random())

            # get the next page
            page_info = response['data']['user']['edge_owner_to_timeline_media']['page_info']
            cursor = page_info['end_cursor']
            has_next_page = page_info['has_next_page']
            params["after"] = cursor
            url = urls.POST_URL.format(json.dumps(params))
            num_requests += 1
            time.sleep(1 + random.random())

        return max_post_date
