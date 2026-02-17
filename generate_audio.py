#!/usr/bin/env python3
"""Generate ElevenLabs TTS audio for each slide of the pipeline demo."""
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen

API_KEY = "sk_0394166f2b9dcf6d33fa3ece9193ccf794f4b70ab8f5444c"
VOICE_ID = "onwK4e9ZLuTAKqWW03F9"  # Daniel - professional narrator
MODEL = "eleven_multilingual_v2"
OUTPUT_DIR = Path(__file__).parent / "audio"

NARRATIONS = [
    # Slide 0: Title
    "Bienvenidos a la demo interactiva de Redegal Prospección. En los próximos cinco minutos veremos cómo funciona el pipeline completo: desde Enginy, la plataforma de prospección B2B que identifica empresas afines al perfil de cliente ideal, pasando por Redegal Brain, la capa de inteligencia que analiza, puntúa y genera outreach personalizado con IA, hasta HubSpot, el CRM donde aterrizan los leads cualificados listos para el equipo comercial.",

    # Slide 1: The Problem
    "El reto es claro. La prospección manual no escala. El equipo comercial dedica horas a investigar empresas una por una, sin datos objetivos para priorizar. Con el pipeline inteligente, todo cambia: Enginy identifica empresas afines al ICP, Redegal Brain las analiza con seis fuentes de datos, las puntúa de cero a cien por línea de negocio, y los leads cualificados llegan directamente a HubSpot con outreach personalizado. De treinta minutos por lead a solo dos.",

    # Slide 2: Architecture
    "La arquitectura tiene tres bloques. Primero, Enginy como plataforma de prospección B2B que identifica empresas en siete mercados y las envía al sistema. Segundo, Redegal Brain, la capa de inteligencia que enriquece cada lead con seis fuentes de datos, aplica scoring en cinco dimensiones, y genera outreach personalizado con Claude. Y tercero, HubSpot como CRM de destino, donde aterrizan los leads cualificados, junto con Google Sheets para reporting, email diario a directivos y alertas por Telegram.",

    # Slide 3: Enginy - Lead Source
    "Enginy es la plataforma de prospección B2B que alimenta todo el pipeline. Busca empresas en siete mercados que encajan con el perfil de cliente ideal de cada línea de negocio. Filtra por sector, tamaño, país y actividad digital. Las empresas identificadas se envían automáticamente a Redegal Brain para su análisis completo. Es el primer eslabón de la cadena: sin Enginy, no hay leads que analizar.",

    # Slide 4: Data Enrichment
    "Una vez que Enginy identifica un lead, Redegal Brain lo enriquece con seis fuentes de datos. BuiltWith para tech stack completo. DataForSEO para métricas SEO. PageSpeed para rendimiento web. SerpAPI para noticias y señales de timing. Datos financieros de fuentes locales según el país. Y Playwright como crawler inteligente cuando las APIs no devuelven datos suficientes.",

    # Slide 5: Scoring
    "El segundo paso del Brain es el scoring. Cada empresa recibe un score de cero a cien para cada una de las cuatro líneas de negocio. El score se calcula con cinco dimensiones, cada una con pesos configurables por línea. ICP Fit, Need Detected, Timing, Investment Capacity y Accessibility. Un score mayor o igual a setenta es hot, mayor o igual a cuarenta y cinco es warm, y por debajo es cold.",

    # Slide 6: Example - Casa del Libro
    "Veamos un ejemplo real. Casa del Libro llega desde Enginy como empresa identificada en el ICP de Boostic. Redegal Brain la analiza: e-commerce con plataforma custom Java, más de quinientas mil referencias, y un PageSpeed de solo cuarenta y dos. Los scores: ochenta y dos en Boostic categoría hot, sesenta y cinco en Digital Tech warm. Claude genera un mensaje de outreach personalizado. Todo esto llega a HubSpot como un contacto y deal cualificado con el outreach listo para el comercial.",

    # Slide 7: Redegal Brain
    "Redegal Brain es el corazón inteligente del sistema. Recibe leads desde Enginy y ejecuta tres fases: enriquecimiento de datos con seis fuentes, scoring determinista con cinco dimensiones por línea de negocio, y generación de outreach personalizado con Claude en el idioma del mercado. Todo sin intervención humana. El resultado: leads cualificados con toda la información necesaria para que el equipo comercial actúe con contexto.",

    # Slide 8: HubSpot CRM
    "HubSpot es el destino final del pipeline. Los leads cualificados por Redegal Brain aterrizan como contactos con custom properties: score de prospección, clasificación hot warm o cold, línea de negocio, y tech stack detectado. Los deals se crean automáticamente por línea. El outreach generado por Claude se adjunta como nota. Y con webhooks, HubSpot puede notificar cambios de stage de vuelta al sistema.",

    # Slide 9: Full Pipeline
    "El pipeline completo en acción. Enginy identifica empresas afines al ICP en siete mercados. Redegal Brain las enriquece con seis fuentes de datos, calcula scores por línea de negocio, y genera outreach personalizado con Claude. Los leads cualificados se sincronizan automáticamente en HubSpot. En paralelo, Google Sheets recibe el reporting, los directivos reciben email diario, y Telegram alerta de hot leads en tiempo real.",

    # Slide 10: Daily Flow
    "Así funciona el sistema día a día. A las seis de la mañana, Enginy entrega nuevos leads identificados. A las seis y media, Redegal Brain ejecuta los collectors y enriquece cada lead. A las siete, los cinco analyzers calculan scores y Claude genera outreach. A las siete y cuarto, los leads cualificados se sincronizan con HubSpot. A las ocho, el email diario llega a los directivos filtrado por línea de negocio. Y de forma continua, cualquier hot lead genera alerta instantánea en Telegram.",

    # Slide 11: Metrics
    "Los números del sistema. Siete países configurados. Cuatro líneas de negocio. Seis fuentes de datos. Cinco dimensiones de scoring. Solo dos minutos por lead analizado. Integración completa con HubSpot como CRM de destino. Cuatrocientos treinta y tres tests pasando. Y funcionando veinticuatro siete de forma automatizada. Añadir un nuevo país, un fichero YAML. Añadir una línea de negocio, otro YAML. Todo extensible sin código.",

    # Slide 12: Next Steps
    "Empezar es fácil. Clona el repositorio, ejecuta bash install punto sh, y el instalador interactivo te guía en cinco minutos. Configura API keys, SMTP, base de datos, y opcionalmente carga datos demo. Luego activa el entorno virtual, arranca uvicorn, y abre el dashboard. El pipeline Enginy, Redegal Brain, HubSpot está listo para producción. Gracias por ver esta demo.",
]

def generate_audio(text: str, output_path: Path) -> bool:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    payload = json.dumps({
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.78,
            "style": 0.15,
        },
    }).encode()

    req = Request(url, data=payload, method="POST")
    req.add_header("xi-api-key", API_KEY)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "audio/mpeg")

    try:
        resp = urlopen(req)
        with open(output_path, "wb") as f:
            f.write(resp.read())
        size_kb = output_path.stat().st_size / 1024
        print(f"  OK  {output_path.name}  ({size_kb:.0f} KB)")
        return True
    except Exception as e:
        print(f"  FAIL  {output_path.name}  {e}")
        return False


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"\nGenerando {len(NARRATIONS)} audios con ElevenLabs...\n")

    ok = 0
    for i, text in enumerate(NARRATIONS):
        path = OUTPUT_DIR / f"slide_{i:02d}.mp3"
        if generate_audio(text, path):
            ok += 1
        # Rate limiting
        if i < len(NARRATIONS) - 1:
            time.sleep(1)

    print(f"\n{ok}/{len(NARRATIONS)} audios generados en {OUTPUT_DIR}/\n")


if __name__ == "__main__":
    main()
