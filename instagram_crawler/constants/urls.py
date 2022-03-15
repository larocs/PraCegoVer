USER_AGENT = 'Mozilla/5.0 (Linux; Android 8.1.0; motorola one Build/OPKS28.63-18-3; wv) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/70.0.3538.80 Mobile ' \
             'Safari/537.36 Instagram 72.0.0.21.98 Android (27/8.1.0; 320dpi; 720x1362; ' \
             'motorola; motorola one; deen_sprout; qcom; pt_BR; 132081645)'

HEADER = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "accept-encoding": "gzip, deflate, br", "accept-language": "en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7",
    "cache-control": "max-age=0",
    "cookie": 'mid=YN6MeAAEAAHpYeGnLLF0mCX__juD; ig_did=53901FD7-01D1-4293-BBED-5B0CF4A87FCC; ig_nrcb=1; csrftoken=iCSEZesnqHTxmEbK98CqduU7YBkmTlhS; ds_user_id=25506656995; sessionid=25506656995%3AscngMfHxytakOG%3A12; shbid="19050\05425506656995\0541657250140:01f7e48abdadf011ca6cf5278b3e603574ed141ba20c98ee468225db29ddeecedd2afe47"; shbts="1625714140\05425506656995\0541657250140:01f711c0f2b58a5b4078be9794b0e8329d2d503f1cf86d3767da361531b22c425871c7af"; rur="NAO\05425506656995\0541657329316:01f7a7d6548838910ffede6e45232a2b58cd6c90dbb4dd46b92f91370674e8552f830348"',
    "sec-fetch-dest": "document", "sec-fetch-mode": "navigate", "sec-fetch-site": "none", "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1", 'user-agent': USER_AGENT, }

# instagram URLs
LOGIN_URL = "https://www.instagram.com/accounts/login/"

PROFILE_URL = "http://www.instagram.com/{}"

HASHTAG_URL = "http://www.instagram.com/explore/tags/{}/?__a=1"
NEXT_PAGE = "&max_id={}"

POST_URL = 'https://www.instagram.com/graphql/query/?query_hash=ea4baf885b60cbf664b34ee760397549&variables={}'
