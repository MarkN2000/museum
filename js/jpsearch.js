/**
 * Japan Search API Data Fetcher
 * Fetches artwork metadata from Japan Search JSON API.
 */

const JPSEARCH_API_BASE = "https://jpsearch.go.jp/api/item/";

/**
 * Fetch artwork data from Japan Search.
 * @param {string} itemId - Japan Search item ID (e.g., "tfam_art_db-3628")
 * @returns {Promise<{title: string, widthCm: number, heightCm: number, imageUrl: string}>}
 */
export async function fetchArtworkData(itemId) {
  const apiUrl = `${JPSEARCH_API_BASE}${itemId}`;
  
  try {
    const response = await fetch(apiUrl);
    
    if (!response.ok) {
      throw new Error(`API returned ${response.status}`);
    }
    
    const data = await response.json();
    console.log("API Response:", data);
    return parseApiData(data, itemId);
    
  } catch (e) {
    console.error(`Failed to fetch data for ${itemId}:`, e);
    throw new Error(`データの取得に失敗しました: ${e.message}`);
  }
}

/**
 * Parse data from Japan Search JSON API response.
 */
function parseApiData(data, itemId) {
  // Extract title
  const title = data.common?.title || data.label || itemId;
  
  // Extract image URL (prefer contentsUrl for higher quality, fallback to thumbnail)
  let imageUrl = null;
  if (data.common?.contentsUrl && data.common.contentsUrl.length > 0) {
    imageUrl = data.common.contentsUrl[0];
  } else if (data.common?.thumbnailUrl && data.common.thumbnailUrl.length > 0) {
    imageUrl = data.common.thumbnailUrl[0];
  }
  
  // Extract size by searching all fields for patterns like "24.6 x 36.5 cm"
  let widthCm = null;
  let heightCm = null;
  
  // Recursively search all string values in the response
  const allStrings = getAllStringValues(data);
  
  for (const str of allStrings) {
    const sizeInfo = parseSizeString(str);
    if (sizeInfo) {
      heightCm = sizeInfo.height;
      widthCm = sizeInfo.width;
      console.log(`Found size: ${heightCm} x ${widthCm} cm from: "${str}"`);
      break;
    }
  }
  
  // Validate required fields
  if (!imageUrl) {
    throw new Error(`画像URLが見つかりません (${itemId})`);
  }
  if (widthCm === null || heightCm === null) {
    throw new Error(`サイズ情報が見つかりません (${itemId})`);
  }
  
  return { title, widthCm, heightCm, imageUrl };
}

/**
 * Parse a size string like "24.6 x 36.5 cm" or "24.6×36.5cm"
 * @param {string} str - String to parse
 * @returns {{ height: number, width: number } | null}
 */
function parseSizeString(str) {
  if (typeof str !== 'string') return null;
  
  // Skip URLs and file paths (they contain patterns like 500x500)
  if (str.includes('http') || str.includes('/')) return null;
  
  // Pattern: number x number with REQUIRED unit (cm or mm)
  // This prevents matching URL dimensions like "500x500"
  const pattern = /(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(cm|mm|センチ)/i;
  
  const match = str.match(pattern);
  if (match) {
    let h = parseFloat(match[1]);
    let w = parseFloat(match[2]);
    const unit = match[3].toLowerCase();
    
    // Convert mm to cm if needed
    if (unit === 'mm') {
      h /= 10;
      w /= 10;
    }
    
    // Japanese art prints are often listed as height x width
    return { height: h, width: w };
  }
  
  return null;
}

/**
 * Recursively get all string values from an object.
 * @param {any} obj - Object to search
 * @param {string[]} values - Accumulator array
 * @returns {string[]}
 */
function getAllStringValues(obj, values = []) {
  if (typeof obj === 'string') {
    values.push(obj);
  } else if (Array.isArray(obj)) {
    for (const item of obj) {
      getAllStringValues(item, values);
    }
  } else if (typeof obj === 'object' && obj !== null) {
    for (const key of Object.keys(obj)) {
      getAllStringValues(obj[key], values);
    }
  }
  return values;
}

/**
 * Get a thumbnail URL for a Japan Search item.
 * @param {string} itemId - Japan Search item ID
 * @param {string|null} directUrl - Direct thumbnail URL from presets (optional)
 */
export function getThumbnailUrl(itemId, directUrl = null) {
  if (directUrl) {
    return directUrl;
  }
  // Fallback: Use the Japan Search API thumbnail endpoint
  return `https://jpsearch.go.jp/item/${itemId}/thumbnail`;
}
