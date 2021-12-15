# github npm packages by downloads -> https://github.com/search?o=desc&package_type=npm&q=stars%3A%3E1&s=downloads&type=RegistryPackages

# docs for stack overflow api -> https://api.stackexchange.com/docs

from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
import sys
import time
import csv
import text2emotion as te

data = json.load(open('packageDict.json'))
packageNamesSortedByDownload = json.load(open('rankedPackages.json'))['top1000Packages']

proxy_host = "proxy.crawlera.com"
proxy_port = "8011"
# Make sure to include ':' at the end
proxy_auth = "03c4dac0358a4c68ac14a361bad75337:"
proxies = {
    "https": f"http://{proxy_auth}@{proxy_host}:{proxy_port}/",
    "http": f"http://{proxy_auth}@{proxy_host}:{proxy_port}/"
}

i = 1;

dataKeys = data.keys();

# we want to navigate to the link of each package, and then scrape everything within the "instructions" section of the package page

while i in range(1,101):
    print("Gathering instructions for page: " + str(i))
    url = "https://github.com/search?o=desc&p="+str(i)+"&package_type=npm&q=stars%3A%3E1&s=downloads&type=RegistryPackages"
    req = requests.get(url, proxies=proxies, verify='zyte-proxy-ca.crt')

    soup = BeautifulSoup(req.text, "html.parser")

    links = soup.find_all(class_="h4");

    for link in links:
        packageName = link.contents[0]
        if (packageName in dataKeys):
            url2 = 'https://github.com' + link['href'] 
            req2 = requests.get(url2, proxies=proxies, verify='zyte-proxy-ca.crt')
            f = BeautifulSoup(req2.text, "html.parser")
            markdown = f.find(class_="markdown-body");

            codeBlocks = markdown.find_all(class_="highlight")

            codeBlocks = codeBlocks + markdown.find_all("code")

            headers = markdown.find_all("h1")
            headers = headers + markdown.find_all("h2")
            headers = headers + markdown.find_all("h3")
            headers = headers + markdown.find_all("h4")
            headers = headers + markdown.find_all("h5")

            hyperlinks = markdown.find_all("a")

            pText = markdown.find_all("p")

            pStr = ''

            for p in pText:
                pStr = pStr + str(p.contents) + ' '

            if ('someVal' in data[packageName].keys()):
                data[packageName].pop('someVal')
            data[packageName]['markdown'] = {
                "html": str(markdown),
                "length": len(str(markdown)),
                "headers": len(headers),
                "codeBlocks": len(codeBlocks),
                "hyperlinks": len(hyperlinks),
                "tone": te.get_emotion(pStr)
            }

            print("---------------")
            print("Markdown Stats For: " + packageName)
            print("---------------")
            print("code blocks: " + str(len(codeBlocks)))
            print("length: " + str(len(str(markdown))))
            print("headers: " + str(len(headers)))
            print("hyperlinks: " + str(len(hyperlinks)))
            print("tone: " + str(te.get_emotion(pStr)))

    i+=1


with open('packageDict.json', 'w') as outfile:
    json.dump(data, outfile)