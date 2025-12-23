# OSS Health Radar 🚀

複数のオープンソースプロジェクトの健全性を、**CHAOSS (Community Health Analytics in Open Source Software)** フレームワークに基づき、インタラクティブなレーダーチャートで比較・可視化するツールです。

## 🌟 特徴

* **全自動同期**: `output` フォルダ内の解析結果を自動スキャンし、ダッシュボードを即座に最新化。
* **マルチプロジェクト比較**: Linux Kernelのような巨大プロジェクトから新進気鋭のDBまで、同一条件で重ね合わせ。
* **タイムライン制御**: 2022年〜2025年までのプロジェクトの成長と変化をスライダーで直感的に確認。
* **CHAOSS準拠**: 国際的なコミュニティ健全性指標に基づいた5軸の科学的評価を採用。

## 📊 指標とLv.5（最大値）の基準

各軸は、以下の基準を満たしたときに最大評価（Lv.5）となるよう設計されています。

| 指標 (Radar Axis) | 対応する CHAOSS メトリクス | Lv.5 の目安と意味 |
| --- | --- | --- |
| **Activity** | Code Changes / Commits | **年間 5,000 commits〜**：開発スピードが極めて活発な状態。 |
| **Diversity** | Organizational Diversity | **所属 15組織以上**：特定企業に依存しない強固なエコシステム。 |
| **Density** | Active Contributors | **Active率 70%〜**：貢献者の多くが常連（年間10回〜）。コミュニティの熱量。 |
| **Responsiveness** | Time to Close | **平均 5日以内**：PR/Issueへの反応が速く、外部貢献を歓迎する体制。 |
| **Robustness** | Elephant Factor / Bus Factor | **CAF 10人以上**：主要開発者が分散しており、属人化リスクが低い。 |

---

## 🛠 ワークフロー

データの「解析」と「表示の同期」を分離しているため、運用が非常にスムーズです。

### 1. データ解析 (Analysis)

まず、解析スクリプトを実行して、最新のメトリクスデータを生成します。

```bash
python analyzer.py

```

※ 解析結果は `./output/` フォルダに JSON レポートとして保存されます。

### 2. ダッシュボードの同期 (Sync)

メンテナンススクリプトを実行し、`output` 内の全データを `index.html` に反映させます。

```bash
python sync_dashboard.py

```

※ これにより `index.html` 内のプロジェクトリストが自動的に書き換えられます。

### 3. ローカルサーバーの起動 (View)

D3.js によるデータ読み込みを正しく動作させるため、Python の標準サーバーを使用して閲覧します。

```bash
# プロジェクトルートで実行
python -m http.server 8000

```

起動後、ブラウザで **`http://localhost:8000/`** にアクセスしてください。

---

## 📂 フォルダ構成

* `analyzer.py`: OSSの履歴を解析し、JSONを出力するメインスクリプト。
* `sync_dashboard.py`: `output` フォルダをスキャンして `index.html` のプロジェクトリストを自動更新するツール。
* `index.html`: D3.js を使用した可視化ダッシュボード。
* `output/`: 各プロジェクトの解析済み JSON レポートが格納される場所。

## 🌐 関連リンク

* [CHAOSS Community Official Site](https://chaoss.community/) - OSSコミュニティの健全性指標に関する国際標準プロジェクト。

