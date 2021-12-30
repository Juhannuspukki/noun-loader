import json
import os

what_is_missing = []

for subdir, dirs, files in os.walk(r'test'):
    for filename in files:
        filepath = subdir + os.sep + filename
        if filepath.endswith(".json"):

            with open(filepath, 'r') as myfile:
                data = myfile.read()

            collection = json.loads(data)
            what_should_be = []

            for icon in collection["icons"]:
                what_should_be.append(icon["link"][6:].replace("/", "-") + '.svg')

            dir_name = "icons/" + str(collection["slug"]) + "-" + str(collection["id"])

            what_is = []
            for (dirpath, dirnames, filenames) in os.walk(dir_name):
                what_is.extend(filenames)
                break

            what_is.sort()
            what_should_be.sort()
            # print(what_is)
            # print(what_should_be)

            for icon in what_should_be:
                if icon not in what_is:
                    print("Collection: " + filepath + " is missing " + icon)
                    what_is_missing.append(icon)


