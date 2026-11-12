---
paths:
  - "tools/**"
  - "Sources/DesktopMascot/Characters/**"
  - "Sources/DesktopMascot/Sprites.swift"
---

# キャラ設定とスプライト

- キャラは `tools/characters/<id>.py` 1ファイルで完結させる。追加はファイルを置いて `./build.sh` するだけでメニューに並ぶ。アプリのコードは触らない
- 新しいキャラは `python3 tools/new_character.py <id> <表示名> [--hair bob|long]` でひな形を作り、髪・色・服を直していく。ひな形は形式チェックと崩れの検出を通る状態で出る
- 体の共通部品は `tools/base_character.py`（顔の形・目の部品と表情 `standard_faces()`・腕のポーズ `ARM_POSES` と袖付きの腕 `sleeved_arm()`・脚のポーズと靴 `legwear()`・横向きの歩き・組み立て `build_standard()`/`assemble()`・標準アクション `standard_actions()`）。キャラのファイルに書くのは髪・服・色と、そのキャラだけの違いだけにする。全キャラに入れたい表情・ポーズ・アクションは `base_character.py` に足す
- 設定ファイルに書くもの: `ID`・`NAME`・`ORDER`（メニュー順）・`W`/`H`/`OY`・`PALETTE`、`build()`（ポーズの絵）、`ACTIONS`（アクション）、任意で `GLYPHS`/`GLYPH_PALETTE`（頭上の絵）・`SNACK`（おやつの `name` と `glyph`。色は `GLYPH_PALETTE` から。無いとメニューの「おやつをあげる」が無効になる）
- 色の文字は共通部品が前提にしている: `K` 輪郭・`H`/`G`/`h` 髪（基本・影・ハイライト）・`S`/`s` 肌（基本・影）・`p`/`P` ほお・`W` 白・`E`/`F`/`e` 目・`R`/`m` 口。服の色はそれ以外の英字を使う（小物の色の数字 `1`〜`7` とぶつからないように）
- `build(outfit)` は衣装 ID を受け取り、その衣装の絵を返す。ふつうは `build_standard(outfit, front_body=..., side_body=..., sleeves=SLEEVES, legwear=LEGWEAR)` を呼ぶだけ。`front_body(outfit)` は正面の髪と服、`side_body(outfit, left)` は右向きの髪と服を描く（顔は `paint_face`/`shade_under_bangs`/`paint_side_face`/`shade_side_under_bangs`）。`SLEEVES` は衣装ごとの袖（`reach` が 2 で手首まで。1.6 くらいで指先がのぞく）、`LEGWEAR` は衣装ごとの `legwear(hip=, tights=, sock=, feet=, shoe=)`。腕・脚の描き方そのものが違うキャラは `assemble()` に自前の関数を渡す（虹夏）
- `OUTFITS = [("id", "表示名"), ...]`（先頭が初期衣装。省略すると `[("default", "標準")]`）。衣装ごとに変わるのは服の絵（`body`・袖・靴下など）で、顔・髪・肌は共通
- `ACCESSORIES = ["cap", "glasses", "ribbon"]`（`sprite_engine.py` に絵がある小物から選ぶ）。小物は頭に重ねる独立した絵で、メニューの「小物」から付け外しできる。新しい小物は `sprite_engine.py` の `front_accessories`/`side_accessories`/`ACCESSORY_NAMES` に足す
- `build()` は `faces`/`arms`/`legs` を名前→レイヤーの辞書で返す。`faces` に `normal`・`blink`、`arms` に `down`、`legs` に `stand` は必須。`lookLeft`/`lookRight` があれば視線に使われる。`drops` で座りなど上半身を下げるポーズを指定する
- `ACTIONS` はふつう `standard_actions(drop=(使わない名前), change={名前: {上書きする項目}}, add=[そのキャラだけのアクション])` で作る
- `ACTIONS` の各要素: `name`、`trigger`（`idle`=待機中ランダム / `click` / `drag` / `fall` / `pet`=なでなで / `throw`=投げられて飛んでいる間 / `land`=強く着地したとき / `eat`=おやつを食べるとき / `ledge`=乗っているウィンドウの端に着いたとき / `wall`=画面の左右の端に着いたとき / `talk`/`listen`=おしゃべりの話す番と聞く番（他のキャラが近くにいて、待機が終わったときに相手も待機中なら 1/3 の確率で始まる。4〜6回交代する。`talk` の吹き出しは相手の側に反転して出る。`listen` は話す側が終わるまで続き、目線は相手へ向けてときどきうなずくので、`duration` は長めにする。`talk` には `mood`（`normal`/`fun`/`question`/`surprise`）を付け、`listen` には反応する話の種類を `moods` に並べる。`moods` が無い `listen` はどの話にも使われる。`question` のあとは相手が必ず `question` 以外で答える）/ `near`=おしゃべりの終わりに出す反応（相手も少し遅れて出す）/ `top`=ウィンドウの上で待機が終わったとき（1/3 の確率）/ `jump`=歩いていて自分より高いウィンドウの端に着き、ジャンプで乗るとき（`frames` のポーズを再生。長さはアプリ側が距離で決める）/ `circle`=マウスをキャラの周りでぐるぐる回したとき / `corner`=メニューの「すみで座る」で画面のすみに着いたとき（`sit: True` を付ける。終わるとまた同じものを再生して座り続ける）/ `chained`=`next` からのみ）、`weight`、`duration`（tick 範囲、20tick=1秒）、`frames`（`face`/`arms`/`legs`/`ticks`）、`lift`（`jump`/`hop`/`rise`/`sink`=キャラ全体を下げる。ふちに座るときに使う / `cling`=`sink` に加えて、乗っているウィンドウの上辺より下を描かない。手だけ見せるときに使う）、`effect`（`glyph`/`period`/`from`=出し始める tick/`until`/`dx`）、`next`（{アクション名: 確率}）、`strength`（`throw`/`land` で投げた強さ=離した瞬間の px/tick の範囲）、`walk: True` で歩行、`sit: True` は座る動き（右クリックの「座る」とメニューの「ウィンドウの上でずっと座る」で、終わったあとにまた座り続ける対象。`trigger: "top"` の `sit` が 1 つ必要で、それが座り始めに使われる。そこから `next` でつなぐ動きにも付ける）、`apps`（裏のウィンドウのアプリの bundle ID のリスト。一致するときだけ候補になる。`sprite_engine.py` の `TERMINAL_APPS`/`BROWSER_APPS`/`MUSIC_APPS` を使える）
- アクションを追加するときは、原則として座っているときにも起きるようにする。右クリックの「座る」で座っている間（と、座ったままのおしゃべり）は、アクションの表情と頭上の絵だけが座った姿に重なる（`Mascot+Sitting.swift` の `reaction`）。腕・足・`lift` は使われないので、表情と絵だけでも伝わるか確かめる。立ち姿でないと成り立たない動きは、座り用の `sit: True` の動きを別に用意するか、座っているときに起きないようにした理由をユーザーに伝える
- `Characters/*.swift` は生成物なので直接編集しない。形式チェックは `tools/gen_sprites.py` が行い、不正なら生成時にエラーで止まる
- 生成するたびに `build/previews/` に確認用の画像を書き出す: `<id>.png`（全衣装のポーズと横向き）・`<id>-faces.png`（表情）・`all.png`（全キャラの全衣装。服の幅や丈をほかのキャラと比べる）。キャラや服を変えたら `open` で見てから報告する
- 生成時に崩れを検出して `warning:` を出す（`tools/sprite_lint.py`）: 目が顔横の髪の輪郭とくっつく・袖で手が隠れる・8px 以下の閉じた隙間。警告が出たら直すか、意図したものかユーザーに確認する
- 図形・輪郭線・共通の頭上の絵は `tools/sprite_engine.py`。吹き出しは `bubbles(名前, 中身)` で作る（相手が左にいるときは `名前@left` が使われ、しっぽだけ反転する）
- 輪郭線は自動で付く。グループの `CLASS` が違う境目に線が入るので、部品を分けて見せたいときは別クラスにする
- 1〜2px の細い形はほぼ輪郭線だけになり黒いトゲに見えるので、幅 3px 以上を目安にする
- 閉じた小さな透明領域ができると内側に輪郭線が出て変な線に見えるので避ける
