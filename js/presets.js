/**
 * Preset artworks for the selection screen.
 * 
 * ローカル画像を使用するバージョン。
 * 画像は assets/images/ に配置してください。
 * 
 * 各エントリ:
 * - id: 識別子
 * - label: 表示名
 * - localImagePath: assets/images/ 内の画像パス
 * - thumbnailPath: サムネイル画像パス（同じでもOK）
 * - widthCm: 横幅 (cm)
 * - heightCm: 縦幅 (cm)
 * - source: 出典URL（ライセンス確認用）
 * - license: ライセンス情報
 */
export const PRESET_ARTWORKS = [
  {
    id: "tfam_art_db-3621",
    label: "冨嶽三十六景 山下白雨",
    localImagePath: "assets/images/03621.jpg",
    thumbnailPath: "assets/images/03621.jpg",
    widthCm: 37.7,
    heightCm: 25.5,
    source: "https://jpsearch.go.jp/item/tfam_art_db-3621",
    license: "パブリックドメイン（著作権切れ）"
  }
  // 他の作品を追加する場合はここに追加
];
