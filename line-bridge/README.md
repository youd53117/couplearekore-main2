# LINE Bridge（iPhoneのLINE公式アカウント連携サーバー）

Python 3 標準ライブラリのみで動作する、LINE Messaging API ⇄ `GEMINI.md` 4部署ワークフロー連携サーバーです（`npm install` / `pip install` 不要）。

## 1. セットアップ手順

### Step 1: `line-bridge/.env` にLINEの認証情報を記入
`line-bridge/.env`（`.gitignore` で保護済み）を開き、LINE Developers コンソールから以下2つを設定してください。**この時点では `ALLOWED_LINE_USER_ID=` は空欄のまま**にします。

```env
LINE_CHANNEL_SECRET=あなたのチャネルシークレット
LINE_CHANNEL_ACCESS_TOKEN=あなたのチャネルアクセストークン（長期）
ALLOWED_LINE_USER_ID=
```

### Step 2: サーバーを起動して公開URL（HTTPS）をLINE Webhookへ登録
1. ターミナルで起動：
   ```bash
   python3 line-bridge/server.py
   ```
2. トンネリングツール（`cloudflared tunnel --url http://127.0.0.1:8787` や `ngrok http 8787` 等）で発行された `https://xxxx.../webhook` を、LINE Developers コンソールの **Webhook URL** に登録して「Webhookの利用」をオンにします。

### Step 3: iPhoneのLINEからメッセージを送って `userId` を取得（確認モード）
`ALLOWED_LINE_USER_ID` が空欄の状態でiPhoneのLINEから適当なメッセージ（例：`テスト`）を送ると、
- ターミナルに **`あなたのユーザーID: Uxxxx...`** が大きく表示されます
- iPhoneのLINE側にも **`あなたのユーザーIDは \`Uxxxx...\` です`** と自動返信されます

### Step 4: `ALLOWED_LINE_USER_ID` を設定してロック完了
取得した `Uxxxx...` を `line-bridge/.env` に記入して保存します。

```env
ALLOWED_LINE_USER_ID=Uxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
AGENT_COMMAND=実行したいエージェントCLIコマンド
```

これ以降は、設定した `ALLOWED_LINE_USER_ID` 以外のユーザーからのメッセージはすべて無視され、あなたの指示だけが `GEMINI.md` の4部署ワークフロー（`01-research` → `02-writer` → `03-affiliate` → `04-inspector`）へ渡されて、完了後にLINEへ通知されます。
