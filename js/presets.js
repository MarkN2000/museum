/**
 * Preset artworks for the selection screen.
 * 
 * ローカル画像を使用するバージョン。
 * 画像は assets/images/ に配置してください。
 * GLBは generate_artwork_glb.py で生成します。
 * 
 * 各エントリ:
 * - id: 識別子
 * - label: 表示名
 * - localImagePath: assets/images/ 内の画像パス
 * - thumbnailPath: サムネイル画像パス（同じでもOK）
 * - glbPath: AR表示用GLBファイルパス
 * - widthCm: 横幅 (cm)
 * - heightCm: 縦幅 (cm)
 * - source: 出典URL（ライセンス確認用）
 * - originalImageUrl: 元の画像URL（RDF記載）
 * - license: ライセンス情報
 */
export const PRESET_ARTWORKS = [
  {
    id: "tfam_art_db-3621",
    label: "冨嶽三十六景 山下白雨",
    localImagePath: "assets/images/03621.jpg",
    thumbnailPath: "assets/images/03621.jpg",
    glbPath: "assets/03621.glb",
    widthCm: 37.7,
    heightCm: 25.5,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3621",
    originalImageUrl: "https://www.fujibi.or.jp/assets/images/collection/base/03621.jpg",
    license: "パブリックドメイン（著作権切れ）"
  },
  {
    id: "tfam_art_db-3628",
    label: "冨嶽三十六景 神奈川沖浪裏",
    localImagePath: "assets/images/3628.webp",
    thumbnailPath: "assets/images/3628.webp",
    glbPath: "assets/3628.glb",
    widthCm: 36.5,
    heightCm: 24.6,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3628",
    originalImageUrl: "https://www.fujibi.or.jp/webp/assets/images/artwork/source/03628.jpg.webp",
    license: "パブリックドメイン"
  },
  {
    id: "tfam_art_db-3557",
    label: "風神雷神図襖",
    localImagePath: "assets/images/3557.webp",
    thumbnailPath: "assets/images/3557.webp",
    glbPath: "assets/3557.glb",
    widthCm: 462.0,
    heightCm: 168.0,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3557",
    originalImageUrl: "https://www.fujibi.or.jp/webp/assets/images/artwork/source/03557_01.jpg.webp",
    license: "パブリックドメイン"
  },
  {
    id: "tfam_art_db-1173",
    label: "名所江戸百景 大はしあたけの夕立",
    localImagePath: "assets/images/1173.webp",
    thumbnailPath: "assets/images/1173.webp",
    glbPath: "assets/1173.glb",
    widthCm: 24.7,
    heightCm: 35.7,
    source: "https://jpsearch.go.jp/item/tfam_art_db-1173",
    originalImageUrl: "https://www.fujibi.or.jp/webp/assets/images/artwork/source/01173.jpg.webp",
    license: "パブリックドメイン"
  },
  {
    id: "tfam_art_db-3547",
    label: "サン＝ベルナール峠を越えるボナパルト",
    localImagePath: "assets/images/3547.webp",
    thumbnailPath: "assets/images/3547.webp",
    glbPath: "assets/3547.glb",
    widthCm: 59.0,
    heightCm: 73.5,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3547",
    originalImageUrl: "https://www.fujibi.or.jp/webp/assets/images/artwork/source/03547.jpg.webp",
    license: "パブリックドメイン"
  },
  {
    id: "tfam_art_db-3577",
    label: "観念",
    localImagePath: "assets/images/3577.webp",
    thumbnailPath: "assets/images/3577.webp",
    glbPath: "assets/3577.glb",
    widthCm: 33.0,
    heightCm: 41.0,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3577",
    originalImageUrl: "https://www.fujibi.or.jp/webp/assets/images/artwork/source/03577.jpg.webp",
    license: "パブリックドメイン"
  }
  // 他の作品を追加する場合はここに追加
];
