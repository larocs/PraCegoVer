import math
import urllib.request


def download_image(url_source, file_name, directory):
    try:
        print('downloading: ', url_source)
        urllib.request.urlretrieve(url_source, str(directory) + "/" + str(file_name))
        print('downloaded')
        return True
    except Exception as e:
        print(e)
        return False


def format_filename(index, size=8):
    result = str(index)
    while len(result) < size:
        result = "0" + result

    return "i-" + result + ".jpg"


def index_img(img_filename):
    try:
        s = img_filename[2:-4]
        return int(s)
    except Exception as e:
        return math.inf
