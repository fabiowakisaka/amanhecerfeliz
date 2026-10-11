import os
import json
import random
from datetime import datetime
import google.generativeai as genai

# Configuração da API
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Datas
hoje_dt = datetime.now()
data_amigavel = hoje_dt.strftime("%d%m%Y")  # Ex: 12102026

dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
data_extenso = f"{dias_semana[hoje_dt.weekday()]}, {hoje_dt.day} de {meses[hoje_dt.month - 1]} de {hoje_dt.year}"

# Escolha da Imagem
imagens_dir = "imagens"
todas_imagens = [f for f in os.listdir(imagens_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
imagem_escolhida = random.choice(todas_imagens) if todas_imagens else "1.png"

# Chamada à IA
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"""
És um redator dedicado a mensagens matinais de carinho, paz e oração para senhoras de idade no WhatsApp.
Data de hoje: {data_extenso}.

Gera um JSON rigoroso com este formato:
{{
  "chamada_zap": "Texto curto chamando para deixar o cansaço para trás com emojis",
  "titulo": "Título reconfortante e caloroso",
  "paragrafos": [
    "Primeiro parágrafo de acolhimento e reflexão de amanhecer.",
    "Segundo parágrafo ligando a serenidade do café ao cuidado do lar.",
    "Terceiro parágrafo inspirando confiança e paciência."
  ],
  "oracao": "Oração sincera, simples e curta em primeira pessoa pedindo paz, saúde e bênçãos para o lar.",
  "versiculo": "Livro e citação bíblica de esperança"
}}

Regras: Retorna APENAS o JSON puro, sem blocos markdown adicionais como ```json.
"""

try:
    response = model.generate_content(prompt)
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    conteudo = json.loads(raw_text)
except Exception as e:
    print(f"Erro ao chamar API, recorrendo ao padrão de segurança: {e}")
    conteudo = {
        "chamada_zap": "Deixe o cansaço para trás e comece o dia com paz.",
        "titulo": "A Renovação das Forças neste Amanhecer",
        "paragrafos": [
            "A cada manhã recebemos um presente silencioso: a oportunidade de recomeçar com calma e gratidão.",
            "Coloque o café no fogo, respire fundo e entregue as preocupações. O dia de hoje trará as suas próprias bênçãos."
        ],
        "oracao": "Senhor, abençoa este amanhecer, guarda a minha família, protege o meu lar e dá-me saúde e tranquilidade para caminhar. Amém!",
        "versiculo": "O choro pode durar uma noite, mas a alegria vem pela manhã. — Salmos 30:5"
    }

# Montagem do HTML
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

reflexao_html = "".join([f"<p>{p}</p>" for p in conteudo["paragrafos"]])

# 1. Página da subpasta (ex: /12102026/index.html)
html_subpasta = template \
    .replace("{{TITULO}}", conteudo["titulo"]) \
    .replace("{{DATA_EXTENSO}}", data_extenso) \
    .replace("{{CHAMADA_ZAP}}", conteudo["chamada_zap"]) \
    .replace("{{IMAGEM_PATH}}", f"imagens/{imagem_escolhida}") \
    .replace("{{IMAGEM_SRC}}", f"../imagens/{imagem_escolhida}") \
    .replace("{{REFLEXAO_HTML}}", reflexao_html) \
    .replace("{{ORACAO}}", conteudo["oracao"]) \
    .replace("{{VERSICULO}}", conteudo["versiculo"])

os.makedirs(data_amigavel, exist_ok=True)
with open(f"{data_amigavel}/index.html", "w", encoding="utf-8") as f:
    f.write(html_subpasta)

# 2. Página inicial da raiz (index.html)
html_raiz = html_subpasta.replace(f"../imagens/{imagem_escolhida}", f"./imagens/{imagem_escolhida}")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_raiz)

# Registo da mensagem do WhatsApp para poder copiar facilmente
msg_zap = f"""🌸☕ BOM DIA COM PAZ E ESPERANÇA! ☕🌸

{conteudo['chamada_zap']}

📖 Leia a oração completa de hoje e pegue a sua bênção matinal:
👉 [https://www.amanhecerfeliz.com/](https://www.amanhecerfeliz.com/){data_amigavel}"""

with open("mensagem_hoje.txt", "w", encoding="utf-8") as f:
    f.write(msg_zap)

print(f"Páginas criadas com sucesso para {data_amigavel}!")
