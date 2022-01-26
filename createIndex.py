import json
import os

collections = []

for subdir, dirs, files in os.walk(r'thai'):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".json"):

            with open(filepath, 'r') as myfile:
                data = myfile.read()

            collection = json.loads(data)

            new_icons = []

            for icon in collection["icons"]:
                new_tags = []

                for tag in icon["tags"]:
                    new_tags.append(tag["slug"])

                new_icon = {
                    "name": icon["name"],
                    "id": icon["link"].replace("/term/", "").replace("/", "-"),
                    "tags": new_tags
                }

                new_icons.append(new_icon)

            new_collection = {
                "name": collection["name"],
                "id": collection["slug"] + "-" + collection["id"],
                "icons": new_icons
            }

            collections.append(new_collection)

with open('icon-data-thai.json', 'w', encoding='utf-8') as f:
    json.dump(collections, f, ensure_ascii=False, indent=4)
