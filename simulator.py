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

def _etica(n=30):
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
def gen_mercado_capitales(n=120):
    """
    Banco amplio y variado (capitales). Basado en conceptos de tus slides:
    mercado primario/secundario, MILA, CP, obligaciones, acciones, bursatilidad,
    capitalización, ETF/trackers/warrants, etc. :contentReference[oaicite:2]{index=2}
    """
    pool = []

    def Q(text, choices, correct, expl):
        pool.append(shuffle_choices(Question("Mercado de Capitales I-II", text, choices, correct, expl)))

    # 1) Mercado capitales: definición
    Q("¿Qué describe mejor al Mercado de Capitales?",
      ["Mercado de largo plazo para financiar capital social/proyectos y negociar valores representativos de capital",
       "Mercado exclusivo para CETES a 28 días",
       "Mercado donde solo se operan derivados",
       "Mercado de préstamos bancarios de consumo"],
      0,
      "Capitales se asocia a financiamiento y negociación de valores representativos de capital a plazos largos.")

    # 2) Primario vs secundario
    Q("En el mercado primario, típicamente:",
      ["La emisora coloca valores por primera vez y recibe los recursos",
       "Solo hay compraventa entre inversionistas y la emisora no participa",
       "Se negocian valores ya emitidos por oferta y demanda",
       "Siempre se fija el precio por el comprador"],
      0,
      "Primario: emisión/colocación inicial; recursos al emisor. :contentReference[oaicite:3]{index=3}")

    Q("En el mercado secundario, lo más correcto es:",
      ["Se negocian valores ya emitidos entre inversionistas; el precio lo determina oferta y demanda",
       "La emisora recibe el dinero de cada operación",
       "No existen intermediarios",
       "El precio lo fija siempre la emisora"],
      0,
      "Secundario: negociación posterior entre contrapartes; precio por oferta/demanda. :contentReference[oaicite:4]{index=4}")

    Q("Una OPI/IPO se refiere a:",
      ["Oferta pública inicial: primera colocación al público",
       "Pago de cupón de un bono",
       "Operación de reporto",
       "Cobertura con forward de divisas"],
      0,
      "IPO/OPI: primera colocación pública. :contentReference[oaicite:5]{index=5}")

    Q("Follow-on se refiere a:",
      ["Oferta subsecuente: colocación adicional de valores ya listados",
       "Emisión privada sin mercado",
       "Pago de dividendos",
       "Split inverso"],
      0,
      "Follow-on: colocación adicional posterior a estar listada. :contentReference[oaicite:6]{index=6}")

    # 3) MILA
    Q("¿Qué es MILA principalmente?",
      ["Plataforma que conecta bolsas (Chile, Colombia, México, Perú) para ruteo/ejecución/post-negociación",
       "Una cámara de compensación de criptomonedas",
       "Un mercado terciario de acciones (existe formalmente)",
       "Una aseguradora regional"],
      0,
      "MILA integra bolsas regionales para operar valores vía intermediario local. :contentReference[oaicite:7]{index=7}")

    Q("En MILA, las operaciones típicamente se realizan:",
      ["En moneda local y con anotación en cuenta a través del intermediario local",
       "Solo en USD y fuera de cada país",
       "Sin intermediarios",
       "Solo en mercado primario"],
      0,
      "En MILA se facilita operar en moneda local con intermediario local. :contentReference[oaicite:8]{index=8}")

    # 4) Emisor de capitales vs deuda / inversionista
    Q("Comparando capitales vs deuda para el emisor, una diferencia clave es:",
      ["Capitales modifica composición del capital social; deuda incrementa pasivos",
       "Capitales siempre tiene vencimiento; deuda nunca vence",
       "Capitales paga cupones fijos; deuda paga dividendos",
       "En deuda entran socios; en capitales no"],
      0,
      "Capitales implica socios; deuda implica acreedores/pasivo. :contentReference[oaicite:9]{index=9}")

    Q("Un inversionista en capitales (accionista) es principalmente:",
      ["Socio dueño proporcional con menor prelación que un acreedor",
       "Acreedor con mayor prelación que todos",
       "Asegurador del emisor",
       "Proveedor del emisor"],
      0,
      "Accionista: socio; más riesgo y menor prelación vs acreedor. :contentReference[oaicite:10]{index=10}")

    # 5) Certificados de Participación (CP)
    Q("Los Certificados de Participación son típicamente:",
      ["Títulos emitidos por fiduciarias que representan participación sobre bienes/valores en fideicomiso",
       "Depósitos bancarios a la vista",
       "Acciones preferentes del gobierno",
       "Pagarés bancarios no bursátiles"],
      0,
      "CP: participación en fideicomisos y derechos sobre productos de esos bienes/valores. :contentReference[oaicite:11]{index=11}")

    Q("Respecto a CP amortizables vs no amortizables, lo más correcto es:",
      ["Pueden existir con amortización (devolución programada) o sin amortización hasta el final",
       "No existe esa clasificación",
       "Siempre pagan dividendo fijo",
       "Son derivados, no títulos de crédito"],
      0,
      "Tus slides distinguen CP amortizables vs no amortizables. :contentReference[oaicite:12]{index=12}")

    # 6) Obligaciones
    Q("Una 'obligación' (bono corporativo tipo obligación) se caracteriza por:",
      ["Ser título de crédito; financia largo plazo; puede pagar tasa fija o variable",
       "Ser acción ordinaria con voto",
       "No tener plazo",
       "Ser siempre sin intereses"],
      0,
      "Obligaciones: crédito colectivo, largo plazo, tasa fija/variable. :contentReference[oaicite:13]{index=13}")

    Q("Por tipo de garantía, una obligación puede ser:",
      ["Quirografaria, prendaria, fiduciaria o hipotecaria",
       "Solo quirografaria",
       "Solo hipotecaria",
       "Solo con garantía del gobierno"],
      0,
      "Clasificación por garantía aparece en tus slides. :contentReference[oaicite:14]{index=14}")

    # 7) Acciones: valores nominal/libros/mercado
    Q("El valor en libros (contable) por acción se aproxima a:",
      ["Capital contable / número de acciones",
       "Precio de mercado / utilidad por acción",
       "Dividendo / precio",
       "Precio de cierre / volumen"],
      0,
      "Valor en libros: contable por acción (capital contable entre acciones). :contentReference[oaicite:15]{index=15}")

    Q("El valor de mercado (precio) de una acción es:",
      ["El determinado por oferta y demanda y puede variar constantemente",
       "El que viene impreso en el acta constitutiva",
       "Siempre igual al valor en libros",
       "Un valor fijo por regulación"],
      0,
      "Precio de mercado varía por oferta/demanda. :contentReference[oaicite:16]{index=16}")

    Q("Una acción preferente suele:",
      ["Tener preferencia en dividendos (p.ej. dividendo fijo antes que la común) y usualmente sin voto",
       "Tener siempre voto y sin preferencia en dividendos",
       "Ser un pagaré bancario",
       "Ser un derivado"],
      0,
      "Preferentes: prioridad en dividendos y normalmente sin derecho a voto. :contentReference[oaicite:17]{index=17}")

    # 8) Bursatilidad
    Q("La bursatilidad de una acción se refiere principalmente a:",
      ["Facilidad/frecuencia con que se puede comprar o vender (liquidez en mercado)",
       "Su tasa de interés fija",
       "Su fecha de vencimiento",
       "Su calificación crediticia"],
      0,
      "Bursatilidad: frecuencia de transacción y facilidad de liquidar posición. :contentReference[oaicite:18]{index=18}")

    Q("Una bolsa puede medir bursatilidad usando variables como:",
      ["Importe operado, número de operaciones e importe representativo (mediana)",
       "Solo dividendos pagados",
       "Solo número de empleados de la emisora",
       "Solo el sector económico"],
      0,
      "Tus slides listan variables típicas para bursatilidad. :contentReference[oaicite:19]{index=19}")

    # 9) Capitalización / Blue chip
    Q("El valor de capitalización (market cap) se calcula como:",
      ["Acciones en circulación × precio de la acción",
       "Utilidad neta / ventas",
       "Deuda total × tasa",
       "Precio / utilidad por acción"],
      0,
      "Capitalización: tamaño en términos de valor de mercado. :contentReference[oaicite:20]{index=20}")

    Q("‘Blue chip’ suele referirse a:",
      ["Compañías grandes y estables, líderes, con alta capitalización",
       "Startups sin ingresos",
       "Empresas no listadas",
       "Instrumentos sin riesgo"],
      0,
      "Blue chip: grandes, reputación de estabilidad y liderazgo. :contentReference[oaicite:21]{index=21}")

    # 10) ETFs / Trackers
    Q("Un ETF normalmente busca:",
      ["Replicar un índice o subyacente y negociarse intradía como acción",
       "Garantizar rendimiento mínimo",
       "Evitar todo riesgo de mercado",
       "Solo invertir en efectivo"],
      0,
      "ETF: replica subyacente/índice y se negocia en bolsa en tiempo real. :contentReference[oaicite:22]{index=22}")

    Q("¿Qué afirmación es más correcta sobre ETF vs fondo tradicional?",
      ["ETF se negocia intradía a precio de mercado; fondo abierto suele operar a valuación (NAV) en cortes",
       "Ambos siempre se operan a NAV intradía",
       "ETF no puede diversificar",
       "Fondo tradicional siempre tiene mercado secundario"],
      0,
      "Tus slides contrastan negociación intradía vs valuación por cortes. :contentReference[oaicite:23]{index=23}")

    Q("Un ‘tracker’ (CBFI indizado) sirve principalmente para:",
      ["Replicar un índice/portafolio y permitir comprar/vender el índice como si fuera una sola acción",
       "Pagar un cupón fijo como un bono",
       "Dar derecho a voto en una emisora",
       "Ser un depósito bancario"],
      0,
      "Tracker: replica subyacente y facilita acceso a índices con un solo instrumento. :contentReference[oaicite:24]{index=24}")

    Q("NAFTRAC se menciona como ejemplo de:",
      ["Tracker que replica el S&P/BMV IPC",
       "Acción preferente",
       "Bono gubernamental",
       "Warrant de divisas"],
      0,
      "NAFTRAC replica S&P/BMV IPC según tus slides. :contentReference[oaicite:25]{index=25}")

    # 11) Warrants vs opciones
    Q("Una diferencia clave entre warrants y opciones (en general) es:",
      ["Warrants son títulos emitidos por intermediarios/empresas; opciones son contratos derivados listados",
       "Warrants siempre son contratos OTC; opciones siempre son títulos de crédito",
       "No hay diferencias",
       "Las opciones solo pueden ser sobre acciones mexicanas"],
      0,
      "Tus slides listan diferencias: naturaleza y emisor/listado. :contentReference[oaicite:26]{index=26}")

    Q("Ejercicio ‘americano’ en un título opcional (warrant) significa:",
      ["Puede ejercerse en cualquier momento antes del vencimiento",
       "Solo puede ejercerse al vencimiento",
       "Nunca puede ejercerse",
       "Se ejerce automáticamente al comprar"],
      0,
      "Americano: ejercicio en cualquier momento previo al vencimiento. :contentReference[oaicite:27]{index=27}")

    Q("Ejercicio ‘europeo’ significa:",
      ["Solo puede ejercerse en la fecha de vencimiento",
       "Puede ejercerse cualquier día",
       "Se ejerce cuando el emisor quiere",
       "No existe ese tipo de ejercicio"],
      0,
      "Europeo: solo al vencimiento. :contentReference[oaicite:28]{index=28}")

    # 12) Variantes numéricas (capitalización / rendimiento simple)
    for _ in range(40):
        shares = random.randint(10_000_000, 200_000_000)
        price = random.choice([8.5, 12.3, 25.0, 41.7, 63.2])
        mc = shares * price
        Q(f"Una empresa tiene {shares:,} acciones en circulación y su precio es ${price:.2f}. ¿Capitalización aproximada?",
          [f"${mc:,.0f}", f"${(mc/10):,.0f}", f"${(mc*1.1):,.0f}", f"${(mc*0.9):,.0f}"],
          0,
          "Market cap = acciones en circulación × precio. :contentReference[oaicite:29]{index=29}")

    # Limita a n, sin repetir dentro del pool (pool ya son distintos)
    random.shuffle(pool)
    return pool[:n]


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
def gen_fondos(n=120):
    """
    Banco amplio y variado (fondos). Basado en tus slides:
    concepto/objeto, AOI, portafolio, comparativos, operaciones autorizadas/prohibidas,
    estados de cuenta, series A/B, régimen de inversión, FIID vs RV, indizadas beta, etc. :contentReference[oaicite:30]{index=30}
    """
    pool = []

    def Q(text, choices, correct, expl):
        pool.append(shuffle_choices(Question("Fondos de Inversión", text, choices, correct, expl)))

    # Concepto y objeto
    Q("Un fondo de inversión se define mejor como:",
      ["Sociedad autorizada que capta recursos del público para invertir colectivamente en un portafolio de valores",
       "Un pagaré bancario a plazo fijo",
       "Una cuenta de cheques sin inversiones",
       "Una emisora de acciones ordinarias"],
      0,
      "Fondo: inversión colectiva administrada profesionalmente. :contentReference[oaicite:31]{index=31}")

    Q("El objeto del fondo de inversión incluye principalmente:",
      ["Adquirir/vender activos objeto de inversión con recursos de la colocación de sus acciones",
       "Emitir billetes y monedas",
       "Otorgar créditos al consumo",
       "Operar exclusivamente criptomonedas"],
      0,
      "Objeto: operar AOI con recursos del público inversionista. :contentReference[oaicite:32]{index=32}")

    # AOI
    Q("Activos Objeto de Inversión (AOI) puede incluir:",
      ["Valores en RNV/SIC, efectivo, derechos/créditos y derivados permitidos por regulación",
       "Solo bienes raíces físicos",
       "Solo acciones de una emisora",
       "Solo CETES a 28 días"],
      0,
      "AOI incluye una gama amplia conforme a LFI/CNBV, según tus slides. :contentReference[oaicite:33]{index=33}")

    # Portafolio
    Q("El portafolio (cartera) de un fondo es:",
      ["Conjunto de instrumentos (deuda, renta variable, derivados, efectivo) propiedad del fondo",
       "El estado de resultados del banco",
       "Una promesa de rendimiento fijo",
       "Un contrato laboral del gestor"],
      0,
      "Portafolio: activos del fondo alineados a objetivo, riesgo y diversificación. :contentReference[oaicite:34]{index=34}")

    # Comparativo con CETES / pagaré / ETF / SIEFORE
    Q("Respecto a fondos vs CETES/pagarés, una diferencia común es:",
      ["Fondos dan participación colectiva y rendimiento variable; pagaré/CETES pueden tener rendimiento pactado",
       "Fondos siempre garantizan rendimiento",
       "CETES no tienen emisor",
       "Pagaré se negocia en bolsa intradía"],
      0,
      "Tus slides comparan rendimiento y relación inversionista-emisor. :contentReference[oaicite:35]{index=35}")

    Q("Una diferencia típica fondo vs ETF es:",
      ["ETF se compra/vende en mercado secundario; fondo abierto tiene recompra por la sociedad y opera a valuación",
       "ETF siempre tiene recompra obligatoria diaria por el emisor",
       "Fondo siempre se negocia intradía en bolsa",
       "ETF está fuera de regulación"],
      0,
      "ETF: mercado secundario; fondo abierto: recompra/valuación. :contentReference[oaicite:36]{index=36}")

    Q("Una SIEFORE se asocia principalmente con:",
      ["Ahorro para el retiro (AFORE/CONSAR) y subcuentas de retiro",
       "ETF de materias primas",
       "Warrant sobre acciones",
       "Cuenta de cheques"],
      0,
      "SIEFORE: retiro, regulada por CONSAR (según comparativo de tus slides). :contentReference[oaicite:37]{index=37}")

    # Fondo de fondos
    Q("Un fondo de fondos es:",
      ["Fondo que invierte en acciones de otros fondos, buscando diversificación multi-gestión",
       "Fondo que solo invierte en CETES",
       "ETF apalancado 3x",
       "Cuenta bancaria con seguro IPAB"],
      0,
      "Fondo de fondos: invierte en fondos para diversificar estilos. :contentReference[oaicite:38]{index=38}")

    # Operaciones autorizadas vs prohibidas
    Q("¿Cuál operación está típicamente AUTORIZADA para un fondo, según tus slides?",
      ["Celebrar reportos (solo como reportadora) y préstamos de valores con bancos/casas de bolsa",
       "Recibir depósitos de dinero como un banco",
       "Otorgar aval/garantía a terceros",
       "Practicar crédito activo (excepto reporto/préstamo de valores)"],
      0,
      "Autorizadas incluyen reporto/préstamo valores; prohibidas incluyen depósitos/avales. :contentReference[oaicite:39]{index=39}")

    Q("¿Cuál conducta aparece como PROHIBIDA en el resumen de tus slides?",
      ["Recibir depósitos de dinero",
       "Mantener acciones propias en tesorería",
       "Comprar/vender AOI conforme régimen",
       "Comprar acciones de otro fondo del mismo tipo (con límites)"],
      0,
      "Prohibición explícita: recibir depósitos. :contentReference[oaicite:40]{index=40}")

    # Estados de cuenta
    Q("Un estado de cuenta de acciones de fondos debe incluir, entre otros:",
      ["Posición valuada al corte, movimientos del periodo y avisos de modificaciones a prospectos",
       "Garantía de rendimientos futuros",
       "Solo el nombre del cliente",
       "Solo noticias del mercado"],
      0,
      "Tus slides listan contenido típico del estado de cuenta. :contentReference[oaicite:41]{index=41}")

    # Series accionarias / capital fijo
    Q("Según tus slides, el capital mínimo (fijo) de un fondo se asocia con una serie:",
      ["Serie A (capital fijo sin derecho a retiro) y la parte variable suele ser Serie B",
       "Serie Z (capital variable)",
       "Serie C (solo institucional)",
       "No existen series en fondos"],
      0,
      "Series: A capital fijo; B capital variable (general). :contentReference[oaicite:42]{index=42}")

    # Regímenes de inversión
    Q("Según la clasificación por régimen de inversión, los fondos pueden ser:",
      ["Renta variable, instrumentos de deuda, capitales y cobertura",
       "Solo renta variable",
       "Solo deuda gubernamental",
       "Solo derivados"],
      0,
      "Régimen: RV, deuda, capitales, cobertura. :contentReference[oaicite:43]{index=43}")

    # FIID vs FIRV
    Q("Un fondo en instrumentos de deuda (FIID) típicamente:",
      ["No invierte en renta variable, es menos volátil y sensible a movimientos de tasas",
       "Invierte mínimo 80% en acciones",
       "Garantiza rendimiento fijo",
       "No está influido por tasas de interés"],
      0,
      "FIID: deuda, sin RV; tasas afectan rendimiento. :contentReference[oaicite:44]{index=44}")

    Q("Comparado con FIID, un fondo de renta variable suele:",
      ["Ser más volátil y afectado por movimientos del mercado accionario",
       "Tener cupón fijo calendarizado",
       "Tener vencimiento como CETE",
       "No tener fluctuaciones de precio"],
      0,
      "RV: más volatilidad por mercado accionario. :contentReference[oaicite:45]{index=45}")

    # Indizadas (beta)
    Q("En fondos indizados, tus slides mencionan como característica:",
      ["Mantener beta entre la variable y el precio de su acción aproximadamente entre 0.95 y 1.05",
       "Mantener beta exactamente 0",
       "No seguir ningún índice",
       "Ser siempre apalancados 3x"],
      0,
      "Fondos indizados buscan replicación cercana (beta ~1). :contentReference[oaicite:46]{index=46}")

    # Categorías por duración (deuda)
    Q("En fondos de deuda, una clasificación frecuente por duración es:",
      ["Corto (≤1 año), mediano (>1 y ≤3), largo (>3)",
       "Corto (≤10 años), mediano (≤20), largo (≤30)",
       "Solo corto plazo",
       "No existe clasificación por duración"],
      0,
      "Tus slides muestran la categorización por duración. :contentReference[oaicite:47]{index=47}")

    # Variantes numéricas NAV
    for _ in range(50):
        activos = random.randint(20_000_000, 250_000_000)
        pasivos = random.randint(0, 15_000_000)
        acciones = random.randint(2_000_000, 15_000_000)
        nav = (activos - pasivos) / acciones
        Q(f"Un fondo tiene activos ${activos:,.0f}, pasivos ${pasivos:,.0f} y {acciones:,} acciones. ¿NAV por acción aprox.?",
          [f"${nav:,.4f}",
           f"${(activos/acciones):,.4f}",
           f"${((activos+pasivos)/acciones):,.4f}",
           f"${((activos-pasivos)/(acciones*10)) :,.4f}"],
          0,
          "NAV = (Activos - Pasivos) / Acciones (definición estándar).")

    random.shuffle(pool)
    return pool[:n]

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

def build_bank(min_per_area=120) -> Dict[str, List[Question]]:
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

AREA_SIZES = {
    "Ética": 60,
    "Servicios de Inversión": 60,
    "Marco Normativo I-III": 60,
    "Matemáticas y Portafolios": 80,
    "Mercado de Capitales I-II": 150,   # grande
    "Títulos de Deuda I-II": 80,
    "Fondos de Inversión": 150,         # grande
    "Derivados y Riesgos": 80,
    "Análisis Económico/Financiero/Técnico": 60,
}

# --- NUEVO: no construir todo al inicio
BANK = {}  # area -> list[Question]
AREAS = [
    "Ética",
    "Servicios de Inversión",
    "Marco Normativo I-III",
    "Matemáticas y Portafolios",
    "Mercado de Capitales I-II",
    "Títulos de Deuda I-II",
    "Fondos de Inversión",
    "Derivados y Riesgos",
    "Análisis Económico/Financiero/Técnico",
]

def init_bank():
    # Solo regresa lista de áreas (instantáneo)
    return AREAS

def ensure_area(area: str):
    """Construye banco solo si hace falta (lazy)."""
    if area in BANK and len(BANK[area]) >= AREA_SIZES.get(area, 60):
        return

    size = AREA_SIZES.get(area, 60)

    if area == "Ética":
        BANK[area] = gen_etica(size)
    elif area == "Servicios de Inversión":
        BANK[area] = gen_servicios_inversion(size)
    elif area == "Marco Normativo I-III":
        BANK[area] = gen_marco_normativo(size)
    elif area == "Matemáticas y Portafolios":
        BANK[area] = gen_matematicas_portafolios(size)
    elif area == "Mercado de Capitales I-II":
        BANK[area] = gen_mercado_capitales(size)
    elif area == "Títulos de Deuda I-II":
        BANK[area] = gen_titulos_deuda(size)
    elif area == "Fondos de Inversión":
        BANK[area] = gen_fondos(size)
    elif area == "Derivados y Riesgos":
        BANK[area] = gen_derivados(size)
    elif area == "Análisis Económico/Financiero/Técnico":
        BANK[area] = gen_analisis(size)
    else:
        raise ValueError("Área desconocida: " + area)

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
