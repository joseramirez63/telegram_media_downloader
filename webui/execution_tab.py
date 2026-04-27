"""Pestaña de ejecución de la interfaz web del Descargador de Medios de Telegram."""

import logging
import os
import urllib.parse

from nicegui import ui

import media_downloader


def build_execution_tab(
    config: dict, load_config_fn, chat_inputs: list, open_media_fn, this_dir: str
):
    """Construye los contenidos del panel de la pestaña Ejecución.

    Parameters
    ----------
    config : dict
        Diccionario de configuración cargado.
    load_config_fn : callable
        Función para recargar la configuración desde el disco.
    chat_inputs : list
        Lista de dicts de entrada de chats (de la pestaña de configuración)
        para actualizar last_read tras la ejecución.
    open_media_fn : callable
        ``open_media(url, filename)`` para el diálogo de vista previa.
    this_dir : str
        Ruta absoluta al directorio raíz del proyecto.
    """
    with ui.column().style("gap: 2px; margin-bottom: 28px;"):
        with ui.row().classes("items-center justify-between").style("width: 100%;"):
            with ui.column().style("gap: 2px;"):
                ui.label("Ejecución").classes("section-title")
                ui.label(
                    "Inicia la descarga de medios desde tus chats configurados."
                ).classes("section-subtitle")
            with ui.row().classes("items-center").style("gap: 8px;"):
                account_badge = ui.html("")
                status_label = ui.html(
                    '<span class="status-badge status-idle">'
                    '<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;"></span>'
                    " Inactivo</span>"
                )

    # ── Progreso de Descarga ──
    with ui.element("div").classes("premium-card").style(
        "padding: 24px; margin-bottom: 20px;"
    ):
        with ui.row().classes("items-center").style("gap: 10px; margin-bottom: 16px;"):
            ui.icon("downloading", size="sm", color="primary")
            ui.label("Descargas Activas").style(
                "font-size: 15px; font-weight: 600; color: var(--text-primary);"
            )

        progress_container = ui.column().style(
            "width: 100%; gap: 8px; max-height: 320px; overflow-y: auto; padding-right: 4px;"
        )
        ui.html(
            '<div style="padding: 12px 0; text-align: center; color: var(--text-tertiary); font-size: 13px;" id="empty-state">Sin descargas activas</div>'
        )

    # ── Registros del Terminal (colapsable) ──
    with ui.element("div").classes("premium-card").style(
        "padding: 0; margin-bottom: 20px; overflow: hidden;"
    ):
        with ui.expansion("Salida del Terminal", icon="terminal", value=False).style(
            "width: 100%; font-size: 15px; font-weight: 600;"
        ).props("dense"):
            log_area = (
                ui.log(max_lines=300)
                .classes("terminal-log")
                .style(
                    "width: 100%; height: 420px; min-height: 420px; max-height: 420px; padding: 16px; font-size: 13px; line-height: 1.7; overflow-y: auto;"
                )
            )

    # Manejador de registros personalizado
    class UILogHandler(logging.Handler):
        def emit(self, record):
            try:
                msg = self.format(record)
                log_area.push(msg)
            except Exception:
                pass

    ui_logger = UILogHandler()
    ui_logger.setFormatter(logging.Formatter("%(message)s"))

    is_running = {"value": False}
    active_downloads = {}

    def update_status(text, style_class):
        dot = '<span style="width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block;"></span>'
        status_label.content = (
            f'<span class="status-badge {style_class}">{dot} {text}</span>'
        )

    def update_account_badge():
        info = media_downloader.ACCOUNT_INFO
        if not info:
            account_badge.content = ""
            return
        username = info.get("username", "")
        is_premium = info.get("is_premium", False)
        if is_premium:
            badge_html = (
                f'<span class="status-badge" style="background:rgba(250,204,21,0.15);color:#b45309;gap:6px;">'
                f'<span style="font-size:14px;">⭐</span> Premium · {username}</span>'
            )
        else:
            badge_html = (
                f'<span class="status-badge status-idle">'
                f"👤 Gratis · {username}</span>"
            )
        account_badge.content = badge_html

    def ui_progress_hook(desc, current, total, file_path=None, media_type=None):
        if desc not in active_downloads:
            with progress_container:
                row = (
                    ui.row()
                    .classes("dl-row")
                    .style("width: 100%; align-items: center; gap: 12px;")
                )
                with row:
                    name_label = ui.label(desc).style(
                        "font-size: 13px; font-weight: 500; color: var(--text-secondary); "
                        "white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 35%;"
                    )
                    bar = (
                        ui.linear_progress(value=0, show_value=False)
                        .props("instant-feedback color=primary size=6px rounded")
                        .style("width: 30%; border-radius: 3px;")
                    )
                    pct_label = ui.label("0%").style(
                        "font-size: 12px; font-weight: 500; color: var(--text-tertiary); "
                        "text-align: center; width: 20%; font-variant-numeric: tabular-nums;"
                    )
                    action_col = ui.column().style(
                        "width: 10%; min-width: 50px; align-items: flex-end;"
                    )
                active_downloads[desc] = (row, name_label, bar, pct_label, action_col)

        row, name_label, bar, pct_label, action_col = active_downloads[desc]
        if total > 0:
            fraction = current / total
            bar.set_value(fraction)
            pct_label.set_text(
                f"{current / 1024 / 1024:.1f}M / {total / 1024 / 1024:.1f}M ({fraction * 100:.1f}%)"
            )
            if current >= total:
                name_label.style(
                    "font-size: 13px; font-weight: 600; color: var(--positive); "
                    "white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 35%;"
                )
                if desc.startswith("Downloading "):
                    name_label.set_text(desc.replace("Downloading ", "✓ ", 1))

                if file_path and not getattr(row, "has_open_btn", False):
                    row.has_open_btn = True
                    global_download_dir = config.get("download_directory", "")
                    file_url = ""
                    try:
                        abs_fpath = os.path.abspath(file_path)
                        abs_base = (
                            os.path.abspath(global_download_dir)
                            if global_download_dir
                            else this_dir
                        )
                        if abs_fpath.startswith(abs_base):
                            rel_path = os.path.relpath(abs_fpath, abs_base)
                            rel_path = rel_path.replace("\\", "/")
                            encoded_path = urllib.parse.quote(rel_path, safe="/")
                            file_url = f"/media/{encoded_path}"
                    except Exception:
                        pass
                    if file_url:
                        with action_col:
                            fname = os.path.basename(file_path)
                            ui.button(
                                "Abrir",
                                on_click=lambda u=file_url, n=fname: open_media_fn(
                                    u, n
                                ),
                            ).props('flat dense color="primary" size="sm"').style(
                                "font-size: 12px;"
                            )
        else:
            bar.set_value(0)
            pct_label.set_text(f"{current} bytes")

    async def run_downloader():
        if is_running["value"]:
            ui.notify("¡El descargador ya está en ejecución!", type="warning")
            return
        is_running["value"] = True
        start_btn.set_enabled(False)
        main_logger = logging.getLogger("media_downloader")
        main_logger.addHandler(ui_logger)
        try:
            log_area.clear()
            progress_container.clear()
            active_downloads.clear()
            update_status("Ejecutando", "status-running")
            ui.notify("Iniciando cliente de Telegram…", type="info")
            media_downloader.UI_PROGRESS_HOOK = ui_progress_hook
            fresh_config = load_config_fn()
            updated_config = await media_downloader.begin_import(
                fresh_config, pagination_limit=100
            )
            media_downloader.update_config(updated_config)
            update_account_badge()
            updated_chats = updated_config.get("chats", [])
            for i, c in enumerate(updated_chats):
                if i < len(chat_inputs):
                    chat_inputs[i]["last_read"].value = c.get("last_read_message_id", 0)
            total_failures = sum(
                len(set(flist)) for flist in media_downloader.FAILED_IDS.values()
            )
            if total_failures > 0:
                update_status(f"Listo · {total_failures} errores", "status-warning")
                log_area.push(
                    f"Advertencia: {total_failures} archivos fallaron. Revisa ids_to_retry en config.yaml."
                )
                ui.notify(
                    f"Finalizado, pero {total_failures} archivos fallaron.",
                    type="warning",
                    position="top",
                )
            else:
                update_status("Completado", "status-success")
                ui.notify(
                    "¡Descarga completada!",
                    type="positive",
                    position="top",
                )
        except Exception as e:
            update_status("Error", "status-error")
            log_area.push(f"Error: {str(e)}")
            ui.notify(f"Error: {str(e)}", type="negative", position="top")
        finally:
            media_downloader.UI_PROGRESS_HOOK = None
            is_running["value"] = False
            start_btn.set_enabled(True)
            main_logger.removeHandler(ui_logger)

    start_btn = (
        ui.button("Iniciar Descarga", on_click=run_downloader, icon="play_arrow")
        .props('unelevated color="primary"')
        .style("width: 100%; height: 48px; font-size: 14px; font-weight: 600;")
    )
