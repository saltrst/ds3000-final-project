import csv
import json

a = json.load(open('questionsPerDownloadDict.json'))

dArr = json.load(open('packageDict.json'))

arr = []

for key in dArr.keys():
    temp = {}
    temp["packageName"] = key;
    print(temp)
    temp["downloads"] = dArr[key]["downloads"]
    temp["markdown"] = dArr[key]["markdown"]["html"]
    temp["markdownLength"] = dArr[key]["markdown"]["length"]
    temp["markdownHeaders"] = dArr[key]["markdown"]["headers"]
    temp["markdownCodeBlocks"] = dArr[key]["markdown"]["codeBlocks"]
    temp["markdownLinks"] = dArr[key]["markdown"]["hyperlinks"]
    temp["toneHappy"] = dArr[key]["markdown"]["tone"]["Happy"]
    temp["toneAngry"] = dArr[key]["markdown"]["tone"]["Angry"]
    temp["toneSurprise"] = dArr[key]["markdown"]["tone"]["Surprise"]
    temp["toneSad"] = dArr[key]["markdown"]["tone"]["Sad"]
    temp["toneFear"] = dArr[key]["markdown"]["tone"]["Fear"]

    if (key in a):
        temp["soQuestions"] = a[key]["soQuestions"]
        temp["questionsPerDownload"] = a[key]["questionsPerDownload"]
    else:
        temp["soQuestions"] = 0
        temp["questionsPerDownload"] = 0

    arr.append(temp)

print(arr)

with open('finalData.json', 'w') as outfile:
    json.dump(arr, outfile)