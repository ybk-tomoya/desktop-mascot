---
paths:
  - "tools/**"
  - "Sources/DesktopMascot/Characters/**"
  - "Sources/DesktopMascot/Sprites.swift"
---

# キャラ設定とスプライト

- キャラは `tools/characters/<id>.py` 1ファイルで完結させる。追加はファイルを置いて `./build.sh` するだけでメニューに並ぶ。アプリのコードは触らない
- 設定ファイルに書くもの: `ID`・`NAME`・`ORDER`（メニュー順）・`W`/`H`/`OY`・`PALETTE`、`build()`（ポーズの絵）、`ACTIONS`（アクション）、任意で `GLYPHS`/`GLYPH_PALETTE`（頭上の絵）・`SNACK`（おやつの `name` と `glyph`。色は `GLYPH_PALETTE` から。無いとメニューの「おやつをあげる」が無効になる）
- `build(outfit)` は衣装 ID を受け取り、その衣装の絵を返す。`OUTFITS = [("id", "表示名"), ...]`（先頭が初期衣装。省略すると `[("default", "標準")]`）。衣装ごとに変わるのは服の絵（`body`・袖・靴下など）で、顔・髪・肌は共通。衣装で使う色は `PALETTE` に足す（小物の色の数字 `1`〜`7` とぶつからないように、文字は英字を使う）
- `ACCESSORIES = ["cap", "glasses", "ribbon"]`（`sprite_engine.py` に絵がある小物から選ぶ）。使うキャラは `SX`/`HX`（横向きの頭の位置）を定義しておく。小物は頭に重ねる独立した絵で、メニューの「小物」から付け外しできる。新しい小物は `sprite_engine.py` の `front_accessories`/`side_accessories`/`ACCESSORY_NAMES` に足す
- `build()` は `faces`/`arms`/`legs` を名前→レイヤーの辞書で返す。名前は自由だが `faces` に `normal`・`blink`、`arms` に `down`、`legs` に `stand` は必須。`lookLeft`/`lookRight` があれば視線に使われる。`drops` で座りなど上半身を下げるポーズを指定する
- `ACTIONS` の各要素: `name`、`trigger`（`idle`=待機中ランダム / `click` / `drag` / `fall` / `pet`=なでなで / `throw`=投げられて飛んでいる間 / `land`=強く着地したとき / `eat`=おやつを食べるとき / `ledge`=乗っているウィンドウの端に着いたとき / `wall`=画面の左右の端に着いたとき / `talk`/`listen`=おしゃべりの話す番と聞く番（他のキャラが近くにいて、待機が終わったときに相手も待機中なら 1/3 の確率で始まる。4〜6回交代する。`talk` の吹き出しは相手の側に反転して出る。`listen` は話す側が終わるまで続き、目線は相手へ向けてときどきうなずくので、`duration` は長めにして顔は指定しない）/ `near`=おしゃべりの終わりに出す反応（相手も少し遅れて出す）/ `top`=ウィンドウの上で待機が終わったとき（1/3 の確率）/ `jump`=歩いていて自分より高いウィンドウの端に着き、ジャンプで乗るとき（`frames` のポーズを再生。長さはアプリ側が距離で決める）/ `circle`=マウスをキャラの周りでぐるぐる回したとき / `chained`=`next` からのみ）、`weight`、`duration`（tick 範囲、20tick=1秒）、`frames`（`face`/`arms`/`legs`/`ticks`）、`lift`（`jump`/`hop`/`rise`/`sink`=キャラ全体を下げる。ふちに座るときに使う / `cling`=`sink` に加えて、乗っているウィンドウの上辺より下を描かない。手だけ見せるときに使う）、`effect`（`glyph`/`period`/`until`/`dx`）、`next`（{アクション名: 確率}）、`strength`（`throw`/`land` で投げた強さ=離した瞬間の px/tick の範囲）、`walk: True` で歩行、`sit: True` は座る動き（右クリックの「座る」とメニューの「ウィンドウの上でずっと座る」で、終わったあとにまた座り続ける対象。`trigger: "top"` の `sit` が 1 つ必要で、それが座り始めに使われる。そこから `next` でつなぐ動きにも付ける）、`apps`（裏のウィンドウのアプリの bundle ID のリスト。一致するときだけ候補になる。`sprite_engine.py` の `TERMINAL_APPS`/`BROWSER_APPS`/`MUSIC_APPS` を使える）
- アクションを追加するときは、原則として座っているときにも起きるようにする。右クリックの「座る」で座っている間（と、座ったままのおしゃべり）は、アクションの表情と頭上の絵だけが座った姿に重なる（`Mascot+Sitting.swift` の `reaction`）。腕・足・`lift` は使われないので、表情と絵だけでも伝わるか確かめる。立ち姿でないと成り立たない動きは、座り用の `sit: True` の動きを別に用意するか、座っているときに起きないようにした理由をユーザーに伝える
- `Characters/*.swift` は生成物なので直接編集しない。形式チェックは `tools/gen_sprites.py` が行い、不正なら生成時にエラーで止まる
- 共通処理（図形、輪郭線、共通の頭上の絵）は `tools/sprite_engine.py`
- 輪郭線は自動で付く。グループの `CLASS` が違う境目に線が入るので、部品を分けて見せたいときは別クラスにする
- 1〜2px の細い形はほぼ輪郭線だけになり黒いトゲに見えるので、幅 3px 以上を目安にする
- 閉じた小さな透明領域ができると内側に輪郭線が出て変な線に見えるので避ける
