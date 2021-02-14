import json
import os
import os.path
import sys
import requests
import time
import cv2

#subscription_key = "d021af95ebae4ea592e6a779a691a84f"
subscription_key = os.environ["COMPUTER_VISION_API_KEY1"]
endpoint = "https://mottyan-solution.cognitiveservices.azure.com/"
text_recognition_url = endpoint + "vision/v3.1/read/analyze"

headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}

def vision(image_url=None):
    print("vision : in")

    filename = image_url
    root, ext = os.path.splitext(filename)
    # image_data = open(filename, "rb").read()
    color = cv2.imread(filename, cv2.IMREAD_COLOR)
    cv2.waitKey(1)
    image_data = cv2.imencode(ext, color)[1].tostring()
    response = requests.post(text_recognition_url, headers=headers, data=image_data)
    response.raise_for_status()

    operation_url = response.headers["Operation-Location"]
    analysis = {}
    poll = True
    while (poll):
        response_final = requests.get(
            response.headers["Operation-Location"], headers=headers)
        analysis = response_final.json()
        #print(json.dumps(analysis, indent=2))

        time.sleep(1)
        if ("analyzeResult" in analysis):
            poll = False
        if ("status" in analysis and analysis['status'] == 'failed'):
            poll = False

    text = analysis["analyzeResult"]["readResults"][0]["lines"][0]["text"]
    #print(text)

    return text