#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ANÁLISIS ORO BOT - Publicador automático a Telegram
Publica análisis de XAUUSD en @analisis_oro_nesti
"""

import requests
import os
from datetime import datetime
from flask import Flask

# Configuración
TOKEN = os.getenv("TELEGRAM_TOKEN", "892167144:AAEVUVa0DoUK3sDBZJ_BIynt1XPpDsnz_jpw")
CHAT_ID = os.getenv("CHAT_ID", "-1002366945826")
API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

app = Flask(__name__)

def publicar_mensaje(titulo, contenido):
    """Publica un mensaje en el canal de Telegram"""
    mensaje = f"""{titulo}
═══════════════════════════════
{contenido}

#ORO #XAUUSD #Trading
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    data = {
        "chat_id": CHAT_ID,
        "text": mensaje,
        "parse_mode": "HTML"
    }

    try:
        response = requests.post(API_URL, json=data, timeout=10)
        print(f"✅ Mensaje publicado: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def apertura_londres():
    """Publica análisis de apertura Londres 08:00 GMT"""
    titulo = "🇬🇧 APERTURA LONDRES - XAUUSD"
    contenido = """⏰ Hora: 08:00 GMT
📊 Análisis técnico: Identifica levels clave, resistencias y soportes
💡 Señal operativa: Dirección probable y entrada recomendada
🎯 Objetivos: Take profit y stop loss"""
    return publicar_mensaje(titulo, contenido)

def preapertura_ny():
    """Publica análisis pre-apertura NY 14:15 UTC"""
    titulo = "🗽 PRE-APERTURA NY - XAUUSD"
    contenido = """⏰ Hora: 14:15 UTC
📊 Análisis técnico: Momentum, niveles clave, perspectiva del día
💡 Señal operativa: Estrategia para la sesión NY
🎯 Niveles críticos y setup potencial"""
    return publicar_mensaje(titulo, contenido)

def cierre_ny():
    """Publica análisis de cierre NY 22:00 UTC"""
    titulo = "📊 CIERRE NY - XAUUSD"
    contenido = """⏰ Hora: 22:00 UTC
📈 Resumen del día: Dirección, volatilidad, movimiento principal
💡 Análisis técnico del cierre: Levels finales, cierre significativo
🎯 Perspectiva para mañana: Setups potenciales
⚠️ Avisos: Eventos económicos próximos, riesgos"""
    return publicar_mensaje(titulo, contenido)

@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok', 'bot': 'analisis-oro', 'timestamp': datetime.now().isoformat()}, 200

@app.route('/cron/apertura-londres', methods=['POST'])
def cron_apertura_londres():
    apertura_londres()
    return {'status': 'ok', 'action': 'apertura-londres'}, 200

@app.route('/cron/preapertura-ny', methods=['POST'])
def cron_preapertura_ny():
    preapertura_ny()
    return {'status': 'ok', 'action': 'preapertura-ny'}, 200

@app.route('/cron/cierre-ny', methods=['POST'])
def cron_cierre_ny():
    cierre_ny()
    return {'status': 'ok', 'action': 'cierre-ny'}, 200

@app.route('/test', methods=['POST'])
def test():
    apertura_londres()
    return {'status': 'ok', 'action': 'test'}, 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
