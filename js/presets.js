/**
 * Preset artworks for the selection screen.
 * Each entry contains:
 * - id: Japan Search item ID (used to fetch metadata)
 * - label: Display name (fallback if fetch fails)
 * - thumbnailUrl: Direct thumbnail URL (for faster loading on selection screen)
 * - textureUrl: CORS-friendly image URL for AR texture (optional override)
 * - widthCm, heightCm: Override size if API doesn't provide it
 */
export const PRESET_ARTWORKS = [
  {
    id: "tfam_art_db-3628",
    label: "冨嶽三十六景 神奈川沖浪裏",
    thumbnailUrl: "https://www.fujibi.or.jp/assets/images/collection/thumb_c/thumb_c_03628.jpg",
    // Use ArtsMIA's version of the same artwork (CORS-friendly)
    textureUrl: "https://0.api.artsmia.org/800/62742.jpg",
    widthCm: 36.5,
    heightCm: 24.6
  },
  {
    id: "cobas_i8232-8232_I00001_2",
    label: "見返り美人図",
    thumbnailUrl: null, // Will be fetched from API
    textureUrl: null,   // Will be fetched from API
    widthCm: null,
    heightCm: null
  },
  {
    id: "C0004228",
    label: "風神雷神図屏風",
    thumbnailUrl: null,
    textureUrl: null,
    widthCm: null,
    heightCm: null
  }
];
