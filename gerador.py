import os
import json
import random
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import google.generativeai as genai

# 1. Configuração da API Gemini
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 2. Tratamento de Datas (Estrutura AAAA/MM/DD para pastas)
hoje_dt = datetime.now()
caminho_pasta = hoje_dt.strftime("%Y/%m/%d")  # Ex: 2026/10/13
data_hoje_iso = hoje_dt.strftime("%Y-%m-%d")  # Ex: 2026-10-13 (Usado no Sitemap)

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

# 4. Matrizes de Variabilidade (O Motor Tridimensional de Caos Controlado)

# 4.1. Eixos Temáticos
ANGULOS = [
    {"tema": "O peso da segunda-feira", "diretriz": "Foque na preguiça natural e no peso de recomeçar a semana de trabalho."},
    {"tema": "O dinheiro que encurta", "diretriz": "Foque na ansiedade de pagar os boletos e fazer a compra do mês render."},
    {"tema": "Luto silencioso", "diretriz": "Foque na saudade de quem já partiu e na cadeira vazia à mesa."},
    {"tema": "Cansaço de cuidar", "diretriz": "Foque na exaustão de quem sempre cuida de todos na família e esquece de si."},
    {"tema": "Ingratidão e silêncio", "diretriz": "Foque na sabedoria de não responder a provocações no ambiente de trabalho ou em casa."},
    {"tema": "Alegria nas frestas", "diretriz": "Foque em perceber um momento minúsculo de paz no meio da turbulência do dia."},
    {"tema": "Paciência nas esperas", "diretriz": "Foque em manter a calma no trânsito, na fila do posto ou esperando uma notícia."},
    {"tema": "Preocupação com filhos", "diretriz": "Foque na entrega invisível de pedir proteção para os filhos que saem para o mundo."},
    {"tema": "Saúde e dores", "diretriz": "Foque nas dores no corpo, no joelho que estala, e na busca por ânimo físico."},
    {"tema": "Culpa pelo passado", "diretriz": "Foque no alívio de perdoar a si mesmo por erros antigos que não podem ser mudados."},
    {"tema": "Medo das notícias", "diretriz": "Foque na blindagem mental contra o excesso de tragédias da TV e do celular."},
    {"tema": "Gratidão pelo teto", "diretriz": "Foque no simples alívio de ter uma porta para trancar à noite e um colchão para deitar."},
    {"tema": "Amizades desgastadas", "diretriz": "Foque na aceitação de que algumas pessoas se afastam e isso faz parte da vida."},
    {"tema": "Desacelerar o relógio", "diretriz": "Foque na sensação de que o ano está voando e a urgência de viver o hoje."},
    {"tema": "A força do pão repartido", "diretriz": "Foque na beleza do pouco que, quando dividido com quem se ama, parece muito."}
]

# 4.2. Âncoras Sensoriais
ANCORAS_DOMESTICAS = [
    "o cheiro forte do pó de café recém-passado",
    "o barulho do motor do ônibus ou dos carros logo cedo lá fora",
    "o som da chave destrancando ou trancando o portão de casa",
    "a água fria batendo no rosto na pia do banheiro",
    "o pão na chapa ou a manteiga derretendo no café da manhã",
    "a vassoura encostada ou o pano de prato secando na pia",
    "o celular vibrando na mesa com as primeiras mensagens do dia",
    "o sapato sendo calçado para mais um dia de luta",
    "o cachorro latindo longe ou os passarinhos na janela",
    "o relógio marcando aquela hora da madrugada em que o sono foge",
    "a roupa balançando no varal com o vento da manhã",
    "a xícara quente esquentando a palma da mão"
]

# 4.3. Esqueletos Narrativos
ESQUELETOS = [
    "Inicie com uma constatação seca e direta. Exemplo: 'A verdade é que tem dias que a gente acorda já querendo que a noite chegue.'",
    "Inicie com uma pergunta franca para quem lê. Exemplo: 'Você também sentiu que a semana já começou exigindo demais da gente?'",
    "Inicie descrevendo primeiramente a cena física da [ÂNCORA], sem falar de sentimentos na primeira frase.",
    "Inicie usando a palavra 'Às vezes'. Exemplo: 'Às vezes o silêncio da casa fala mais alto que qualquer conselho.'",
    "Inicie confessando uma teimosia humana comum. Exemplo: 'A gente tem a mania feia de querer controlar até o que não é nosso.'",
    "Inicie com um tom de alívio. Exemplo: 'Graças a Deus a noite passou e o sol resolveu aparecer de novo para a nossa lida.'",
    "Inicie com um imperativo carinhoso. Exemplo: 'Deixa a pressa do lado de fora da porta só por um minuto hoje.'"
]

# Sorteios dinâmicos usando a data como semente fixa para o dia
random.seed(hoje_dt.strftime("%Y%m%d"))
angulo_hoje = random.choice(ANGULOS)
ancora_hoje = random.choice(ANCORAS_DOMESTICAS)
esqueleto_hoje = random.choice(ESQUELETOS)

# 5. Seleção de Imagem do Acervo
imagens_dir = "imagens"
todas_imagens = [f for f in os.listdir(imagens_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))] if os.path.exists(imagens_dir) else []
imagem_escolhida = random.choice(todas_imagens) if todas_imagens else "1.png"

# 6. Chamada à IA - Prompt Blindado e Neutro
model = genai.GenerativeModel("gemini-1.5-flash")

prompt = f"""
Você é a voz sábia e acolhedora de uma família brasileira, escrevendo no WhatsApp para pessoas queridas. 
O texto precisa soar como uma mensagem real repassada por um tio, uma avó ou um pai de família.
Portanto, seja NEUTRO EM GÊNERO ao falar de si mesmo (use "a gente", "nós", "quem cuida", evitando "eu estou cansada/cansado"). 

DADOS DO DIA:
- Contexto nacional de hoje: {noticias_contexto}
- Tema de hoje: {angulo_hoje['tema']} - {angulo_hoje['diretriz']}

REGRAS RÍGIDAS DE ENGENHARIA DE TEXTO (EVITE O "SOTAQUE DE IA"):
1. ATERRAMENTO OBRIGATÓRIO: Inicie o texto aplicando o seguinte molde: "{esqueleto_hoje}".
2. CENA VISUAL: Integre a seguinte imagem natural e sorrateiramente no primeiro parágrafo: "{ancora_hoje}".
3. ASSIMETRIA BRUTAL: Proibido fazer listas de três itens (ex: "paz, amor e luz" ou "escutar, entender e abraçar"). Intercale frases bem curtas (3 palavras) com frases um pouco mais longas.
4. GAFES DE IA (PROIBIDO USAR): jornada, tapeçaria, trama, inabalável, farol, resiliência, abraçar (sentido figurado), adentrar, dádiva, sublime, essência, tecer. Não use palavras difíceis ou poéticas demais. Use o português do dia a dia.
5. PRECE SIMPLES: A oração final deve ser coloquial, como alguém que senta na cama e fala baixo com Deus.

Retorne EXCLUSIVAMENTE um JSON puro:
{{
  "chamada_zap": "Chamada (máx 2 linhas) amigável, instigando a ler",
  "titulo": "Título com cara de reflexão diária (ex: O tempo de cada coisa)",
  "paragrafos": [
    "Parágrafo 1: A âncora visual e a constatação da vida.",
    "Parágrafo 2: A reflexão principal focada no tema, sem romantizar as dificuldades.",
    "Parágrafo 3: Fechamento curto e pé no chão."
  ],
  "oracao": "Oração (máx 4 linhas). Neutra em gênero, pedindo pelos nossos.",
  "versiculo": "Citação bíblica curta de embasamento com referência."
}}
"""

try:
    response = model.generate_content(prompt)
    raw_text = response.text.strip().replace("```json", "").replace("```", "").strip()
    conteudo = json.loads(raw_text)
except Exception as e:
    print(f"Erro na chamada da API Gemini: {e}. Usando texto de segurança.")
    conteudo = {
        "chamada_zap": "🌸☕ Em meio à correria, que a nossa casa escolha a paz hoje.",
        "titulo": "A Calma Possível",
        "paragrafos": [
            "A verdade é que tem dias que a gente acorda e o barulho dos carros lá fora já parece avisar que a luta vai ser grande. A cabeça enche de preocupações antes mesmo do café.",
            "Mas a sabedoria de quem já viveu muito é saber escolher as batalhas. Não dá para abraçar o mundo com as mãos e não adianta sofrer pelo boleto que só vence semana que vem.",
            "Faz o que dá conta hoje. O resto a gente entrega. Que o peso fique lá fora e a calma entre pela porta da frente."
        ],
        "oracao": "Senhor, olha pelos nossos passos hoje. Livra a nossa mente da ansiedade, protege quem a gente ama na rua e traz todo mundo em segurança de volta para casa. Amém.",
        "versiculo": "Entregue o seu caminho ao Senhor; confie nele, e ele o fará. — Salmos 37:5"
    }

# 7. Carrega o Molde HTML
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

reflexao_html = "".join([f"<p>{p}</p>" for p in conteudo["paragrafos"]])

# 7.8 Lógica de Navegação Interna (Ontem e Hoje)
ontem_dt = hoje_dt - timedelta(days=1)
caminho_ontem = ontem_dt.strftime("%Y/%m/%d")

if os.path.exists(caminho_ontem):
    bloco_navegacao = f"""
    <div class="flex justify-between items-center mt-8 pt-5 border-t border-amber-200/60">
      <a href="/{caminho_ontem}/" class="text-amber-700 text-sm font-bold hover:text-amber-900 flex items-center gap-2 transition-colors">
        &larr; Bênção de Ontem
      </a>
      <a href="/" class="text-amber-700 text-sm font-bold hover:text-amber-900 flex items-center gap-2 transition-colors">
        Bênção de Hoje &rarr;
      </a>
    </div>
    """
else:
    bloco_navegacao = f"""
    <div class="flex justify-end items-center mt-8 pt-5 border-t border-amber-200/60">
      <a href="/" class="text-amber-700 text-sm font-bold hover:text-amber-900 flex items-center gap-2 transition-colors">
        Bênção de Hoje &rarr;
      </a>
    </div>
    """

# 8. Carrega os Produtos Afiliados (Vitrine)
try:
    with open("produtos.json", "r", encoding="utf-8") as f:
        produtos_afiliados = json.load(f)
    dia_do_ano = hoje_dt.timetuple().tm_yday
    produto_hoje = produtos_afiliados[dia_do_ano % len(produtos_afiliados)]
except Exception as e:
    print(f"Aviso ao carregar produtos.json: {e}")
    produto_hoje = {
        "titulo": "Bíblia Sagrada Letra Hipergigante",
        "descricao": "Leitura confortável e descansada para os seus momentos de oração diária.",
        "imagem_url": "https://down-br.img.susercontent.com/file/br-11134207-81z1k-mees0ay86fia59@resize_w900_nl.webp",
        "link_shopee": "https://s.shopee.com.br/7AeIVV2Xnq"
    }

# 9. Monta a Página da Subpasta do Dia com Pastas Aninhadas (AAAA/MM/DD)
html_subpasta = template \
    .replace("{{TITULO}}", conteudo["titulo"]) \
    .replace("{{DATA_EXTENSO}}", data_extenso) \
    .replace("{{CHAMADA_ZAP}}", conteudo["chamada_zap"]) \
    .replace("{{IMAGEM_PATH}}", f"imagens/{imagem_escolhida}") \
    .replace("{{IMAGEM_SRC}}", f"../../../imagens/{imagem_escolhida}") \
    .replace("{{REFLEXAO_HTML}}", reflexao_html) \
    .replace("{{ORACAO}}", conteudo["oracao"]) \
    .replace("{{VERSICULO}}", conteudo["versiculo"]) \
    .replace("{{NAVEGACAO}}", bloco_navegacao) \
    .replace("{{PRODUTO_NOME}}", produto_hoje["titulo"]) \
    .replace("{{PRODUTO_DESC}}", produto_hoje["descricao"]) \
    .replace("{{PRODUTO_IMAGEM}}", produto_hoje["imagem_url"]) \
    .replace("{{PRODUTO_LINK}}", produto_hoje["link_shopee"])

os.makedirs(caminho_pasta, exist_ok=True)
with open(f"{caminho_pasta}/index.html", "w", encoding="utf-8") as f:
    f.write(html_subpasta)

# 10. Monta e Atualiza a Página Inicial da Raiz (index.html)
html_raiz = html_subpasta.replace(f"../../../imagens/{imagem_escolhida}", f"./imagens/{imagem_escolhida}")
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_raiz)

# 11. Geração/Atualização Automática do XML de Sitemap (SEO Orgânico)
sitemap_path = "sitemap.xml"
url_diaria = f"https://www.amanhecerfeliz.com/{caminho_pasta}/"

if os.path.exists(sitemap_path):
    with open(sitemap_path, "r", encoding="utf-8") as f:
        sitemap_content = f.read()
else:
    sitemap_content = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n</urlset>'

if url_diaria not in sitemap_content:
    nova_url_xml = f'  <url>\n    <loc>{url_diaria}</loc>\n    <lastmod>{data_hoje_iso}</lastmod>\n  </url>\n</urlset>'
    sitemap_content = sitemap_content.replace('</urlset>', nova_url_xml)
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(sitemap_content)

# 12. Salva o Texto Formatado para Envio Rápido no WhatsApp
msg_zap = f"""🌸☕ BOM DIA COM PAZ E BÊNÇÃO! ☕🌸

{conteudo['chamada_zap']}

📖 Leia a oração do lar completa e pegue a bênção de hoje:
👉 https://www.amanhecerfeliz.com/{caminho_pasta}/"""

with open("mensagem_hoje.txt", "w", encoding="utf-8") as f:
    f.write(msg_zap)

print(f"Sucesso: Páginas geradas em {caminho_pasta}. Navegação inteligente criada. Sitemap atualizado.")
