from os import listdir, makedirs, walk
from os.path import isfile, join, exists
from shutil import rmtree
import re

if exists("./docs/"):
    rmtree("./docs/")

# print(listdir())
exhibita = list(walk('.'))
exhibitb = []
exhibitccc = []
exhibite = ''
# print(exhibita)
x = 0
for i in exhibita:
    y = 0
    # print(exhibita[x])
    for j in exhibita[x][2]:
        exhibitb.append(join(exhibita[x][0],exhibita[x][2][y]))
        y += 1
    x += 1
# top 10 spaghetti code

z = 0
for k in exhibitb:
    if exhibitb[z][-4:] == '.ccc' and not exhibitb[z][:7] == "./docs/":
        exhibitccc.append(exhibitb[z])
    if exhibitb[z] == "./html/main.html":
        exhibite = exhibitb[z]
    z += 1

aa = 0
for l in exhibitccc:
    exhibitd = open(exhibitccc[aa]).read()
    if exhibite:
        exhibitered = open(exhibite).read()
        exhibitfinal = exhibitered.replace("[[[content]]]", "<pre>\n" + exhibitd + "\n</pre>")
    else:
        exhibitfinal = "<pre>\n" + exhibitd + "\n</pre>"
    pathtowriteto = exhibitccc[aa].replace("./", "./docs/").replace(".ccc", ".html")
    ptwtdirs = pathtowriteto.split("/")
    ptwtdirlist = ['.']
    ab = 0
    for m in ptwtdirs:
        if ab != 0 and ab != (len(ptwtdirs) - 1):
            ptwtdirlist.append(ptwtdirs[ab])
            ptwtdirlistjoin = "/".join(ptwtdirlist)
            if not exists(ptwtdirlistjoin):
                makedirs(ptwtdirlistjoin)
        ab += 1
    open(pathtowriteto, "w+").write(exhibitfinal)
    aa += 1

# top 2 spaghetti code
