# Museum AR

絵画を実寸でARで見られるWebアプリケーション。

## セットアップ

```bash
# 依存関係インストール
pip install Pillow

# 開発サーバー起動
npx -y http-server . -p 8080 -c-1

# AR機能テスト用（HTTPS必須）
npx -y local-ssl-proxy --source 8443 --target 8080
```

## 作品を追加する

ジャパンサーチから作品を追加できます。

### 方法1: 自動スクリプト（推奨）

```bash
python add_artwork.py https://jpsearch.go.jp/item/作品ID
```

**例:**
```bash
python add_artwork.py tfam_art_db-3628
```

スクリプトが自動で：
1. ジャパンサーチAPIから情報を取得
2. 画像をダウンロード
3. GLBファイルを生成
4. `presets.js` 用のエントリを出力

出力されたエントリを `js/presets.js` の配列に追加してください。

### 方法2: 手動

1. 画像を `assets/images/` に保存
2. GLB生成:
   ```bash
   python generate_artwork_glb.py assets/images/画像.jpg 幅cm 高さcm
   ```
3. `js/presets.js` にエントリを追加

## ファイル構成

```
museum/
├── index.html          # メインページ
├── js/
│   └── presets.js      # 作品データ
├── assets/
│   ├── images/         # 作品画像
│   └── *.glb           # AR用3Dモデル
├── add_artwork.py      # 作品追加スクリプト
└── generate_artwork_glb.py  # GLB生成スクリプト
```

## ドキュメント

- [AI Guidelines](doc/ai_guidelines.md)
- [Architecture](doc/architecture.md)
