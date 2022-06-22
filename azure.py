
import requests


# Define constants.
HEADERS = {
    "Content-Type": "application/octet-stream",
    "Ocp-Apim-Subscription-Key": "8c7f1a47ada94b44842b207b02a6d61d"
}


# Define functions.

def face_api(image) -> dict:
    response = requests.post("https://face-recog-0wvlz16vpuihpubqedfq.cognitiveservices.azure.com/face/v1.0/detect?returnFaceId=false&returnFaceAttributes=smile", headers=HEADERS, data=image)
    status_code = response.status_code

    if status_code == 200:
        result = response.json()
    else:
        result = None

    return {'status': status_code, 'result': result}


def is_smiling(image) -> float:
    smile = -1
    resp = face_api(image)

    if resp['status'] == 200:
        if len(resp['result']) > 0:
            smile = resp['result'][0]['faceAttributes']['smile']

    return smile
