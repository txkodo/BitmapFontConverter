from pathlib import Path
from defcon.objects.contour import Contour

from defcon.objects.font import Font
from defcon.objects.glyph import Glyph
from sub.mcGlyph import McGlyph
from typing import Callable, Union
from PIL import Image
from multiprocessing import Pool
from tqdm import tqdm

import os

class GlyphSizes:
  def __init__(self,binary:bytes) -> None:
    self.binary = binary
  
  def __getitem__(self,index):
    def split(i:int) -> tuple[int,int]:
      if i == 0:
        return (0,0)
      return ( i//16,i%16 + 1 )
    return split(self.binary[index])

class BitmapGlyphs:
  def __init__(self,path:Path,columnCount:int,rowCount:int,height:int) -> None:
    # 二値化されたbitmap
    img:Image.Image = Image.open(path).convert('RGBA')
    _,_,_,alpha =img.split()
    self.img = alpha.convert('1')
    self.width = self.img.width
    self.height = self.img.height
    print(self.width , columnCount)
    self.w_unit = self.width // columnCount
    self.h_unit = self.height// rowCount
    self.scale  = height/self.h_unit/8

  def __getitem__(self,coord:tuple[int,int]):
    x,y = coord
    return self.img.crop((x*self.w_unit,y*self.h_unit,(x+1)*self.w_unit,(y+1)*self.h_unit))

class BitmapFont:
  def __init__(self,assets:Path,filepath:str,height:int,ascent:int,chars:list[str]) -> None:
    namespace,filepath = filepath.split(':')
    filepath = assets/namespace/'textures'/filepath
    self.bitmap = BitmapGlyphs(filepath,len(chars[0]),len(chars),height)
    self.ascentRate = ascent/8
    self.width  = self.bitmap.w_unit
    self.height = self.bitmap.h_unit
    self.scale  = self.bitmap.scale

    self.chars = chars

  def genImgMap(self,matrix):
    a,b,c,d,e,f = matrix
    matrix = (int(a*self.scale),int(b*self.scale),int(c*self.scale),int(d*self.scale),e,f-int(d*self.ascentRate))

    chars = ( char for string in self.chars for char in string)
    multiProcessArgs = ((matrix,self.bitmap[x,y]) for y,string in enumerate(self.chars) for x in range(len(string)))

    with Pool(None) as p:
      result = dict(zip(chars,p.map(McGlyph,multiProcessArgs)))
    return result

class LegacyUnicodeFont:
  def __init__(self,assets:Path,sizes:str,template:str) -> None:
    templateNamespace,templatePath = template.split(':')
    self.template:Callable[[str],Path] = lambda x : assets/templateNamespace/'textures'/( templatePath % x )

    sizesNamespace,sizesPath = sizes.split(':')
    sizesPath = assets/sizesNamespace/sizesPath
    self.sizes = GlyphSizes(sizesPath.read_bytes())
    
    self.ascentRate = 7/8
    self.width  = 16
    self.height = 16
    self.scale  = 1/16

  def genImgMap(self,matrix):
    a,b,c,d,e,f = matrix
    matrix = (int(a*self.scale),int(b*self.scale),int(c*self.scale),int(d*self.scale),e,f-int(d*self.ascentRate))

    multiProcessArgs = []
    chars = []
    def codePoint(i,y,x):return 16**2*i+16*y+x
    for i in range(16**2):
      if not self.template(f'{i:02X}').exists():continue
      bitmap = BitmapGlyphs(self.template(f'{i:02X}'),16,16)
      chars += (chr(codePoint(i,y,x)) for y in range(16) for x in range(16))
      # TODO: Matrixのピクセル数による補正
      multiProcessArgs += ((matrix,bitmap[x,y],self.sizes[codePoint(i,y,x)])for y in range(16) for x in range(16))

    with Pool(None) as p:
      result = dict(zip(chars,p.map(McGlyph,multiProcessArgs)))
    return result

class FontBitmaps:
  def __init__(self,assets:Path,providers:list[dict],matrix:tuple[int,int,int,int,int,int]) -> None:
    self.assets = assets
    print('フォントプロバイダを解析しています')
    self.providers = [ self._loadProvider(provider) for provider in tqdm(reversed(providers),total = len(providers) ) ]
    self.state = 'init'
    self._genImages(matrix)
    self.length = len(self.imgMap)

  def _loadProvider(self,provider:dict[str,Union[str,int]]):
    if provider['type'] == 'bitmap':
      height = provider['height'] if 'height' in provider else 8
      return BitmapFont(self.assets,provider['file'],height,provider['ascent'],provider['chars'])

    if provider['type'] == 'legacy_unicode':
      return LegacyUnicodeFont(self.assets,provider['sizes'],provider['template'])
    assert False

  def _genImages(self,matrix):
    assert self.state == 'init'
    self.state = 'generated'
    imgMap:dict[str,McGlyph] = {}
    print('フォントファイルを取得しています')
    for provider in tqdm(self.providers):
      imgMap |= provider.genImgMap(matrix)
    self.imgMap = imgMap

  def export(self,font:Font):

    assert self.state == 'generated'
    self.state = 'calculated'

    glypheDatas:list[tuple[list[Contour], int]] = []
    # プログレスバーを表示させつつマルチスレッド処理
    print('ビットマップを変換しています')
    with tqdm(total=self.length) as t:
      with Pool(os.cpu_count()-1) as p:
        for result,k in zip(p.map(McGlyph.export,self.imgMap.values()),self.imgMap.keys()):
          glypheDatas.append(result)
          t.update(1)

    def genGlyph(char:str,contours:list[Contour],width:int):
      glyph:Glyph = font.newGlyph(str(ord(char)))
      glyph.unicode = ord(char)
      glyph.width = width
      for contour in contours:
        glyph.appendContour(contour)
    
    print('フォントに文字を登録しています')
    for char,(contours,width) in tqdm(zip(self.imgMap.keys(),glypheDatas),total=self.length):
      # \u0000は別途指定、\uFFFFと\uFFFEは無効?であるため除外
      if char not in b'\ufffe\uffff'.decode('unicode-escape'):
        if contours:
          genGlyph(char,contours,width)
        else:
          glyph:Glyph = font.newGlyph('cid00001')
          glyph.unicode = ord(char)

    space = b'\u0020'.decode('unicode-escape')
    glyph:Glyph = font.newGlyph('cid00001')
    glyph.unicode = ord(space)
    glyph.width = 64 # 空白文字は3ピクセル
