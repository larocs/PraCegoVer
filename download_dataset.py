import argparse
import requests
import os

RECORD_ID = "5710562"


def unpack_image_files():
    os.system("cat images.tar.gz.part* > images.tar.gz")
    os.system("tar -xzvf images.tar.gz")
    os.system("rm images.tar.gz.part*")
    os.system("rm images.tar.gz")


def download(access_token):
    r = requests.get(f"https://zenodo.org/api/records/{RECORD_ID}", params={"access_token": access_token})
    files_to_download = {f["key"]: f["links"]["self"] for f in r.json()["files"]}
    for filename, url in files_to_download.items():
        print("Downloading:", filename)

        r = requests.get(url, params={"access_token": access_token})
        with open(filename, "wb") as f:
            f.write(r.content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("This script download the dataset #PraCegoVer from Zenodo.")
    parser.add_argument("-a", "--access_token", type=str, required=True,
                        help="Your access token from Zenodo. If you don't an access token, you can create it in \
                        https://zenodo.org/account/settings/applications/")

    args = parser.parse_args()

    download(args.access_token)
    unpack_image_files()
