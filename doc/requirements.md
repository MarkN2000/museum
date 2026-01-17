# Requirements Document: Japan Search AR Viewer

WebXRを使用して、ジャパンサーチのIIIFデータを利用した絵画AR表示アプリケーションの要件定義です。

## 1. Project Overview
- **Goal**: ウェブサイトに埋め込み可能なARコンテンツを作成し、スマホを通して絵画を実寸大で空間に配置・鑑賞できる体験を提供する。
- **Source**: ジャパンサーチ (IIIF manifest) から画像と寸法データを取得。

## 2. Target Devices
- **Priority**: iPhone (iOS 15+ WebXR/ModelViewer via QuickLook/WebAR ecosystem), Android (Chrome).
- **Secondary**: Oculus Quest, PC Browsers (2D fallback or emulator).
- **Tech Stack**: WebXR (Three.js / A-Frame / model-viewer / ar.js etc - TBD).

## 3. User Flow

### Phase 1: Selection (2D UI)
1. **Landing Page**: 
   - タイトルと簡単な説明。
   - 表示する作品を選択するUI。
2. **Selection Methods**:
   - **Presets**: 事前に設定された有名な絵画リストから選択。
   - **Search**: ジャパンサーチAPIを利用してキーワード検索し、IIIF対応コンテンツを選択。
3. **Transition**: 作品決定後、「ARで見る」ボタンでWebXRモードへ移行。

### Phase 2: AR Experience (3D/Camera View)
1. **AR Session Start**: カメラ権限の承認。
2. **Placement**:
   - ユーザーは空間内の配置したい場所（壁面など）を認識させる。
   - **Placement Strategy**: 
     - 壁面認識 (Vertical Plane Detection) が理想。
     - 難しい場合は、自分の前方の空中に浮かせる or ヒットテストで配置位置を指定。
3. **Rendering**:
   - IIIFマニフェストから取得した実際の縦横寸法 (`width`, `height` in real world units) に基づき、正確なスケールでプレーン（板状オブジェクト）を生成。
   - テクスチャとして高解像度画像を貼り付け。
4. **Interaction**:
   - 配置後の位置調整（移動、回転）。
   - 作品情報の表示（タップでキャプション表示など）。

## 4. Technical Requirements
- **IIIF Integration**: 
  - メタデータから実際の寸法（mm/cm）を取得できるか確認が必要。寸法データがない場合はデフォルト値またはユーザー入力で補完。
  - 画像はタイル画像ではなく、適度なサイズの画像を生成してテクスチャとして利用（IIIF Image API）。
- **AR Framework**: 
  - WebXR Hit Test API (for transparency/placement).
  - フォールバックとして `model-viewer` (Google) のARモードも検討（実装が容易だがカスタマイズに制限あり）。

## 5. Potential Challenges
- **Scale Data**: ジャパンサーチのすべてのIIIFデータに正確な物理サイズメタデータが含まれているとは限らない。
- **Browser Compatibility**: iOS SafariでのWebXRサポート状況（WebXRはまだ実験的な場合があるため、MozillaのWebXR Viewerや、`model-viewer` のQuickLook/SceneViewer連携が必要になる可能性が高い）。

## 6. Next Steps
- 技術選定（特にiOS対応のアプローチ）。
- `architecture.md` の更新。
