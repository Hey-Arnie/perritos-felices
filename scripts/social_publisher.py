#!/usr/bin/env python3
"""
Publicador Zero-Trust para Redes Sociales — Perritos Felices.

Convierte artes SVG 4:5 (1080x1350) a JPEG, los aloja temporalmente en la ruta
oculta no indexada `/_social_staging/` de www.perritosfelices.com y publica en
Instagram mediante Meta Graph API v21.0 leyendo el System User Token desde el
Llavero de macOS (Keychain).

Uso:
  python3 01_Infraestructura_Web/scripts/social_publisher.py verify
  python3 01_Infraestructura_Web/scripts/social_publisher.py stage 03_Assets_Visuales/artes_redes_2026/arte_01_toxicidad_45.svg
  python3 01_Infraestructura_Web/scripts/social_publisher.py publish-ig --image-url https://www.perritosfelices.com/_social_staging/arte_01_toxicidad_45.jpg --caption "..."
  python3 01_Infraestructura_Web/scripts/social_publisher.py clean --all
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = ROOT_DIR / "01_Infraestructura_Web"
STAGING_DIR = WEB_DIR / "_social_staging"
CONNECTIONS_FILE = ROOT_DIR / "05_Studio_Privado" / "studio_connections.json"

GRAPH_API_BASE = "https://graph.facebook.com/v21.0"
KEYCHAIN_ACCOUNT = "perritosfelices"
KEYCHAIN_SERVICE = "META_SYSTEM_USER_TOKEN"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SAFE_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,80}$")


def load_meta_config() -> dict:
    if not CONNECTIONS_FILE.exists():
        raise RuntimeError(f"No se encontró {CONNECTIONS_FILE}")
    data = json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))
    meta = data.get("metaGraphApi", {})
    if not meta.get("instagramAccountId"):
        raise RuntimeError("Falta instagramAccountId en studio_connections.json")
    return meta


def get_keychain_token(service: str = KEYCHAIN_SERVICE) -> str:
    """Lee el System User Token desde macOS Keychain sin tocar Google Drive."""
    try:
        res = subprocess.run(
            ["security", "find-generic-password", "-a", KEYCHAIN_ACCOUNT, "-s", service, "-w"],
            capture_output=True,
            text=True,
            check=True,
        )
        token = res.stdout.strip()
        if not token:
            raise RuntimeError("El secreto en Keychain está vacío.")
        return token
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "No se encontró META_SYSTEM_USER_TOKEN en el Llavero de macOS.\n"
            "Guárdalo en tu terminal con:\n"
            f'  security add-generic-password -a "{KEYCHAIN_ACCOUNT}" -s "{service}" -w "TU_TOKEN" -U'
        ) from exc


def graph_request(endpoint: str, method: str = "GET", params: dict | None = None, token: str = "") -> dict:
    """Ejecuta una petición HTTPS a Meta Graph API sin exponer el token en errores."""
    url = f"{GRAPH_API_BASE}/{endpoint.lstrip('/')}"
    query = dict(params or {})
    if token:
        query["access_token"] = token

    if method == "GET":
        qs = urllib.parse.urlencode(query)
        req = urllib.request.Request(f"{url}?{qs}", method="GET")
    else:
        body = urllib.parse.urlencode(query).encode("utf-8")
        req = urllib.request.Request(url, data=body, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        raw = err.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(raw)
            msg = err_json.get("error", {}).get("message", raw)
        except Exception:
            msg = raw
        raise RuntimeError(f"Meta Graph API ({err.code}): {msg}") from err


def sanitize_slug(raw_name: str) -> str:
    stem = Path(raw_name).stem.lower().strip()
    slug = re.sub(r"[^a-z0-9_-]+", "_", stem).strip("_-")
    if not SAFE_NAME_RE.match(slug):
        raise ValueError(f"Nombre de archivo no válido para staging: {raw_name}")
    return slug


def render_svg_to_jpg(svg_path: Path, out_jpg: Path) -> None:
    """Renderiza un SVG 1080x1350 con Chrome headless y lo exporta a JPEG con sips."""
    if not Path(CHROME_BIN).exists():
        raise RuntimeError(f"No se encontró Google Chrome en {CHROME_BIN}")

    with tempfile.TemporaryDirectory(prefix="pf_render_") as tmpdir:
        tmp_dir = Path(tmpdir)
        tmp_png = tmp_dir / "render.png"
        chrome_profile = tmp_dir / "chrome_profile"
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--no-sandbox",
            f"--user-data-dir={chrome_profile}",
            "--disable-gpu",
            "--window-size=1080,1350",
            "--hide-scrollbars",
            f"--screenshot={tmp_png}",
            svg_path.resolve().as_uri(),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if not tmp_png.exists():
            raise RuntimeError(f"Chrome no pudo renderizar el SVG: {proc.stderr[-300:]}")

        subprocess.run(
            ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(tmp_png), "--out", str(out_jpg)],
            capture_output=True,
            text=True,
            check=True,
        )


def convert_raster_to_jpg(src_path: Path, out_jpg: Path) -> None:
    if src_path.suffix.lower() in {".jpg", ".jpeg"}:
        shutil.copy2(src_path, out_jpg)
        return
    subprocess.run(
        ["sips", "-s", "format", "jpeg", "-s", "formatOptions", "92", str(src_path), "--out", str(out_jpg)],
        capture_output=True,
        text=True,
        check=True,
    )


def cmd_verify(_args: argparse.Namespace) -> int:
    meta = load_meta_config()
    service = meta.get("keychainService", KEYCHAIN_SERVICE)
    token = get_keychain_token(service)
    page_id = meta.get("pageId", "")
    ig_id = meta["instagramAccountId"]

    me = graph_request("me", method="GET", params={"fields": "id,name"}, token=token)
    print(f"✔ Token válido para usuario/sistema: {me.get('name')} (ID: {me.get('id')})")

    perms_res = graph_request("me/permissions", method="GET", token=token)
    granted = {
        p["permission"]
        for p in perms_res.get("data", [])
        if p.get("status") == "granted"
    }
    required = {"instagram_basic", "instagram_content_publish", "pages_show_list", "pages_read_engagement"}
    missing_perms = sorted(required - granted)
    if missing_perms:
        print(f"⚠ Faltan permisos en el token: {', '.join(missing_perms)}")
    else:
        print("✔ Permisos requeridos concedidos en el token.")

    if page_id:
        try:
            page_info = graph_request(
                page_id,
                method="GET",
                params={"fields": "id,name,instagram_business_account"},
                token=token,
            )
            linked_ig = page_info.get("instagram_business_account", {}).get("id")
            print(f"✔ Página de Facebook accesible: {page_info.get('name')} (ID: {page_info.get('id')})")
            if linked_ig and linked_ig != ig_id:
                print(f"⚠ El IG Account ID vinculado a esta página es {linked_ig} (configurado: {ig_id}).")
                ig_id = linked_ig
            elif not linked_ig:
                print("⚠ La Página no reporta instagram_business_account vinculado (revisa el enlace IG ↔ FB).")
        except RuntimeError as exc:
            print(f"⚠ No se pudo leer la Página {page_id}: {exc}")

    info = graph_request(
        ig_id,
        method="GET",
        params={"fields": "id,username,name,followers_count,media_count"},
        token=token,
    )
    print("✔ Conexión con Instagram verificada:")
    print(f"  • Cuenta IG ID : {info.get('id')}")
    print(f"  • Usuario      : @{info.get('username', 'N/D')}")
    print(f"  • Nombre       : {info.get('name', 'N/D')}")
    print(f"  • Publicaciones: {info.get('media_count', 'N/D')}")
    return 0


def cmd_stage(args: argparse.Namespace) -> int:
    src = Path(args.source).expanduser().resolve()
    if not src.exists():
        print(f"❌ Archivo no encontrado: {src}", file=sys.stderr)
        return 1

    STAGING_DIR.mkdir(parents=True, exist_ok=True)
    slug = sanitize_slug(args.slug or src.stem)
    out_jpg = STAGING_DIR / f"{slug}.jpg"

    if src.suffix.lower() == ".svg":
        render_svg_to_jpg(src, out_jpg)
    elif src.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}:
        convert_raster_to_jpg(src, out_jpg)
    else:
        print(f"❌ Formato no soportado para imagen: {src.suffix}", file=sys.stderr)
        return 1

    meta = load_meta_config()
    base_url = meta.get("publicBaseUrl", "https://www.perritosfelices.com/_social_staging").rstrip("/")
    public_url = f"{base_url}/{out_jpg.name}"

    print(f"✔ Arte preparado en staging oculto (noindex): {out_jpg.relative_to(ROOT_DIR)}")
    print(f"✔ URL pública HTTPS (tras git push): {public_url}")
    return 0


def wait_for_container(creation_id: str, token: str, timeout_s: int = 45) -> str:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        res = graph_request(creation_id, method="GET", params={"fields": "status_code,status"}, token=token)
        status = res.get("status_code", "IN_PROGRESS")
        if status == "FINISHED":
            return status
        if status in {"ERROR", "EXPIRED"}:
            raise RuntimeError(f"Contenedor {creation_id} falló con estado {status}: {res}")
        time.sleep(2)
    raise RuntimeError(f"Tiempo de espera agotado para el contenedor {creation_id}")


def cmd_publish_ig(args: argparse.Namespace) -> int:
    meta = load_meta_config()
    ig_id = meta["instagramAccountId"]
    caption_val = args.caption
    caption_path = Path(args.caption)
    if caption_path.exists() and caption_path.is_file():
        caption_val = caption_path.read_text(encoding="utf-8").strip()

    urls = args.image_url
    for u in urls:
        if not u.startswith("https://"):
            print(f"❌ Meta Graph API requiere URL HTTPS pública: {u}", file=sys.stderr)
            return 1

    if args.dry_run:
        print("🔎 [DRY-RUN] Publicación simulada en Instagram:")
        print(f"  • IG Account ID: {ig_id}")
        print(f"  • Tipo         : {'Carrusel' if len(urls) > 1 else 'Imagen única'}")
        print(f"  • URLs         : {urls}")
        print(f"  • Caption ({len(caption_val)} chars): {caption_val[:120]}...")
        return 0

    token = get_keychain_token(meta.get("keychainService", KEYCHAIN_SERVICE))

    if len(urls) == 1:
        container = graph_request(
            f"{ig_id}/media",
            method="POST",
            params={"image_url": urls[0], "caption": caption_val},
            token=token,
        )
        creation_id = container["id"]
        wait_for_container(creation_id, token)
    else:
        child_ids = []
        for img_url in urls:
            child = graph_request(
                f"{ig_id}/media",
                method="POST",
                params={"image_url": img_url, "is_carousel_item": "true"},
                token=token,
            )
            wait_for_container(child["id"], token)
            child_ids.append(child["id"])

        carousel = graph_request(
            f"{ig_id}/media",
            method="POST",
            params={
                "media_type": "CAROUSEL",
                "children": ",".join(child_ids),
                "caption": caption_val,
            },
            token=token,
        )
        creation_id = carousel["id"]
        wait_for_container(creation_id, token)

    published = graph_request(
        f"{ig_id}/media_publish",
        method="POST",
        params={"creation_id": creation_id},
        token=token,
    )
    print(f"✔ Publicado en Instagram exitosamente. Media ID: {published.get('id')}")
    return 0


def cmd_verify_tiktok(args: argparse.Namespace) -> int:
    if not CONNECTIONS_FILE.exists():
        raise RuntimeError(f"No se encontró {CONNECTIONS_FILE}")
    data = json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))
    tt = data.get("tikTokApi", {})
    client_key = tt.get("clientKey")
    target_user = tt.get("targetUser")
    service = tt.get("keychainService", "TIKTOK_SANDBOX_CLIENT_SECRET")

    if not client_key:
        raise RuntimeError("Falta clientKey en tikTokApi dentro de studio_connections.json")

    secret = get_keychain_token(service)
    print(f"✔ Configuración de TikTok encontrada:")
    print(f"  • Modo        : {tt.get('mode')}")
    print(f"  • Client Key  : {client_key}")
    print(f"  • Target User : @{target_user}")
    print(f"  • Redirect URI: {tt.get('redirectUri')}")
    print(f"  • Secret en Llavero ({service}): {'Presente (' + str(len(secret)) + ' caracteres)' if secret else 'NO ENCONTRADO'}")
    return 0


TIKTOK_API_BASE = "https://open.tiktokapis.com/v2"
TIKTOK_TOKEN_SERVICE = "TIKTOK_USER_ACCESS_TOKEN"


def load_tiktok_config() -> tuple[str, str, str]:
    if not CONNECTIONS_FILE.exists():
        raise RuntimeError(f"No se encontró {CONNECTIONS_FILE}")
    data = json.loads(CONNECTIONS_FILE.read_text(encoding="utf-8"))
    tt = data.get("tikTokApi", {})
    client_key = tt.get("clientKey")
    service = tt.get("keychainService", "TIKTOK_SANDBOX_CLIENT_SECRET")
    redirect_uri = tt.get("redirectUri", "https://www.perritosfelices.com/auth/tiktok/callback")
    if not client_key:
        raise RuntimeError("Falta clientKey en studio_connections.json")
    client_secret = get_keychain_token(service)
    return client_key, client_secret, redirect_uri


def cmd_tiktok_auth_url(args: argparse.Namespace) -> int:
    client_key, _, redirect_uri = load_tiktok_config()
    scope = "user.info.basic,video.upload,video.publish"
    params = {
        "client_key": client_key,
        "scope": scope,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "state": "pf_tiktok_state",
    }
    url = f"https://www.tiktok.com/v2/auth/authorize/?{urllib.parse.urlencode(params)}"
    print(f"🔗 Abre esta URL en tu navegador para autorizar la publicación:")
    print(f"\n{url}\n")
    print("Después de autorizar, copia el valor del parámetro 'code' de la URL a la que te redirija.")
    print("Y ejecútalo así:")
    print("  python3 01_Infraestructura_Web/scripts/social_publisher.py tiktok-exchange-code --code TU_CODIGO")
    return 0


def cmd_tiktok_exchange_code(args: argparse.Namespace) -> int:
    client_key, client_secret, redirect_uri = load_tiktok_config()
    url = f"{TIKTOK_API_BASE}/oauth/token/"
    data = urllib.parse.urlencode({
        "client_key": client_key,
        "client_secret": client_secret,
        "code": args.code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    }).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Cache-Control": "no-cache"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8")
        raise RuntimeError(f"Error al canjear código TikTok ({err.code}): {body}")

    access_token = res_data.get("access_token")
    if not access_token:
        error_msg = res_data.get("error_description") or res_data.get("message") or str(res_data)
        raise RuntimeError(f"TikTok no devolvió access_token: {error_msg}")

    # Guardar access token en Keychain
    cmd = [
        "security", "add-generic-password",
        "-a", KEYCHAIN_ACCOUNT,
        "-s", TIKTOK_TOKEN_SERVICE,
        "-w", access_token,
        "-U"
    ]
    subprocess.run(cmd, check=True)
    print(f"✔ Access token de TikTok guardado exitosamente en el Llavero ({TIKTOK_TOKEN_SERVICE}).")
    print(f"  • Expira en : {res_data.get('expires_in', 86400)} segundos")
    print(f"  • Open ID   : {res_data.get('open_id')}")
    return 0


def cmd_publish_tiktok(args: argparse.Namespace) -> int:
    client_key, _, _ = load_tiktok_config()
    token = get_keychain_token(TIKTOK_TOKEN_SERVICE)
    if not token:
        raise RuntimeError(
            f"No se encontró {TIKTOK_TOKEN_SERVICE} en Keychain. Genera uno con:\n"
            "  python3 01_Infraestructura_Web/scripts/social_publisher.py tiktok-auth-url"
        )

    title = args.title[:150]
    local_path = None
    if getattr(args, "video_file", None):
        local_path = Path(args.video_file).resolve()
    elif getattr(args, "video_url", None) and "_social_staging" in args.video_url:
        filename = args.video_url.split("/")[-1]
        candidate = STAGING_DIR / filename
        if candidate.exists():
            local_path = candidate

    print(f"🚀 Iniciando publicación en TikTok Sandbox...")
    print(f"  • Modo     : {'FILE_UPLOAD (Directo)' if local_path else 'PULL_FROM_URL'}")
    print(f"  • Título   : {title}")

    if args.dry_run:
        print("🔎 [DRY-RUN] Simulación completa. Video listo para publicarse.")
        return 0

    init_url = f"{TIKTOK_API_BASE}/post/publish/video/init/"
    
    if local_path and local_path.exists():
        video_size = local_path.stat().st_size
        payload = json.dumps({
            "post_info": {
                "title": title,
                "privacy_level": "SELF_ONLY",
                "disable_duet": False,
                "disable_stitch": False,
                "disable_comment": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "FILE_UPLOAD",
                "video_size": video_size,
                "chunk_size": video_size,
                "total_chunk_count": 1
            }
        }).encode("utf-8")
    else:
        video_url = args.video_url
        payload = json.dumps({
            "post_info": {
                "title": title,
                "privacy_level": "SELF_ONLY",
                "disable_duet": False,
                "disable_stitch": False,
                "disable_comment": False,
                "video_cover_timestamp_ms": 1000
            },
            "source_info": {
                "source": "PULL_FROM_URL",
                "video_url": video_url
            }
        }).encode("utf-8")

    req = urllib.request.Request(
        init_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=UTF-8"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8")
        raise RuntimeError(f"Error TikTok init ({err.code}): {body}")

    error_info = data.get("error", {})
    if error_info.get("code") != "ok":
        raise RuntimeError(f"TikTok error: {error_info}")

    publish_id = data.get("data", {}).get("publish_id")
    upload_url = data.get("data", {}).get("upload_url")

    if upload_url and local_path and local_path.exists():
        print(f"📤 Subiendo video directamente a los servidores de TikTok ({video_size} bytes)...")
        with open(local_path, "rb") as vf:
            video_bytes = vf.read()
        
        upload_req = urllib.request.Request(
            upload_url,
            data=video_bytes,
            headers={
                "Content-Type": "video/mp4",
                "Content-Range": f"bytes 0-{video_size - 1}/{video_size}",
                "Content-Length": str(video_size)
            },
            method="PUT"
        )
        try:
            with urllib.request.urlopen(upload_req) as up_resp:
                pass
        except urllib.error.HTTPError as up_err:
            up_body = up_err.read().decode("utf-8")
            raise RuntimeError(f"Error al subir video a TikTok ({up_err.code}): {up_body}")
        print(f"✔ Video subido con éxito.")

    print(f"✔ Publicación completada en TikTok exitosamente. Publish ID: {publish_id}")
    return 0


def cmd_clean(args: argparse.Namespace) -> int:
    if not STAGING_DIR.exists():
        print("ℹ No existe carpeta _social_staging.")
        return 0

    removed = 0
    for item in STAGING_DIR.iterdir():
        if item.name == ".gitkeep":
            continue
        if args.all or (args.file and item.name == args.file):
            if item.is_file():
                item.unlink()
                removed += 1
    print(f"✔ Archivos temporales eliminados de _social_staging: {removed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Publicador Zero-Trust para Instagram — Perritos Felices")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("verify", help="Verifica token en Keychain y conexión con Instagram Graph API")
    sub.add_parser("verify-tiktok", help="Verifica configuración y credenciales de TikTok Sandbox")
    sub.add_parser("tiktok-auth-url", help="Genera la URL de autorización OAuth de TikTok")

    p_exch = sub.add_parser("tiktok-exchange-code", help="Canjea el código de autorización por access token")
    p_exch.add_argument("--code", required=True, help="Código de autorización devuelto en el redirect")

    p_tt_pub = sub.add_parser("publish-tiktok", help="Publica video 9:16 en TikTok vía Content Posting API")
    p_tt_pub.add_argument("--video-url", help="URL pública HTTPS del video MP4")
    p_tt_pub.add_argument("--video-file", help="Ruta local al archivo MP4")
    p_tt_pub.add_argument("--title", required=True, help="Título del post en TikTok")
    p_tt_pub.add_argument("--dry-run", action="store_true", help="Simula la petición sin publicar")

    p_stage = sub.add_parser("stage", help="Convierte SVG/imagen a JPG 1080x1350 en _social_staging")
    p_stage.add_argument("source", help="Ruta al archivo SVG, PNG o JPG")
    p_stage.add_argument("--slug", help="Nombre de archivo destino sin extensión")

    p_pub = sub.add_parser("publish-ig", help="Publica imagen o carrusel en Instagram vía Meta Graph API")
    p_pub.add_argument("--image-url", nargs="+", required=True, help="Una o más URLs públicas HTTPS")
    p_pub.add_argument("--caption", required=True, help="Texto del post o ruta a archivo .txt/.md")
    p_pub.add_argument("--dry-run", action="store_true", help="Simula la petición sin publicar")

    p_clean = sub.add_parser("clean", help="Limpia archivos temporales de _social_staging")
    p_clean.add_argument("--all", action="store_true", help="Elimina todos los archivos temporales")
    p_clean.add_argument("--file", help="Nombre exacto de archivo a eliminar")

    args = parser.parse_args()
    try:
        if args.command == "verify":
            return cmd_verify(args)
        if args.command == "verify-tiktok":
            return cmd_verify_tiktok(args)
        if args.command == "tiktok-auth-url":
            return cmd_tiktok_auth_url(args)
        if args.command == "tiktok-exchange-code":
            return cmd_tiktok_exchange_code(args)
        if args.command == "publish-tiktok":
            return cmd_publish_tiktok(args)
        if args.command == "stage":
            return cmd_stage(args)
        if args.command == "publish-ig":
            return cmd_publish_ig(args)
        if args.command == "clean":
            return cmd_clean(args)
    except Exception as exc:
        print(f"❌ Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
