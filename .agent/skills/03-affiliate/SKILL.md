---
name: 03-affiliate
description: 記事作成ワークフローの第3工程（楽天アフィリエイト・メディア組み込み・CTAボタン整形・index.html反映担当）。楽天公式ID変換、公式サイトフォールバック、Wikimedia Commons写真の目視厳選・リサイズ・Googleマップ代替、TikTokスクリプト統合、黒色CTAボタン完全統一を実行する。
---

# 第3部署：アフィリエイト・メディア・CTA整形担当（03-affiliate）

本スキルは「カップルあれこれ（couple-arekore.com）」の記事制作ワークフローにおける **第3工程** です。
`02-writer` が執筆した記事初稿に対して、**楽天アフィリエイトリンク変換、Wikimedia Commons 写真の目視厳選と加工（またはGoogleマップ/楽天画像フォールバック）、SNS埋め込みスクリプト整形、黒色CTAボタン完全統一、`index.html` 追記** を実施します。

## 実行前に必ず読むファイル
1. `GEMINI.md`: 公式楽天アフィリエイトID、CTA色・文言ルール、画像品質基準
2. `knowledge/brand-tone.md`: CTAボタンHTML仕様、Wikimediaキャプション仕様、TikTok埋め込み仕様、`index.html` カード仕様
3. `knowledge/ng-rules.md`: アフィリエイト・写真・SNSに関するNG事例一覧

---

## ステップ1: 楽天アフィリエイトリンク変換＆公式サイト仕分け

1. **公式楽天アフィリエイトID（`GEMINI.md` 準拠）**:
   - **`526779c3.02e0dab7.526779c4.c2c3e62b`**
2. **変換ルールと厳格な適用制限**:
   - **専用ページが存在する場合のみ変換**:
     楽天市場の該当商品個別ページ、楽天トラベル観光体験のチケットページ、宿泊施設単体の予約ページに対してのみ、以下のUTF-8 URLエンコード形式へ自動変換する。
     ```text
     https://hb.afl.rakuten.co.jp/hgc/526779c3.02e0dab7.526779c4.c2c3e62b/?pc=<URLエンコード済み対象URL>
     ```
   - **検索結果・周辺ホテル一覧は禁止**:
     `travel.rakuten.co.jp/yado/spot/...` 等、周辺宿泊一覧や検索結果ページになるURLは絶対に変換せず、**必ずその施設・商品の公式サイトURLをそのまま設定**する。

---

## ステップ2: 詳細CTAボタンの文言・デザイン（黒色）完全統一

リンク先が楽天アフィリエイトであっても公式サイトであっても、すべての詳細ボタンを以下に完全統一する。
- **赤色ボタン（`bg-[#bf0000]` 等）や色分けは全面禁止**。サイト基本カラーの黒（`#111111` ベース）のみ使用する（価格表示テキストの `text-[#bf0000]` は維持可）。
- **文言の統一**:
  - デートスポット・施設記事（パターンB）: `この施設の詳細を見る`
  - 商品・ギフト記事（パターンA / C）: `この商品の詳細を見る`
- **HTMLコード（全パターン共通）**:
  ```html
  <a href="確定URL" target="_blank" rel="noopener noreferrer" class="block w-full bg-black hover:bg-gray-800 text-white text-center font-bold py-4 rounded-lg transition shadow-sm text-lg">
      この施設の詳細を見る <i class="fa-solid fa-arrow-up-right-from-square ml-2"></i>
  </a>
  ```
  （※商品記事の場合は `この商品の詳細を見る` に変更）

---

## ステップ3: ハイブリッド画像・スポット表示ルール（建物外観フリー素材は全面禁止）

場所・店舗・施設を紹介する記事の「各スポット枠」は、必ず以下の **【A】と【B】の両方をセットで実装** する。**単なるホテルや建物の外観写真（Wikimedia Commons等）をメイン画像に使うことは一切禁止**する。

### ■ A. メインビジュアル（以下の優先順位で1つ決定）
1. **第1優先（ユーザーからInstagram投稿URLの指定がある場合）**:
   - 指定されたURLをInstagram公式埋め込みコード（`<blockquote class="instagram-media" ...>` ＋ `<script async src="https://www.instagram.com/embed.js"></script>` 末尾1回）として配置する。
2. **第2優先（URL指定がなく、楽天トラベル掲載施設の場合）**:
   - 楽天トラベルの該当施設ページから「食事・レストラン・内観」の公式画像URL（`img.travel.rakuten.co.jp/...` 等）を取得・目視確認し、楽天アフィリエイトID（`526779c3.02e0dab7.526779c4.c2c3e62b`）を経由した**アフィリエイトリンク付き画像**として配置する。
   ```html
   <a href="https://hb.afl.rakuten.co.jp/hgc/526779c3.02e0dab7.526779c4.c2c3e62b/?pc=エンコード済みホテルURL" target="_blank" rel="noopener noreferrer" class="block overflow-hidden">
       <img src="楽天トラベル公式の料理・内観画像URL" alt="店名・料理・空間" class="w-full h-64 md:h-96 object-cover bg-gray-100 hover:scale-105 transition duration-500">
   </a>
   ```
3. **第3優先（上記で画像が取得できない場合）**:
   - 料理ジャンルや空間ムード（鉄板焼きのステーキ調理シーン、ホテル最上階バーの夜景とカクテル、記念日コース料理など）が直感的に伝わる高画質な料理・内観イメージ写真（Unsplash等）を配置する。

### ■ B. 全スポット共通の標準装備（Aでどれが選ばれた場合でも例外なく全項目に必ず設置）
1. **店舗情報エリアへの「Googleマップ埋め込み（`<iframe>`）」の設置**（読者が位置関係をすぐ把握できるようにする）。
2. **黒ボタン（「この施設の詳細を見る」）の直上に「📸 Instagramで実際の料理・店内写真を見る」（Instagramの店名タグ検索等へのリンク）ボタンを設置**（※すでにAの第1優先でインスタ公式埋め込み済みのスポットのみ省略可）。
   ```html
   <!-- 店舗情報枠内 Googleマップ埋め込み（全スポット必須） -->
   <div class="mb-6 rounded-lg overflow-hidden border border-gray-200">
       <iframe src="https://maps.google.com/maps?q=店舗名+エリア&t=&z=15&ie=UTF8&iwloc=&output=embed" class="w-full h-48 md:h-56" loading="lazy" allowfullscreen="" referrerpolicy="no-referrer-when-downgrade" title="店舗名 Googleマップ"></iframe>
   </div>
   <!-- 黒ボタン直上のInstagram検索ボタン（第1優先のインスタ公式埋め込み時のみ省略可） -->
   <a href="https://www.instagram.com/explore/tags/タグ名/" target="_blank" rel="noopener noreferrer" class="block w-full border-2 border-black hover:bg-black hover:text-white text-black text-center font-bold py-3 rounded-lg transition text-sm md:text-base mb-3">
       📸 Instagramで実際の料理・店内写真を見る <i class="fa-solid fa-arrow-up-right-from-square ml-1"></i>
   </a>
   ```
4. **`index.html` 用サムネイル（1:1正方形）生成**:
   - エリアやテーマの雰囲気が伝わる高画質写真を `sips` 等で中央1:1クロップ＆`1080x1080` リサイズしてルート直下に保存する（例: `maihama.jpg`）。

---

## ステップ4: SNS埋め込み整形＆ `index.html` へのカード追記

1. **TikTok埋め込みスクリプトの一元化**:
   - `blockquote.tiktok-embed` が記事内にある場合のみ、`<script async src="https://www.tiktok.com/embed.js"></script>` を **`</body>` 直前（ページ最末尾）に1回だけ** 配置する。`blockquote` がなければ不要スクリプトを入れない。
2. **`index.html` の該当セクションへリンクカードを追記**:
   - すでに該当記事（`article-<slug>.html`）へのリンクカードが存在しないか確認（重複追記禁止）。
   - **パターンA / C**: `#gift` の `space-y-12` 内に横長 `<article>` カードを追加。
   - **パターンB**: `#date` の `grid grid-cols-1 md:grid-cols-3 gap-6` 内に正方形 `aspect-square` リンクカードを追加し、ステップ3で作成した1:1画像を `src` に指定する。
