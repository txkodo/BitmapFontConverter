from sub.mcFont import McFont
from pathlib import Path
import sys

def convert(fontJsonPath:str,genTTf:bool=True,genWOFF:bool=False,name:str='BitmapMc'):
  if not (genTTf or genWOFF): return
  mcFont = McFont(name)
  jsonPath = Path(fontJsonPath)
  assetsPath = jsonPath.parent.parent.parent
  mcFont.generate(jsonPath,assetsPath)
  if genTTf: mcFont.exportTTF()
  if genWOFF: mcFont.exportWoff()

if __name__ == '__main__':

  args = sys.argv

  if len(args) > 1:
    jsonPath = args[1]
    print(jsonPath)
    try:
      convert(jsonPath)
    except Exception as e:
      print(e)
      raise e
    input()

### スクリプトから実行する場合
#   # <path>は次のようなパスになる：C:.../assets/<namespace>/font/<fontname>.json
#   convert('<path>',genTTf=True,genWOFF=False,name:str='BitmapMc')
