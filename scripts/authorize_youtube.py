"""One-time local Google authorization. Credential contents are never printed."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Autorizar o canal na tela oficial do Google.")
    parser.add_argument("--client-file", required=True, type=Path)
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    output = project_root / ".secrets" / "youtube_oauth.json"
    if output.exists():
        print("Já existe uma credencial local. Guarde-a antes de refazer a autorização.")
        return 1
    try:
        client_info = json.loads(args.client_file.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        print("Não foi possível ler o JSON de credenciais baixado do Google.")
        return 1
    if not isinstance(client_info, dict) or not isinstance(client_info.get("installed"), dict):
        print("Crie um cliente OAuth do tipo Aplicativo para computador / Desktop app.")
        return 1
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        print("Instale as dependências de requirements-setup.txt antes de continuar.")
        return 1
    try:
        flow = InstalledAppFlow.from_client_config(client_info, scopes=SCOPES)
        credentials = flow.run_local_server(
            host="localhost",
            port=0,
            open_browser=True,
            access_type="offline",
            prompt="consent",
            timeout_seconds=300,
            authorization_prompt_message="Autorize o aplicativo na janela oficial do Google que será aberta.",
            success_message="Autorização recebida. Você pode fechar esta janela e voltar ao terminal.",
        )
    except Exception:
        # Third-party exceptions can contain OAuth payloads; do not echo them.
        print("A autorização não foi concluída. Confira o cliente OAuth, o usuário de teste e a permissão no Google.")
        return 1
    if not credentials.refresh_token:
        print("O Google não forneceu uma credencial de renovação. Refaça o consentimento com acesso offline.")
        return 1
    try:
        output.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        descriptor = os.open(output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(credentials.to_json())
            handle.write("\n")
    except OSError:
        print("Não foi possível salvar a credencial na pasta local .secrets.")
        return 1
    print("Autorização salva em .secrets/youtube_oauth.json.")
    print("Cole o conteúdo em um GitHub Secret chamado YOUTUBE_OAUTH_JSON.")
    print("Mantenha o arquivo privado. Consulte o README sobre o prazo do modo Em teste.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
