# BitmapFontConverter

マインクラフトのassetのビットマップフォントデータを**ttf**(基本的なフォントファイル)/**woff**(webフォント用のフォントファイル)に変換するツール。

------

## 前提ツール

- python 3.9x + パッケージ
  `$`以降はコマンドプロンプト/シェルに入力し実行すること。

  - pillow `$ pip install Pillow`
  - fonttools  `$ pip install fonttools`
  - ufo2ft `$ pip install ufo2ft`
  - defcon `$ pip install defcon`

  

- Minecraft Java Edition

------

## 使用方法

#### リソースファイルを入手する

Minecraftのjar内部のassetsフォルダを展開する。

※リソースパック内のassetsフォルダを使うことでデフォルト以外のカスタムフォントの変換も可能



#### jsonファイルをドラッグドロップする

先ほどのassetsフォルダを開き、assets/minecraft/font/default.jsonをこのフォルダ内のconverter.pyにドラッグドロップする。

コマンドプロンプト/シェルの画面が立ち上がり変換が始まる。



#### 待つ

変換が始まりしばらくはCPU使用率が100%に張り付き、使用率が落ち着いた後も変換がつづく。かなり時間がかかるため焦らずに待つ。

※参考までに作者のデスクトップRyzen 5 3600で実行すると10分程かかる。

このフォルダ内にBitmapMc.ttfというファイルが生成されれば成功。



#### pythonスクリプトから実行する(発展編)

pythonの文法がある程度わかる場合はpythonの関数を呼び出すことで変換することもできる。

.woffファイルを生成する場合はこちらの方法をとること。



## 免責事項

#### 著作権に関して

本ツールの著作権は作者txkodoにありますが、本ツールを使って変換されたフォントファイルの著作権はフォントの作者にあります。たとえば、本ツールを用いてMinecraftのデフォルトのフォントを変換した場合に生成されたフォントファイルにはMinecraftの著作権が適用され、公式ガイドラインに基づき改変および配布はできません。

