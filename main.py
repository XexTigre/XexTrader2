import os
import time
import random
import requests
from datetime import datetime, timedelta
from threading import Thread
from flask import Flask
from zoneinfo import ZoneInfo  # Para fuso horário

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

def agora_brasilia():
    return datetime.now(ZoneInfo('America/Sao_Paulo'))

def aguardar_ate(horario):
    while True:
        agora = agora_brasilia()
        diff = (horario - agora).total_seconds()
        if diff <= 0:
            break
        time.sleep(min(diff, 1))

def ciclo():
    while True:
        agora = agora_brasilia()
        espera = random.randint(1, 2)
        inicio_jogo = agora + timedelta(minutes=espera)
        fim_jogo = inicio_jogo + timedelta(minutes=2)
        aviso = inicio_jogo - timedelta(minutes=1)

        # Mensagem 1: Validando Entrada (1 min antes do jogo)
        aguardar_ate(aviso)
        enviar(
            f'🔔 Validando Entrada 🔔\n\n'
            f'CADASTRE-SE ANTES DE JOGAR ➡️\n\n'
            f'[BETFURY](https://betfury.ac/?r=User9165603)\n'
            f'CLIQUE AQUI PARA JOGAR\n\n'
            f'💰Banca recomendada, acima de R$50,00\n'
            f'\n'
            f'Enviado às {aviso.strftime("%H:%M")}'
        )

        # Mensagem 2: Oportunidade Identificada (início do jogo)
        enviar(
            f'✅ OPORTUNIDADE IDENTIFICADA\n\n'
            f'🐯 Fortune Tiger 🐯\n'
            f'⏰ Válido até: {fim_jogo.strftime("%H:%M")}\n\n'
            f'👉 12x Normal\n'
            f'⚡ 7x Turbo\n\n'
            f'[BETFURY](https://betfury.ac/?r=User9165603)\n'
            f'CLIQUE AQUI PARA JOGAR'
        )

        # Aguarda o fim do jogo
        aguardar_ate(fim_jogo)

        # Mensagem 3: Sinal Finalizado (logo após o jogo)
        enviar(
            f'🍀 Sinal Finalizado 🍀\n'
            f'🐯 Fortune Tiger 🐯\n'
            f'🕑 Finalizado às: {fim_jogo.strftime("%H:%M")}'
        )

        # Aguarda entre 30 e 40 minutos antes da mensagem promocional
        espera_promo = random.randint(30, 40)
        proxima_promo = fim_jogo + timedelta(minutes=espera_promo)
        aguardar_ate(proxima_promo)

        # Mensagem 4: Promoção (sem sinal ativo)
        enviar(
            f'🚨ACABOU DE LANÇAR PLATAFORMA NOVA🚨\n\n'
            f'[BETFURY](https://betfury.ac/?r=User9165603)\n\n'
            f'CLIQUE AQUI PARA SE CADASTRAR\n\n'
            f'🚨FAÇA UM DEPÓSITO DE NO MÍNIMO 10 E MANDA UM PRINT DA CONTA COM O DEPÓSITO NESSE CONTATO @XEXTRADER PARA GANHAR UMA BANCA NO DOBRO DO VALOR DEPOSITADO!'
        )

        # Espera entre 1 a 5 minutos antes do próximo ciclo
        time.sleep(random.randint(60, 300))

if __name__ == '__main__':
    Thread(target=ciclo, daemon=True).start()
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
