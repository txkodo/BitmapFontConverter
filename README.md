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

#### 本リポジトリをクローンする

gitの使用方法がわかる場合:

​	`$ git clone https://github.com/txkodo/BitmapFontConverter`

zip形式でダウンロードする場合:

​	本ページ右上の[ **Code▼** ]をクリックし[Download Zip]を選択、ダウンロードされたZipファイルを展開する

入手したフォルダを以後"本フォルダ"と呼称する。





#### リソースファイルを入手する

Minecraftのjar内部のassetsフォルダを展開する。

`C:\Users\<user>\AppData\Roaming\.minecraft\versions\<version>\<version>.jar`　を7zip等のツールで開き、内部のassetsフォルダを任意の場所に展開する。

※リソースパック内のassetsフォルダを使うことでデフォルト以外のカスタムフォントの変換も可能





#### jsonファイルをドラッグドロップする

先ほどのassetsフォルダを開き、assets/minecraft/font/default.jsonを本フォルダ内のconverter.pyにドラッグドロップする。

コマンドプロンプト/シェルの画面が立ち上がり変換が始まる。

本フォルダ内にBitmapMc.ttfというファイルが生成されれば成功。





#### pythonスクリプトから実行する(発展編)

pythonの文法がある程度わかる場合はpythonの関数を呼び出すことで変換することもできる。

converter.py内部に呼び出し方法が記載されているためそちらを参照すること。

.woffファイルを生成する場合はこちらの方法をとること。



------

## 免責事項

#### 著作権に関して

本ツールの著作権は作者txkodoにありますが、本ツールを使って変換されたフォントファイルの著作権はフォントの作者にあります。たとえば、本ツールを用いてMinecraftのデフォルトのフォントを変換した場合に生成されたフォントファイルにはMinecraftの著作権が適用され、公式ガイドラインに基づき改変および配布はできません。



#### 使用に関して

本ツール及び本ツールが参照しているpythonライブラリにおいて問題が発生した場合、作者は責任を負いかねます。ツールの使用は自己責任でお願いします。また、変換対象のフォントの利用規約もご確認の上お使いください。



#### 改変/再配布に関して

個人利用における改変は自己責任でお願します。また、改変の有無にかかわらず再配布は可能ですが、本ツールの複製/改変であること、改変した場合は改変個所を明示するようお願いします。
