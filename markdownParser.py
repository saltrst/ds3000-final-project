from bs4 import BeautifulSoup
import text2emotion as te
f = BeautifulSoup(open('markdownExample.html'), features="html.parser")

codeBlocks = f.find_all(class_="highlight")
codeBlocks = codeBlocks + f.findAll("code")

headers = f.find_all("h1")
headers = headers + f.find_all("h2")
headers = headers + f.find_all("h3")
headers = headers + f.find_all("h4")
headers = headers + f.find_all("h5")

hyperlinks = f.find_all("a")

pText = f.find_all("p")

pStr = ''

for p in pText:
    pStr = pStr + str(p.contents)

print("---------------")
print("Markdown Stats:")
print("---------------")
print("code blocks: " + str(len(codeBlocks)))
print("length: " + str(len(f.text)))
print("headers: " + str(len(headers)))
print("hyperlinks: " + str(len(hyperlinks)))
print("tone: " + str(te.get_emotion(pStr)))