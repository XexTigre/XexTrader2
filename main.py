import os
import time
import random
import requests
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask

TOKEN = os.getenv('TOKEN')  # seu token no config var do Heroku
CANAL_ID = -1002873312101   # coloque seu ID do canal aqui (com -100 na frente)

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot está online!", 200

def enviar(texto):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    data = {
        'chat_id': CANAL_ID,
        'text': texto,
        'parse_mode': 'Markdown'
    }
    resp = requests.post(url, data=data)
    if not resp.ok:
        print(f"Erro ao enviar mensagem: {resp.text}")
    else:
        print("✅ Mensagem enviada com sucesso!")

def aguardar_ate(horario):
    while True:
        agora = datetime.now()
        diff = (horario - agora).total_seconds()
        if diff <= 0:
            break
        time.sleep(min(diff, 1))

def ciclo():
    while True:
        agora = datetime.now()
        espera = random.randint(1, 2)
        inicio_jogo = agora + timedelta(minutes=espera)
        fim_jogo = inicio_jogo + timedelta(minutes=2)
        aviso = inicio_jogo - timedelta(minutes=1)

        print(f"⏳ Próximo sinal às {aviso.strftime('%H:%M')} → jogo de {inicio_jogo.strftime('%H:%M')} até {fim_jogo.strftime('%H:%M')}")

        aguardar_ate(aviso)
        enviar(
            f'🚨 *SINAL DETECTADO!*\n\n'
            f'🎰 *Jogue entre:* ⏱️ {inicio_jogo.strftime("%H:%M")} – {fim_jogo.strftime("%H:%M")}\n\n'
            '🔥 *Preparado? Vai que é tua, TIGREIRO!*'
        )

        aguardar_ate(fim_jogo)
        aguardar_ate(fim_jogo + timedelta(minutes=3))
        enviar(
            '💬 *E aí tropa, quem pegou o sinal?*\n'
            '🐾 Comenta aí se deu bom!'
        )

        time.sleep(random.randint(60, 300))

if __name__ == '__main__':
    Thread(target=ciclo, daemon=True).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
