#!/usr/bin/env python3
"""LINE Messaging API <-> GEMINI.md 4-Department Workflow Bridge Server."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import shlex
import subprocess
import sys
import threading
import urllib.error
import urllib.request
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = BASE_DIR.parent
ENV_PATH = BASE_DIR / ".env"
LOG_DIR = BASE_DIR / "logs"

LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"
LINE_PUSH_ENDPOINT = "https://api.line.me/v2/bot/message/push"


def load_env(path: Path) -> dict[str, str]:
    """Load key=value pairs from .env without requiring external packages."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        env[key] = value
    return env


def get_config() -> dict[str, str]:
    """Read live config from .env (with process env overrides)."""
    cfg = load_env(ENV_PATH)
    for key in (
        "LINE_CHANNEL_SECRET",
        "LINE_CHANNEL_ACCESS_TOKEN",
        "ALLOWED_LINE_USER_ID",
        "PORT",
        "HOST",
        "AGENT_COMMAND",
        "AGENT_TIMEOUT_SECONDS",
        "AUTO_GIT_PUSH",
    ):
        if key in os.environ:
            cfg[key] = os.environ[key]
    return cfg


def verify_line_signature(body: bytes, signature: str, channel_secret: str) -> bool:
    """Verify X-Line-Signature using HMAC-SHA256."""
    if not channel_secret or not signature:
        return False
    digest = hmac.new(
        channel_secret.encode("utf-8"), body, hashlib.sha256
    ).digest()
    expected = base64.b64encode(digest).decode("ascii")
    return hmac.compare_digest(expected, signature)


def _post_line_api(url: str, payload: dict[str, Any], access_token: str) -> tuple[int, str]:
    if not access_token:
        return 0, "LINE_CHANNEL_ACCESS_TOKEN is not configured"
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, body
    except Exception as exc:
        return 0, str(exc)


def chunk_text(text: str, limit: int = 4500) -> list[str]:
    """Split text into LINE-safe message chunks (max 5000 chars per message)."""
    text = text.strip()
    if not text:
        return ["(空の応答)"]
    chunks: list[str] = []
    while text:
        if len(text) <= limit:
            chunks.append(text)
            break
        split_at = text.rfind("\n", 0, limit)
        if split_at <= 0:
            split_at = limit
        chunks.append(text[:split_at].rstrip())
        text = text[split_at:].lstrip()
    return chunks[:5]  # LINE allows up to 5 message objects per request


def send_reply(reply_token: str, text: str, access_token: str) -> bool:
    if not reply_token:
        return False
    messages = [{"type": "text", "text": part} for part in chunk_text(text)]
    status, resp = _post_line_api(
        LINE_REPLY_ENDPOINT,
        {"replyToken": reply_token, "messages": messages},
        access_token,
    )
    if status != 200:
        print(f"[LINE Reply Error] status={status} body={resp}", file=sys.stderr)
        return False
    return True


def send_push(user_id: str, text: str, access_token: str) -> bool:
    if not user_id:
        return False
    messages = [{"type": "text", "text": part} for part in chunk_text(text)]
    status, resp = _post_line_api(
        LINE_PUSH_ENDPOINT,
        {"to": user_id, "messages": messages},
        access_token,
    )
    if status != 200:
        print(f"[LINE Push Error] status={status} body={resp}", file=sys.stderr)
        return False
    return True


def print_user_id_banner(user_id: str) -> None:
    """Print an unmistakable terminal banner for ALLOWED_LINE_USER_ID setup."""
    banner = f"""
========================================================================
  [確認モード] LINE 送信元のユーザーIDを検出しました！
------------------------------------------------------------------------
  あなたのユーザーID:  {user_id}

  次の手順でロックを有効化してください:
  1. line-bridge/.env を開く
  2. ALLOWED_LINE_USER_ID={user_id} を記入して保存
  3. サーバーは再起動不要で即座に反映されます（念のため再起動も可）
========================================================================
"""
    print(banner, flush=True)


def build_workflow_prompt(user_instruction: str) -> str:
    """Wrap the user's LINE request with GEMINI.md 4-department workflow instructions."""
    return (
        "以下のユーザー指示を、このリポジトリの `GEMINI.md` に定義された"
        "4部署ワークフロー（01-research -> 02-writer -> 03-affiliate -> 04-inspector）"
        "および `knowledge/brand-tone.md`・`knowledge/ng-rules.md` に厳密に従って実行してください。\n"
        "【厳守事項】\n"
        "- ステップの飛び越し禁止（01-research -> 02-writer -> 03-affiliate -> 04-inspector の順で実施）\n"
        "- 楽天アフィリエイトID `526779c3.02e0dab7.526779c4.c2c3e62b` を使用（専用ページのみ変換、周辺ホテル一覧 `yado/spot` 等は禁止し公式サイトURL使用）\n"
        "- 詳細ボタンはすべて黒（bg-black hover:bg-gray-800）＆統一文言（この施設の詳細を見る / この商品の詳細を見る）\n"
        "- 最後に変更ファイル・採用画像ライセンス・設定CTA・検品結果を簡潔に報告すること\n\n"
        f"【LINEからの指示】\n{user_instruction}"
    )


def run_workflow_task(user_id: str, instruction: str, cfg: dict[str, str]) -> None:
    """Run the configured agent command in the background and push result to LINE."""
    access_token = cfg.get("LINE_CHANNEL_ACCESS_TOKEN", "")
    agent_cmd = cfg.get("AGENT_COMMAND", "").strip()
    timeout_sec = int(cfg.get("AGENT_TIMEOUT_SECONDS", "1800") or "1800")
    auto_push = cfg.get("AUTO_GIT_PUSH", "false").lower() == "true"

    if not agent_cmd:
        send_push(
            user_id,
            "指示を受信しましたが、`line-bridge/.env` の `AGENT_COMMAND` が未設定のため自動実行できませんでした。\n"
            "実行コマンドを設定後に再度送信してください。",
            access_token,
        )
        return

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = LOG_DIR / f"run-{ts}.log"

    full_prompt = build_workflow_prompt(instruction)
    try:
        tokens = shlex.split(agent_cmd)
        cmd = [
            tok.replace("{prompt}", full_prompt).replace("{workdir}", str(REPO_ROOT))
            for tok in tokens
        ]
        if "{prompt}" not in agent_cmd:
            cmd.append(full_prompt)

        print(f"[Workflow Start] {ts} user={user_id} cmd={cmd[0]}", flush=True)
        proc = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=timeout_sec,
        )
        combined = (proc.stdout or "") + (
            f"\n[STDERR]\n{proc.stderr}" if proc.stderr else ""
        )
        log_file.write_text(combined, encoding="utf-8")

        if proc.returncode != 0:
            tail = combined.strip()[-1500:] or "(出力なし)"
            send_push(
                user_id,
                f"ワークフロー実行中にエラーが発生しました (exit={proc.returncode})。\n"
                f"ログ: {log_file.name}\n\n{tail}",
                access_token,
            )
            return

        git_note = ""
        if auto_push:
            git_res = subprocess.run(
                [
                    "bash",
                    "-lc",
                    "git add -A && git reset -q -- line-bridge/.env line-bridge/logs .DS_Store 2>/dev/null || true; "
                    'if ! git diff --cached --quiet; then git commit -m "LINE instruction update" && git push origin main; fi',
                ],
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=60,
            )
            git_note = (
                "\n\n[Git Push] 完了"
                if git_res.returncode == 0
                else f"\n\n[Git Push Error] {git_res.stderr.strip()[:400]}"
            )

        summary = (proc.stdout or "").strip()
        if len(summary) > 3500:
            summary = summary[-3500:]
        if not summary:
            summary = "処理が完了しました（詳細はローカルログを確認してください）。"

        send_push(
            user_id,
            f"4部署ワークフローが完了しました！\n\n{summary}{git_note}",
            access_token,
        )
    except subprocess.TimeoutExpired:
        send_push(
            user_id,
            f"ワークフローがタイムアウト（{timeout_sec}秒）しました。ログを確認してください: {log_file.name}",
            access_token,
        )
    except Exception as exc:
        send_push(
            user_id,
            f"ワークフロー起動時に予期せぬエラーが発生しました: {exc}",
            access_token,
        )


def handle_line_event(event: dict[str, Any], cfg: dict[str, str]) -> None:
    """Process one LINE webhook event according to confirmation / allowlist rules."""
    if event.get("type") != "message":
        return
    message = event.get("message") or {}
    if message.get("type") != "text":
        return

    source = event.get("source") or {}
    user_id = (source.get("userId") or "").strip()
    reply_token = (event.get("replyToken") or "").strip()
    text = (message.get("text") or "").strip()
    access_token = cfg.get("LINE_CHANNEL_ACCESS_TOKEN", "")
    allowed_raw = cfg.get("ALLOWED_LINE_USER_ID", "").strip()

    if not user_id:
        return

    # 1. ALLOWED_LINE_USER_ID が空欄/未設定 → 確認モード
    if not allowed_raw:
        print_user_id_banner(user_id)
        confirm_msg = (
            f"あなたのユーザーIDは `{user_id}` です。\n"
            "line-bridge/.env の ALLOWED_LINE_USER_ID に設定してください。"
        )
        if not send_reply(reply_token, confirm_msg, access_token):
            send_push(user_id, confirm_msg, access_token)
        return

    # 2. ALLOWED_LINE_USER_ID が設定済み → 許可ID以外はすべて無視
    allowed_ids = {item.strip() for item in allowed_raw.split(",") if item.strip()}
    if user_id not in allowed_ids:
        print(f"[Ignored] Unauthorized userId={user_id}", flush=True)
        return

    # 3. 許可ユーザーからの簡易コマンド / ワークフロー実行指示
    if text in {"/id", "id"}:
        send_reply(reply_token, f"現在設定中のユーザーID: `{user_id}`", access_token)
        return

    if text in {"/status", "status"}:
        cmd_configured = "設定済み" if cfg.get("AGENT_COMMAND", "").strip() else "未設定"
        send_reply(
            reply_token,
            f"LINE Bridge 稼働中\n・許可ID: {user_id}\n・AGENT_COMMAND: {cmd_configured}",
            access_token,
        )
        return

    if text in {"/help", "help"}:
        send_reply(
            reply_token,
            "使い方:\n"
            "・記事作成や更新の指示文をそのまま送信 → GEMINI.md の4部署ワークフローを実行し完了後に通知します。\n"
            "・`/status` → 稼働状態確認\n"
            "・`/id` → 自分のユーザーID確認",
            access_token,
        )
        return

    send_reply(
        reply_token,
        "指示を受け付けました！\nGEMINI.md の4部署ワークフロー（01-research → 02-writer → 03-affiliate → 04-inspector）で実行します。完了したら通知します。",
        access_token,
    )
    threading.Thread(
        target=run_workflow_task, args=(user_id, text, cfg), daemon=True
    ).start()


class LineWebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(b'{"status":"ok"}')
            return
        self.send_response(404)
        self.end_headers()

    def do_POST(self) -> None:
        if self.path not in {"/webhook", "/callback", "/"}:
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get("Content-Length", "0") or "0")
        body = self.rfile.read(length)
        signature = self.headers.get("X-Line-Signature", "")
        cfg = get_config()
        secret = cfg.get("LINE_CHANNEL_SECRET", "").strip()

        if secret and not verify_line_signature(body, signature, secret):
            print("[Rejected] Invalid X-Line-Signature", file=sys.stderr, flush=True)
            self.send_response(401)
            self.end_headers()
            return

        try:
            payload = json.loads(body.decode("utf-8"))
        except Exception:
            self.send_response(400)
            self.end_headers()
            return

        # Return 200 immediately to satisfy LINE Webhook timeout
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b"{}")

        for event in payload.get("events", []):
            handle_line_event(event, cfg)

    def log_message(self, format: str, *args: Any) -> None:
        # Suppress noisy default HTTP logs; custom logs are printed explicitly
        return


def main() -> None:
    cfg = get_config()
    host = cfg.get("HOST", "127.0.0.1") or "127.0.0.1"
    port = int(cfg.get("PORT", "8787") or "8787")
    mode = (
        "確認モード（ALLOWED_LINE_USER_ID 未設定: 受信時に userId を表示・返信）"
        if not cfg.get("ALLOWED_LINE_USER_ID", "").strip()
        else f"本番ロックモード（許可ID: {cfg['ALLOWED_LINE_USER_ID'].strip()}）"
    )
    print(f"LINE Bridge listening on http://{host}:{port}/webhook", flush=True)
    print(f"Mode: {mode}", flush=True)
    server = ThreadingHTTPServer((host, port), LineWebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down LINE Bridge.", flush=True)
        server.server_close()


if __name__ == "__main__":
    main()
