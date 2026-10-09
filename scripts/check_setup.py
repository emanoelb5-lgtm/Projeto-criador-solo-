"""Offline readiness report. Does not authenticate, spend credits, or publish."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path

UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
READ_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"


def nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def positive_number(value: object) -> bool:
    return isinstance(value, (float, int)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def inspect(config: dict, env: dict) -> list[tuple[str, bool]]:
    video = config.get("video") if isinstance(config.get("video"), dict) else {}
    schedule = config.get("schedule") if isinstance(config.get("schedule"), dict) else {}
    ai = config.get("ai") if isinstance(config.get("ai"), dict) else {}
    execution = config.get("execution") if isinstance(config.get("execution"), dict) else {}
    budget = ai.get("monthly_budget_brl")
    times = schedule.get("publish_times_local")
    times_valid = isinstance(times, list) and len(times) == 2 and len(set(str(t) for t in times)) == 2
    if times_valid:
        for value in times:
            if not isinstance(value, str) or len(value) != 5 or value[2] != ":":
                times_valid = False
                break
            try:
                hour, minute = (int(part) for part in value.split(":"))
                if not (0 <= hour <= 23 and 0 <= minute <= 59):
                    times_valid = False
                    break
            except ValueError:
                times_valid = False
                break
    youtube_valid = False
    credential = env.get("YOUTUBE_OAUTH_JSON", "")
    if nonempty_string(credential):
        try:
            token = json.loads(credential)
            required = ("refresh_token", "client_id", "client_secret", "token_uri")
            scopes = token.get("scopes", []) if isinstance(token, dict) else []
            youtube_valid = (
                isinstance(token, dict)
                and all(nonempty_string(token.get(key)) for key in required)
                and token.get("token_uri") in (
                    "https://oauth2.googleapis.com/token",
                    "https://accounts.google.com/o/oauth2/token",
                )
                and isinstance(scopes, list)
                and UPLOAD_SCOPE in scopes
                and READ_SCOPE in scopes
            )
        except (ValueError, TypeError):
            youtube_valid = False
    basic_checks = [
        ("Formato 1920 × 1080 em 16:9 e duração de oito minutos", video.get("width") == 1920 and video.get("height") == 1080 and video.get("aspect_ratio") == "16:9" and video.get("duration_seconds") == 480),
        ("Nicho definido", nonempty_string(config.get("topic"))),
        ("Canal de destino definido", nonempty_string(config.get("channel_id"))),
        ("Credencial do YouTube em formato esperado", youtube_valid),
    ]
    if config.get("mode") == "chat_command":
        return basic_checks + [
            ("IA e início por mensagem no ChatGPT Work", ai.get("auth_mode") == "chat_work" and execution.get("production") == "interactive_workspace" and execution.get("trigger") == "user_message"),
        ]
    return basic_checks + [
        ("Meta de dois vídeos por dia", schedule.get("target_videos_per_day") == 2),
        ("Dois horários distintos definidos", times_valid),
        ("Orçamento mensal de IA definido", positive_number(budget)),
        ("Chave de IA cadastrada em OPENAI_API_KEY", nonempty_string(env.get("OPENAI_API_KEY"))),
        ("Servidor externo de produção configurado", execution.get("production") == "external_worker" and execution.get("worker_configured") is True),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Conferir configuração sem chamadas externas.")
    parser.add_argument("--config", type=Path, default=Path(__file__).resolve().parents[1] / "config" / "channel.json")
    args = parser.parse_args()
    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        if not isinstance(config, dict):
            raise ValueError
    except (OSError, ValueError):
        print("Não foi possível ler uma configuração JSON válida.")
        return 1
    checks = inspect(config, os.environ)
    lines = ["# Configuração do Criador Solo", "", "| Item | Situação |", "|---|---|"]
    lines.extend(f"| {label} | {'Configurado' if ready else 'Pendente'} |" for label, ready in checks)
    lines.extend(["", "Esta conferência é local: não autentica serviços, não gasta créditos e não publica vídeos.", "O fluxo de produção completo e a integração de publicação ainda serão implementados."])
    report = "\n".join(lines) + "\n"
    print(report)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as summary:
            summary.write(report)
    return 0 if all(ready for _, ready in checks) else 2


if __name__ == "__main__":
    raise SystemExit(main())
