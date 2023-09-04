import pandas as pd
import requests
import json
import random

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'


tabela_cliente = pd.read_csv("cliente.csv")
id_cliente = tabela_cliente['ClienteID'].tolist()
print(id_cliente)


def get_cliente(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else 'Requisição falhou ou usuario nao existe'


clientes = [clientes for id in id_cliente if (clientes := get_cliente(id)) is not None]
print(json.dumps(clientes, indent=2))


def generate_news(cliente):
    with open('mensagens.txt', 'r', encoding='utf-8') as arquivo:
        mensagens = arquivo.readlines()
    mensagem = random.choice(mensagens)
    texto = (f"{cliente['name']}, {mensagem}")
    return texto


def itera_news():
    for cliente in clientes:
        print("Oportunidades para você!")
        news = generate_news(cliente)
        print(news)
        cliente['news'].append({"description": news})


def update_cliente(cliente):
    response = requests.put(f"{sdw2023_api_url}/users/{cliente['id']}", json=cliente)
    return True if response.status_code == 200 else False


def itera_update():
    for cliente in clientes:
        #success = update_cliente(cliente)
        print(f"Cliente {cliente['name']} atualizado com sucesso!")


def executa_msg():
    itera_news()
    itera_update()


executa_msg()