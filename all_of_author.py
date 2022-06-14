#!/usr/bin/env python3

import os, re, requests, time

# Path where will be created folder of artist.
original_path = os.getcwd() 

# Time between downloading images.
sleep_time = 1  # in seconds.


def download_author(author):
    link = f"https://{ author }.artstation.com/projects.json"

    with requests.get(link) as response:
        if not response.ok:
            print(response)
            return
        json = response.json()

        path = f"{ original_path }/{ json['data'][0]['user']['full_name'] }"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        os.chdir(path)
        
        print(f"{ '-' * 50 }\nDownloading pictures of author { author }")

        for project in json["data"]:
            title = re.sub(r"\s+", "_", project["title"])
            print(f"    Downloading project { title }")

            for asset in project["assets"]:
                with requests.get(asset["image_url"]) as img_response:
                    if not img_response.ok:
                        print(img_response)
                        continue

                    print(f"        Downloaded { asset['id'] }")
                    filename = f"{ title }_{ asset['id'] }.jpg"

                    with open(filename, "wb") as handler:
                        handler.write(img_response.content)

                    time.sleep(sleep_time)


def main(author):
    if "," in author:
        for i in author.split(","):
            download_author(i)
    else:
        download_author(author)


if __name__ == "__main__":
    print("Please, enter artstation author name:")
    author = input("")

    main(author)
