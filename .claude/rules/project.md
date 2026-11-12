# プロジェクト概要

macOS のデスクトップマスコットアプリ（Swift / AppKit、Xcode プロジェクトなし）。

- ビルド: `./build.sh`（スプライト生成 → `swiftc` で `build/DesktopMascot.app` を作る）
- 再起動: `pkill -x DesktopMascot; open build/DesktopMascot.app`
- 変更後はビルドしてアプリを再起動し、ユーザーがすぐ実物を見られるようにする
- `Sources/DesktopMascot/main.swift`: 起動処理だけ
- `Sources/DesktopMascot/MascotApp.swift`: メニューバーのメニュー（モード・キャラ・衣装と小物・おやつ・座る・ログイン）と、`Mascot` の生成と破棄。モードは「ひとり」（選んだキャラ1体）と「みんな」（登録済みの全キャラ）
- `Sources/DesktopMascot/Mascot.swift`: 1体分のウィンドウの作成・マウス入力の受け口・タイマーと、状態を持つ変数（extension には保存プロパティを置けないのでここに残す）
- `Sources/DesktopMascot/Mascot+Wardrobe.swift`: キャラ・衣装・小物の切り替えと、おやつ（メニューからは `MascotApp` 経由で呼ぶ）
- `Sources/DesktopMascot/Mascot+Peers.swift`: 近くにいる他の `Mascot` の検出と、近づいたときの反応（`near` トリガー）
- `Sources/DesktopMascot/Mascot+Sitting.swift`: 座る動き（右クリックの「座る」・ずっと座る・座っている間の反応と視線）
- `Sources/DesktopMascot/Mascot+Behavior.swift`: 状態遷移の中心。`step()` は状態ごとの `stepXxx` を呼ぶだけで、`start`/`finish` がアクションの開始と終わりを決める。歩く・まばたき・視線・ドラッグ・重力・ウィンドウへのジャンプ移動だけが組み込みで、他のアクションはキャラ設定を再生する
- `Sources/DesktopMascot/Mascot+Movement.swift`: 足場の判定（`ground`）と、歩く・ドラッグ・投げ・落下・ジャンプ・おやつへ向かう動き、乗っているウィンドウへの追従
- `Sources/DesktopMascot/Mascot+Input.swift`: マウスの検出（なでる・ぐるぐる回す・視線・カーソル）
- `Sources/DesktopMascot/Mascot+Render.swift`: ポーズの適用と描画（フレームのキャッシュ）
- `Sources/DesktopMascot/MascotView.swift`: 描画とマウス入力
- `Sources/DesktopMascot/Desktop.swift`: 画面上の他アプリのウィンドウ一覧
- `Sources/DesktopMascot/Sprites.swift`: `MascotCharacter` / `MascotAction` などのデータ型とレイヤー合成
- `references/` は公式資料のスキャンなので git に入れない（`.gitignore` 済み）
- コミットはユーザーに頼まれたときだけ行う
- 落下中・投げられて飛んでいる途中にクリックすると、空中に浮いたまま止まる。ユーザーが面白いので残すと決めた仕様なので直さない
