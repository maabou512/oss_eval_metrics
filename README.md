
# OSS Health Radar 🚀

GitHubリポジトリの活動データから、OSSプロジェクトの「健康状態」と「コミュニティ特性」を多角的に分析・可視化するツールキットです。

## 📋 概要

このプロジェクトは、単なるコミット数だけでなく、CHAOSS（Community Health Analytics Open Source Software）の概念を参考に、以下の5つの軸でプロジェクトの個性を可視化します。

1. **Activity（活動量）**: 開発スピードと更新頻度
2. **Diversity（多様性）**: 特定企業への依存度
3. **Density（密度）**: 継続的な常連貢献者の割合
4. **Responsiveness（反応速度）**: Issue/PRへの対応スピード
5. **Robustness（堅牢性）**: 知識の分散度（Bus Factor / CAF）

## 🛠 構成

### 1. データ抽出部 (`chaoss_metrics_collector.py`)
Pythonを使用してローカルGitログとGitHub APIからデータを抽出します。
- **入力**: ローカルリポジトリパス、開始年、GitHubアクセストークン
- **出力**: `output/` フォルダ内に年次メトリクスのJSONファイルを生成

### 2. 可視化ダッシュボード (`index.html`)
D3.jsを使用したブラウザベースのレーダーチャート比較ツールです。
- 複数プロジェクトの重ね合わせ比較
- 統計データの正規化表示
- 特性プロファイルの解説表示

## 🚀 使い方

### ステップ 1: セットアップ
```bash
pip install PyGithub
export GIT_TOKEN_CLASSIC="あなたのGitHubトークン"

```

### ステップ 2: データの収集

解析したいリポジトリをローカルにクローンし、スクリプトを実行します。

```bash
python chaoss_metrics_collector.py /path/to/your-repo 2022

```

### ステップ 3: 可視化

1. `index.html` 内の `projectFiles` 配列に出力されたJSONファイル名を追加します。
2. ローカルサーバーを起動します。
```bash
python -m http.server 8000

```


3. ブラウザで `http://localhost:8000` を開き、プロジェクトを選択して比較します。

## 📊 指標の正規化基準

本ツールでは「通信簿」のような絶対評価ではなく、各項目の「強度」を可視化するために以下の基準（レベル5の目安）を設けています。

| 指標 | レベル5の目安 | 解説 |
| --- | --- | --- |
| **Activity** | 5,000 commits/yr | 開発の回転速度。活発な機能追加の状態。 |
| **Diversity** | 15+ Orgs | 複数の組織が支える自立したエコシステム。 |
| **Density** | 70%+ Active Rate | 常連貢献者が主体となっているコミュニティ。 |
| **Responsiveness** | < 5 days to close | フィードバックループが速く、貢献しやすい。 |
| **Robustness** | 10+ Bus Factor | 知見が分散され、主要メンバー離脱耐性が高い。 |

## ⚖️ ライセンス

CC0 1.0 Universal

```
