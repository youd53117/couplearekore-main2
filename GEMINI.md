# カップルあれこれ（couple-arekore.com）開発・記事作成ガイドライン

このドキュメントは、本リポジトリ（`カップルあれこれ | 公式Webマガジン`）のHTML/CSS構成、Tailwind CSSデザインルール、および記事ページのレイアウト構造をまとめたものです。
今後の記事追加やサイト更新時は、本ガイドラインならびに `knowledge/` 配下のナレッジ・4部署スキル体制に必ず準拠してください。

---

## 0. 4部署体制・強制ワークフローとナレッジ運用ルール

新規記事の作成や記事の大規模改修を行う際は、**必ず以下の4部署スキルを順守（ステップの飛び越し禁止）** し、ナレッジベースを参照しながら進行すること。

### 0.1 ナレッジベース（制作前に必読）
- `knowledge/brand-tone.md`: 既存記事から抽出した文体・HTMLコンポーネント・TikTok連動・黒色CTAボタン仕様書
- `knowledge/ng-rules.md`: 禁止表現・AI構文・HTML/写真/アフィリエイトの過去教訓NG集

### 0.2 強制ワークフロー（4部署連携）
1. **`.agent/skills/01-research/SKILL.md`（第1部署：リサーチ・一次情報収集担当）**
   - テーマ・パターン（A/B/C）・スラッグ確定、最新一次情報（アクセス・営業時間・税込価格・公式URL）収集、楽天「専用ページ」有無判定、Wikimedia Commons 複数画像候補＆TikTok動画ID収集
2. **`.agent/skills/02-writer/SKILL.md`（第2部署：執筆＋TikTok連動構成担当）**
   - `knowledge/brand-tone.md` ＆ `knowledge/ng-rules.md` を読み込み、パターンA/B/C骨格・本文・TikTok連動セクション・`index.html` 追加カード文案を執筆
3. **`.agent/skills/03-affiliate/SKILL.md`（第3部署：アフィリエイト・メディア・CTA整形担当）**
   - 楽天公式ID（`526779c3.02e0dab7.526779c4.c2c3e62b`）自動変換（専用ページ限定）、公式サイトURLフォールバック、黒色CTAボタン統一、Wikimedia Commons 候補の目視厳選＆クレジット付与（またはGoogleマップ/楽天画像フォールバック）、1:1サムネイル生成、`embed.js` 末尾1回統合、`index.html` 反映
4. **`.agent/skills/04-inspector/SKILL.md`（第4部署：公開前の最終検品・表示確認・差し戻し担当）**
   - HTML構文検証、画像目視、黒色ボタン・文言・アフィリエイト規約検証、PC/モバイル表示確認を実施。**1項目でもNGがあれば該当部署へ差し戻し＋再検品を行う**

---

## 1. サイト概要・ファイル構成

- **サイト名**: カップルあれこれ | 公式Webマガジン
- **ドメイン**: `couple-arekore.com`（`CNAME` で設定）
- **構成**: ビルドツール・バンドラーを使用しない静的HTML構成（各ページ単一HTML完結）
- **ディレクトリ構成（フラット構成）**:
  - `index.html`: トップページ（Hero、GIFT一覧、DATE一覧、TikTok動画エリア）
  - `article-*.html`: 各記事ページ（例: `article-perfume5.html`, `article-tokyo.html`）
  - 画像ファイル（`.jpg` / `.jpeg` / `.png`）: **ルート直下に配置**し、HTMLからは相対パス（例: `src="shibuyasky.jpeg"`）で参照する。
    - ※新規追加する画像は、URLエンコードやパス問題を避けるため、可能な限り半角英数字・ハイフン（`-`）のファイル名にしてルート直下へ配置すること。
    - ※**著作権クリア・写真品質ルール**: 新規記事の本文内および `index.html` の一覧サムネイルには、ログイン制限のあるInstagram埋め込みを使わず、**Wikimedia Commons（ウィキメディア・コモンズ）から著作権フリーの実物写真を複数候補比較・目視確認して自動取得・ローカル保存し、`<img>` 表示する**ことを基本とする（CC BY / CC BY-SA 等クレジット表記が必要な場合は、画像直下のキャプションに著者名・ライセンスを小さく明記する）。写真は「その施設の象徴的な外観や建築全体がしっかり映っており、一目でその施設・商品だと分かる映える構図」のみを採用し、床・デッキの一部や看板のアップ、判別しづらい遠景写真はNGとする。適切な写真が見つからないスポットのみ、Googleマップ公式埋め込み（`<iframe>`）または楽天アフィリエイト画像枠を配置する。

---

## 2. 技術スタック・共通 `<head>` 設定

すべてのHTMLファイルで以下のCDNおよび `tailwind.config` を共通で使用する。

### 2.1 読み込みライブラリ
1. **Tailwind CSS (Play CDN)**: `https://cdn.tailwindcss.com`
2. **Google Fonts**:
   - `Cormorant Garamond` (italic, 400 / regular, 400)
   - `Kiwi Maru` (400, 500)
   - `Noto Serif JP` (300, 400, 500, 600, 700)
   - `Zen Kaku Gothic New` (300, 400, 500, 700)
3. **FontAwesome (v6.4.0)**: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css`

### 2.2 Tailwind CSS デザインルール (`tailwind.config`)
`<head>` 内に必ず以下の設定を記述する。

```javascript
tailwind.config = {
    theme: {
        extend: {
            fontFamily: {
                sans: ['"Zen Kaku Gothic New"', 'sans-serif'],
                serif: ['"Noto Serif JP"', 'serif'],
                english: ['"Cormorant Garamond"', 'serif'],
                title: ['"Kiwi Maru"', 'serif'],
            },
            colors: {
                black: '#111111',
                gray: {
                    50: '#fafafa',
                    100: '#f5f5f5',
                    900: '#1a1a1a',
                }
            }
        }
    }
}
```

### 2.3 カラー・タイポグラフィ使い分け
- **ベース背景**: `bg-gray-50` (`#fafafa`)
- **カード・コンテンツ背景**: `bg-white`（内側の画像背景や補足ボックスには `bg-gray-100` / `bg-gray-50`）
- **基本文字色**: `text-black` (`#111111`)、本文は `text-gray-700` または `text-gray-600`、注釈は `text-gray-400`
- **テキスト選択色**: `selection:bg-black selection:text-white`
- **アクセントカラー・CTAカラー**:
  - 価格表示には `#bf0000`（`text-[#bf0000]`）を使用
  - **詳細ボタン（「この施設の詳細を見る」「この商品の詳細を見る」）・公式サイトリンク・汎用CTAは、リンク先が楽天アフィリエイトか公式サイトかに関わらず、すべてサイトの基本カラーである黒（`#111111` ベース: `bg-black hover:bg-gray-800` または `border-2 border-black hover:bg-black hover:text-white`）に統一する。赤色など別の色に分けることは禁止**
- **フォント使い分け**:
  - `font-title` (`Kiwi Maru`): サイトロゴ「カップルあれこれ」専用
  - `font-english` (`Cormorant Garamond`): ナビゲーション、英字セクション見出し（`italic`）、英字カテゴリバッジ、コピーライト
  - `font-serif` (`Noto Serif JP`): 記事タイトル（`h1`）、セクション見出し（`h2` / `h3`）、日付メタ情報
  - `font-sans` (`Zen Kaku Gothic New`): 本文、カード内見出し、ボタン、注釈（`body` のデフォルト）

### 2.4 カスタムCSS (`<style>`)
```css
html { scroll-behavior: smooth; }
.fade-in { animation: fadeIn 1.2s cubic-bezier(0.4, 0, 0.2, 1) forwards; opacity: 0; transform: translateY(20px); }
.delay-1 { animation-delay: 0.3s; }
.delay-2 { animation-delay: 0.6s; }
@keyframes fadeIn {
    to { opacity: 1; transform: translateY(0); }
}
.img-zoom { transition: transform 0.6s ease; }
.group:hover .img-zoom { transform: scale(1.05); }

.reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease-out;
}
.reveal.active {
    opacity: 1;
    transform: translateY(0);
}
```
> **注意**: `.reveal` クラスを要素に付与する場合は、必ずページ末尾に `.reveal` を `.active` に切り替えるスクロール監視用 `<script>` を配置すること（配置しない場合、要素が `opacity: 0` のまま非表示になる）。

---

## 3. 共通パーツ仕様

### 3.1 `<body>` ベースクラス
```html
<body class="bg-gray-50 text-black font-sans antialiased selection:bg-black selection:text-white">
```

### 3.2 ナビゲーションバー (`<nav>`)
全ページ上部に `sticky top-0 z-50` で固定配置する。
- 背景・枠線: `bg-white/90 backdrop-blur-md border-b border-gray-100 py-3 md:py-4 shadow-sm`
- コンテナ: `max-w-5xl mx-auto px-4 md:px-6 flex justify-between items-center`
- 左（ロゴ）: `font-title font-medium text-sm md:text-xl tracking-wide`
  - トップページは `href="#"`、記事ページは `href="index.html"`
- 中央（メニュー）: `flex gap-3 md:gap-8 text-[10px] md:text-sm tracking-widest font-english`
  - `GIFT` (`index.html#gift`), `DATE` (`index.html#date`), `TIPS` (`index.html#tips`)
- 右（SNS）: TikTok公式アカウント (`https://www.tiktok.com/@couplearekore`, `target="_blank"`)

### 3.3 PR表記
アフィリエイトリンクや紹介記事を含む場合は、ヘッダー直下に必ず明記する。
- ギフト系記事: `<p class="text-[10px] md:text-xs text-gray-400">※本記事にはアフィリエイト広告（PR）が含まれています。</p>`
- デートスポット系記事: `<p class="text-xs text-gray-400 text-center mb-8">※本ページはプロモーションが含まれています</p>`

### 3.4 フッター (`<footer>`)
- **まとめ系記事ページ（標準）**:
  ```html
  <footer class="bg-white border-t border-gray-200 py-10 md:py-12 mt-10 md:mt-12 text-center">
      <p class="text-gray-400 text-xs md:text-sm font-serif">&copy; 2026 カップルあれこれ</p>
  </footer>
  ```
- **トップページ（`index.html`）・ブランド紹介強めの記事（`article-aliba.html`）**:
  `bg-black text-white` のダークフッターを使用。

---

## 4. 記事ページのレイアウト構造（3パターン）

新規記事を作成する際は、内容に応じて以下の3パターンのいずれかを選択する。

### 4.1 記事内メディア＆CTAリンクの基本方針（全パターン共通）
- **ハイブリッド画像選定ルール（建物外観のフリー素材は全面禁止）**:
  - スポット・グルメ・ホテル記事の画像は以下の優先順位で必ず実装する。**単なるホテルや建物の外観写真（Wikimedia Commons等）をメイン画像に使うことは一切禁止**する：
    1. **第1優先（ユーザーからInstagram投稿URLの指定がある場合）**:
       指定されたURLをInstagram公式埋め込みコード（`blockquote.instagram-media` + `https://www.instagram.com/embed.js`）として記事内に配置する（※ユーザー指定がない場合のみ次の優先順位へ進む）。
    2. **第2優先（URL指定がなく、楽天トラベル掲載ホテル内のレストラン・施設の場合）**:
       楽天トラベルの該当施設ページから「食事・レストラン・コース料理・ラウンジ内観」の公式画像URLを取得し、公式楽天アフィリエイトID（`526779c3.02e0dab7.526779c4.c2c3e62b`）を経由した**アフィリエイトリンク付き画像**として表示する。
    3. **第3優先（上記で料理・内観画像が取得できない場合）**:
       その店舗の料理ジャンルや空間ムード（鉄板焼きのステーキ調理シーン、ホテル最上階バーの夜景とカクテル、記念日コース料理など）が直感的に伝わる高画質な料理・内観イメージ写真（Unsplash等）を配置する。さらに、黒CTAボタンの直上に **「📸 Instagramで実際の料理・店内写真を見る」**（Instagramの店名タグ検索等へのリンク）ボタンと、店舗情報枠への **Googleマップ埋め込み（`<iframe>`）** を必ずセットで配置する。
  - ※商品・ギフト記事（パターンA/C）やエリア代表サムネイルで、楽天画像等が使えない場合のみ著作権クリアの実物写真（Wikimedia Commons等）を使用する。
- **楽天アフィリエイトリンク自動生成ルール（適用条件の厳格化）**:
  - **公式楽天アフィリエイトID（`hgc/` の後ろの文字列）**: `526779c3.02e0dab7.526779c4.c2c3e62b`
  - **変換対象は「専用ページが存在する場合」のみに限定**:
    - 楽天市場の該当商品ページ、楽天トラベル観光体験のチケットページ（例: YOKOHAMA AIR CABIN）、宿泊施設そのものの予約ページなど、**その施設・商品そのものの専用ページが楽天に存在する場合のみ**、生のURLではなく上記IDを使った**URLエンコード済み楽天アフィリエイトリンク形式**へ自動変換して組み込む：
      ```text
      https://hb.afl.rakuten.co.jp/hgc/526779c3.02e0dab7.526779c4.c2c3e62b/?pc=<URLエンコード済みの対象URL>
      ```
    - **検索結果・周辺ホテル一覧ページの禁止**: 赤レンガ倉庫のように、楽天側にその施設専用の体験・予約ページがなく、周辺ホテルの検索結果一覧ページ（`travel.rakuten.co.jp/yado/spot/...` 等）や検索一覧になってしまうケースでは、無理に楽天アフィリエイトを使わず、**必ずその施設の公式サイトURLをそのまま設定する**。
- **詳細ボタンの文言・デザイン（黒色）の完全統一**:
  - リンク先が楽天アフィリエイトであっても公式サイトであっても、ボタンの表示テキストおよびカラーデザインは**必ず以下に完全統一する（赤色などへの色分け禁止）**：
    - **表示テキスト**:
      - デートスポット・施設記事（パターンB）: `この施設の詳細を見る`
      - 商品・ギフト記事（パターンA / C）: `この商品の詳細を見る`
    - **ボタンデザイン（黒 `#111111` ベース統一）**:
      - `block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg`

### パターンA: ギフト・アイテムまとめ型（標準リファレンス: `article-perfume5.html`）
複数アイテム（5選など）をカード形式で紹介するレイアウト。

1. **記事ヘッダー (`<header class="max-w-4xl mx-auto px-6 pt-10 md:pt-12 pb-6 md:pb-8 text-center">`)**
   - カテゴリバッジ: `text-[10px] md:text-xs border border-black text-black px-3 py-1 tracking-wider inline-block mb-4 md:mb-6`（例: `GIFT & PRESENT`）
   - タイトル `<h1>`: `font-serif text-xl md:text-4xl font-semibold leading-tight mb-4`
   - メタ情報: 年月 / サブカテゴリ（例: `2026.09 / Fragrance & Beauty`）
2. **PR表記**
3. **メインカラム (`<main class="max-w-3xl mx-auto px-5 md:px-6 pb-20 md:pb-24">`)**
   - **導入文**: `mb-10 md:mb-12 space-y-3 md:space-y-4`（`text-sm md:text-base text-gray-700 leading-relaxed`）
   - **アイテムカード一覧**: `space-y-12 md:space-y-16`
     - カード外枠: `bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm`
     - メディアエリア: Wikimedia Commons から取得した実物写真 `<img>`（必要時は直下にクレジット表記）、または楽天アフィリエイト画像枠
     - テキストエリア (`p-5 md:p-8`):
       - キャッチバッジ: `bg-black text-white text-[9px] md:text-[10px] tracking-wider font-bold px-2 py-1 rounded-sm mb-3 inline-block`
       - 商品名 `<h2>`: `font-bold text-lg md:text-2xl mb-2`
       - 価格表示: `font-bold text-[#bf0000] text-sm md:text-base mb-4`
       - 説明文: `text-sm md:text-base text-gray-700 leading-relaxed mb-6`
       - CTAボタン（**専用ページがある場合は楽天アフィリエイト優先・周辺検索一覧は禁止、ボタン色・文言は黒「この商品の詳細を見る」で完全統一**）:
         - `block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg`
   - **（任意）関連SNSまとめカード**: `mt-20 bg-white p-6 md:p-8 rounded-xl border border-gray-200 shadow-sm text-center`
   - **「記事一覧に戻る」ボタン**: `mt-12 md:mt-16 text-center` 内に `href="index.html"` のアウトラインボタン

### パターンB: デートスポットランキング型（標準リファレンス: `article-tokyo.html`, `article-nagoya.html`, `article-yokohama.html`）
地域別のデートスポットをランキング形式で紹介するレイアウト。

1. **メインカラム (`<main class="max-w-3xl mx-auto px-6 py-12 fade-in">`)**
   - **タイトルエリア (`mb-12 text-center`)**:
     - カテゴリバッジ: `inline-block border border-black px-3 py-1 text-xs tracking-widest mb-4 font-english`（`DATE SPOT`）
     - タイトル `<h1>`: `text-2xl md:text-4xl font-bold mb-4 leading-snug font-serif`
     - 導入文: `text-gray-600 text-xs md:text-sm leading-relaxed mb-2`
     - PR表記
   - **スポットカード (`mb-12 bg-white rounded-xl shadow-sm overflow-hidden reveal`)**:
     - メディアエリア:
       - (1) Wikimedia Commons から取得した実物写真 `<img>`（`w-full h-64 md:h-96 object-cover bg-gray-100` または `object-contain bg-gray-100`）＋必要なクレジット表記（`<p class="text-[11px] text-gray-400 text-right px-6 pt-2">写真：著者名 / Wikimedia Commons (ライセンス)</p>`）
       - (2) 写真が見つからない場合は Googleマップ公式埋め込み（`<iframe ...>`）
     - 本文エリア (`p-6 md:p-8`):
       - 順位・キャッチバッジ: `inline-block bg-black text-white text-xs font-bold px-3 py-1 rounded-sm mb-4`
       - スポット名 `<h3>`: `text-2xl font-bold mb-4 font-serif`
       - 説明文: `text-gray-600 leading-relaxed mb-6`
       - CTAボタン（**文言「この施設の詳細を見る」・黒色デザインで完全統一**）:
         - リンク先（楽天専用ページまたは公式サイト）に関わらず: `block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg`
2. **スクロールアニメーション用JS**: ページ末尾に `.reveal` 監視スクリプトを配置。

### パターンC: 単体アイテム深掘りレビュー型（リファレンス: `article-aliba.html`）
1つの商品を詳しく解説するレビュー記事向けレイアウト。

- 構成順: `header`（`REVIEW` バッジ + `h1` + 年月/カテゴリ） → PR表記 → メディアエリア（Wikimedia Commons実物写真または楽天アフィリエイト画像枠） → リード文 → 番号付き `h2` セクション（`border-b-2 border-black pb-2 inline-block`） → 特徴リスト（`bg-gray-100 rounded p-6`） → スペック＆Q&Aカード（`rounded-xl border border-gray-200`） → まとめ＆CTAボックス（`bg-gray-100 p-8 text-center`、自動変換した楽天アフィリエイトURL優先・ボタン文言「この商品の詳細を見る」）。

---

## 5. トップページ (`index.html`) への記事追加ルール

新しい記事を公開したら、`index.html` の該当セクションへリンクカードを追加する。

### 5.1 GIFT記事を追加する場合 (`#gift` 内の `space-y-12`)
横長カード（PC時は画像2/5・テキスト3/5の2カラム、スマホ時は縦積み）を追加する。
```html
<article class="bg-white p-6 md:p-8 border border-gray-200 flex flex-col md:flex-row gap-8 items-center shadow-sm">
    <div class="w-full md:w-2/5 overflow-hidden relative rounded-xl">
        <img src="サムネイル画像" alt="記事タイトル" class="w-full h-auto object-cover hover:scale-105 transition duration-500">
    </div>
    <div class="w-full md:w-3/5 space-y-4">
        <span class="text-xs border border-black text-black px-3 py-1 tracking-wider inline-block">GIFT & PRESENT</span>
        <h4 class="font-serif text-xl md:text-2xl font-semibold leading-relaxed">
            記事タイトル
        </h4>
        <p class="text-sm text-gray-600 leading-relaxed">
            記事の要約文
        </p>
        <div class="pt-4">
            <a href="article-xxx.html" class="inline-block border border-black hover:bg-black hover:text-white text-black transition px-6 py-2 text-sm font-semibold">
                記事を読む <i class="fa-solid fa-arrow-right ml-1"></i>
            </a>
        </div>
    </div>
</article>
```

### 5.2 DATE記事を追加する場合 (`#date` 内の `grid grid-cols-1 md:grid-cols-3 gap-6`)
正方形（`aspect-square`）のオーバーレイカードを追加する。
```html
<a href="article-xxx.html" class="group block relative overflow-hidden aspect-square">
    <img src="エリア画像" class="w-full h-full object-cover img-zoom brightness-75 group-hover:brightness-50 transition" alt="エリア名">
    <div class="absolute inset-0 flex flex-col items-center justify-center text-white text-center">
        <span class="font-english text-sm tracking-widest mb-1 border-b border-white pb-1">AREA NAME</span>
        <h3 class="font-serif text-lg md:text-xl font-semibold">日本語タイトル</h3>
    </div>
</a>
```

---

## 6. 開発・更新時の禁止事項と品質チェックリスト

過去の実装で見られた不具合を再発させないため、新規作成・編集時は以下を必ず確認すること。

1. **HTMLタグの開閉整合性**
   - `</header>`、`</h1>`、`</div>` の重複や閉じ忘れ、`<main>` の二重ネストを作らないこと。
   - `index.html` の `<html>` タグを先頭行で即閉じしないこと。
2. **メタ情報の更新**
   - 記事ごとに固有の `<title>記事タイトル | カップルあれこれ 公式Webマガジン</title>` と `<meta name="description" content="...">` を設定すること（テンプレートの使い回しによるタイトル未変更を防ぐ）。
3. **SNS埋め込みスクリプトの重複禁止**
   - TikTok等の埋め込みコードを貼る際は `<blockquote>...</blockquote>` のみを配置し、`<script async src="https://www.tiktok.com/embed.js"></script>` は **ページ末尾に1回だけ** 記述する（ログイン制限のあるInstagram埋め込みは新規記事には使用しない）。
4. **モバイル（スマホ）での改行・文字サイズ最適化**
   - タイトルやリード文でスマホ幅のみ改行したい場合は `<br class="block md:hidden">`、PC幅のみ改行したい場合は `<br class="hidden md:block">` を使い、不自然な途中改行を防ぐ。
   - レスポンシブクラス（`text-sm md:text-base`, `p-5 md:p-8` 等）を適切に指定する。
5. **メディア・リンク・文言の確認**
   - `alt` 属性に画像の内容を簡潔に記載する。
   - 外部リンク・アフィリエイトリンクには `target="_blank"` を付与する。
   - 記事内の写真および `index.html` サムネイルは、原則 Wikimedia Commons から著作権フリーの実物写真を複数候補比較・目視確認のうえで（「象徴的な外観や建築全体が映え、一目で施設・商品だと分かる構図」のみ採用し、床・デッキの一部や看板アップ、判別しづらい遠景はNG）ローカル保存して `<img>` 表示する（CC BY / CC BY-SA 等は画像直下に著者名・ライセンスを小さく明記。見つからない場合のみ Googleマップ公式埋め込み `<iframe>` または楽天アフィリエイト画像枠を使用）。
   - 楽天アフィリエイトリンク（`https://hb.afl.rakuten.co.jp/hgc/526779c3.02e0dab7.526779c4.c2c3e62b/?pc=<URLエンコード済みURL>`）は、その施設・商品そのものの**専用ページが楽天に存在する場合のみ**使用し、周辺ホテル一覧や検索結果ページしか存在しない場合は必ず公式サイトURLを設定する。
   - 詳細ボタンの表示テキストと色は、リンク先に関わらず **施設記事は「この施設の詳細を見る」・商品記事は「この商品の詳細を見る」**、カラーは **すべて黒（`#111111`ベース `bg-black hover:bg-gray-800`）** で完全統一する（赤色等への色分け禁止）。

---

## 7. 検品差し戻し・NG集自動追記＆完了報告ルール

- `04-inspector` での最終検品において差し戻しが発生した場合、またはユーザーから記事の表現・写真構図・リンク・HTML構造・デザインに関する修正指摘を受けた場合は、**修正作業とあわせて必ず `knowledge/ng-rules.md` の「過去教訓ログ」へ原因・NG例・正解ルールを自動追記する**こと。
- 次回以降の記事制作では `01-research`〜`04-inspector` 全部署が最新の `knowledge/ng-rules.md` を読み込むことで、同じ指摘・不具合の再発をゼロにする。
- **完了報告時のプレビューリンク提示ルール（必須）**:
  今後のすべての作業（PCのAsk anythingからの指示・LINEからの遠隔指示のどちらであっても）において、記事の新規作成や既存HTMLの修正が完了した際は、**報告メッセージの【一番最後】に必ず以下の形式で「ワンクリックで確認できるプレビューリンク」を明記する**こと（`.preview_url.txt` の内容を先頭に付与し、URLは必ず `http://` または `https://` から始まる完全なリンク形式で出力すること。`file://` パスのみの記載は禁止）。

  ```markdown
  ---
  👀 **現段階のサイトプレビュー（ワンクリック確認）**
  - Mac・Antigravity内蔵ブラウザ用： http://127.0.0.1:8787/preview/{対象HTMLファイル名}
  - スマホ・LINE遠隔確認用： {.preview_url.txtの中身}/preview/{対象HTMLファイル名}
  - 本番公開URL（GitHub push後に反映）： https://couple-arekore.com/{対象HTMLファイル名}
  ```

## LINE経由の新規記事作成・2段階承認ルール
LINEから新規記事のテーマや企画依頼を受けた場合、**いきなりHTMLファイルの作成や編集を行わないこと**。必ず以下の2段階で進行すること。

1. **第1段階（企画・構成の提案と待機）：**
   - まず「タイトル案（3パターン）」「記事の対象読者・切り口」「見出し構成案（H2・H3一覧と掲載スポット・商品候補）」のみを作成し、LINEの返信テキストとして出力してユーザーに確認を求める。
   - この時点ではファイルの新規作成・変更・`git push` は一切行わず、ユーザーの承認返信を待つこと。
2. **第2段階（承認後の執筆・実装）：**
   - ユーザーから「OK」「2番で進めて」などの承認指示が返ってきたら、`create-article` スキルおよび統一デザイン仕様（黒背景・白文字の「施設の詳細を見る」ボタン、著作権配慮、楽天アフィリエイト形式）に従ってHTML記事の執筆・実装を実行し、完了報告を返信する。

---

## 本番公開（GitHub Pages反映）ワークフロー

1. 記事の新規作成・修正の段階では、**絶対に自動で `git push` を行わないこと**（必ずプレビュー確認の承認を待つ）。
2. ユーザーから「本番公開して」「GitHubにpushして」「公開OK」などの明示的な公開指示を受けた場合のみ、リポジトリルート（`/Users/watanabetasuku/Desktop/couplearekore-main` 等）で以下を順番に実行すること：
   - `git status` で変更ファイル（新規記事HTML、更新された `index.html`、画像等）を確認
   - 関係ない一時ファイル（`.preview_url.txt` 等）が含まれていれば `.gitignore` に追記して除外
   - `git add -A && git commit -m "Add/Update: {記事タイトルまたは変更内容の要約}" && git push origin main` を実行
3. `git push` が正常終了（終了コード0）したことを確認したうえで、完了報告に「本番公開完了」と、実際の公開URL（`https://couple-arekore.com/{対象HTMLファイル名}` および `https://couple-arekore.com/`）を必ず明記すること。
