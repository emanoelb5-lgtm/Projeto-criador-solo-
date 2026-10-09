"""Original diagrams and a storyboard aligned to the real narration timings."""
from __future__ import annotations

import json
import math
from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont

EP = Path(__file__).resolve().parent
ROOT = EP.parents[1]
ASSETS = EP / "assets"
WORK = ROOT / "work" / EP.name
W, H = 1920, 1080
BG, PANEL = "#091b2b", "#132c40"
CREAM, CYAN, GOLD, MUTED = "#fff1dc", "#88dbea", "#f3ba62", "#a7bac7"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(BOLD if bold else FONT, size)


def label(draw, x, y, text, size=34, color=CREAM, bold=False, anchor=None):
    draw.text((x, y), text, fill=color, font=font(size, bold), anchor=anchor)


def arrow(draw, start, end, color=CYAN, width=9):
    draw.line((start, end), fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    wing = 23
    points = [end, (end[0] - wing * math.cos(angle - 0.5), end[1] - wing * math.sin(angle - 0.5)),
              (end[0] - wing * math.cos(angle + 0.5), end[1] - wing * math.sin(angle + 0.5))]
    draw.polygon(points, fill=color)


def base(title, subtitle, source):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    for x in range(0, W, 120):
        draw.line((x, 330, x, 960), fill="#102637", width=1)
    for y in range(350, 970, 100):
        draw.line((80, y, 1840, y), fill="#102637", width=1)
    draw.rounded_rectangle((82, 70, 115, 103), radius=6, fill=CYAN)
    label(draw, 136, 72, "ANTES DE SER NORMAL", 27, bold=True)
    label(draw, 1825, 80, "EP. 001", 24, MUTED, anchor="ra")
    draw.rectangle((82, 151, 92, 276), fill=GOLD)
    label(draw, 120, 151, textwrap.fill(title, 38), 69, bold=True)
    label(draw, 120, 309, textwrap.fill(subtitle, 85), 32, MUTED)
    draw.line((85, 1022, 1835, 1022), fill="#294353", width=2)
    label(draw, 90, 1038, source, 21, MUTED)
    label(draw, 1830, 1038, "Fontes na descrição", 21, MUTED, anchor="ra")
    return image, draw


def nodes(draw, items):
    size, gap = 450, 95
    total = len(items) * size + (len(items) - 1) * gap
    x = (W - total) // 2
    for index, (word, detail) in enumerate(items):
        left = x + index * (size + gap)
        draw.rounded_rectangle((left, 465, left + size, 805), radius=24, fill=PANEL, outline="#315569", width=3)
        draw.ellipse((left + 177, 510, left + 273, 606), fill=CYAN)
        label(draw, left + size // 2, 620, word, 36, bold=True, anchor="ma")
        label(draw, left + size // 2, 698, textwrap.fill(detail, 20), 28, MUTED, anchor="ma")
        if index < len(items) - 1:
            arrow(draw, (left + size + 15, 635), (left + size + gap - 16, 635), GOLD)


def clock(draw):
    cx, cy, r = 600, 665, 195
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=CYAN, width=13)
    for number in range(12):
        angle = math.pi * 2 * number / 12
        a = (cx + (r-18)*math.sin(angle), cy - (r-18)*math.cos(angle))
        b = (cx + (r-40)*math.sin(angle), cy - (r-40)*math.cos(angle))
        draw.line((a, b), fill=MUTED, width=5)
    draw.line((cx, cy, cx+100, cy-70), fill=GOLD, width=12)
    draw.line((cx, cy, cx, cy-135), fill=CREAM, width=10)
    draw.ellipse((cx-15, cy-15, cx+15, cy+15), fill=GOLD)
    label(draw, 1050, 550, "COMIDA", 68, bold=True)
    label(draw, 1050, 642, "×", 70, CYAN)
    label(draw, 1050, 738, "TEMPO", 68, bold=True)


def icebox(draw):
    draw.rounded_rectangle((727, 414, 1187, 911), radius=25, fill="#483d33", outline=GOLD, width=7)
    draw.rectangle((752, 444, 1162, 621), fill=PANEL, outline="#62707a", width=3)
    draw.polygon([(833, 473), (1080, 464), (1117, 501), (1105, 579), (840, 592), (807, 552)], fill="#96d9e6", outline=CREAM, width=4)
    label(draw, 958, 518, "GELO", 42, BG, True, anchor="mm")
    draw.rectangle((752, 646, 1162, 877), fill="#16334a", outline="#62707a", width=3)
    for y in (730, 813):
        draw.line((768, y, 1150, y), fill=MUTED, width=4)
    for x in (800, 930, 1060):
        draw.rounded_rectangle((x, 680, x+66, 725), radius=8, fill="#7ea56a")
        draw.rounded_rectangle((x, 760, x+66, 808), radius=8, fill="#ad865d")
    label(draw, 186, 519, "Armário", 45, bold=True)
    label(draw, 186, 582, "com isolamento", 35, MUTED)
    arrow(draw, (460, 612), (702, 612), GOLD)
    label(draw, 1272, 492, "O bloco absorve calor", 35, CYAN)
    label(draw, 1272, 548, "e precisa ser reposto.", 30, MUTED)
    arrow(draw, (1196, 542), (1247, 542), CYAN)
    arrow(draw, (958, 912), (958, 964), CYAN)
    label(draw, 1290, 790, "Água do gelo\nderretido", 28, MUTED)


def cycle(draw, highlight=None):
    locations = [(190, 433), (1120, 433), (1120, 713), (190, 713)]
    titles = ["EVAPORADOR", "COMPRESSOR", "CONDENSADOR", "EXPANSÃO"]
    details = ["Absorve calor do interior", "Aumenta a pressão do vapor",
               "Libera calor para fora", "Reduz a pressão do fluido"]
    for index, ((x, y), title, detail) in enumerate(zip(locations, titles, details)):
        active = index == highlight
        fill = "#1e4c60" if active else PANEL
        draw.rounded_rectangle((x, y, x+610, y+157), radius=19, fill=fill,
                               outline=GOLD if active else "#386077", width=5 if active else 2)
        label(draw, x+32, y+29, title, 37, CYAN if index in (0, 3) else GOLD, True)
        label(draw, x+32, y+90, detail, 28, CREAM)
    arrow(draw, (820, 510), (1095, 510), CYAN)
    arrow(draw, (1425, 609), (1425, 690), GOLD)
    arrow(draw, (1094, 787), (825, 787), GOLD)
    arrow(draw, (490, 695), (490, 611), CYAN)
    label(draw, 960, 885, "Um circuito fechado • esquema simplificado", 30, MUTED, anchor="ma")


def heat(draw):
    draw.rounded_rectangle((760, 417, 1160, 910), radius=25, outline=CREAM, width=8, fill="#1b4456")
    draw.line((781, 594, 1137, 594), fill=CREAM, width=5)
    for y in (660, 748, 835):
        draw.line((790, y, 1119, y), fill=CYAN, width=3)
    label(draw, 960, 480, "FRIO", 62, CYAN, True, "ma")
    label(draw, 200, 590, "INTERIOR", 41, bold=True)
    label(draw, 200, 658, "perde calor", 33, MUTED)
    arrow(draw, (466, 620), (724, 620), CYAN)
    arrow(draw, (1195, 620), (1480, 620), GOLD)
    label(draw, 1525, 587, "AMBIENTE", 41, GOLD, True)
    label(draw, 1525, 655, "recebe calor", 33, MUTED)
    label(draw, 960, 380, "O equipamento usa energia para transportar calor.", 29, MUTED, anchor="ma")


def coldchain(draw):
    words = ["PRODUÇÃO", "DEPÓSITO", "TRANSPORTE", "MERCADO", "CASA"]
    x0, size, gap = 90, 290, 70
    for index, word in enumerate(words):
        x = x0 + index*(size+gap)
        draw.rounded_rectangle((x, 477, x+size, 811), radius=20, fill=PANEL, outline="#315569", width=3)
        label(draw, x+size//2, 514, f"{index+1:02d}", 76, CYAN, True, "ma")
        label(draw, x+size//2, 680, word, 26, bold=True, anchor="ma")
        label(draw, x+size//2, 738, "Condição adequada", 23, MUTED, anchor="ma")
        if index < len(words)-1:
            arrow(draw, (x+size+10, 635), (x+size+gap-10, 635), GOLD, 7)
    label(draw, 960, 878, "A geladeira doméstica é um dos elos.", 38, MUTED, anchor="ma")


SPECS = [
    ("Um gesto comum. Uma revolução.", "A história escondida na porta da geladeira.", "clock", "Abertura"),
    ("A geladeira mudou nossa relação", "Com a comida e com o tempo.", "clock", "Interpretação editorial"),
    ("Antes da tomada", "Conservar alimentos exigia outras estratégias.", "preserve", "Fonte: USDA / Agricultural Research Service"),
    ("O tempo fazia parte da compra", "Uma situação imaginada para entender o problema.", "clock", "Exemplo ilustrativo"),
    ("Quando o inverno era vendido", "Blocos de gelo eram cortados e guardados.", "icebox", "Fonte: National Park Service • caso histórico dos EUA"),
    ("O frio chegava de carroça", "Havia entrega, compra e reposição.", "icebox", "Fonte: National Park Service • caso histórico dos EUA"),
    ("Um armário que consumia gelo", "O bloco derretia enquanto absorvia calor.", "icebox", "Fonte: National Park Service"),
    ("A transformação foi gradual", "Equipamentos, isolamento e acesso à eletricidade.", "transition", "Fontes: National Park Service / Science Museum"),
    ("De blocos a um ciclo", "Os objetos preservados contam essa mudança.", "transition", "Fonte: Science Museum, Londres"),
    ("O calor precisa sair", "A geladeira transfere energia para o ambiente.", "heat", "Fonte: Danfoss • esquema simplificado"),
    ("1. Receber calor no evaporador", "O fluido passa ao estado de vapor.", "cycle0", "Fonte: Danfoss • esquema simplificado"),
    ("2, 3 e 4. Continuar o percurso", "Comprimir, liberar calor e reduzir a pressão.", "cycle1", "Fonte: Danfoss • esquema simplificado"),
    ("Frio por dentro, calor por fora", "Paredes e vedação reduzem a entrada de calor.", "heat", "Fonte: Danfoss • esquema simplificado"),
    ("A cozinha ganha possibilidades", "Armazenamento e planejamento da rotina.", "routine", "Fonte: Science Museum • interpretação editorial"),
    ("O frio vai além de casa", "Depósitos, veículos, mercados e geladeiras.", "chain", "Fonte: PNUMA / FAO"),
    ("Do armazenamento à sua mesa", "Cada elo ajuda a conservar os produtos.", "chain", "Fonte: PNUMA / FAO"),
    ("Produzir não basta", "Conservar também faz parte do abastecimento.", "chain", "Fonte: PNUMA / FAO • relatório de 2022"),
    ("Tecnologia também é rotina", "O trabalho de casa muda com os equipamentos.", "routine", "Fonte: Science Museum"),
    ("Pequenas decisões, todos os dias", "Compras, armazenamento e preparo.", "routine", "Interpretação editorial"),
    ("Conservar tem limites", "O frio não substitui os demais cuidados.", "limits", "Fonte: FDA • orientação geral"),
    ("O frio tem um custo", "Energia, fluidos refrigerantes e manutenção.", "cost", "Fonte: PNUMA / FAO"),
    ("Eficiência faz parte da história", "Instalação e uso acompanham o fabricante.", "cost", "Fonte: Governo australiano / energy.gov.au"),
    ("O caminho até a sua cozinha", "Gelo transportado. Calor movimentado. Redes de abastecimento.", "transition", "Síntese do episódio"),
    ("Antes de Ser Normal", "Qual objeto do seu dia a dia merece o próximo episódio?", "clock", "História e ciência das coisas que parecem comuns"),
]


def main():
    ASSETS.mkdir(exist_ok=True)
    text = (EP / "narracao.txt").read_text().strip()
    paragraphs = text.split("\n\n")
    words = json.loads((WORK / "words.json").read_text())
    if len(words) != len(text.split()) or len(paragraphs) != len(SPECS):
        raise ValueError("Confira os limites de parágrafo na marcação da voz.")
    count = 0
    starts = []
    cardnames = []
    for index, (paragraph, spec) in enumerate(zip(paragraphs, SPECS)):
        starts.append(words[count]["offset"] / 10000000)
        count += len(paragraph.split())
        title, subtitle, kind, source = spec
        image, draw = base(title, subtitle, source)
        if kind == "clock":
            clock(draw)
        elif kind == "preserve":
            nodes(draw, [("SECAGEM", "Retirar umidade"), ("SALGA", "Usar sal"), ("FERMENTAÇÃO", "Transformar o alimento")])
        elif kind == "icebox":
            icebox(draw)
        elif kind == "heat":
            heat(draw)
        elif kind.startswith("cycle"):
            cycle(draw, int(kind[-1]))
        elif kind == "chain":
            coldchain(draw)
        elif kind == "transition":
            nodes(draw, [("GELO", "Bloco que é reposto"), ("MÁQUINA", "Ciclo de refrigeração"), ("REDE", "Cadeia do frio")])
        elif kind == "routine":
            nodes(draw, [("COMPRAR", "Organizar escolhas"), ("GUARDAR", "Conservar produtos"), ("PREPARAR", "Planejar a rotina")])
        elif kind == "limits":
            nodes(draw, [("REFRIGERAR", "Ajuda a conservar"), ("CUIDAR", "Higiene e preparo"), ("RESPEITAR", "Condições de uso")])
        elif kind == "cost":
            nodes(draw, [("ENERGIA", "Consumo elétrico"), ("SISTEMA", "Fluidos e manutenção"), ("USO", "Instalação e rotina")])
        name = f"assets/diagrama-{index+1:02d}.png"
        image.save(EP / name)
        cardnames.append(name)
    starts[0] = 0
    starts.append(480)
    photo_choices = {0:"moderna",1:"moderna",4:"gelo",5:"gelo",6:"gelo",
                     13:"moderna",14:"mercado",15:"mercado",16:"mercado",
                     17:"moderna",18:"moderna",21:"moderna",22:"mercado",23:"moderna"}
    shots = []
    for index in range(len(paragraphs)):
        begin_frame = round(starts[index] * 30)
        end_frame = round(starts[index+1] * 30)
        midpoint = begin_frame + (end_frame-begin_frame)//2
        first_asset = f"assets/{photo_choices[index]}.png" if index in photo_choices else cardnames[index]
        first = {"asset":first_asset,"duration_seconds":(midpoint-begin_frame)/30,"motion":index in photo_choices}
        if index in photo_choices:
            first.update({"caption":textwrap.fill(SPECS[index][0], 36),
                          "label":"Ilustração gerada por IA • reconstituição histórica" if photo_choices[index]=="gelo" else "Ilustração gerada por IA"})
        shots.extend([first,{"asset":cardnames[index],"duration_seconds":(end_frame-midpoint)/30,"motion":False}])
    storyboard={"duration_seconds":480,"fps":30,"shots":shots}
    (EP / "storyboard.json").write_text(json.dumps(storyboard,ensure_ascii=False,indent=2)+"\n")
    chapters = [(0,"Um gesto que mudou a cozinha"),(2,"Antes da geladeira"),(4,"Quando o gelo era entregue"),
                (7,"A chegada da geladeira elétrica"),(9,"Como a geladeira move calor"),(14,"A cadeia do frio"),
                (17,"O que mudou na rotina"),(19,"O frio e seus limites"),(20,"Energia e eficiência"),(22,"Antes de ser normal")]
    metadata={"title":"Como a geladeira mudou o que você come",
              "alternative_titles":["A história da geladeira: do bloco de gelo à sua cozinha","Como a geladeira mudou a comida e a nossa rotina"],
              "summary":"Você abre a geladeira todos os dias. Mas esse gesto comum esconde uma revolução.\n\nNeste documentário de 8 minutos, seguimos a história das caixas de gelo, explicamos como a geladeira transporta calor e mostramos por que a cadeia do frio mudou o abastecimento e a rotina da cozinha.\n\nAntes de Ser Normal — a história e a ciência das coisas que parecem comuns.\nQual objeto você quer ver no próximo episódio?",
              "language":"pt-BR","category_id":27,"publication_mode":"manual",
              "tags":["história da geladeira","como funciona a geladeira","refrigeração","cadeia do frio","história da tecnologia","ciência do cotidiano","documentário","Antes de Ser Normal"],
              "hashtags":["#AntesDeSerNormal","#HistóriaDaTecnologia","#Ciência"],
              "chapters":[{"start_seconds":int(starts[p]),"title":title} for p,title in chapters],
              "sources":[
                  {"name":"National Park Service — The Icebox","url":"https://www.nps.gov/articles/000/the-icebox-the-predecessor-of-modern-refrigeration.htm"},
                  {"name":"Science Museum — The Secret Life of the Home","url":"https://blog.sciencemuseum.org.uk/saying-goodbye-to-the-secret-life-of-the-home-gallery/"},
                  {"name":"Danfoss — How a refrigerator works","url":"https://www.danfoss.com/en/about-danfoss/our-businesses/cooling/the-fridge-how-it-works/"},
                  {"name":"PNUMA e FAO — Sustainable Food Cold Chains (2022)","url":"https://www.unep.org/resources/report/sustainable-food-cold-chains-opportunities-challenges-and-way-forward"},
                  {"name":"FDA — Are You Storing Food Safely?","url":"https://www.fda.gov/consumers/consumer-updates/are-you-storing-food-safely"},
                  {"name":"Governo australiano — Appliances","url":"https://www.energy.gov.au/households/appliances"},
                  {"name":"USDA ARS — Food processing, preservation, and packaging","url":"https://www.ars.usda.gov/research/publications/publication/?seqNo115=401741"}],
              "credits":"Roteiro e diagramas originais: Antes de Ser Normal. Ilustrações de cenas e miniatura geradas por IA neste projeto; a cena histórica é uma reconstituição ilustrativa, não uma fotografia de arquivo. Narração sintética: voz pt-BR-AntonioNeural. Pesquisa e produção assistidas por IA. Sem música ou imagens de terceiros."}
    (EP / "metadata.json").write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+"\n")
    script="# Como a geladeira mudou o que você come\n\nCanal: Antes de Ser Normal. Duração final: 08:00. Formato: 1920 × 1080, 16:9, 30 fps.\n\n"
    for index,(paragraph,spec) in enumerate(zip(paragraphs,SPECS)):
        script+=f"## Cena {index+1:02d} — {spec[0]}\n\n**Visual:** {spec[1]}  \n**Referência:** {spec[3]}\n\n{paragraph}\n\n"
    (EP / "roteiro.md").write_text(script)
    print(f"{len(SPECS)} diagramas, {len(shots)} planos e {len(chapters)} capítulos preparados.")


if __name__=="__main__":
    main()
