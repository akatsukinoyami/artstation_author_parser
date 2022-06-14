#!/usr/bin/env python3

import os, re, requests, time

original_path = os.getcwd()  # Path where will be created folder of artist.
sleep_time = 1  # in seconds. Time between downloading images.


def main(author):
    link = f"https://{ author }.artstation.com/projects.json"

    with requests.get(link) as response:
        if not response.ok:
            print(response)
            return

        path = f"{ original_path }/{ author }"
        try:
            os.mkdir(path)
        except FileExistsError:
            pass

        os.chdir(path)

        for project in response.json()["data"]:
            for asset in project["assets"]:
                with requests.get(asset["image_url"]) as img_response:
                    if not img_response.ok:
                        print(img_response)
                        continue

                    title = re.sub(r"\s+", "_", project["title"])
                    filename = f"{ title }_{ asset['id'] }.jpg"
                    print(f"Downloading {filename}")

                    with open(filename, "wb") as handler:
                        handler.write(img_response.content)

                    time.sleep(sleep_time)


if __name__ == "__main__":
    print("Please, enter artstation author name:")
    author = input("")

    main(author)
