import random
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple

LETTERS = ["A","B","C","D"]

@dataclass
class Question:
    area: str
    text: str
    choices: List[str]
    correct_index: int
    explanation: str

def shuffle_choices(q: Question) -> Question:
    idxs = list(range(len(q.choices)))
    random.shuffle(idxs)
    new_choices = [q.choices[i] for i in idxs]
    new_correct = idxs.index(q.correct_index)
    return Question(q.area, q.text, new_choices, new_correct, q.explanation)

def pct(correct: int, total: int) -> float:
    return 0.0 if total == 0 else (100.0 * correct / total)

def score_to_amib_scale(correct: int, total: int) -> int:
    # Aproximación lineal útil para práctica
    if total <= 0:
        return 200
    return int(round(200 + (correct / total) * 900))

OFFICIAL_EXAM_BLUEPRINT = [
    ("Ética", 20),
    ("Servicios de Inversión", 20),
    ("Marco Normativo I-III", 25),
    ("Matemáticas y Portafolios", 25),
    ("Mercado de Capitales I-II", 25),
    ("Títulos de Deuda I-II", 25),
    ("Fondos de Inversión", 20),
    ("Derivados y Riesgos", 25),
    ("Análisis Económico/Financiero/Técnico", 25),
]

def gen_etica(n=30):
    principios = [
        ("Evitar conflicto de interés", "Revelar conflicto y priorizar al cliente"),
        ("Confidencialidad", "No divulgar información del cliente ni de emisoras de forma indebida"),
        ("Integridad", "No falsear información ni prometer rendimientos"),
        ("Diligencia", "Sustentar recomendaciones con información razonable"),
        ("Equidad", "Trato justo, sin preferir clientes por comisiones"),
    ]
    acciones_incorrectas = [
        "prometer un rendimiento garantizado",
        "ocultar una comisión o incentivo",
        "compartir datos del cliente con un tercero sin autorización",
        "recomendar algo sin conocer objetivo/horizonte del cliente",
        "operar primero para beneficio propio (front-running)",
    ]
    out=[]
    for _ in range(n):
        p, buena = random.choice(principios)
        mala = random.choice(acciones_incorrectas)
        text = (f"En una asesoría, ¿qué conducta es MÁS consistente con el principio de '{p}'?\n"
                f"Escenario: detectas la tentación de {mala}.")
        choices = [buena,
                   "Realizar la acción si el cliente no se da cuenta",
                   "Hacerlo solo si el mercado está 'seguro'",
                   "Hacerlo si aumenta la comisión del asesor"]
        expl = f"Ética aplicada: '{p}' implica {buena.lower()} y evitar conductas como {mala}."
        out.append(shuffle_choices(Question("Ética", text, choices, 0, expl)))
    return out

def gen_servicios_inversion(n=30):
    out=[]
    for _ in range(n):
        tipo = random.choice(["Asesoría de inversiones", "Comercialización/Promoción", "Ejecución de operaciones"])
        text = f"¿Cuál enunciado describe MEJOR el servicio de '{tipo}'?"
        if tipo == "Asesoría de inversiones":
            choices = [
                "Incluir recomendaciones razonables basadas en el perfil del cliente y del producto",
                "Solo ejecutar órdenes sin emitir sugerencias",
                "Solo informar precios sin analizar adecuación",
                "Garantizar rendimiento mínimo al cliente",
            ]
            expl = "La asesoría supone recomendaciones/consejos y un estándar de razonabilidad ligado a perfiles."
        elif tipo == "Ejecución de operaciones":
            choices = [
                "Ejecutar instrucciones del cliente sin necesariamente recomendar",
                "Formular recomendaciones personalizadas obligatoriamente",
                "Sustituir al cliente en todas las decisiones sin contrato",
                "Cobrar solo si hay ganancia del cliente",
            ]
            expl = "Ejecución se enfoca en ejecutar instrucciones; no implica por sí misma recomendación."
        else:
            choices = [
                "Ofrecer información/recomendaciones sobre productos, cuidando adecuación según reglas aplicables",
                "Operar con información privilegiada para mejorar precios",
                "Evitar cualquier registro de comunicaciones",
                "No mostrar comisiones ni costos",
            ]
            expl = "Promoción/comercialización implica ofrecer productos con transparencia y reglas de adecuación."
        out.append(shuffle_choices(Question("Servicios de Inversión", text, choices, 0, expl)))
    return out

def gen_marco_normativo(n=30):
    out=[]
    conceptos = [
        ("Información privilegiada", "Información no pública que podría influir en el precio de un valor"),
        ("Información relevante", "Evento/dato que puede impactar decisiones de inversión"),
        ("Conflicto de interés", "Situación donde el interés del asesor puede contraponerse al del cliente"),
        ("Sanas prácticas", "Conductas profesionales alineadas con integridad, transparencia y trato justo"),
    ]
    for _ in range(n):
        c, defin = random.choice(conceptos)
        text = f"¿Cuál opción define MEJOR: '{c}'?"
        choices = [defin, "Un rumor sin sustento", "Una opinión personal", "Cualquier dato público ya difundido"]
        expl = f"Definición base: {c} se refiere a: {defin.lower()}."
        out.append(shuffle_choices(Question("Marco Normativo I-III", text, choices, 0, expl)))
    return out

def gen_matematicas_portafolios(n=30):
    out=[]
    for _ in range(n):
        pv = random.randint(5_000, 50_000)
        r = random.choice([0.06, 0.08, 0.10, 0.12])
        t = random.choice([1,2,3,4])
        vf = pv*((1+r)**t)
        text = f"Si inviertes ${pv:,.0f} a tasa anual {r*100:.0f}% compuesta por {t} años, ¿VF aproximado?"
        choices = [f"${vf:,.0f}", f"${(pv*(1+r*t)):,.0f}", f"${(vf*0.95):,.0f}", f"${(vf*1.05):,.0f}"]
        expl = "Interés compuesto: VF = VP(1+r)^t."
        out.append(shuffle_choices(Question("Matemáticas y Portafolios", text, choices, 0, expl)))
    return out

def gen_mercado_capitales(n=30):
    out=[]
    temas = ["mercado primario","mercado secundario","IPO","dividendo","split","índice"]
    for _ in range(n):
        tema = random.choice(temas)
        if tema=="mercado primario":
            text="¿Qué ocurre principalmente en el mercado primario?"
            choices=["Emisión/colocación inicial de valores; recursos van al emisor",
                     "Compra-venta entre inversionistas; recursos van al vendedor",
                     "Solo derivados","Solo repos"]
            expl="Primario: emisión/colocación; el emisor recibe recursos."
        elif tema=="mercado secundario":
            text="¿Qué describe mejor al mercado secundario?"
            choices=["Intercambio de valores ya emitidos entre inversionistas",
                     "Emisión inicial por el emisor","Pago de impuestos","Registro contable interno"]
            expl="Secundario: negociación de valores ya emitidos."
        elif tema=="IPO":
            text="Una IPO (oferta pública inicial) se asocia más con:"
            choices=["Colocar acciones por primera vez al público","Pagar cupones","Convertir tasa fija a variable","Forward FX"]
            expl="IPO: primera colocación pública de acciones."
        elif tema=="dividendo":
            text="Si una acción paga dividendo, en general implica:"
            choices=["Distribución a accionistas (según política)","Obligación fija como cupón","Garantía de alza de precio","Que no hay utilidades"]
            expl="Dividendo: distribución; no es obligación contractual fija como cupón."
        elif tema=="split":
            text="Un split normalmente busca:"
            choices=["Ajustar # de acciones y precio unitario sin cambiar el valor económico total",
                     "Aumentar utilidades","Cambiar cupón","Eliminar volatilidad"]
            expl="Split: cambia piezas (acciones) y precio unitario, no el valor total por sí mismo."
        else:
            text="¿Para qué sirve principalmente un índice accionario?"
            choices=["Medir desempeño agregado de un conjunto de acciones","Garantizar rendimiento","Eliminar riesgo","Sustituir estados financieros"]
            expl="Índice: benchmark/medida de desempeño agregado."
        out.append(shuffle_choices(Question("Mercado de Capitales I-II", text, choices, 0, expl)))
    return out

def gen_titulos_deuda(n=30):
    out=[]
    for _ in range(n):
        fv = random.choice([10_000,20_000,50_000])
        y  = random.choice([0.07,0.09,0.11])
        t  = random.choice([1,2,3,4,5])
        pv = fv/((1+y)**t)
        text=f"Un cupón cero paga ${fv:,.0f} en {t} años. Con y={y*100:.0f}%, ¿precio hoy aprox.?"
        choices=[f"${pv:,.0f}", f"${(fv/(1+y*t)):,.0f}", f"${(pv*0.95):,.0f}", f"${(pv*1.05):,.0f}"]
        expl="Cupón cero: Precio = FV/(1+y)^t."
        out.append(shuffle_choices(Question("Títulos de Deuda I-II", text, choices, 0, expl)))
    return out

def gen_fondos(n=30):
    out=[]
    for _ in range(n):
        text="Diferencia general más común entre ETF y fondo tradicional:"
        choices=["ETF suele negociarse en bolsa intradía; fondo tradicional a NAV en cortes",
                 "ETF no tiene riesgo","Fondo siempre gana","ETF nunca cobra comisiones"]
        expl="Generalmente: ETF intradía en bolsa; fondos abiertos operan a NAV según horarios."
        out.append(shuffle_choices(Question("Fondos de Inversión", text, choices, 0, expl)))
    return out

def gen_derivados(n=30):
    out=[]
    for _ in range(n):
        fwd = random.randint(17,25)
        spot = random.randint(17,25)
        pnl = spot - fwd
        text=f"Forward (posición larga): pactas {fwd}. Spot al vencimiento {spot}. ¿Payoff S-K?"
        choices=[str(pnl), str(-pnl), str(spot+fwd), str(spot*fwd)]
        expl="Payoff largo forward: S_T - K."
        out.append(shuffle_choices(Question("Derivados y Riesgos", text, choices, 0, expl)))
    return out

def gen_analisis(n=30):
    out=[]
    for _ in range(n):
        text="En análisis técnico, una tendencia alcista suele caracterizarse por:"
        choices=["Máximos y mínimos crecientes","Máximos y mínimos decrecientes","Precios constantes","Volatilidad cero"]
        expl="Tendencia alcista: higher highs & higher lows."
        out.append(shuffle_choices(Question("Análisis Económico/Financiero/Técnico", text, choices, 0, expl)))
    return out

def build_bank(min_per_area=30) -> Dict[str, List[Question]]:
    return {
        "Ética": gen_etica(min_per_area),
        "Servicios de Inversión": gen_servicios_inversion(min_per_area),
        "Marco Normativo I-III": gen_marco_normativo(min_per_area),
        "Matemáticas y Portafolios": gen_matematicas_portafolios(min_per_area),
        "Mercado de Capitales I-II": gen_mercado_capitales(min_per_area),
        "Títulos de Deuda I-II": gen_titulos_deuda(min_per_area),
        "Fondos de Inversión": gen_fondos(min_per_area),
        "Derivados y Riesgos": gen_derivados(min_per_area),
        "Análisis Económico/Financiero/Técnico": gen_analisis(min_per_area),
    }

# Estado global (simple)
BANK = None
QUESTIONS: List[Question] = []
ANSWERS: List[int] = []  # -1 = skip, 0..3 option index

def init_bank():
    global BANK
    BANK = build_bank(30)
    return sorted(list(BANK.keys()))

def start_quiz(mode: str, topic: str = ""):
    global QUESTIONS, ANSWERS, BANK
    if BANK is None:
        init_bank()

    q=[]
    if mode == "exam":
        for area, k in OFFICIAL_EXAM_BLUEPRINT:
            q += random.sample(BANK[area], k)
        random.shuffle(q)
    elif mode == "topic":
        q = random.sample(BANK[topic], 30)
        random.shuffle(q)
    elif mode == "quick":
        for area in BANK:
            q += random.sample(BANK[area], 10)
        random.shuffle(q)
    else:
        raise ValueError("Modo inválido")

    QUESTIONS = q
    ANSWERS = [-2 for _ in QUESTIONS]  # -2 = no respondida aún
    return len(QUESTIONS)

def get_question(i: int):
    q = QUESTIONS[i]
    return {
        "i": i,
        "n": len(QUESTIONS),
        "area": q.area,
        "text": q.text,
        "choices": q.choices
    }

def answer_question(i: int, choice_index: int):
    # choice_index: -1 skip, else 0..3
    ANSWERS[i] = choice_index

def finish():
    results=[]
    correct=0
    by_area={}
    wrongs=[]
    for i,q in enumerate(QUESTIONS):
        a = ANSWERS[i]
        ok = (a == q.correct_index)
        if ok:
            correct += 1
        by_area.setdefault(q.area, {"correct":0,"total":0})
        by_area[q.area]["total"] += 1
        if ok:
            by_area[q.area]["correct"] += 1

        if (a != q.correct_index):
            wrongs.append({
                "index": i,
                "area": q.area,
                "text": q.text,
                "choices": q.choices,
                "your": a,
                "correct": q.correct_index,
                "explanation": q.explanation
            })

    total=len(QUESTIONS)
    summary = {
        "correct": correct,
        "total": total,
        "pct": round(pct(correct,total), 2),
        "scale": score_to_amib_scale(correct,total),
        "by_area": {k: {"correct": v["correct"], "total": v["total"],
                        "pct": round(pct(v["correct"], v["total"]),2)}
                    for k,v in by_area.items()},
        "wrongs": wrongs
    }
    return summary
import json

def get_question_json(i: int):
    return json.dumps(get_question(i), ensure_ascii=False)

def finish_json():
    return json.dumps(finish(), ensure_ascii=False)
