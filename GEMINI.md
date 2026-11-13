# カップルあれこれ（couple-arekore.com）開発・記事作成ガイドライン

このドキュメントは、本リポジトリ（`カップルあれこれ | 公式Webマガジン`）のHTML/CSS構成、Tailwind CSSデザインルール、および記事ページのレイアウト構造をまとめたものです。
今後の記事追加やサイト更新時は、本ガイドラインに準拠してください。

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
- **メディア（写真）の自動取得と品質・表示ルール（著作権クリア）**:
  - ログイン制限のある Instagram 埋め込みは使用しない。
  - 以下の優先順位でエージェントが自動取得・配置する：
    1. **Wikimedia Commons（ウィキメディア・コモンズ）** から該当スポット・商品の著作権フリー実物写真を検索し、**必ず複数候補を目視確認したうえで、「その施設の象徴的な外観や建築全体がしっかり映っていて、読者がパッと見た瞬間に『あ、この施設だ』と一目で分かる映える構図の写真」だけを厳選**し、ルート直下にローカル保存して通常の `<img>` として表示する（CC BY / CC BY-SA 等クレジット表記が必要な場合は、画像直下に小さく `text-[11px] text-gray-400 text-right px-6 pt-2` で著者・ライセンス・出典を記載する）。
       - **NG例**: デッキや床・壁の一部だけの切り取り、看板や案内板のみのアップ、遠くから小さくしか映っていない判別しづらい構図。
    2. 適切な写真が見つからない場合は、そのスポットの **Googleマップ公式埋め込み（`<iframe>`）** または **楽天アフィリエイト画像枠** を配置する。
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
