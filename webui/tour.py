"""Tutorial de navegación para la interfaz web del Descargador de Medios de Telegram."""

from nicegui import ui

# ── Definición de pasos del tour ──
TOUR_STEPS = [
    {
        "icon": "👋",
        "title": "Bienvenido a TG Downloader",
        "body": (
            "Esta herramienta te ayuda a descargar medios en masa desde chats y canales de Telegram.\n\n"
            "Te guiaremos a través de **cada sección** paso a paso para que puedas configurarte rápidamente.\n\n"
            "Usa **Siguiente** para continuar o **✕** para cerrar en cualquier momento."
        ),
    },
    {
        "icon": "🔑",
        "title": "Paso 1 · Credenciales de API",
        "page": "config",
        "body": (
            "Primero necesitas un API ID y Hash de Telegram. Así se obtienen:\n\n"
            "1. Ve a [my.telegram.org](https://my.telegram.org) e inicia sesión con tu número de teléfono\n"
            "2. Haz clic en **Herramientas de Desarrollo de API**\n"
            "3. Crea una nueva aplicación (cualquier nombre sirve)\n"
            "4. Copia el **API ID** (un número) y el **API Hash** (una cadena)\n\n"
            "Pégalos en los campos **API ID** y **API Hash** de la primera tarjeta. "
            "El hash está oculto por defecto — haz clic en el ícono de ojo para verlo.\n\n"
            "> ⚠️ Mantén estas credenciales en privado. Se almacenan solo en tu `config.yaml` local."
        ),
    },
    {
        "icon": "📂",
        "title": "Paso 2 · Directorio de Descarga",
        "page": "config",
        "body": (
            "En la tarjeta **Configuración de Descarga**, indica dónde se guardarán tus archivos:\n\n"
            "- **Directorio de Descarga** — La carpeta donde se guardarán todos los medios. "
            "Déjalo vacío para usar el directorio propio de la app\n"
            "- La ruta puede ser absoluta (p.ej. `/Usuarios/tu/Descargas/telegram`) o "
            "relativa al directorio desde donde se ejecuta la app\n\n"
            "¡Asegúrate de que el directorio exista y tenga permisos de escritura!"
        ),
    },
    {
        "icon": "⚡",
        "title": "Paso 3 · Concurrencia y Cadencia",
        "page": "config",
        "body": (
            "Estos ajustes te ayudan a **evitar bloqueos por límite de velocidad de Telegram**:\n\n"
            "- **Máx. Concurrentes** — Cuántos archivos se descargan simultáneamente. "
            "Empieza con `1`–`3` para mayor seguridad. Valores más altos son más rápidos pero más arriesgados\n"
            "- **Retraso de Descarga (seg)** — Tiempo de espera entre el inicio de cada archivo. "
            "Ingresa un número como `2`, o un rango como `1,5` para un retraso aleatorio "
            "entre 1–5 segundos\n\n"
            "> 💡 **Consejo:** Si es la primera vez que descargas de un canal grande, "
            "usa configuraciones conservadoras (máx. 2 concurrentes, 2–3 seg de retraso)."
        ),
    },
    {
        "icon": "🎬",
        "title": "Paso 4 · Tipos de Medios",
        "page": "config",
        "body": (
            "Aún en **Configuración de Descarga**, elige qué tipos de medios descargar:\n\n"
            "- **photo** — Imágenes y fotos\n"
            "- **video** — Archivos de video\n"
            "- **document** — PDFs, ZIPs y otros documentos\n"
            "- **audio** — Música y archivos de audio\n"
            "- **voice** — Mensajes de voz y notas de voz\n\n"
            "Haz clic en la ✕ de un chip para eliminarlo, o escribe en el campo para volver a añadirlo.\n\n"
            "Marca también **Chats en Paralelo** si quieres descargar de varios chats a la vez."
        ),
    },
    {
        "icon": "💬",
        "title": "Paso 5 · Chats Objetivo",
        "page": "config",
        "body": (
            "En la tarjeta **Chats Objetivo**, añade los chats de los que descargar:\n\n"
            "- Haz clic en **＋ Añadir Chat** para agregar una nueva entrada\n"
            "- **Chat ID** — El ID numérico del chat/canal. Puedes encontrarlo con bots "
            'como @userinfobot o activando "Mostrar ID de Chat" en Telegram Desktop\n'
            "- **Último Msg ID Leído** — Registra dónde se detuvo el descargador. Se actualiza automáticamente tras cada ejecución\n\n"
            "Expande **Opciones Avanzadas** para establecer un directorio de descarga por chat o seleccionar tipos de medios específicos para ese chat."
        ),
    },
    {
        "icon": "💾",
        "title": "Paso 6 · Guardar la Configuración",
        "page": "config",
        "body": (
            "Cuando termines de configurar, desplázate hacia abajo y haz clic en **Guardar Configuración**.\n\n"
            "Esto escribe tus ajustes en `config.yaml` en el directorio de la app.\n\n"
            "- **Guardar Configuración** — Escribe todos los ajustes actuales en disco\n"
            "- **Recargar desde Disco** — Descarta los cambios no guardados y recarga desde el archivo\n\n"
            "> 📌 **Debes** guardar antes de iniciar una descarga — el descargador lee desde el archivo de configuración guardado."
        ),
    },
    {
        "icon": "▶️",
        "title": "Paso 7 · Ejecutar Descargas",
        "page": "execution",
        "body": (
            "Cambia a la pestaña **Ejecución** para comenzar la descarga:\n\n"
            "1. Haz clic en el botón **Iniciar Descarga** al final\n"
            "2. La app se conecta a Telegram (puede que debas autenticarte en la primera ejecución vía terminal)\n"
            "3. Observa el **indicador de estado** en la esquina superior derecha — muestra:\n"
            "   - 🔵 **Inactivo** — Listo para iniciar\n"
            "   - 🟡 **Ejecutando** — Descarga en progreso\n"
            "   - 🟢 **Completado** — Finalizado con éxito\n"
            "   - 🔴 **Error** — Algo salió mal\n\n"
            "También verás junto al estado un badge con el tipo de cuenta: "
            "**⭐ Premium** o **👤 Gratis**, junto con tu nombre de usuario.\n\n"
            "La tarjeta **Descargas Activas** muestra barras de progreso en tiempo real para cada archivo, "
            "con tamaño y porcentaje. Los archivos completados muestran ✓ y un botón **Abrir**."
        ),
    },
    {
        "icon": "🖥️",
        "title": "Paso 8 · Registros del Terminal",
        "page": "execution",
        "body": (
            "Debajo de Descargas Activas hay una sección colapsable de **Salida del Terminal**:\n\n"
            "- Haz clic en el encabezado para **expandir/colapsar**\n"
            "- Muestra registros detallados: estado de conexión, progreso archivo por archivo, errores y advertencias\n"
            "- Útil para depurar si las descargas fallan o se quedan bloqueadas\n"
            "- Mantiene las últimas 300 líneas de registro — las entradas más antiguas se eliminan automáticamente\n\n"
            "> 💡 **Consejo:** Si una descarga parece atascada, expande el terminal para revisar "
            "advertencias de límite de velocidad de Telegram o solicitudes de autenticación."
        ),
    },
    {
        "icon": "📋",
        "title": "Paso 9 · Historial de Descargas",
        "page": "history",
        "body": (
            "La pestaña **Historial** muestra cada archivo que se ha descargado:\n\n"
            "- **Buscar** — Escribe un nombre de archivo para filtrar resultados al instante\n"
            "- **Filtro de tipo** — Desplegable para mostrar solo fotos, videos, documentos, etc.\n"
            "- **Ordenar columnas** — Haz clic en cualquier encabezado de columna para ordenar por Fecha, Chat, Nombre o Tamaño\n"
            "- **Paginación** — Navega por páginas al final, 20 elementos por página\n"
            "- **Abrir ↗** — Haz clic para previsualizar archivos en el navegador (imágenes, videos, audio, PDFs)\n"
            "- **Limpiar Todo** — Borra el registro del historial (no elimina los archivos reales)\n\n"
            "¡Todo listo! Feliz descarga 🎉"
        ),
    },
]


def build_tour(current_page: dict, tab_panels, nav_items: list):
    """Build the floating tour panel and return (show_tour, check_first_visit) functions.

    Parameters
    ----------
    current_page : dict
        Mutable dict with ``{"value": "config"}`` for sidebar navigation state.
    tab_panels : nicegui TabPanels element
        The tab panels container to switch pages.
    nav_items : list[tuple]
        List of ``(nav_element, page_key)`` tuples for sidebar highlighting.

    Returns
    -------
    tuple[callable, callable]
        ``(show_tour, check_first_visit)`` functions.
    """
    tour_panel = ui.element("div").style(
        "position: fixed; bottom: 24px; right: 24px; z-index: 9999; "
        "width: 420px; max-width: calc(100vw - 320px); "
        "background: var(--surface); border: 1px solid var(--border); "
        "border-radius: var(--radius-xl); box-shadow: var(--shadow-lg); "
        "overflow: hidden; display: none; transition: all 0.3s ease;"
    )
    tour_state = {"step": 0}

    with tour_panel:
        # Header bar
        with ui.row().classes("items-center justify-between").style(
            "padding: 12px 16px; border-bottom: 1px solid var(--border); background: var(--surface-dim);"
        ):
            with ui.row().classes("items-center").style("gap: 8px;"):
                tour_icon = ui.label("").style("font-size: 20px;")
                tour_title = ui.label("").style(
                    "font-size: 14px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.01em;"
                )
            ui.button(icon="close", on_click=lambda: finish_tour()).props(
                "flat dense round size=sm color=grey-6"
            )

        # Body
        tour_body = ui.markdown("").style(
            "font-size: 13px; color: var(--text-secondary); line-height: 1.65; "
            "padding: 16px 20px 12px; max-height: 320px; overflow-y: auto;"
        )

        # Footer: progress + buttons
        with ui.column().style("padding: 0 20px 16px; gap: 10px;"):
            with ui.row().classes("items-center").style("gap: 8px; width: 100%;"):
                tour_progress = (
                    ui.linear_progress(value=0, show_value=False)
                    .props("instant-feedback color=primary size=3px rounded")
                    .style("flex: 1;")
                )
                tour_counter = ui.label("").style(
                    "font-size: 11px; font-weight: 600; color: var(--text-tertiary); "
                    "white-space: nowrap;"
                )

            with ui.row().style(
                "width: 100%; justify-content: space-between; gap: 8px;"
            ):
                tour_back_btn = (
                    ui.button("Atrás", on_click=lambda: tour_navigate(-1))
                    .props("flat dense color=grey-7")
                    .style("font-size: 12px;")
                )
                tour_next_btn = (
                    ui.button("Siguiente", on_click=lambda: tour_navigate(1))
                    .props('unelevated dense color="primary"')
                    .style("font-size: 12px; padding: 4px 20px;")
                )

    def show_tour():
        tour_state["step"] = 0
        render_tour_step()
        ui.run_javascript(
            f"document.querySelector('[id=\"c{tour_panel.id}\"]').style.display = 'block'"
        )

    def render_tour_step():
        s = TOUR_STEPS[tour_state["step"]]
        tour_icon.set_text(s["icon"])
        tour_title.set_text(s["title"])
        tour_body.set_content(s["body"])

        # Navigate to relevant page
        if "page" in s:
            current_page["value"] = s["page"]
            tab_panels.set_value(s["page"])
            for item, key in nav_items:
                if key == s["page"]:
                    item.classes(replace="nav-item active")
                else:
                    item.classes(replace="nav-item")

        # Update counter + progress
        total = len(TOUR_STEPS)
        current = tour_state["step"] + 1
        tour_counter.set_text(f"{current}/{total}")
        tour_progress.set_value(current / total)

        # Update buttons
        is_first = tour_state["step"] == 0
        is_last = tour_state["step"] == len(TOUR_STEPS) - 1
        tour_back_btn.set_visibility(not is_first)
        if is_last:
            tour_next_btn.set_text("Finalizar")
        else:
            tour_next_btn.set_text("Siguiente")

    def tour_navigate(direction):
        new_step = tour_state["step"] + direction
        if new_step >= len(TOUR_STEPS):
            finish_tour()
            return
        tour_state["step"] = max(0, new_step)
        render_tour_step()

    def finish_tour():
        ui.run_javascript(
            f"document.querySelector('[id=\"c{tour_panel.id}\"]').style.display = 'none'"
        )
        tour_state["step"] = 0
        ui.run_javascript("localStorage.setItem('tg_dl_tour_seen', '1')")

    async def check_first_visit():
        result = await ui.run_javascript("localStorage.getItem('tg_dl_tour_seen')")
        if not result:
            show_tour()

    return show_tour, check_first_visit
