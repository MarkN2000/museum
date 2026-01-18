#!/usr/bin/env python3
"""
作品追加スクリプト - ジャパンサーチから作品を追加

使用方法:
    python add_artwork.py <ジャパンサーチURL>
    
例:
    python add_artwork.py https://jpsearch.go.jp/item/tfam_art_db-3621
    python add_artwork.py tfam_art_db-3621
"""

import sys
import os
import re
import json
import urllib.request
import urllib.error
from pathlib import Path

# 画像保存先
IMAGES_DIR = Path("assets/images")
ASSETS_DIR = Path("assets")

def extract_item_id(url_or_id):
    """URLまたはIDから作品IDを抽出"""
    if url_or_id.startswith("http"):
        # URLからIDを抽出
        match = re.search(r'/item/([^/\?]+)', url_or_id)
        if match:
            return match.group(1)
        match = re.search(r'/data/([^/\?]+)', url_or_id)
        if match:
            return match.group(1)
    return url_or_id

def fetch_rdf_data(item_id):
    """RDFからデータを取得"""
    rdf_url = f"https://jpsearch.go.jp/api/item/{item_id}"
    print(f"📥 APIからデータ取得: {rdf_url}")
    
    try:
        req = urllib.request.Request(rdf_url, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data
    except urllib.error.HTTPError as e:
        print(f"❌ API取得エラー: {e.code}")
        return None
    except Exception as e:
        print(f"❌ エラー: {e}")
        return None

def parse_size(size_str):
    """サイズ文字列から幅と高さを抽出 (cm単位)"""
    if not size_str:
        return None, None
    
    # "24.6×36.5cm" or "24.6 x 36.5 cm" パターン
    patterns = [
        r'(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*cm',
        r'(\d+\.?\d*)\s*cm\s*[x×]\s*(\d+\.?\d*)\s*cm',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, size_str, re.IGNORECASE)
        if match:
            # 通常: 幅 x 高さ だが、浮世絵は 高さ x 幅 の場合も
            val1 = float(match.group(1))
            val2 = float(match.group(2))
            # 大きい方を幅とする（横長の浮世絵を想定）
            width = max(val1, val2)
            height = min(val1, val2)
            return width, height
    
    return None, None

def download_image(url, save_path):
    """画像をダウンロード"""
    print(f"📥 画像ダウンロード: {url}")
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=60) as response:
            with open(save_path, 'wb') as f:
                f.write(response.read())
        print(f"✅ 保存: {save_path}")
        return True
    except Exception as e:
        print(f"❌ ダウンロードエラー: {e}")
        return False

def generate_glb(image_path, width_cm, height_cm):
    """GLBファイルを生成"""
    import subprocess
    glb_name = image_path.stem + ".glb"
    glb_path = ASSETS_DIR / glb_name
    
    print(f"🔧 GLB生成: {glb_path}")
    result = subprocess.run([
        sys.executable, "generate_artwork_glb.py",
        str(image_path), str(width_cm), str(height_cm)
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ GLB生成完了")
        return glb_path
    else:
        print(f"❌ GLB生成エラー: {result.stderr}")
        return None

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    url_or_id = sys.argv[1]
    item_id = extract_item_id(url_or_id)
    print(f"\n🎨 作品ID: {item_id}\n")
    
    # RDFデータ取得
    data = fetch_rdf_data(item_id)
    if not data:
        sys.exit(1)
    
    # 情報を抽出
    common = data.get('common', {})
    title = common.get('title', '不明')
    if isinstance(title, list):
        title = title[0]
    
    # 画像URL
    image_urls = common.get('contentsUrl', []) or common.get('thumbnailUrl', [])
    if not image_urls:
        # RDFから直接探す
        for key, value in data.items():
            if 'url' in key.lower() and isinstance(value, str) and value.startswith('http'):
                image_urls = [value]
                break
    
    image_url = image_urls[0] if image_urls else None
    
    # サイズ情報
    size_str = None
    for key, value in data.items():
        if 'size' in key.lower() or '寸法' in key or 'cm' in str(value).lower():
            if isinstance(value, str) and 'cm' in value.lower():
                size_str = value
                break
    
    width_cm, height_cm = parse_size(size_str)
    
    # ライセンス
    license_info = common.get('rights', 'パブリックドメイン')
    if isinstance(license_info, list):
        license_info = license_info[0] if license_info else 'パブリックドメイン'
    
    print(f"📋 タイトル: {title}")
    print(f"🖼️  画像URL: {image_url}")
    print(f"📐 サイズ: {width_cm} x {height_cm} cm")
    print(f"📜 ライセンス: {license_info}")
    print()
    
    # サイズが取得できなかった場合は手動入力
    if not width_cm or not height_cm:
        print("⚠️ サイズを自動取得できませんでした。手動で入力してください:")
        width_cm = float(input("  幅 (cm): "))
        height_cm = float(input("  高さ (cm): "))
    
    # 画像URLがなければ手動入力
    if not image_url:
        print("⚠️ 画像URLを自動取得できませんでした。手動で入力してください:")
        image_url = input("  画像URL: ")
    
    # 画像ダウンロード
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    image_ext = Path(image_url.split('?')[0]).suffix or '.jpg'
    image_filename = f"{item_id.split('-')[-1]}{image_ext}"
    image_path = IMAGES_DIR / image_filename
    
    if not download_image(image_url, image_path):
        sys.exit(1)
    
    # GLB生成
    glb_path = generate_glb(image_path, width_cm, height_cm)
    if not glb_path:
        sys.exit(1)
    
    # プリセットエントリを生成
    print("\n" + "="*60)
    print("📝 presets.js に追加するエントリ:")
    print("="*60)
    preset_entry = f'''  {{
    id: "{item_id}",
    label: "{title}",
    localImagePath: "{image_path.as_posix()}",
    thumbnailPath: "{image_path.as_posix()}",
    glbPath: "{glb_path.as_posix()}",
    widthCm: {width_cm},
    heightCm: {height_cm},
    source: "https://jpsearch.go.jp/item/{item_id}",
    originalImageUrl: "{image_url}",
    license: "{license_info}"
  }}'''
    print(preset_entry)
    print("="*60)
    print("\n✅ 完了！上記のエントリを presets.js の配列に追加してください。")
    print("   カンマを忘れずに！")

if __name__ == "__main__":
    main()
