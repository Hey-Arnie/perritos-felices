#!/usr/bin/env python3
"""
PERRITOS FELICES STUDIO — Servidor Local de Administración Visual (Zero-Trust)
Permite al usuario controlar visualmente todo el sitio sin saber programación:
  • Portada & Marketing (Hero, métricas, titulares, boletín)
  • Guías & Blog (Constructor visual por secciones H2 + viñetas + callouts)
  • Calendario Editorial Kanban (Ideas -> En preparación -> Publicadas)
  • Directorio Canino Verificado (Altas, bajas y ediciones en vivo)
  • Botón de Compilación, Auditoría de Ciberseguridad y Simulador en Vivo

Funciona tanto abriendo http://127.0.0.1:8765 como abriendo studio/index.html directamente.
"""

import argparse
import io
import json
import mimetypes
import sys
import urllib.parse
import webbrowser
from contextlib import redirect_stdout
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Importar funciones y constantes oficiales del motor publicar.py
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
import publicar as pub  # noqa: E402

STUDIO_DIR = pub.ROOT_DIR / "05_Studio_Privado"


def capture_cmd(func, *args, **kwargs):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = func(*args, **kwargs)
    return code, buf.getvalue()


class StudioRequestHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _add_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(204)
        self._add_cors_headers()
        self.end_headers()

    def _send_json(self, payload: dict, status: int = 200):
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self._add_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(raw)

    def _serve_file(self, base_dir: Path, rel_path: str):
        clean_rel = rel_path.lstrip("/") or "index.html"
        target = (base_dir / clean_rel).resolve()
        if not target.is_relative_to(base_dir.resolve()) or not target.is_file():
            self.send_error(404, "Archivo no encontrado")
            return

        ctype, _ = mimetypes.guess_type(str(target))
        ctype = ctype or "application/octet-stream"
        if ctype.startswith("text/") or ctype in ("application/javascript", "application/json"):
            ctype += "; charset=utf-8"

        data = target.read_bytes()
        self.send_response(200)
        self._add_cors_headers()
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/state":
            pub.ensure_editorial_calendar()
            articles = (
                json.loads(pub.ARTICLES_JSON.read_text(encoding="utf-8"))
                if pub.ARTICLES_JSON.exists()
                else []
            )
            directory = (
                json.loads(pub.DIRECTORY_JSON.read_text(encoding="utf-8"))
                if pub.DIRECTORY_JSON.exists()
                else []
            )
            calendar = (
                json.loads(pub.CALENDAR_JSON.read_text(encoding="utf-8"))
                if pub.CALENDAR_JSON.exists()
                else []
            )
            marketing = (
                json.loads(pub.MARKETING_JSON.read_text(encoding="utf-8"))
                if pub.MARKETING_JSON.exists()
                else {}
            )
            self._send_json(
                {
                    "articles": articles,
                    "directory": directory,
                    "calendar": calendar,
                    "marketing": marketing,
                }
            )
            return

        if path in ("/", "/index.html", "/studio", "/studio/", "/studio/index.html"):
            self._serve_file(STUDIO_DIR, "index.html")
            return

        if path.startswith("/studio/"):
            rel = path[len("/studio/") :]
            self._serve_file(STUDIO_DIR, rel)
            return

        if path.startswith("/site/"):
            rel = path[len("/site/") :]
            self._serve_file(pub.WEB_DIR, rel)
            return

        if path.startswith("/01_Infraestructura_Web/"):
            rel = path[len("/01_Infraestructura_Web/") :]
            self._serve_file(pub.WEB_DIR, rel)
            return

        # Si el archivo existe en STUDIO_DIR (ej. studio.css, studio.js), servirlo primero
        candidate_studio = (STUDIO_DIR / path.lstrip("/")).resolve()
        if candidate_studio.is_relative_to(STUDIO_DIR.resolve()) and candidate_studio.is_file():
            self._serve_file(STUDIO_DIR, path)
            return

        # De lo contrario servir desde WEB_DIR (assets/logo/..., css/styles.css, index.html, etc.)
        self._serve_file(pub.WEB_DIR, path)

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            body = json.loads(raw_body)
        except Exception as exc:
            self._send_json({"error": f"JSON inválido: {exc}"}, status=400)
            return

        try:
            if path == "/api/build":
                code, out = capture_cmd(pub.cmd_build)
                self._send_json({"ok": code == 0, "output": out}, status=200 if code == 0 else 500)
                return

            if path == "/api/audit":
                code, out = capture_cmd(pub.cmd_audit)
                self._send_json({"ok": code == 0, "output": out}, status=200 if code == 0 else 400)
                return

            if path == "/api/deploy":
                ns = argparse.Namespace(msg=body.get("msg"))
                code, out = capture_cmd(pub.cmd_deploy, ns)
                self._send_json({"ok": code == 0, "output": out}, status=200)
                return

            if path == "/api/marketing":
                clean_mkt = {}
                for k, v in body.items():
                    if isinstance(v, list):
                        clean_mkt[k] = [
                            pub.strip_dangerous_unicode(str(i)).strip()[:80]
                            for i in v
                            if str(i).strip()
                        ][:8]
                    else:
                        clean_mkt[k] = pub.strip_dangerous_unicode(str(v)).strip()[:500]
                pub.MARKETING_JSON.write_text(
                    json.dumps(clean_mkt, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                code, out = capture_cmd(pub.cmd_build)
                self._send_json({"ok": code == 0, "output": out})
                return

            if path == "/api/article":
                articles = (
                    json.loads(pub.ARTICLES_JSON.read_text(encoding="utf-8"))
                    if pub.ARTICLES_JSON.exists()
                    else []
                )
                title = pub.strip_dangerous_unicode(str(body.get("title", "Nueva Guía"))).strip()
                slug = pub.sanitize_slug(body.get("slug", ""), title)
                cat = pub.strip_dangerous_unicode(str(body.get("category", "Bienestar y Juegos")))
                if cat not in pub.ALLOWED_ARTICLE_CATEGORIES:
                    cat = "Bienestar y Juegos"
                defaults = pub.CATEGORY_DEFAULTS[cat]

                sections = body.get("sections", [])
                body_html, toc = pub.build_body_from_sections(sections)

                art_obj = {
                    "id": pub.strip_dangerous_unicode(str(body.get("id") or f"art-{len(articles)+1:02d}")),
                    "slug": slug,
                    "title": title,
                    "subtitle": pub.strip_dangerous_unicode(str(body.get("subtitle") or body.get("excerpt", ""))).strip(),
                    "excerpt": pub.strip_dangerous_unicode(str(body.get("excerpt", ""))).strip(),
                    "category": cat,
                    "readTime": pub.strip_dangerous_unicode(str(body.get("readTime", "7 min de lectura"))).strip(),
                    "date": pub.strip_dangerous_unicode(str(body.get("date", ""))).strip(),
                    "author": pub.strip_dangerous_unicode(str(body.get("author", "Equipo Editorial"))).strip(),
                    "authorRole": pub.strip_dangerous_unicode(str(body.get("authorRole", "Perritos Felices"))).strip(),
                    "emoji": defaults["emoji"],
                    "topbarTag": defaults["topbarTag"],
                    "sectionTag": defaults["sectionTag"],
                    "bgGradient": defaults["bgGradient"],
                    "featured": bool(body.get("featured", False)),
                    "toc": toc,
                    "bodyHtml": body_html,
                }

                if art_obj["featured"]:
                    for a in articles:
                        a["featured"] = False

                replaced = False
                for idx, existing in enumerate(articles):
                    if existing.get("slug") == slug or existing.get("id") == art_obj["id"]:
                        art_obj["bgGradient"] = existing.get("bgGradient", defaults["bgGradient"])
                        art_obj["emoji"] = existing.get("emoji", defaults["emoji"])
                        articles[idx] = art_obj
                        replaced = True
                        break
                if not replaced:
                    articles.insert(0, art_obj)

                pub.write_markdown_file(art_obj)
                pub.ARTICLES_JSON.write_text(
                    json.dumps(articles, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                code, out = capture_cmd(pub.cmd_build)
                self._send_json({"ok": code == 0, "slug": slug, "output": out})
                return

            if path == "/api/calendar":
                cal_list = body.get("calendar", [])
                clean_cal = []
                for idx, item in enumerate(cal_list, start=1):
                    clean_cal.append(
                        {
                            "id": pub.strip_dangerous_unicode(str(item.get("id") or f"cal-{idx:02d}")),
                            "status": pub.strip_dangerous_unicode(str(item.get("status", "pendiente"))),
                            "title": pub.strip_dangerous_unicode(str(item.get("title", ""))).strip(),
                            "category": pub.strip_dangerous_unicode(str(item.get("category", "Bienestar y Juegos"))).strip(),
                            "author": "Equipo Editorial",
                            "authorRole": "Perritos Felices",
                            "targetAudience": pub.strip_dangerous_unicode(str(item.get("targetAudience", ""))).strip(),
                            "keywords": [
                                pub.strip_dangerous_unicode(str(k)).strip()
                                for k in (item.get("keywords") or [])
                                if str(k).strip()
                            ],
                        }
                    )
                pub.CALENDAR_JSON.write_text(
                    json.dumps(clean_cal, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                self._send_json({"ok": True})
                return

            if path == "/api/directory":
                directory = (
                    json.loads(pub.DIRECTORY_JSON.read_text(encoding="utf-8"))
                    if pub.DIRECTORY_JSON.exists()
                    else []
                )
                biz_id = pub.strip_dangerous_unicode(str(body.get("id") or f"dir-{len(directory)+1:02d}")).strip()
                new_biz = {
                    "id": biz_id,
                    "name": pub.strip_dangerous_unicode(str(body.get("name", ""))).strip()[:100],
                    "category": pub.strip_dangerous_unicode(str(body.get("category", "Veterinaria y Salud"))).strip(),
                    "city": pub.strip_dangerous_unicode(str(body.get("city", "Ciudad de Guatemala"))).strip()[:60],
                    "rating": min(max(round(float(body.get("rating", 5.0)), 1), 1.0), 5.0),
                    "reviews": max(int(body.get("reviews", 10)), 1),
                    "verified": bool(body.get("verified", True)),
                    "emoji": pub.strip_dangerous_unicode(str(body.get("emoji", "🏥"))).strip()[:8],
                    "description": pub.strip_dangerous_unicode(str(body.get("description", ""))).strip()[:400],
                    "address": pub.strip_dangerous_unicode(str(body.get("address", ""))).strip()[:180],
                    "phone": pub.strip_dangerous_unicode(str(body.get("phone", ""))).strip()[:32],
                    "hours": pub.strip_dangerous_unicode(str(body.get("hours", ""))).strip()[:80],
                    "highlights": [
                        pub.strip_dangerous_unicode(str(h)).strip()[:60]
                        for h in (body.get("highlights") or [])
                        if str(h).strip()
                    ][:4]
                    or ["Trato Amable Verificado"],
                }

                replaced = False
                for idx, existing in enumerate(directory):
                    if existing.get("id") == biz_id:
                        directory[idx] = new_biz
                        replaced = True
                        break
                if not replaced:
                    directory.append(new_biz)

                pub.DIRECTORY_JSON.write_text(
                    json.dumps(directory, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                code, out = capture_cmd(pub.cmd_build)
                self._send_json({"ok": code == 0, "id": biz_id, "output": out})
                return

            if path == "/api/directory/delete":
                target_id = str(body.get("id", "")).strip()
                directory = (
                    json.loads(pub.DIRECTORY_JSON.read_text(encoding="utf-8"))
                    if pub.DIRECTORY_JSON.exists()
                    else []
                )
                directory = [b for b in directory if b.get("id") != target_id]
                pub.DIRECTORY_JSON.write_text(
                    json.dumps(directory, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8",
                )
                code, out = capture_cmd(pub.cmd_build)
                self._send_json({"ok": code == 0, "output": out})
                return

            if path == "/api/shutdown":
                self._send_json({"ok": True})
                import threading
                threading.Thread(target=self.server.shutdown, daemon=True).start()
                return

            self._send_json({"error": "Ruta API no reconocida"}, status=404)
        except Exception as exc:
            self._send_json({"error": str(exc)}, status=500)


class ReuseAddrHTTPServer(HTTPServer):
    allow_reuse_address = True


def main():
    parser = argparse.ArgumentParser(description="Servidor Visual — Perritos Felices Studio")
    parser.add_argument("--port", type=int, default=8765, help="Puerto local (por defecto 8765)")
    parser.add_argument("--no-browser", action="store_true", help="No abrir el navegador automáticamente")
    args = parser.parse_args()

    port = args.port
    server = None
    for candidate in (port, 8766, 8767):
        try:
            server = ReuseAddrHTTPServer(("127.0.0.1", candidate), StudioRequestHandler)
            port = candidate
            break
        except OSError:
            continue

    if server is None:
        print(f"✔ Perritos Felices Studio ya está activo en http://127.0.0.1:{args.port}")
        if not args.no_browser:
            webbrowser.open(f"http://127.0.0.1:{args.port}")
        return

    url = f"http://127.0.0.1:{port}"
    print("=================================================================")
    print(" 🐾 PERRITOS FELICES STUDIO — MINI-APP VISUAL ACTIVA")
    print("=================================================================")
    print(f" 🌐 Panel de Control : {url}")
    print(f" 🖥️  Sitio en Vivo    : {url}/site/index.html")
    print(" 🔒 Seguridad        : 100% Local (127.0.0.1) + Zero-Trust CSP")
    print("=================================================================")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Cerrando Perritos Felices Studio.")
        server.server_close()


if __name__ == "__main__":
    main()
