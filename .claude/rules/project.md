# プロジェクト概要

macOS のデスクトップマスコットアプリ（Swift / AppKit、Xcode プロジェクトなし）。

- ビルド: `./build.sh`（`swiftc` で `build/DesktopMascot.app` を作る）
- 再起動: `pkill -x DesktopMascot; open build/DesktopMascot.app`
- 変更後はビルドしてアプリを再起動し、ユーザーがすぐ実物を見られるようにする
- `Sources/DesktopMascot/main.swift`: ウィンドウ・状態遷移（歩く、ドラム、居眠りなど）・メニュー
- `Sources/DesktopMascot/Sprites.swift`: `MascotCharacter`、レイヤー合成、エフェクト（ハート・音符・Z）
- `references/` は公式資料のスキャンなので git に入れない（`.gitignore` 済み）
- コミットはユーザーに頼まれたときだけ行う
