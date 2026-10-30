---
paths:
  - "tools/**"
  - "Sources/DesktopMascot/Characters/**"
  - "Sources/DesktopMascot/Sprites.swift"
---

# スプライトの作り方

- キャラの絵は `tools/characters/<id>.py` に図形（楕円・多角形・線）で定義し、`python3 tools/gen_sprites.py` で `Sources/DesktopMascot/Characters/*.swift` を生成する
- `Characters/*.swift` は生成物なので直接編集しない
- 共通処理（図形、輪郭線、ポーズ一覧）は `tools/sprite_engine.py`
- 輪郭線は自動で付く。グループの `CLASS` が違う境目に線が入るので、部品を分けて見せたいときは別クラスにする
- 1〜2px の細い形はほぼ輪郭線だけになり黒いトゲに見えるので、幅 3px 以上を目安にする
- 閉じた小さな透明領域ができると内側に輪郭線が出て変な線に見えるので避ける
- 新しいキャラは `nijika.py` をコピーして `ID`・`NAME`・`PALETTE`・形を書き換える。生成すればメニューに自動で並ぶ
