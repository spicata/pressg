from os import listdir, makedirs, walk
from os.path import isfile, join, exists
from shutil import rmtree, copytree
from pathlib import Path
import re

# not the biggest fan of functions but having three repeats seems a bit wasteful
def reLink(pattern, textString, absoluteLink):
    while re.search(pattern, textString):
        linkStart = int((re.split('[\(\),]', str(re.search(pattern, textString))))[1])
        linkEnd = int((re.split('[\(\),]', str(re.search(pattern, textString))))[2])
        linkFound = textString[linkStart:linkEnd]
        urlOnly = re.sub('=>\s*', '', linkFound, count=1)
        if urlOnly[-len(fileType):] == '.ccc':
            urlOnly = urlOnly[:-len(fileType)]
        if absoluteLink:
            textString = re.sub(pattern, '<a href="' + subUrl + urlOnly + '">' + urlOnly + '</a>', textString, count=1)
        else:
            textString = re.sub(pattern, '<a href="' + urlOnly + '">' + urlOnly + '</a>', textString, count=1)
    return(textString)

# defaults (change if you want to configure)
# if you are on windows, replace all '/' with '\' (ctrl+h)
outputDir = './docs/'
fileType = '.ccc'
baseHtml = './html/main.html'
replacement = '[[[content]]]'
subUrl = '/pressg'

# reset /docs/ and add .nojekyll
if exists(outputDir):
    rmtree(outputDir)
makedirs(outputDir)
Path(outputDir + '.nojekyll').touch()
if exists('./assets/'):
    copytree("./assets/", "./docs/assets/")

walkedFilesList = list(walk('.'))
allFilePaths = []
cFilePaths = []
htmlWrapper = ''

x = 0
for i in walkedFilesList:
    y = 0
    for j in walkedFilesList[x][2]:
        allFilePaths.append(join(walkedFilesList[x][0],walkedFilesList[x][2][y]))
        y += 1
    x += 1

z = 0
for k in allFilePaths:
    if allFilePaths[z][-len(fileType):] == fileType and not allFilePaths[z][:len(outputDir)] == outputDir and not allFilePaths[z][:9] == "./assets/":
        cFilePaths.append(allFilePaths[z])
    if allFilePaths[z] == baseHtml:
        htmlWrapper = allFilePaths[z]
    z += 1

aa = 0
for l in cFilePaths:
    openCFile = open(cFilePaths[aa]).read()
    openCFile = reLink('=>\s*https:\/\/\S*', openCFile, False)
    openCFile = reLink('=>\s*\/\S*', openCFile, True)
    openCFile = reLink('=>\s*\S*', openCFile, False)
    if htmlWrapper:
        tempFinalFile = open(htmlWrapper).read().replace(replacement, "<pre>\n" + openCFile + "\n</pre>")
    else:
        tempFinalFile = "<pre>\n" + openCFile + "\n</pre>"
    writeToPath = cFilePaths[aa].replace("./", outputDir).replace(fileType, ".html")
    writeToDir = writeToPath.split("/")
    writeToPathAsList = ['.']
    ab = 0
    for m in writeToDir:
        if ab != 0 and ab != (len(writeToDir) - 1):
            writeToPathAsList.append(writeToDir[ab])
            writeToPathAsListjoin = "/".join(writeToPathAsList)
            if not exists(writeToPathAsListjoin):
                makedirs(writeToPathAsListjoin)
        ab += 1
    open(writeToPath, "w+").write(tempFinalFile)
    aa += 1
