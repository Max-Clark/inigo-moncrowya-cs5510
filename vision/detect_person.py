import os
import json

def analyze_images():
    people = ["man", "woman", "person", "beard", "male", "female"]
    dir_contents = os.listdir("./output")
    person_detected = False
    for file in dir_contents:
        with open(f"./output/{file}") as f:
            file_dict = json.load(f)
            tags = file_dict['result']['tags']
            for tag in tags:
                if tag['tag']['en'] in people:
                    person_detected = True
    return person_detected
