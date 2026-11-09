#!/usr/bin/env python3
"""
PERRITOS FELICES — BOT DE TELEGRAM PARA APROBACIÓN REMOTA (REGLA DEL 10%)
Protocolo Zero-Trust: Cero Puertos Expuestos (Long Polling saliente)
Cero dependencias externas (Python 3 urllib estándar)

Permite a Luis y su pareja:
  • Recibir notificaciones instantáneas de nuevas cápsulas, artes 4:5 y videos 9:16
  • Aprobar piezas con 1 clic desde el chat de Telegram
  • Abrir el visor interactivo de pines/anotaciones para solicitar cambios
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

# Directorio raíz del proyecto
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
APROBACIONES_FILE = ROOT_DIR / "05_Studio_Privado" / "aprobaciones_state.json"

# Configuración Segura (Cero credenciales en el repo de Drive)
# Se busca en variables de entorno o en ~/.perritos_felices_telegram.json
EXTERNAL_CONFIG = Path.home() / ".perritos_felices_telegram.json"


def load_bot_credentials():
    """Carga credenciales desde variables de entorno o ~/.perritos_felices_telegram.json"""
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    allowed_users = os.environ.get("TELEGRAM_ALLOWED_USERS", "")
    allowed_list = [int(u.strip()) for u in allowed_users.split(",") if u.strip().isdigit()]

    if not token and EXTERNAL_CONFIG.exists():
        try:
            data = json.loads(EXTERNAL_CONFIG.read_text(encoding="utf-8"))
            token = data.get("bot_token")
            allowed_list = data.get("allowed_users", allowed_list)
        except Exception:
            pass

    return token, allowed_list


def api_request(token, method, payload=None):
    """Ejecuta una petición a la API de Telegram vía urllib estándar"""
    url = f"https://api.telegram.org/bot{token}/{method}"
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload).encode("utf-8") if payload else None

    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=35) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        print(f"[Telegram API Error {e.code}] {error_msg}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[Telegram Network Error] {e}", file=sys.stderr)
        return None


def get_aprobaciones():
    """Lee el archivo de estado de aprobaciones"""
    if APROBACIONES_FILE.exists():
        try:
            return json.loads(APROBACIONES_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"items": []}


def save_aprobaciones(data):
    """Guarda el archivo de estado de aprobaciones de forma atómica"""
    data["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    temp_file = APROBACIONES_FILE.with_suffix(".tmp")
    temp_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    temp_file.replace(APROBACIONES_FILE)


def send_message(token, chat_id, text, reply_markup=None):
    """Envía un mensaje con formato HTML y teclado opcional"""
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return api_request(token, "sendMessage", payload)


def handle_update(token, update, allowed_users):
    """Procesa una actualización de Telegram (mensaje o callback de botón)"""
    # Manejo de Callback Queries (Clics en botones inline)
    if "callback_query" in update:
        cb = update["callback_query"]
        user_id = cb.get("from", {}).get("id")
        chat_id = cb.get("message", {}).get("chat", {}).get("id")
        cb_id = cb.get("id")
        data = cb.get("data", "")

        # Verificación Zero-Trust de usuario autorizado
        if allowed_users and user_id not in allowed_users:
            api_request(token, "answerCallbackQuery", {"callback_query_id": cb_id, "text": "Acceso no autorizado."})
            return

        if data.startswith("aprobar:"):
            pieza_id = data.split(":", 1)[1]
            aprobaciones = get_aprobaciones()
            for it in aprobaciones.get("items", []):
                if it.get("id") == pieza_id:
                    it["estado"] = "aprobado"
                    it["aprobado_por"] = f"Telegram User {user_id}"
                    it["fecha_aprobacion"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                    save_aprobaciones(aprobaciones)
                    api_request(token, "answerCallbackQuery", {
                        "callback_query_id": cb_id,
                        "text": "✔ Pieza aprobada exitosamente."
                    })
                    send_message(token, chat_id, f"✅ <b>Pieza Aprobada:</b> {it.get('titulo')}\n\n<i>Queda lista para despliegue en Netlify/GitHub.</i>")
                    return

        elif data == "cmd:pendientes":
            api_request(token, "answerCallbackQuery", {"callback_query_id": cb_id})
            send_pendientes(token, chat_id)
            return

    # Manejo de Mensajes de Texto
    message = update.get("message", {})
    user_id = message.get("from", {}).get("id")
    chat_id = message.get("chat", {}).get("id")
    text = (message.get("text") or "").strip()

    if not chat_id or not text:
        return

    # Verificación Zero-Trust: si hay lista blanca configurada y el usuario no está, ignorar
    if allowed_users and user_id not in allowed_users:
        print(f"[Zero-Trust Guard] Intento de acceso bloqueado desde User ID: {user_id}")
        return

    if text.startswith("/start") or text.startswith("/menu"):
        menu_text = (
            "🐶 <b>Perritos Felices Studio — Aprobación Remota (Regla del 10%)</b>\n\n"
            "Bienvenido Luis. Desde aquí puedes aprobar artes, videos 9:16 y cápsulas web sin necesidad de encender tu Mac.\n\n"
            "Elige una opción:"
        )
        keyboard = {
            "inline_keyboard": [
                [{"text": "📋 Ver Piezas Pendientes", "callback_data": "cmd:pendientes"}],
                [{"text": "📍 Abrir Visor de Feedback Visual", "url": "https://www.perritosfelices.com/aprobacion"}]
            ]
        }
        send_message(token, chat_id, menu_text, keyboard)

    elif text.startswith("/pendientes"):
        send_pendientes(token, chat_id)

    elif text.startswith("/aprobar"):
        parts = text.split(maxsplit=1)
        if len(parts) > 1:
            pieza_id = parts[1].strip()
            aprobaciones = get_aprobaciones()
            encontrado = False
            for it in aprobaciones.get("items", []):
                if it.get("id") == pieza_id:
                    it["estado"] = "aprobado"
                    it["aprobado_por"] = f"Telegram User {user_id}"
                    it["fecha_aprobacion"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                    save_aprobaciones(aprobaciones)
                    encontrado = True
                    send_message(token, chat_id, f"✅ <b>Pieza Aprobada:</b> {it.get('titulo')}")
                    break
            if not encontrado:
                send_message(token, chat_id, f"❌ No se encontró la pieza con ID: <code>{pieza_id}</code>")
        else:
            send_message(token, chat_id, "ℹ Uso: <code>/aprobar &lt;id_de_pieza&gt;</code>")


def send_pendientes(token, chat_id):
    """Envía la lista de piezas pendientes con botones inline de acción directa"""
    aprobaciones = get_aprobaciones()
    pendientes = [it for it in aprobaciones.get("items", []) if it.get("estado") == "pendiente"]

    if not pendientes:
        send_message(token, chat_id, "🎉 <b>¡Todo al día!</b> No hay piezas pendientes de aprobación por ahora.")
        return

    for it in pendientes:
        p_id = it.get("id")
        titulo = it.get("titulo")
        tipo = it.get("tipo", "").replace("_", " ").upper()
        pines = len(it.get("pines", []))

        msg = (
            f"⚡ <b>Pieza Pendiente:</b> [{tipo}]\n"
            f"📌 <b>Título:</b> {titulo}\n"
            f"📍 <b>Notas de cambio activas:</b> {pines}\n"
            f"🆔 <code>{p_id}</code>"
        )
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "✅ Aprobar", "callback_data": f"aprobar:{p_id}"},
                    {"text": "🔍 Revisar Pines", "url": "https://www.perritosfelices.com/aprobacion"}
                ]
            ]
        }
        send_message(token, chat_id, msg, keyboard)


def run_bot_polling(token, allowed_users):
    """Bucle principal de Long Polling (Cero puertos entrantes abiertos)"""
    print(f"🤖 Bot de Telegram Perritos Felices iniciado con Long Polling...")
    print(f"🛡️  Zero-Trust: 0 puertos expuestos al exterior. Usuarios autorizados: {allowed_users or 'Modo abierto / sin restricción'}")

    offset = None
    while True:
        try:
            payload = {"timeout": 30}
            if offset:
                payload["offset"] = offset

            updates_res = api_request(token, "getUpdates", payload)
            if updates_res and updates_res.get("ok"):
                for upd in updates_res.get("result", []):
                    offset = upd["update_id"] + 1
                    handle_update(token, upd, allowed_users)

        except KeyboardInterrupt:
            print("\nDeteniendo bot...")
            break
        except Exception as e:
            print(f"[Polling Error] {e}", file=sys.stderr)
            time.sleep(3)


def main():
    parser = argparse.ArgumentParser(description="Bot de Telegram para Aprobación Remota de Perritos Felices")
    parser.add_argument("--test", action="store_true", help="Comprueba la conectividad con la API de Telegram y sale")
    parser.add_argument("--status", action="store_true", help="Muestra el estado de piezas pendientes en la base de datos")
    args = parser.parse_args()

    if args.status:
        data = get_aprobaciones()
        items = data.get("items", [])
        print(f"Total piezas registradas: {len(items)}")
        for it in items:
            print(f"  • [{it.get('estado').upper()}] {it.get('id')}: {it.get('titulo')}")
        return

    token, allowed_users = load_bot_credentials()

    if not token:
        print("ℹ AVISO: No se detectó TELEGRAM_BOT_TOKEN en variables de entorno ni en ~/.perritos_felices_telegram.json.")
        print("  El script está listo. Para activarlo cuando desees en tu Mac o en Oracle Cloud Always Free:")
        print("  1. Guarda tu token en ~/.perritos_felices_telegram.json:")
        print('     {"bot_token": "TU_BOT_TOKEN", "allowed_users": [TU_TELEGRAM_ID]}')
        print("  2. Ejecuta: python3 01_Infraestructura_Web/scripts/telegram_approval_bot.py")
        return

    if args.test:
        me = api_request(token, "getMe")
        if me and me.get("ok"):
            bot_info = me["result"]
            print(f"✔ Conectado exitosamente al bot @{bot_info.get('username')} ({bot_info.get('first_name')})")
        else:
            print("❌ No se pudo conectar a la API de Telegram con el token proporcionado.")
        return

    run_bot_polling(token, allowed_users)


if __name__ == "__main__":
    main()
