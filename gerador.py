import os
import json
import random
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
import google.generativeai as genai

# 1. Configuração da API Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 2. Tratamento de Datas
hoje_dt = datetime.now()
data_amigavel = hoje_dt.strftime("%d%m%Y")  # Ex: 12102026

dias_semana = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
data_extenso = f"{dias_semana[hoje_dt.weekday()]}, {hoje_dt.day} de {meses[hoje_dt.month - 1]} de {hoje_dt.year}"

# 3. Leitura Segura de Notícias do Brasil (Termômetro Social)
def obter_termometro_noticias():
    try:
        url = "https://g1.globo.com/rss/g1/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        xml_data = urllib.request.urlopen(req, timeout=6).read()
        root = ET.fromstring(xml_data)
        titulos = [item.find('title').text for item in root.findall('./channel/item')[:6]]
        return "\n".join([f"- {t.strip()}" for t in titulos if t])
    except Exception as e:
        print(f"Aviso ao consultar notícias: {e}")
        return "- Dia a dia dos trabalhadores e famílias brasileiras com foco em saúde, trabalho e perseverança."

noticias_contexto = obter_termometro_noticias()

# 4. Matriz com 12 Eixos Temáticos Anti-Repetição
ANGULOS = [
    {"tema": "Acolhimento da Mente e Serenidade", "diretriz": "Foque no silêncio, em desacelerar pensamentos e esvaziar preocupações acumuladas."},
    {"tema": "Gratidão Simples pelas Pequenas Coisas", "diretriz": "Foque na bênção da saúde, do teto, do pão à mesa e da vida que continua."},
    {"tema": "Proteção, Firmeza e Blindagem do Lar", "diretriz": "Foque na oração como escudo para a família contra atritos ou notícias pesadas lá fora."},
    {"tema": "Paciência, Confiança e o Tempo Certo", "diretriz": "Foque na sabedoria de esperar o momento certo e na entrega das causas difíceis."},
    {"tema": "União Familiar e Bênção aos Filhos e Netos", "diretriz": "Foque em abençoar os passos dos mais jovens, no convívio pacífico e no afeto."},
    {"tema": "Alívio da Solidão e Conforto do Coração", "diretriz": "Foque no acolhimento de quem se sente só, trazendo a presença de Deus como amparo."},
    {"tema": "Sabedoria nas Palavras e Paz nos Relacionamentos", "diretriz": "Foque no valor do silêncio sábio, de não revidar ofensas e de manter a calma no lar."},
    {"tema": "Renovação das Forças Físicas e Saúde", "diretriz": "Foque no alívio do corpo cansado, nas dores físicas e no ânimo para mais uma jornada."},
    {"tema": "Entrega das Incertezas do Amanhã", "diretriz": "Foque em vencer a ansiedade com o futuro e com as contas, confiando na providência."},
    {"tema": "A Força da Intercessão e Oração Silenciosa", "diretriz": "Foque no poder da prece feita no quarto em favor de quem amamos."},
    {"tema": "Misericórdia e Perdão para Recomeçar", "diretriz": "Foque na leveza de não carregar culpas de erros passados e na chance de um novo dia."},
    {"tema": "Alegria Serena e Gentileza com o Próximo", "diretriz": "Foque na beleza de espalhar palavras doces e ser um ponto de paz para os outros."}
]

# Rotação temática diária baseada no dia do ano
angulo_hoje = ANGULOS[hoje_dt.timetuple().tm_yday % len(ANGULOS)]

# 5. Seleção de Imagem do Acervo
imagens_dir = "imagens"
todas_imagens = [f for f in os.listdir(imagens_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(imagens_dir) else []
imagem_escolhida = random.choice(todas_imagens) if todas_imagens else "1.png"

# 6. Chamada à IA
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"""
Você é um escritor devocional sênior brasileiro que escreve para mães, avós e famílias no WhatsApp.
Data de hoje: {data_extenso}.
Eixo temático obrigatório de hoje: {angulo_hoje['tema']}.
Diretriz específica: {angulo_hoje['diretriz']}.

NOTÍCIAS RECENTES NO BRASIL (Use apenas como termômetro de sentimento coletivo da sociedade):
{noticias_contexto}

REGRAS EDITORIAIS RIGOROSAS:
1. TEMPERO DE ATUALIDADES: Demonstre que você vive a realidade do Brasil hoje (compreende o custo de vida, a correria, as aflições ou o cansaço que estão no ar), mas NUNCA cite nomes de políticos, partidos, marcas ou tragédias violentas específicas.
2. DUPLO OLHAR SOBRE ONTEM: Não afirme que ontem foi um dia pesado para todos. Acolha quem venceu (com gratidão) e quem lutou com cansaço (com alívio e renovação).
3. PROIBIÇÃO CLIMÁTICA: NÃO mencione chuva, frio, calor ou sol forte (o Brasil tem climas diferentes e isso gera ruído).
4. ANTI-CLICHÊ: NÃO inicie com frases gastas como "coloque a chaleira no fogo", "respire fundo", "uma folha em branco" ou "a dádiva de acordar". Varie a metáfora.
5. PRECE ROBUSTA: A oração deve ser comovente, maternal e em primeira pessoa do singular, pedindo paz, saúde e proteção para o lar.

Retorne EXCLUSIVAMENTE um JSON puro no seguinte formato:
{{
  "chamada_zap": "Chamada magnética e curta (máximo 3 linhas) para legenda do WhatsApp que toque no sentimento atual e convide para a oração de hoje",
  "titulo": "Título reconfortante e autêntico",
  "paragrafos": [
    "Primeiro parágrafo: acolhimento da transição de ontem para hoje sob o eixo temático, demonstrando sintonia com a realidade do dia a dia.",
    "Segundo parágrafo: reflexão profunda com sabedoria prática sobre a serenidade no lar e a confiança em Deus.",
    "Terceiro parágrafo: palavras de ânimo, firmeza espiritual e calma para conduzir a família hoje."
  ],
  "oracao": "Prece profunda e comovente em primeira pessoa, blindando a família, pedindo saúde e paz no coração.",
  "versiculo": "Citação bíblica de esperança adequada ao tema de hoje com livro, capítulo e versículo"
}}
"""

try:
    response = model.generate_content(prompt)
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    conteudo = json.loads(raw_text)
except Exception as e:
    print(f"Erro na chamada da API Gemini: {e}. Usando texto de segurança.")
    conteudo = {
        "chamada_zap": "🌸☕ Em meio a tantas correrias e notícias lá fora, que a nossa casa escolha a paz e a confiança hoje.",
        "titulo": "A Certeza que Abriga o Nosso Lar",
        "paragrafos": [
            "Se o dia de ontem trouxe vitórias, que a nossa gratidão permaneça viva. Se trouxe cansaço ou preocupações com os nossos passos, que a certeza da proteção divina renove as forças neste amanhecer.",
            "O mundo lá fora muitas vezes se enche de ruído e incertezas, mas a sabedoria da vida nos ensina a cuidar daquilo que está ao nosso alcance: o afeto da família, o pão compartilhado e a calma no coração.",
            "Que o dia de hoje seja conduzido com paciência e fé inabalável, sabendo que cada oração sincera abre caminhos de amparo para os que amamos."
        ],
        "oracao": "Senhor, estende a Tua mão sobre a nossa mesa e sobre a saúde da minha família. Afasta qualquer discórdia e inquietação do nosso lar e concede-nos um dia sereno debaixo da Tua graça. Amém!",
        "versiculo": "O Senhor é o meu refúgio e a minha fortaleza, o meu Deus, em quem confio. — Salmos 91:2"
    }

# 7. Carrega o Molde HTML
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

reflexao_html = "".join([f"<p>{p}</p>" for p in conteudo["paragrafos"]])

# 8. Monta a Página da Subpasta do Dia (/11102026/index.html)
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

# 9. Monta e Atualiza a Página Inicial da Raiz (index.html)
html_raiz = html_subpasta.replace(f"../imagens/{imagem_escolhida}", f"./imagens/{imagem_escolhida}")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_raiz)

# 10. Salva o Texto Formatado para Envio Rápido no WhatsApp
msg_zap = f"""🌸☕ BOM DIA COM PAZ E BÊNÇÃO! ☕🌸

{conteudo['chamada_zap']}

📖 Leia a oração do lar completa e pegue a bênção de hoje:
👉 https://fabiowakisaka.github.io/amanhecerfeliz/{data_amigavel}/"""

with open("mensagem_hoje.txt", "w", encoding="utf-8") as f:
    f.write(msg_zap)

print(f"Sucesso: Páginas atualizadas para {data_amigavel} sob o eixo '{angulo_hoje['tema']}'!")
