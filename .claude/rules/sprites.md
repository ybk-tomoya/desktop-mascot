---
paths:
  - "tools/**"
  - "Sources/DesktopMascot/Characters/**"
  - "Sources/DesktopMascot/Sprites.swift"
---

# キャラ設定とスプライト

- キャラは `tools/characters/<id>.py` 1ファイルで完結させる。追加はファイルを置いて `./build.sh` するだけでメニューに並ぶ。アプリのコードは触らない
- 設定ファイルに書くもの: `ID`・`NAME`・`ORDER`（メニュー順）・`W`/`H`/`OY`・`PALETTE`、`build()`（ポーズの絵）、`ACTIONS`（アクション）、任意で `GLYPHS`/`GLYPH_PALETTE`（頭上の絵）
- `build()` は `faces`/`arms`/`legs` を名前→レイヤーの辞書で返す。名前は自由だが `faces` に `normal`・`blink`、`arms` に `down`、`legs` に `stand` は必須。`lookLeft`/`lookRight` があれば視線に使われる。`drops` で座りなど上半身を下げるポーズを指定する
- `ACTIONS` の各要素: `name`、`trigger`（`idle`=待機中ランダム / `click` / `drag` / `fall` / `chained`=`next` からのみ）、`weight`、`duration`（tick 範囲、20tick=1秒）、`frames`（`face`/`arms`/`legs`/`ticks`）、`lift`（`jump`/`hop`/`rise`）、`effect`（`glyph`/`period`/`until`/`dx`）、`next`（{アクション名: 確率}）、`walk: True` で歩行
- `Characters/*.swift` は生成物なので直接編集しない。形式チェックは `tools/gen_sprites.py` が行い、不正なら生成時にエラーで止まる
- 共通処理（図形、輪郭線、共通の頭上の絵）は `tools/sprite_engine.py`
- 輪郭線は自動で付く。グループの `CLASS` が違う境目に線が入るので、部品を分けて見せたいときは別クラスにする
- 1〜2px の細い形はほぼ輪郭線だけになり黒いトゲに見えるので、幅 3px 以上を目安にする
- 閉じた小さな透明領域ができると内側に輪郭線が出て変な線に見えるので避ける
