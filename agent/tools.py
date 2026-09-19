# agent/tools.py — Herramientas del agente
# Generado por AgentKit

"""
Herramientas especificas del negocio: Negocio en Automatico.

OJO: estas funciones NO se ejecutan solas todavia. La informacion del negocio le llega
al agente por el system prompt (config/prompts.yaml), asi que para CONTESTAR preguntas
no hace falta nada de aca. Este archivo es el lugar para las ACCIONES —agendar una
llamada, registrar un lead— y conectarlas al ciclo de tool use de Claude es un paso
aparte que todavia no esta hecho.

Casos de uso elegidos en la entrevista: FAQ, agendar llamadas, calificar y atender leads.
"""

import logging
from pathlib import Path

import yaml

logger = logging.getLogger("agentkit")

CARPETA_KNOWLEDGE = Path("knowledge")


def cargar_info_negocio() -> dict:
    """Carga la informacion del negocio desde config/business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atencion del negocio. Negocio en Automatico atiende 24/7."""
    info = cargar_info_negocio()
    return {
        "horario": info.get("negocio", {}).get("horario", "No disponible"),
        "esta_abierto": True,  # 24/7: siempre abierto
    }


def buscar_en_knowledge(consulta: str) -> str:
    """
    Busca informacion en los archivos de /knowledge.
    Retorna los fragmentos que coinciden con la consulta.
    """
    if not CARPETA_KNOWLEDGE.is_dir():
        return "No hay archivos de conocimiento disponibles."

    resultados = []
    for ruta in sorted(CARPETA_KNOWLEDGE.iterdir()):
        if ruta.name.startswith(".") or not ruta.is_file():
            continue
        try:
            contenido = ruta.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue  # binarios y archivos ilegibles se saltean
        if consulta.lower() in contenido.lower():
            resultados.append(f"[{ruta.name}]: {contenido[:500]}")

    if resultados:
        return "\n---\n".join(resultados)
    return "No encontre informacion especifica sobre eso en mis archivos."


# ════════════════════════════════════════════════════════════
# Agendar llamadas
# ════════════════════════════════════════════════════════════
#
# TODO: hoy no hay un calendario conectado. Estas funciones dejan la
# estructura lista; para que agenden de verdad hace falta conectarlas
# a Google Calendar / Calendly / lo que uses, y al ciclo de tool use.

def obtener_slots_disponibles(fecha: str) -> list[dict]:
    """
    Retorna los horarios disponibles para agendar una llamada en una fecha dada.

    TODO: conectar con el calendario real (Google Calendar, Calendly, etc).
    Por ahora retorna una lista vacia: el agente debe pedirle a la persona
    que Nicolas la contacte directamente para coordinar.
    """
    logger.info(f"obtener_slots_disponibles llamado para {fecha} (todavia no conectado a un calendario)")
    return []


def agendar_llamada(telefono: str, nombre: str, negocio: str, fecha: str, hora: str) -> dict:
    """
    Registra la intencion de agendar una llamada.

    TODO: conectar con el calendario real. Por ahora solo deja el registro
    en el log para que Nicolas la agende a mano.
    """
    logger.info(
        f"[AGENDAR LLAMADA] telefono={telefono} nombre={nombre} "
        f"negocio={negocio} fecha={fecha} hora={hora}"
    )
    return {"registrado": True, "confirmado": False}


# ════════════════════════════════════════════════════════════
# Calificar y atender leads
# ════════════════════════════════════════════════════════════
#
# TODO: hoy no hay un CRM conectado. Estas funciones dejan la estructura
# lista para cuando quieras conectar un CRM real (o una hoja de calculo)
# y engancharlas al ciclo de tool use de Claude.

def registrar_lead(telefono: str, nombre: str, negocio: str, interes: str) -> dict:
    """
    Registra un lead nuevo con lo que se sabe hasta el momento.

    TODO: conectar con un CRM real (HubSpot, una hoja de Google Sheets, etc).
    Por ahora solo deja el registro en el log.
    """
    logger.info(
        f"[LEAD] telefono={telefono} nombre={nombre} negocio={negocio} interes={interes}"
    )
    return {"registrado": True}


def calificar_lead(telefono: str) -> str:
    """
    Devuelve una calificacion simple del lead segun lo conversado hasta ahora.

    TODO: hoy es un placeholder. La logica real de calificacion (tiene negocio
    activo, presupuesto, urgencia) debe salir de lo que el agente ya converso
    y guardar en agent/memory.py, no de una funcion aparte.
    """
    return "sin_calificar"


def escalar_a_nicolas(telefono: str, contexto: str) -> dict:
    """
    Marca la conversacion para que Nicolas la revise directamente
    (lead caliente, pregunta que el agente no pudo resolver, etc).

    TODO: conectar una notificacion real (email, Slack, WhatsApp propio).
    Por ahora solo deja el registro en el log.
    """
    logger.warning(f"[ESCALAR A NICOLAS] telefono={telefono} contexto={contexto}")
    return {"escalado": True}
