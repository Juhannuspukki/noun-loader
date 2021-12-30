import json
import requests
import os
import base64
import time
import datetime


headers = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/json",
    "sec-ch-ua": "\" Not A;Brand\";v=\"99\", \"Chromium\";v=\"92\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "origin": "https://thenounproject.com",
    "referer": "https://thenounproject.com/icon/ambulance-light-3478132/",
    "cookie": #TODO
}

errors = []
i = 1
now = datetime.datetime.now()
start_index = 1241

for subdir, dirs, files in os.walk(r'test'):
    for filename in files:

        # Skip everything that follows if start_index has not been reached yet
        if i < start_index:
            i += 1
            continue

        filepath = subdir + os.sep + filename
        if filepath.endswith(".json"):

            elapsed_time = datetime.datetime.now() - now

            print("\n\n" + "File " + str(i) + "/" + str(len(files)) + ": " + filepath)
            print("Time Elapsed: " + str(elapsed_time))
            if i != start_index:

                average_time_per_collection_thus_far = elapsed_time / (i - start_index)
                files_remaining = len(files) - i

                print("Estimated time remaining: " + str(average_time_per_collection_thus_far * files_remaining))

            print(errors)
            print("\n")

            with open(filepath, 'r') as myfile:
                data = myfile.read()

            collection = json.loads(data)
            dir_name = "icons/" + str(collection["slug"]) + "-" + str(collection["id"])
            os.mkdir(dir_name)

            j = 1

            for icon in collection["icons"]:
                print("Icon " + str(j) + "/" + str(len(collection["icons"])) + ": " + icon["link"])

                response = requests.post('https://thenounproject.com/graphql/',
                                         data='{"operationName":"downloadIcon","variables":{"iconId":"' + str(icon["id"]) + '","imageFormat":"SVG","exportSize":1200,"foregroundColor":"#000000","backgroundShapeColor":"#000000","backgroundShapeOpacity":0,"backgroundShape":"SQUARE","rotation":0,"flipX":false,"flipY":false},"query":"mutation downloadIcon($iconId: ID\u0021, $exportSize: Int, $imageFormat: IconFileType, $foregroundColor: String, $backgroundShapeColor: String, $backgroundShapeOpacity: Float, $backgroundShape: IconBackgroundShape, $rotation: Int, $flipX: Boolean, $flipY: Boolean) {\\n  downloadIcon(iconId: $iconId, exportSize: $exportSize, imageFormat: $imageFormat, foregroundColor: $foregroundColor, backgroundShapeColor: $backgroundShapeColor, backgroundShapeOpacity: $backgroundShapeOpacity, backgroundShape: $backgroundShape, rotation: $rotation, flipX: $flipX, flipY: $flipY) {\\n    ok\\n    errors\\n    base64Stream\\n    __typename\\n  }\\n}\\n"}',
                                         headers=headers)

                if response.ok:
                    decodedResponse = json.loads(response.content.decode("utf-8"))
                    svg = base64.b64decode(decodedResponse["data"]["downloadIcon"]["base64Stream"]).decode("utf-8")

                    with open(dir_name + "/" + icon["link"][6:].replace("/", "-") + '.svg', 'w',
                              encoding='utf-8') as f:
                        f.write(svg)
                        f.close()

                else:
                    print("Error!")
                    errors.append(icon["link"])

                j += 1

                time.sleep(0.6)

        i += 1

print("\n\nErrors:")
print(errors)
