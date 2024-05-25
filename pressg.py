from os import listdir, makedirs, walk
from os.path import isfile, join, exists
from shutil import rmtree, copytree
from pathlib import Path
import re

# not the biggest fan of functions but having three repeats seems a bit wasteful
def reLink(pattern, textString, absoluteLink):
    linkPattern = re.compile(pattern, flags=re.M)
    aliasPattern = re.compile(pattern + '[^\n]*$', flags=re.M)

    while aliasPattern.search(textString):
        linkAliasStart = int((re.split('[\(\),]', str(aliasPattern.search(textString))))[1])
        linkAliasEnd = int((re.split('[\(\),]', str(aliasPattern.search(textString))))[2])
        linkEnd = int((re.split('[\(\),]', str(linkPattern.search(textString))))[2])

        linkAliasFound = textString[linkAliasStart:linkAliasEnd]
        linkFound = textString[linkAliasStart:linkEnd]
        aliasFound = textString[linkEnd+1:linkAliasEnd]

        urlOnly = re.sub('^=>\s*', '', linkFound, count=1, flags=re.M)
        if urlOnly[-4:] == '.ccc':
            urlOnly = urlOnly[:-4]

        if not aliasFound:
            aliasFound = urlOnly
        
        if absoluteLink:
            textString = aliasPattern.sub('<a href="' + subUrl + urlOnly + '">' + aliasFound + '</a>', textString, count=1)
        else:
            textString = aliasPattern.sub('<a href="' + urlOnly + '">' + aliasFound + '</a>', textString, count=1)
    return(textString)

def slug(text):
    return(text.replace(' ', '_'))

# defaults (change if you want to configure)
# if you are on windows, replace all '/' with '\' (ctrl+h)
outputDir = './docs/'
baseHtml = './html/main.html'
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
    if '.git' not in walkedFilesList[x][0] and 'docs' not in walkedFilesList[x][0]:
        for j in walkedFilesList[x][2]:
            if not walkedFilesList[x][2][y].rfind('.') == 0:
                # tempFileInfo = [path, name, extension]
                tempFileInfo = [join(walkedFilesList[x][0],walkedFilesList[x][2][y]), walkedFilesList[x][2][y][:walkedFilesList[x][2][y].rfind('.')], walkedFilesList[x][2][y][walkedFilesList[x][2][y].rfind('.'):]]
                allFilePaths.append(tempFileInfo)
            y += 1
    x += 1

z = 0
for k in allFilePaths:
    if allFilePaths[z][2] == '.ccc' and not allFilePaths[z][0][:len(outputDir)] == outputDir and not allFilePaths[z][0][:9] == "./assets/":
        cFilePaths.append(allFilePaths[z])
    if allFilePaths[z][0] == baseHtml:
        htmlWrapper = open(allFilePaths[z][0], 'r').read()
    z += 1

aa = 0
for l in cFilePaths:
    openCFile = open(cFilePaths[aa][0]).read()
    openCFile = reLink('^=>\s*https:\/\/\S*', openCFile, False)
    openCFile = reLink('^=>\s*\/\S*', openCFile, True)
    openCFile = reLink('^=>\s*\S*', openCFile, False)
    wikilinkPattern = re.compile('\[\[[^\n]*\]\]')
    while wikilinkPattern.search(openCFile):
        wikiStart = int((re.split('[\(\),]', str(wikilinkPattern.search(openCFile))))[1])
        wikiEnd = int((re.split('[\(\),]', str(wikilinkPattern.search(openCFile))))[2])
        wikiContent = openCFile[wikiStart+2:wikiEnd-2]
        if '|' in wikiContent:
            wikiToFile = slug(wikiContent.split('|')[0])
            wikiAlias = wikiContent.split('|')[1]
        else:
            wikiToFile = slug(wikiContent)
            wikiAlias = ''
        ac = 0
        for n in allFilePaths:
            if allFilePaths[ac][1] == wikiToFile or (str(allFilePaths[ac][1]) + str(allFilePaths[ac][2])) == wikiToFile:
                wikiPath = allFilePaths[ac][0][1:]
                if not wikiAlias:
                    wikiAlias = allFilePaths[ac][1]
                if wikiPath[-4:] == '.ccc':
                    wikiPath = wikiPath[:-4]
                break
            ac += 1
        openCFile = wikilinkPattern.sub('<a href="' + subUrl + wikiPath + '">' + wikiAlias + '</a>', openCFile, count=1)

    if htmlWrapper:
        tempFinalFile = htmlWrapper.replace('{{content}}', "<pre>\n" + openCFile + "\n</pre>")
        tempFinalFile = tempFinalFile.replace('{{page.name}}', cFilePaths[aa][1])
    else:
        tempFinalFile = "<pre>\n" + openCFile + "\n</pre>"
    writeToPath = cFilePaths[aa][0].replace("./", outputDir).replace('.ccc', ".html")
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
