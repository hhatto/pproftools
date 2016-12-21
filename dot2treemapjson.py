import base64
import copy
import re
import json
import argparse
import pygraphviz as pgv
from networkx.drawing.nx_agraph import from_agraph
from networkx.readwrite import json_graph

RE_DIGIT = re.compile(" \(([0-9.]+)\w*\)")
LINKS = None
NODES = None
PARENT_MARKS = set()


INDEX_BASE64_FILE
FLARE_JSON_BASE64_FILE = """\
eyJzaXplIjogMi45NywgImNoaWxkcmVuIjogW3sibmFtZSI6ICJzeXNjYWxsLlN5c2NhbGxcbjAu
MTRzKDMuOTglKVxub2YgMC4xNXMoNC4yNiUpIiwgInNpemUiOiAwLjE1fSwgeyJzaXplIjogMS4z
MSwgImNoaWxkcmVuIjogW3sic2l6ZSI6IDAuNDksICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAicnVu
dGltZS5tYXBpdGVybmV4dFxuMC4xNXMoNC4yNiUpIiwgInNpemUiOiAwLjE1fSwgeyJzaXplIjog
MC4xNCwgImNoaWxkcmVuIjogW3sic2l6ZSI6IDAuMiwgImNoaWxkcmVuIjogW3sibmFtZSI6ICJz
eW5jL2F0b21pYy5BZGRVaW50MzJcbjAuMzNzKDkuMzglKSIsICJzaXplIjogMC4zM31dLCAibmFt
ZSI6ICJzeW5jLigqUldNdXRleCkuUlVubG9ja1xuMC4wNHMoMS4xNCUpXG5vZiAwLjIwcyg1LjY4
JSkifSwgeyJuYW1lIjogInN5bmMuKCpSV011dGV4KS5STG9ja1xuMC4wNHMoMS4xNCUpXG5vZiAw
LjIycyg2LjI1JSkiLCAic2l6ZSI6IDAuMjJ9XSwgIm5hbWUiOiAibHVtL2dhbWUvY2hhcmFjdGVy
LigqQ2hhcmFjdGVyKS5Jc0JhdHRsZVxuMC4wM3MoMC44NSUpXG5vZiAwLjE0cygzLjk4JSkifSwg
eyJzaXplIjogMC4yMiwgImNoaWxkcmVuIjogW3sic2l6ZSI6IDAuMDUsICJjaGlsZHJlbiI6IFt7
InNpemUiOiAwLjA1LCAiY2hpbGRyZW4iOiBbeyJzaXplIjogMC4yNCwgImNoaWxkcmVuIjogW3si
bmFtZSI6ICJydW50aW1lLmhlYXBCaXRzU2V0VHlwZVxuMC4wNnMoMS43MCUpIiwgInNpemUiOiAw
LjA2fSwgeyJuYW1lIjogInJ1bnRpbWUubWVtY2xyXG4wLjA0cygxLjE0JSkiLCAic2l6ZSI6IDAu
MDR9LCB7InNpemUiOiAwLjA0LCAiY2hpbGRyZW4iOiBbeyJzaXplIjogMC4xNywgImNoaWxkcmVu
IjogW3sibmFtZSI6ICJydW50aW1lLmdlbnRyYWNlYmFja1xuMC4wM3MoMC44NSUpXG5vZiAwLjA4
cygyLjI3JSkiLCAic2l6ZSI6IDAuMDh9LCB7InNpemUiOiAwLjA0LCAiY2hpbGRyZW4iOiBbeyJz
aXplIjogMC4wNCwgImNoaWxkcmVuIjogW3sibmFtZSI6ICJydW50aW1lLigqbWNlbnRyYWwpLmNh
Y2hlU3BhblxuMCBvZiAwLjA0cygxLjE0JSkiLCAic2l6ZSI6IDAuMDR9XSwgIm5hbWUiOiAicnVu
dGltZS4oKm1jYWNoZSkucmVmaWxsXG4wIG9mIDAuMDRzKDEuMTQlKSJ9XSwgIm5hbWUiOiAicnVu
dGltZS4oKm1jYWNoZSkubmV4dEZyZWUuZnVuYzFcbjAgb2YgMC4wNHMoMS4xNCUpIn1dLCAibmFt
ZSI6ICJydW50aW1lLnN5c3RlbXN0YWNrXG4wLjAxcygwLjI4JSlcbm9mIDAuMTdzKDQuODMlKSJ9
XSwgIm5hbWUiOiAicnVudGltZS4oKm1jYWNoZSkubmV4dEZyZWVcbjAgb2YgMC4wNHMoMS4xNCUp
In1dLCAibmFtZSI6ICJydW50aW1lLm1hbGxvY2djXG4wLjEycygzLjQxJSlcbm9mIDAuMjRzKDYu
ODIlKSJ9XSwgIm5hbWUiOiAicnVudGltZS5uZXdhcnJheVxuMC4wMXMoMC4yOCUpXG5vZiAwLjA1
cygxLjQyJSkifV0sICJuYW1lIjogInJ1bnRpbWUuaGFzaEdyb3dcbjAgb2YgMC4wNXMoMS40MiUp
In0sIHsibmFtZSI6ICJydW50aW1lLnR5cGVkbWVtbW92ZVxuMC4wMnMoMC41NyUpXG5vZiAwLjA0
cygxLjE0JSkiLCAic2l6ZSI6IDAuMDR9LCB7Im5hbWUiOiAicnVudGltZS5ldmFjdWF0ZVxuMC4w
NXMoMS40MiUpXG5vZiAwLjA3cygxLjk5JSkiLCAic2l6ZSI6IDAuMDd9XSwgIm5hbWUiOiAicnVu
dGltZS5tYXBhc3NpZ24xXG4wLjA4cygyLjI3JSlcbm9mIDAuMjJzKDYuMjUlKSJ9XSwgIm5hbWUi
OiAibHVtL2dhbWUvcm9vbS4oKlJvb20pLmdldENoYXJhTGlzdE5vdEluQmF0dGxlXG4wLjAxcygw
LjI4JSlcbm9mIDAuNDlzKDEzLjkyJSkifSwgeyJuYW1lIjogInJ1bnRpbWUubWFwaXRlcm5leHRc
bjAuMTVzKDQuMjYlKSIsICJzaXplIjogMC4xNX0sIHsibmFtZSI6ICJsdW0vZ2FtZS9yb29tL3N5
bWJvbC4oKlN5bWJvbCkuQ2FuSm9pbkJhdHRsZVxuMC4wMXMoMC4yOCUpXG5vZiAwLjA3cygxLjk5
JSkiLCAic2l6ZSI6IDAuMDd9LCB7Im5hbWUiOiAibHVtL2dhbWUvY2hhcmFjdGVyLigqQ2hhcmFj
dGVyKS5DYW5FbmNvdW50XG4wLjAxcygwLjI4JSlcbm9mIDAuMDVzKDEuNDIlKSIsICJzaXplIjog
MC4wNX0sIHsic2l6ZSI6IDAuNjEsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjM4LCAiY2hpbGRy
ZW4iOiBbeyJzaXplIjogMC4zLCAiY2hpbGRyZW4iOiBbeyJuYW1lIjogImx1bS9nYW1lVGltZS5H
YW1lVGltZS5HZXREaWZmRHVyYXRpb25cbjAuMDFzKDAuMjglKVxub2YgMC4wNHMoMS4xNCUpIiwg
InNpemUiOiAwLjA0fSwgeyJuYW1lIjogInJ1bnRpbWUubmV3b2JqZWN0XG4wLjAycygwLjU3JSlc
bm9mIDAuMTZzKDQuNTUlKSIsICJzaXplIjogMC4xNn0sIHsic2l6ZSI6IDAuMTMsICJjaGlsZHJl
biI6IFt7InNpemUiOiAwLjA3LCAiY2hpbGRyZW4iOiBbeyJuYW1lIjogInRpbWUubm93XG4wLjA1
cygxLjQyJSkiLCAic2l6ZSI6IDAuMDV9XSwgIm5hbWUiOiAidGltZS5Ob3dcbjAuMDJzKDAuNTcl
KVxub2YgMC4wN3MoMS45OSUpIn1dLCAibmFtZSI6ICJsdW0vZ2FtZVRpbWUuR2V0TmV3R2FtZVRp
bWVcbjAuMDZzKDEuNzAlKVxub2YgMC4xM3MoMy42OSUpIn1dLCAibmFtZSI6ICJsdW0vZ2FtZS9w
b3NpdGlvbi4oKk1vdmVtZW50KS5nZXRDdXJyZW50UG9zaXRpb25cbjAuMDhzKDIuMjclKVxub2Yg
MC4zMHMoOC41MiUpIn1dLCAibmFtZSI6ICJsdW0vZ2FtZS9wb3NpdGlvbi4oKk1vdmVtZW50KS5H
ZXRDdXJyZW50UG9zaXRpb25cbjAgb2YgMC4zOHMoMTAuODAlKSJ9XSwgIm5hbWUiOiAibHVtL2dh
bWUvcG9zaXRpb24uSXNIaXRcbjAuMTFzKDMuMTIlKVxub2YgMC42MXMoMTcuMzMlKSJ9XSwgIm5h
bWUiOiAibHVtL2dhbWUvcm9vbS4oKlJvb20pLnN5bVJ1blxuMCBvZiAxLjMxcygzNy4yMiUpIn0s
IHsic2l6ZSI6IDEuMDcsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjM5LCAiY2hpbGRyZW4iOiBb
eyJzaXplIjogMC41MiwgImNoaWxkcmVuIjogW3sic2l6ZSI6IDAuNTEsICJjaGlsZHJlbiI6IFt7
InNpemUiOiAwLjEsICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAibHVtL3ZlbmRvci9naXRodWIuY29t
L2dvbGFuZy9wcm90b2J1Zi9wcm90by4oKkJ1ZmZlcikuZW5jX3N0cnVjdFxuMC4wMnMoMC41NyUp
XG5vZiAwLjA3cygxLjk5JSkiLCAic2l6ZSI6IDAuMDd9XSwgIm5hbWUiOiAibHVtL3ZlbmRvci9n
aXRodWIuY29tL2dvbGFuZy9wcm90b2J1Zi9wcm90by5NYXJzaGFsXG4wIG9mIDAuMTBzKDIuODQl
KSJ9XSwgIm5hbWUiOiAibHVtL3Byb3RvLkZpZWxkU2VydmljZV9Ob3RpY2VNb3ZlX1JlcXVlc3Qu
UGFja2V0XG4wLjAxcygwLjI4JSlcbm9mIDAuNTFzKDE0LjQ5JSkifV0sICJuYW1lIjogImx1bS9w
cm90by4oKkZpZWxkU2VydmljZV9Ob3RpY2VNb3ZlX1JlcXVlc3QpLlBhY2tldFxuMC4wMXMoMC4y
OCUpXG5vZiAwLjUycygxNC43NyUpIn0sIHsic2l6ZSI6IDAuMDQsICJjaGlsZHJlbiI6IFt7InNp
emUiOiAwLjA0LCAiY2hpbGRyZW4iOiBbeyJzaXplIjogMC4wNCwgImNoaWxkcmVuIjogW3sic2l6
ZSI6IDAuNjQsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjYzLCAiY2hpbGRyZW4iOiBbeyJuYW1l
IjogInJ1bnRpbWUuZHVmZmNvcHlcbjAuMDZzKDEuNzAlKSIsICJzaXplIjogMC4wNn0sIHsic2l6
ZSI6IDAuMDUsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjAzLCAiY2hpbGRyZW4iOiBbeyJuYW1l
IjogImJ5dGVzLigqQnVmZmVyKS5ncm93XG4wLjAxcygwLjI4JSlcbm9mIDAuMDRzKDEuMTQlKSIs
ICJzaXplIjogMC4wNH1dLCAibmFtZSI6ICJieXRlcy4oKkJ1ZmZlcikuV3JpdGVCeXRlXG4wLjAy
cygwLjU3JSlcbm9mIDAuMDNzKDAuODUlKSJ9XSwgIm5hbWUiOiAibHVtL3ZlbmRvci9naXRodWIu
Y29tL2dvbGFuZy9wcm90b2J1Zi9wcm90by53cml0ZU5hbWVcbjAgb2YgMC4wNXMoMS40MiUpIn0s
IHsic2l6ZSI6IDAuMDQsICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAicnVudGltZS5nZXRpdGFiXG4w
LjAycygwLjU3JSlcbm9mIDAuMDVzKDEuNDIlKSIsICJzaXplIjogMC4wNX1dLCAibmFtZSI6ICJy
dW50aW1lLmFzc2VydEUySTJcbjAuMDFzKDAuMjglKVxub2YgMC4wNHMoMS4xNCUpIn0sIHsic2l6
ZSI6IDAuNTgsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjI2LCAiY2hpbGRyZW4iOiBbeyJuYW1l
IjogImZtdC5uZXdQcmludGVyXG4wLjAycygwLjU3JSlcbm9mIDAuMDVzKDEuNDIlKSIsICJzaXpl
IjogMC4wNX0sIHsic2l6ZSI6IDAuMTcsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjExLCAiY2hp
bGRyZW4iOiBbeyJzaXplIjogMC4wOCwgImNoaWxkcmVuIjogW3sibmFtZSI6ICJzdHJjb252Ligq
ZXh0RmxvYXQpLlNob3J0ZXN0RGVjaW1hbFxuMC4wMnMoMC41NyUpXG5vZiAwLjA0cygxLjE0JSki
LCAic2l6ZSI6IDAuMDR9XSwgIm5hbWUiOiAic3RyY29udi5nZW5lcmljRnRvYVxuMC4wMnMoMC41
NyUpXG5vZiAwLjA4cygyLjI3JSkifV0sICJuYW1lIjogImZtdC4oKmZtdCkuZm10X2Zsb2F0XG4w
LjAxcygwLjI4JSlcbm9mIDAuMTFzKDMuMTIlKSJ9XSwgIm5hbWUiOiAiZm10LigqcHApLmRvUHJp
bnRcbjAuMDNzKDAuODUlKVxub2YgMC4xN3MoNC44MyUpIn0sIHsibmFtZSI6ICJieXRlcy4oKkJ1
ZmZlcikuV3JpdGVcbjAgb2YgMC4wM3MoMC44NSUpIiwgInNpemUiOiAwLjAzfV0sICJuYW1lIjog
ImZtdC5GcHJpbnRcbjAuMDFzKDAuMjglKVxub2YgMC4yNnMoNy4zOSUpIn0sIHsic2l6ZSI6IDAu
MDQsICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjA0LCAiY2hpbGRyZW4iOiBbeyJuYW1lIjogInJl
ZmxlY3QucGFja0VmYWNlXG4wLjAxcygwLjI4JSlcbm9mIDAuMDRzKDEuMTQlKSIsICJzaXplIjog
MC4wNH1dLCAibmFtZSI6ICJyZWZsZWN0LnZhbHVlSW50ZXJmYWNlXG4wIG9mIDAuMDRzKDEuMTQl
KSJ9XSwgIm5hbWUiOiAicmVmbGVjdC5WYWx1ZS5JbnRlcmZhY2VcbjAgb2YgMC4wNHMoMS4xNCUp
In1dLCAibmFtZSI6ICJsdW0vdmVuZG9yL2dpdGh1Yi5jb20vZ29sYW5nL3Byb3RvYnVmL3Byb3Rv
LigqVGV4dE1hcnNoYWxlcikud3JpdGVBbnlcbjAuMDNzKDAuODUlKVxub2YgMC41OHMoMTYuNDgl
KSJ9XSwgIm5hbWUiOiAibHVtL3ZlbmRvci9naXRodWIuY29tL2dvbGFuZy9wcm90b2J1Zi9wcm90
by4oKlRleHRNYXJzaGFsZXIpLndyaXRlU3RydWN0XG4wLjA1cygxLjQyJSlcbm9mIDAuNjNzKDE3
LjkwJSkifV0sICJuYW1lIjogImx1bS92ZW5kb3IvZ2l0aHViLmNvbS9nb2xhbmcvcHJvdG9idWYv
cHJvdG8uQ29tcGFjdFRleHRTdHJpbmdcbjAgb2YgMC42NHMoMTguMTglKSJ9XSwgIm5hbWUiOiAi
bHVtL3Byb3RvLigqRmllbGRTZXJ2aWNlX05vdGljZVJvb21JbmZvX1JlcXVlc3QpLlN0cmluZ1xu
MCBvZiAwLjA0cygxLjE0JSkifV0sICJuYW1lIjogImx1bS9wcm90by5GaWVsZFNlcnZpY2VfTm90
aWNlUm9vbUluZm9fUmVxdWVzdC5QYWNrZXRcbjAgb2YgMC4wNHMoMS4xNCUpIn1dLCAibmFtZSI6
ICJsdW0vcHJvdG8uKCpGaWVsZFNlcnZpY2VfTm90aWNlUm9vbUluZm9fUmVxdWVzdCkuUGFja2V0
XG4wIG9mIDAuMDRzKDEuMTQlKSJ9XSwgIm5hbWUiOiAibHVtL25vdGljZS4oKlRhcmdldHNOb3Rp
Y2UpLlBhY2tldFxuMCBvZiAwLjM5cygxMS4wOCUpIn0sIHsic2l6ZSI6IDAuMzEsICJjaGlsZHJl
biI6IFt7InNpemUiOiAwLjI1LCAiY2hpbGRyZW4iOiBbeyJzaXplIjogMC4xMiwgImNoaWxkcmVu
IjogW3sic2l6ZSI6IDAuMDgsICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAicnVudGltZS5tYWtlc2xp
Y2VcbjAgb2YgMC4wNXMoMS40MiUpIiwgInNpemUiOiAwLjA1fSwgeyJzaXplIjogMC4wNSwgImNo
aWxkcmVuIjogW3sic2l6ZSI6IDAuMDQsICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAiY3J5cHRvL3No
YTEuYmxvY2tBTUQ2NFxuMC4wNHMoMS4xNCUpIiwgInNpemUiOiAwLjA0fV0sICJuYW1lIjogImNy
eXB0by9zaGExLmJsb2NrXG4wIG9mIDAuMDRzKDEuMTQlKSJ9XSwgIm5hbWUiOiAiY3J5cHRvL3No
YTEuKCpkaWdlc3QpLldyaXRlXG4wLjAxcygwLjI4JSlcbm9mIDAuMDVzKDEuNDIlKSJ9XSwgIm5h
bWUiOiAiY3J5cHRvL2htYWMuTmV3XG4wLjAycygwLjU3JSlcbm9mIDAuMDhzKDIuMjclKSJ9XSwg
Im5hbWUiOiAibHVtL3ZlbmRvci9rbGFiL2Ztb2YvZm1vZi9ycGNzdi9lbmNvZGUuY29tcHV0ZUht
YWNQYWNrZXRcbjAuMDFzKDAuMjglKVxub2YgMC4xMnMoMy40MSUpIn0sIHsic2l6ZSI6IDAuMDYs
ICJjaGlsZHJlbiI6IFt7InNpemUiOiAwLjA1LCAiY2hpbGRyZW4iOiBbeyJuYW1lIjogImNyeXB0
by9hZXMuaGFzR0NNQXNtXG4wLjA0cygxLjE0JSkiLCAic2l6ZSI6IDAuMDR9XSwgIm5hbWUiOiAi
Y3J5cHRvL2Flcy5uZXdDaXBoZXJcbjAgb2YgMC4wNXMoMS40MiUpIn1dLCAibmFtZSI6ICJjcnlw
dG8vYWVzLk5ld0NpcGhlclxuMC4wMXMoMC4yOCUpXG5vZiAwLjA2cygxLjcwJSkifV0sICJuYW1l
IjogImx1bS92ZW5kb3Iva2xhYi9mbW9mL2Ztb2YvcnBjc3YuKCpDb25uKS5vdXRnb2luZ0ZpbHRl
clxuMCBvZiAwLjI1cyg3LjEwJSkifSwgeyJuYW1lIjogImx1bS92ZW5kb3Iva2xhYi9mbW9mL2Zt
b2YvcnBjc3YuKCpDb25uKS5hcHBlbmRUb1NlbmRCdWZcbjAuMDFzKDAuMjglKVxub2YgMC4wNnMo
MS43MCUpIiwgInNpemUiOiAwLjA2fV0sICJuYW1lIjogImx1bS92ZW5kb3Iva2xhYi9mbW9mL2Zt
b2YvcnBjc3YuKCpDb25uKS5TZW5kXG4wIG9mIDAuMzFzKDguODElKSJ9LCB7Im5hbWUiOiAibHVt
L25vdGljZS4oKkFsbE5vdGljZSkuUGFja2V0XG4wLjAxcygwLjI4JSlcbm9mIDAuMzVzKDkuOTQl
KSIsICJzaXplIjogMC4zNX1dLCAibmFtZSI6ICJsdW0vZ2FtZS9yb29tLigqUm9vbSkuc2VuZGVy
XG4wIG9mIDEuMDdzKDMwLjQwJSkifSwgeyJzaXplIjogMC4zOCwgImNoaWxkcmVuIjogW3sic2l6
ZSI6IDAuMjksICJjaGlsZHJlbiI6IFt7Im5hbWUiOiAicnVudGltZS5oZWFwQml0c0Zvck9iamVj
dFxuMC4wOXMoMi41NiUpIiwgInNpemUiOiAwLjA5fSwgeyJuYW1lIjogInJ1bnRpbWUuZ3JleW9i
amVjdFxuMC4wN3MoMS45OSUpXG5vZiAwLjEwcygyLjg0JSkiLCAic2l6ZSI6IDAuMX1dLCAibmFt
ZSI6ICJydW50aW1lLnNjYW5vYmplY3RcbjAuMTNzKDMuNjklKVxub2YgMC4yOXMoOC4yNCUpIn1d
LCAibmFtZSI6ICJydW50aW1lLmdjRHJhaW5cbjAgb2YgMC4zOHMoMTAuODAlKSJ9XSwgIm5hbWUi
OiAicnVudGltZS5nb2V4aXQgKDIuOTdzKSJ9Cg=="""

def find_children(index, root_node):
    global LINKS, NODES, PARENT_MARKS
    PARENT_MARKS.add(index)
    children = []
    c_nodes = []
    for node in LINKS:
        if node['target'] in PARENT_MARKS:
            continue
        if index == node['source']:
            children.append(node['target'])
    if len(children) != 0:
        if 'children' not in root_node:
            root_node['children'] = []
        cnt = 0
        for child in children:
            name = NODES[child]['label'].replace('\\n', '\n')
            if 'size' not in NODES[child]:
                # NOTE: ignore to function local buffer
                size = float(NODES[child]['tooltip'])
                continue
            else:
                size = NODES[child]['size']
            root_node['children'].append({'name': name, 'size': size})
            c_nodes.append(find_children(child, root_node['children'][cnt]))
            cnt += 1
        root_node['children'] = copy.copy(c_nodes)
        if len(root_node['children']) == 0:
            del(root_node['children'])
    return copy.copy(root_node)


def main():
    global NODES, LINKS
    parser = argparse.ArgumentParser(description='Render a dot tree as a treemap.')
    parser.add_argument('-b', '--bind', help='self host bind address')
    parser.add_argument('filepath', help='A dot file')

    args = parser.parse_args()

    graph = pgv.AGraph(args.filepath)
    graph_netx = from_agraph(graph)
    graph_json = json_graph.node_link_data(graph_netx)
    root_node_index = 0
    root = {}
    for cnt, node in enumerate(graph_json['nodes']):
        _id = node['id']
        if _id[:2] != "NN" and _id[0] != "L":
            s = RE_DIGIT.search(node['tooltip'])
            size = float(s.group(1))
            node['size'] = size
        if _id == 'N1':
            root_node_index = cnt
            root = {'name': node['tooltip'], 'size': size}

    LINKS = [n for n in graph_json['links']]
    NODES = [n for n in graph_json['nodes']]
    ret = find_children(root_node_index, root)
    if args.bind:
        pass
    else:
        print(json.dumps(ret))

if __name__ == '__main__':
    main()
