from sub.mcFont import McFont
from pathlib import Path
import sys

def spinner_gen():
    while 1:
        yield '|'
        yield '/'
        yield '-'
        yield '\\'

if __name__ == '__main__':
    for spinner in spinner_gen():
        print(spinner + '\033[1D', end='', file=sys.stderr)

def convert(fontJsonPath:str,genTTf:bool=True,genWOFF:bool=False,name:str='BitmapMc'):
  if not (genTTf or genWOFF): return
  mcFont = McFont(name)
  jsonPath = Path(fontJsonPath)
  assetsPath = jsonPath.parent.parent.parent
  mcFont.generate(jsonPath,assetsPath)
  if genTTf:
    print('ttfを生成しています')
    mcFont.exportTTF()
  if genWOFF:
    print('woffを生成しています')
    mcFont.exportWoff()

if __name__ == '__main__':

  args = sys.argv

  if len(args) > 1:
    jsonPath = args[1]
    print(jsonPath)
    try:
      convert(jsonPath)
    except Exception as e:
      print(e)
      print('変換時にエラーが発生しました')
      print('閉じるにはaを入力してください')
      while input() != 'a':
        pass
      raise e
    print('変換が正常に終了しました')
    print('閉じるにはaを入力してください')
    while input() != 'a':
      pass

### スクリプトから実行する場合
#   # <path>は次のようなパスになる：C:.../assets/<namespace>/font/<fontname>.json
#   convert('<path>',genTTf=True,genWOFF=False,name:str='BitmapMc')
