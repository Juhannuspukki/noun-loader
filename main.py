# See the Documentation for more information: https://tomaarsen.github.io/TheNounProjectAPI
import TheNounProjectAPI.exceptions
from TheNounProjectAPI import API
import json
import re


if __name__ == "__main__":
    # API Key and Secret from https://api.thenounproject.com/getting_started.html#creating-an-api-key
    key = #TODO
    secret = #TODO

    with open('collections-2.txt') as f:
        lines = f.readlines()

    id_list = []

    for line in lines:
        id = re.findall(r"-\d*\/", line)[0][1:-1]
        id_list.append(id)

    # Create api object
    api = API(key=key, secret=secret)

    i = 1

    for collection_id in id_list:

        print(i)

        index = 1

        data = {
            "icons": []
        }

        while True:
            try:
                icons = api.get_collection_icons(collection_id, page=index)

            except TheNounProjectAPI.exceptions.NotFound:
                print("Error: Not found")
                break

            print("\n\n")
            print(icons.collection)
            print(icons.collection.name)
            print(icons.collection.id)
            print("Icons in this collection: " + str(len(icons)))
            print("\n\n")

            data["name"] = icons.collection.name
            data["slug"] = icons.collection.slug
            data["id"] = icons.collection.id

            for icon in icons:
                # print(icon.id)
                # print(icon.term)
                # print("- -")

                icon_data = {
                    "id": icon.id,
                    "name": icon.term,
                    "link": icon.permalink,
                    "tags": icon.tags
                }

                data["icons"].append(icon_data)

            index += 1

            if len(icons) < 50:
                break

        with open("test/" + str(icons.collection.slug) + "-" + str(collection_id) + '.json', 'w',
                  encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        i += 1
