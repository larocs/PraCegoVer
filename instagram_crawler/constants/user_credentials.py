import os


# set your environment variables $PRACEGOVER_USERNAME and $PRACEGOVER_PASS with the corrected
# Instagram username and password
def get_user_credentials():
    username = os.environ['PRACEGOVER_USERNAME']
    password = os.environ['PRACEGOVER_PASS']
    return {"username": username, "password": password}
