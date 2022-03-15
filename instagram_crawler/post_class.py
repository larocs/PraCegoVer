from datetime import datetime

from utils import date_handler


class Post:
    def __init__(self, image, accessibility_caption, width, height,
                 post_date=None, caption="", owner="",
                 image_type="GraphImage", number_likes=-1, shortcode=0,
                 filename="", collect_date=None):
        self.image_url = image
        self.caption = caption
        self.owner = owner
        self.accessibility_caption = accessibility_caption
        self.image_type = image_type
        self.number_likes = number_likes
        self.shortcode = shortcode
        self.filename = filename
        self.width = width
        self.height = height

        if post_date is not None:
            if isinstance(post_date, str):
                self.post_date = date_handler.string_to_datetime(post_date)
            else:
                self.post_date = datetime.utcfromtimestamp(float(post_date)).strftime("%d-%m-%Y")

        if collect_date is None:
            self.collect_date = datetime.now().strftime("%d-%m-%Y")
        else:
            if isinstance(collect_date, str):
                self.collect_date = date_handler.string_to_datetime(collect_date)
            else:
                self.collect_date = collect_date

    @staticmethod
    def from_dict(post_dict):
        return Post(image=post_dict['image_url'],
                    accessibility_caption=post_dict['accessibility_caption'],
                    width=post_dict['width'],
                    height=post_dict['height'],
                    post_date=post_dict['post_date'],
                    collect_date=post_dict['collect_date'],
                    caption=post_dict['caption'],
                    owner=post_dict['owner'],
                    image_type=post_dict['image_type'],
                    number_likes=post_dict['number_likes'],
                    shortcode=post_dict['shortcode'],
                    filename=post_dict['filename'])

    def get_dict(self):
        return {'shortcode': self.shortcode,
                'owner': self.owner,
                'image_url': self.image_url,
                'filename': self.filename,
                'caption': self.caption,
                'accessibility_caption': self.accessibility_caption,
                'image_type': self.image_type,
                'number_likes': self.number_likes,
                'width': self.width,
                'height': self.height,
                'post_date': self.post_date if isinstance(self.post_date, str) else self.post_date.strftime("%d-%m-%Y"),
                'collect_date': self.collect_date if isinstance(self.collect_date, str) else self.collect_date.strftime(
                    "%d-%m-%Y")
                }
