# 📊 Follower Counter（Qiita対応・表示付き）

Qiita API を用いて、特定ユーザーの「合計いいね数」を取得し、画面に表示する軽量なフォロワーカウンターです。  
X（旧Twitter）・Instagram・Facebookは定数で仮表示されており、今後API連携を予定しています。

---

## 🚀 特徴

- Qiita API でいいね数をリアルタイム取得
- `.env` による秘密情報の安全管理
- PyQt5 によるシンプルな全画面表示 UI
- Raspberry Pi 向けに動作確認済み

---

## 🧱 ディレクトリ構成

```
follower_counter/
├── main.py             # アプリ起動エントリーポイント
├── ui.py               # PyQt5で画面レイアウトを表示
├── config.py           # .env読み込みと定数管理
├── API/                # API呼び出しモジュール群
│   ├── __init__.py
│   └── QiitaAPI.py     # Qiitaいいね数取得用API関数
├── asset/              # SNSアイコン画像（Git管理対象外）
├── .env                # 環境変数（Git管理しない）
├── .gitignore
├── requirements.txt    # 仮想環境全体を書き出したもの
└── README.md           # このファイル（プロジェクト説明書）
```

---

## 🔐 `.env` の例

```env
QIITA_TOKEN=your_qiita_token
ORGANIZATION_NAME=technosphere
```

---

## 📦 セットアップ手順

### ① 仮想環境の作成と有効化

```bash
cd follower_counter
python3 -m venv venv
source venv/bin/activate
```

### ② 必要パッケージのインストール

```bash
pip install -r requirements.txt
```

> ⚠ この `requirements.txt` は Raspberry Pi の仮想環境を丸ごと書き出したものであり、実行に不要なパッケージも含まれています。

---

## ▶️ 実行方法

```bash
python main.py
```

> 実行してもコンソールには何も表示されません。  
> 全画面ウィンドウで以下の内容が表示されます：

- Qiita：APIで取得した合計いいね数
- X：表示は定数（今後API対応予定）
- Instagram：表示は定数
- Facebook：表示は定数

---

## 🖼️ アイコン画像について

- 各SNSのロゴは `asset/` 配下に配置される前提で `ui.py` が動作します。
- 画像が存在しない場合はアプリがエラーになる可能性があるため、**ダミー画像を配置するか、コード側で適切に例外処理してください。**
- **著作権やブランドガイドラインの観点から、SNS公式ロゴ画像は GitHub 上で配布・管理しません。**
- 必要に応じてご自身でライセンスを確認のうえ画像を調達してください。

`.gitignore` により `asset/` ディレクトリも Git 管理対象外となっています。

---

## 🔧 今後の予定

- X / Instagram / Facebook の API連携
- 非同期更新・自動リフレッシュ機能

---

## 🌿 Gitのブランチ運用規約

| branch        | description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| 🚀 `main`        | **納品** まで行った統一ブランチ（最終成果物）                                 |
| 🧪 `staging`     | **検証** 用の統一ブランチ（本番前の確認用）                                   |
| 🛠 `develop`     | **開発** 用の統一ブランチ（すべての作業のベース）                              |
| ✨ `feature/***` | 機能ごとに分けて作業する開発ブランチ（`***`には機能名を明記）                   |
| 📦 `release/***` | リリース時のタグ付け用ブランチ（`git tag`を使用してもOK）                      |
| 🐞 `fix/***`     | バグ対応やIssue修正用ブランチ（`***`には **Issue番号を必ず明記**）             |

---

### 🧭 ブランチの流れ（開発→検証→納品）

```mermaid
gitGraph
  branch staging
  branch develop
  checkout develop
  commit
  branch feature/func-1
  checkout feature/func-1
  commit
  commit
  checkout develop
  merge feature/func-1
  commit
  branch feature/func-2
  checkout feature/func-2
  commit
  commit
  checkout develop
  merge feature/func-2
  commit
  checkout staging
  commit
  merge develop
  commit
  checkout main
  commit
  merge staging
```

---

この運用ルールに従って、ブランチ名と目的を明確にしながら開発・管理を行ってください。
