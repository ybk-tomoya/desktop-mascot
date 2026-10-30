# プロジェクト概要

macOS のデスクトップマスコットアプリ（Swift / AppKit、Xcode プロジェクトなし）。

- ビルド: `./build.sh`（スプライト生成 → `swiftc` で `build/DesktopMascot.app` を作る）
- 再起動: `pkill -x DesktopMascot; open build/DesktopMascot.app`
- 変更後はビルドしてアプリを再起動し、ユーザーがすぐ実物を見られるようにする
- `Sources/DesktopMascot/main.swift`: 起動処理だけ
- `Sources/DesktopMascot/Mascot.swift`: ウィンドウ・メニュー・キャラ切り替えと、状態を持つ変数（extension には保存プロパティを置けないのでここに残す）
- `Sources/DesktopMascot/Mascot+Behavior.swift`: 状態遷移（歩く・まばたき・視線・ドラッグ・重力だけが組み込み。他のアクションはキャラ設定を再生する）。`step()` は状態ごとの `stepXxx` を呼ぶだけ
- `Sources/DesktopMascot/MascotView.swift`: 描画とマウス入力
- `Sources/DesktopMascot/Desktop.swift`: 画面上の他アプリのウィンドウ一覧
- `Sources/DesktopMascot/Sprites.swift`: `MascotCharacter` / `MascotAction` などのデータ型とレイヤー合成
- `references/` は公式資料のスキャンなので git に入れない（`.gitignore` 済み）
- コミットはユーザーに頼まれたときだけ行う
- 落下中・投げられて飛んでいる途中にクリックすると、空中に浮いたまま止まる。ユーザーが面白いので残すと決めた仕様なので直さない
