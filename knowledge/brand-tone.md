# ブランドトーン・HTMLコンポーネント・CTA仕様書（brand-tone.md）

本ファイルは、`index.html` および既存記事群（`article-perfume5.html`, `article-tokyo.html`, `article-nagoya.html`, `article-kansai.html`, `article-aliba.html`, `article-gift5.html`, `article-girlfriend-gift5.html`, `article-yokohama.html`）から抽出した **文体・レイアウトコンポーネント・TikTok連動・CTAボタン仕様** の公式リファレンスです。

---

## 1. ブランドアイデンティティ & 文体（トーン＆マナー）

- **媒体名**: カップルあれこれ | 公式Webマガジン（`couple-arekore.com` / TikTok `@couplearekore`）
- **タグライン**: `Make every moment special.` / `2人の毎日を、もっと特別に。`
- **基本スタンス**:
  - ミニマルで大人っぽいモノトーンデザインの中に、カップル読者が親しみやすい温度感のある語り口を乗せる「Webマガジン調」。
  - TikTok動画（`@couplearekore`）の視聴者が「保存したアイテムの詳細・最新価格・行き方」を確認しに来る導線を意識する。
- **文体の基準（パターン別）**:
  - **ギフト記事（パターンA）**:
    - です・ます調（「〜ですよね」「〜に最適です」「〜が一品です」）。
    - **導入**: 悩みに寄り添い（「大切な人へのプレゼントだからこそ〜」）、選定軸と「最新の国内正規価格でまとめている」旨を簡潔に伝える。
    - **本文**: 香り・質感・デザイン・高見えポイント・どんなシーンや相手に贈ると喜ばれるかを3〜4文（120〜180文字前後）で具体的に書く。
  - **デート記事（パターンB）**:
    - です・ます調を基本に、軽快でワクワク感のある表現（一部親しみやすい感嘆や具体体験フレーズは可。ただし過剰な絵文字連打は避ける）。
    - **導入**: 季節・週末・雨の日・エリアの雰囲気に触れ、読者の利用シーンを提示。
    - **本文**: 見どころ・カップルでの過ごし方＋`<br><br>` のあとに **`・アクセス：...` / `・営業時間：...` / `・料金：...`** の箇条書きを添え、すぐ出かけられる実用性を担保する。
  - **単体レビュー記事（パターンC）**:
    - キャッチコピー（短いワンフレーズ）＋読者の悩み共感リード＋番号付き見出し（`1. 〜`、`2. 〜`）による深掘り解説＋特徴ボックス＋スペック一覧＋Q&A＋背中を押すまとめ。

---

## 2. 共通デザインシステム（`<head>`・タイポグラフィ・パーツ）

### 2.1 `<head>` 共通テンプレート
新規記事は必ず以下をベースにし、`<title>` と `<meta name="description">` のみを記事固有に差し替える。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【記事タイトル】 | カップルあれこれ 公式Webマガジン</title>
    <meta name="description" content="【記事固有のディスクリプション】">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;1,400&family=Kiwi+Maru:wght@400;500&family=Noto+Serif+JP:wght@300;400;500;600;700&family=Zen+Kaku+Gothic+New:wght@300;400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script>
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
    </script>
    <style>
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
    </style>
</head>
<body class="bg-gray-50 text-black font-sans antialiased selection:bg-black selection:text-white">
```

### 2.2 フォント・カラー使い分け表
| 用途 | クラス / カラーコード | 備考 |
| :--- | :--- | :--- |
| サイトロゴ | `font-title` (`Kiwi Maru`) | 「カップルあれこれ」専用 |
| 英字ナビ・バッジ・コピーライト | `font-english` (`Cormorant Garamond`) | セクション見出しは `italic` |
| `h1` / `h2` / `h3` / 年月メタ | `font-serif` (`Noto Serif JP`) | 和文見出しの品格を担保 |
| 本文・ボタン・注釈 | `font-sans` (`Zen Kaku Gothic New`) | `body` デフォルト |
| ページ背景 / カード背景 | `bg-gray-50` (`#fafafa`) / `bg-white` | 画像余白や補足枠は `bg-gray-100` |
| **価格表示のみ** | `text-[#bf0000]` | **CTAボタンでの赤色使用は禁止** |
| **詳細CTAボタン（全記事共通）** | `bg-black hover:bg-gray-800 text-white` | リンク先が楽天・公式問わず黒 `#111111` ベース統一 |

### 2.3 共通パーツ（ナビゲーション・PR表記・フッター）
- **ナビゲーションバー**:
```html
<nav class="sticky top-0 z-50 bg-white/90 backdrop-blur-md border-b border-gray-100 py-3 md:py-4 shadow-sm">
    <div class="max-w-5xl mx-auto px-4 md:px-6 flex justify-between items-center">
        <a href="index.html" class="font-title font-medium text-sm md:text-xl tracking-wide whitespace-nowrap">カップルあれこれ</a>
        <div class="flex gap-3 md:gap-8 text-[10px] md:text-sm tracking-widest font-english">
            <a href="index.html#gift" class="hover:text-gray-500 transition">GIFT</a>
            <a href="index.html#date" class="hover:text-gray-500 transition">DATE</a>
            <a href="index.html#tips" class="hover:text-gray-500 transition">TIPS</a>
        </div>
        <a href="https://www.tiktok.com/@couplearekore" target="_blank" rel="noopener noreferrer" class="text-xs md:text-sm tracking-wider hover:opacity-70 transition flex items-center gap-1.5 font-sans">
            <i class="fa-brands fa-tiktok text-sm md:text-base"></i> <span class="hidden md:inline">公式アカウント</span>
        </a>
    </div>
</nav>
```
- **PR表記**:
  - ギフト・レビュー系（パターンA/C）: `<p class="text-[10px] md:text-xs text-gray-400">※本記事にはアフィリエイト広告（PR）が含まれています。</p>`
  - デート系（パターンB）: `<p class="text-xs text-gray-400 text-center mb-8">※本ページはプロモーションが含まれています</p>`
- **フッター**:
  - 標準まとめ記事（パターンA/B）:
    ```html
    <footer class="bg-white border-t border-gray-200 py-10 md:py-12 mt-10 md:mt-12 text-center">
        <p class="text-gray-400 text-xs md:text-sm font-serif">&copy; 2026 カップルあれこれ</p>
    </footer>
    ```
  - 単体ブランドレビュー（パターンC）: `<footer class="bg-black text-white py-12 text-center">...</footer>`

---

## 3. パターン別HTMLコンポーネント仕様

### 3.1 パターンA（ギフト・アイテムまとめ型 / 参考: `article-perfume5.html`）
- ヘッダー: `GIFT & PRESENT` バッジ + `font-serif text-xl md:text-4xl` `<h1>` + 年月/サブカテゴリ
- カード（`bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm`）:
  - メディア: Wikimedia Commons 実物写真（必要時はクレジット）または楽天アフィリエイト画像枠
  - キャッチバッジ: `bg-black text-white text-[9px] md:text-[10px] tracking-wider font-bold px-2 py-1 rounded-sm mb-3 inline-block`
  - 商品名 `<h2>`: `font-bold text-lg md:text-2xl mb-2`（例: `01. ブランド名 / 商品名`）
  - 価格表示: `font-bold text-[#bf0000] text-sm md:text-base mb-4`（例: `最新価格：約○,○○○円（税込）〜`）
  - 説明文: `text-sm md:text-base text-gray-700 leading-relaxed mb-6`
  - **統一CTAボタン**:
    ```html
    <a href="URL" target="_blank" rel="noopener noreferrer" class="block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg">
        この商品の詳細を見る <i class="fa-solid fa-arrow-up-right-from-square ml-2"></i>
    </a>
    ```

### 3.2 パターンB（デートスポットランキング型 / 参考: `article-yokohama.html`, `article-tokyo.html`, `article-nagoya.html`）
- タイトルエリア: `DATE SPOT` バッジ (`font-english`) + `font-serif text-2xl md:text-4xl font-bold` `<h1>` + 導入文 + PR表記
- スポットカード（`mb-12 bg-white rounded-xl shadow-sm overflow-hidden reveal`）:
  - メディア:
    - 写真あり: `<img src="..." alt="..." class="w-full h-64 md:h-96 object-cover bg-gray-100">`（全体余白を見せる場合は `object-contain bg-gray-100`）+ クレジット `<p class="text-[11px] text-gray-400 text-right px-6 pt-2">写真：著者名 / Wikimedia Commons (ライセンス名)</p>`
    - 写真なしフォールバック: `<div class="w-full h-72 md:h-96 bg-gray-100 border-b border-gray-200"><iframe src="https://maps.google.com/maps?q=スポット名&output=embed" class="w-full h-full border-0" loading="lazy" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade"></iframe></div>`
  - 順位・キャッチバッジ: `inline-block bg-black text-white text-xs font-bold px-3 py-1 rounded-sm mb-4`（例: `第1位・定番スポット`）
  - スポット名 `<h3>`: `text-2xl font-bold mb-4 font-serif`
  - 説明文: `text-gray-600 leading-relaxed mb-6`（紹介文 + `<br><br>・アクセス：...<br>・営業時間：...`）
  - **統一CTAボタン**:
    ```html
    <a href="URL" target="_blank" rel="noopener noreferrer" class="block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg">
        この施設の詳細を見る <i class="fa-solid fa-arrow-up-right-from-square ml-2"></i>
    </a>
    ```
- 末尾 `.reveal` 監視 `<script>` を必ず配置。

### 3.3 パターンC（単体アイテム深掘りレビュー型 / 参考: `article-aliba.html`）
- ヘッダー（`REVIEW` 黒白反転バッジ + `h1` + 年月/カテゴリ） → PR表記 → メイン画像 → キャッチ＋リード文 → 番号付き `h2`（`border-b-2 border-black pb-2 inline-block`）＋特徴ボックス（`bg-gray-100 rounded p-6`） → スペック＆Q&Aカード（`rounded-xl border border-gray-200`） → まとめ＆CTAボックス（`bg-gray-100 p-8 text-center`、黒ボタン＋文言「この商品の詳細を見る」）。

---

## 4. TikTok連動構成コンポーネント＆ `index.html` カード仕様

### 4.1 記事末尾のTikTok連動動画エリア（`article-gift5.html`, `article-girlfriend-gift5.html` 準拠）
TikTok（`@couplearekore`）の元動画が存在する場合は、一覧の最後に以下のカードを追加できる。`<script async src="https://www.tiktok.com/embed.js"></script>` は **ページ全体で最末尾に1回だけ** 配置する。

```html
<!-- TikTok動画エリア -->
<div class="mt-20 bg-white p-6 md:p-8 rounded-xl border border-gray-200 shadow-sm text-center">
    <h3 class="font-bold text-xl mb-3 font-serif">今回紹介した内容をTikTok動画でもチェック</h3>
    <p class="text-sm text-gray-600 mb-6">TikTok（@couplearekore）でも反響をいただいたまとめ動画です。<br>保存してデートやお買い物の参考にしてみてください。</p>
    <div class="flex justify-center w-full overflow-hidden">
        <blockquote class="tiktok-embed" cite="https://www.tiktok.com/@couplearekore/video/動画ID" data-video-id="動画ID" style="max-width: 605px;min-width: 325px;">
            <section><a target="_blank" title="@couplearekore" href="https://www.tiktok.com/@couplearekore?refer=embed">@couplearekore</a></section>
        </blockquote>
    </div>
</div>
```

### 4.2 `index.html` 追加カード（`#gift` / `#date`）
- **GIFTカード（`#gift` 内 `space-y-12`）**: 横長2カラム `<article>`、`border border-black hover:bg-black hover:text-white text-black` の「記事を読む」リンク。
- **DATEカード（`#date` 内 `grid grid-cols-1 md:grid-cols-3 gap-6`）**: 1:1正方形（`aspect-square`）オーバーレイ `<a>`、サムネイルは1:1トリミング済み実物写真（`1080×1080` 等）。
