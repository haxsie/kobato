# KOBATO
KOBATOは、Python、Pygameで開発されたシンプルなアクションゲームです。  
方向キーで紅い飛行体を操作し、敵を避けながら宝石を集めます。

このゲームには、 **「不連続時間操作」** 、 **「疑似慣性」** という独特のギミックが備わっています。  
この文書の末尾の注を読んだ上でのプレイをおすすめします。

## 内容物
- KOBATO.exe  
ダブルクリックするとゲームが起動します。
- dataフォルダ  
ゲームで使用する外部ファイル（音声ファイル等）が格納されています。
- replayフォルダ  
リプレイ機能を使用すると作成されます。リプレイファイルはこの中に生成され、使用したいときはこの中に入れます。詳しくは後述します。
- その他
動作に必要なファイルです。他の場所に移したり削除してはいけません。

## 遊び方

### 基本操作
方向キーで紅い飛行体を操作します。  
これがあなたです。

規定の条件で現れる敵に当たるとライフ（画面左上に表示）が減ります。  
ライフが尽きるとゲームオーバーです。

画面に現れる宝石に触れると獲得宝石（画面右上に表示）が増えます。  
獲得宝石が規定数に達するとレベル（ステージ）が進行します。  
この際、獲得宝石の数はリセットされ、獲得規定数は一つ増えます。
レベル10に進むことが出来ればクリアです。（スコア要素等は実装していません。）

### その他の操作
ゲーム起動画面に書かれているとおりです。  
以下解説です。

- Rキー  
起動画面で入力するとリプレイ記録を開始します。  
リプレイファイルはreplayフォルダに保存されます。  
- Pキー  
リプレイを再生します。  
replayフォルダ内のリプレイファイルを参照しますが、複数のファイルが入っている場合そのうちどれが再生されるかは不定です。  
- spaceキー  
スクリーンショットを保存します。  
おまけ機能です。
- enterキー  
ゲーム起動画面に戻ります。  
ゲーム進行のリセットなどに使います。
- escキー  
ゲームを終了します。  
ウインドウを閉じることでも終了できます。

## 注）本作の特異な要素について
本作は基本的に単純なアクションゲームです。  
しかし以下の２つの点に注意してください。  
これらは本作の特殊な要素であり、注釈なしで始めると戸惑うことになるはずです。

### 不連続時間操作について
このゲームはターン制で進行します。  
一つのターンはプレイヤーの一回の入力に始まり、全ての物体の移動と衝突判定が行われ、最後にその結果が画面に出力されることで終わります。  
その後、次の入力があるまで画面は一切変化しません。

### 疑似慣性について
このゲームにおいて、すべての物体は見えない格子上に存在します。  
飛行体は、各ターンこの格子の交点から交点へ、基本的に前のターンと同じように移動します。  
プレイヤーの入力や敵の方向修正処理は、この移動における到達点の「ひとマス単位」での微調整として働きます。  

## このソフトウェアについて
このソフトウェアはフリーソフトです。  
作者はこのソフトウェアの正常な動作や安全性に関し、一切の保証責任を負いません。  
本作に関する要望、不具合等に関しては、下記連絡先までお送りください。

- 動作環境: Windows(バージョン8.1での動作を確認。)
- 開発環境: Windows8.1, Python, Pygame, Py2exe

- バージョン: 0.1

- 作者: はくし
- 作者HP: [空理計画](http://kuuri.net)
- 作者メールアドレス: createblankdevelop@gmail.com
- 権利表示: (c) 2017 空理計画

## 更新履歴
- 2017/02/10  
Ver 0.1 公開