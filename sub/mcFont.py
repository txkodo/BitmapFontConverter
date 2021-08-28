from pathlib import Path
from sub.bitmapFont import FontBitmaps
from fontTools.ttLib import TTFont
import ufo2ft
import defcon
import json

class McFont:
  def __init__(self,name:str) -> None:
    self.fontname = name
    font = defcon.Font()

    # フォント名、基本メトリックの設定
    font.info.familyName = name.replace(' ','')
    font.info.unitsPerEm = 128
    font.info.descender = -16
    font.info.ascender = 112
    font.info.xHeight = 64
    font.info.capHeight = 102

    self.font = font

    self.saved = False
  
  def generate(self,jsonPath:Path,assetPath:Path):
    providers = json.loads(jsonPath.read_text())['providers']
    fb = FontBitmaps(assetPath,providers,(128,0,0,-128,8,112))
    fb.export(self.font)

  def exportTTF(self):
    otf = ufo2ft.compileTTF(self.font)
    otf.save(self.fontname + '.ttf')
    self.saved = True

  def exportWoff(self):
    if not self.saved:
      self.exportTTF()
    
    t = TTFont(self.fontname + '.ttf')
    t.flavor='woff'
    t.save(self.fontname + '.woff')