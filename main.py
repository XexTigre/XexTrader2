import time
import random
import requests
from datetime import datetime, timedelta

TOKEN = '7841706687:AAH6PP7FYcSNt8fW3ElEkKKjQGTiDq3_BR0'
CANAL_ID = -1002873312101  # ✅ ID numérico com prefixo correto

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

def aguardar_ate(horario: datetime):
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

        print(f"⏳ Próximo sinal às {aviso.strftime('%H:%M:%S')} → jogo de {inicio_jogo.strftime('%H:%M:%S')} até {fim_jogo.strftime('%H:%M:%S')}")

        aguardar_ate(aviso)
        enviar(
            f'🚨 *ATENÇÃO TIGREIROS!* 🚨\n'
            f'🎯 *SINAL DETECTADO!*\n\n'
            f'💰 *HORÁRIO DO JOGO:* ⏱️ {inicio_jogo.strftime("%H:%M")}–{fim_jogo.strftime("%H:%M")}\n\n'
            '🔥 *Preparem-se!*'
        )

        aguardar_ate(fim_jogo)
        aguardar_ate(fim_jogo + timedelta(minutes=3))
        enviar(
            '🧐 *E aí, tropa?*\n'
            '🎰 *Alguém acertou o TIGRINHO?*\n\n'
            '💬 Comenta aí se pegou o sinal e se deu bom!\n'
            '📲 *Vamos ver quem tá com a sorte no dedo!* 🍀'
        )

        time.sleep(random.randint(1, 5) * 60)

if __name__ == '__main__':
    ciclo()
