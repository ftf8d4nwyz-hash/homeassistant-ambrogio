"""Génère la configuration Lovelace du dashboard NEXUS."""
import json

DASH = "dashboard-nexus"
NAV_FLAG = "input_boolean.nexus_navigation_compacte"

# ── Design tokens ────────────────────────────────────────────────────────────
CY, BL, VI, GR, AM, RD = "#22D3EE", "#5B8DEF", "#A78BFA", "#34D399", "#FBBF24", "#F87171"
MUT = "#8B95A7"

KF = "@keyframes nxIn{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}"
KF_SH = "@keyframes nxSh{0%{background-position:-460px 0}to{background-position:460px 0}}"
EASE = "cubic-bezier(.22,.61,.36,1)"


def glass(delay=0.0, accent=BL, radius=18, extra=""):
    """Carte 'verre dépoli' + animation d'entrée décalée."""
    return {
        "style": (
            "ha-card{--ha-card-background:transparent;"
            "background:linear-gradient(155deg,#1c2333f0,#0e121bf7);"
            f"border:1px solid #ffffff12;border-radius:{radius}px;"
            "box-shadow:0 12px 34px -16px #000000d9,inset 0 1px 0 #ffffff0d;"
            f"animation:nxIn .55s {EASE} {delay:.2f}s both;"
            "transition:transform .28s,border-color .28s,box-shadow .28s}"
            f"ha-card:hover{{transform:translateY(-3px);border-color:{accent}59;"
            f"box-shadow:0 20px 46px -18px #000000e6,0 0 0 1px {accent}2b}}"
            f"{KF}{extra}"
        )
    }


def skeleton(delay=0.0, accent=BL):
    """Carte verre + squelette scintillant tant que l'entité n'a pas d'état."""
    extra = (
        "ha-card{{% if states(config.entity) in ['unavailable','unknown','None'] %}"
        "--primary-text-color:transparent;--secondary-text-color:transparent;"
        "--state-icon-color:transparent;pointer-events:none;"
        "background-image:linear-gradient(100deg,#fff0 18%,#ffffff14 40%,#fff0 62%);"
        "background-size:460px 100%;background-repeat:no-repeat;"
        "animation:nxSh 1.6s linear infinite;{% endif %}}"
        f"{KF_SH}"
    )
    return glass(delay, accent, extra=extra)


# ── Navigation ───────────────────────────────────────────────────────────────
NAV = [
    ("Accueil", "mdi:view-dashboard-outline", "accueil", CY),
    ("Énergie", "mdi:lightning-bolt-outline", "energie", AM),
    ("Maison", "mdi:home-heart", "maison", VI),
    ("Sécurité", "mdi:shield-home-outline", "securite", GR),
]


def nav_style(accent, on, dashed=False):
    """Chrome de navigation : léger, sans animation d'entrée (élément persistant)."""
    bg = f"{accent}26,#0e121bf5" if on else "#1c2333e6,#0e121bf2"
    return {
        "style": (
            "ha-card{--ha-card-background:transparent;"
            f"background:linear-gradient(150deg,{bg});"
            f"border:1px {'dashed' if dashed else 'solid'} {accent}{'8c' if on else '1f'};"
            "border-radius:14px;box-shadow:0 8px 22px -14px #000000cc;"
            "transition:transform .25s,border-color .25s}"
            f"ha-card:hover{{transform:translateY(-2px);border-color:{accent}8c}}"
            f"ha-card ha-state-icon{{color:{accent if on else MUT};transition:color .25s}}"
            f"ha-card:hover ha-state-icon{{color:{accent}}}"
            f"ha-card div.name{{color:{'#E6EAF2' if on else MUT};"
            "font-weight:600;font-size:13px}"
        )
    }


def nav_btn(label, icon, path, accent, active, compact):
    card = {
        "type": "button",
        "icon": icon,
        "show_name": not compact,
        "show_state": False,
        "tap_action": {"action": "navigate", "navigation_path": f"/{DASH}/{path}"},
        "card_mod": nav_style(accent, path == active),
    }
    if not compact:
        card["name"] = label
    return card


def nav_section(active):
    """Barre de navigation pleine largeur, mode étendu / compact / mobile."""
    toggle = lambda compact: {
        "type": "button",
        "icon": "mdi:dock-right" if compact else "mdi:dock-left",
        "name": "Réduire",
        "show_name": not compact,
        "show_state": False,
        "tap_action": {"action": "toggle"},
        "entity": NAV_FLAG,
        "card_mod": nav_style(MUT, False, dashed=True),
    }

    def rail(compact):
        return {
            "type": "grid",
            "columns": 5,
            "square": False,
            "cards": [nav_btn(*n, active, compact) for n in NAV] + [toggle(compact)],
            "visibility": [
                {
                    "condition": "state",
                    "entity": NAV_FLAG,
                    "state": "on" if compact else "off",
                }
            ],
            "grid_options": {"columns": "full"},
        }

    return {
        "type": "grid",
        "column_span": 4,
        "cards": [rail(False), rail(True)],
    }


# ── Cartes réutilisables ─────────────────────────────────────────────────────
def heading(text, icon, style="title", badges=None):
    card = {"type": "heading", "heading": text, "heading_style": style, "icon": icon}
    if badges:
        card["badges"] = badges
    return card


def kpi(entity, name, icon, accent, color, delay, hours=24):
    return {
        "type": "tile",
        "entity": entity,
        "name": name,
        "icon": icon,
        "color": color,
        "hide_state": False,
        "vertical": False,
        "features_position": "bottom",
        "features": [{"type": "trend-graph", "hours_to_show": hours}],
        "grid_options": {"columns": 6, "rows": 2},
        "card_mod": skeleton(delay, accent),
    }


HERO = {
    "type": "markdown",
    "content": (
        "{% set h = now().hour %}"
        "{% set sal = 'Bonne nuit' if h < 6 else ('Bonjour' if h < 12 else "
        "('Bon après-midi' if h < 18 else 'Bonsoir')) %}"
        "{% set on = states.light | selectattr('state','eq','on') | list | count %}"
        "{% set ici = states.person | selectattr('state','eq','home') | list | count %}"
        "{% set w = states('weather.forecast_maison') %}"
        "{% set t = state_attr('weather.forecast_maison','temperature') %}"
        "{% set p = states('sensor.capteur_de_consommation_electrique_electric_power_consumption') %}"
        "# {{ sal }}\n"
        "### {{ t | round(0) if t is not none else '—' }}°C · "
        "{{ p | int(0) }} W · {{ on }} lumière{{ 's' if on > 1 }} allumée{{ 's' if on > 1 }}\n"
        "{{ ici }} personne{{ 's' if ici > 1 }} à la maison — "
        "{{ now().strftime('%A %d %B') }}"
    ),
    "grid_options": {"columns": "full"},
    "card_mod": {
        "style": (
            "ha-card{--ha-card-background:transparent;"
            "background:radial-gradient(120% 180% at 0% 0%,#22d3ee38 0%,"
            "#5b8def21 34%,#0c1018f7 72%);"
            "border:1px solid #ffffff17;border-radius:22px;"
            "box-shadow:0 22px 60px -26px #000000f2,inset 0 1px 0 #ffffff12;"
            "padding:6px 4px;"
            f"animation:nxIn .6s {EASE} both}}"
            "ha-card h1{font-size:34px;font-weight:700;letter-spacing:-.02em;"
            "margin:4px 0 2px;line-height:1.1}"
            f"ha-card h3{{font-size:15px;font-weight:600;color:{CY};margin:0 0 6px}}"
            f"ha-card p{{color:{MUT};font-size:13px;margin:0}}"
            f"{KF}"
        )
    },
}

# État vide : ne s'affiche QUE si aucune lumière n'est allumée.
EMPTY_LIGHTS = {
    "type": "markdown",
    "content": (
        "### 🌙 Tout est éteint\n"
        "Aucune lumière allumée dans la maison. Les pièces actives "
        "apparaîtront ici automatiquement."
    ),
    "grid_options": {"columns": "full"},
    "card_mod": {
        "style": (
            "ha-card{"
            "{% if states.light | selectattr('state','eq','on') | list | count > 0 %}"
            "display:none;{% endif %}"
            "--ha-card-background:transparent;"
            "background:linear-gradient(155deg,#181e2c8c,#0d1119b3);"
            "border:1px dashed #ffffff21;border-radius:18px;"
            "box-shadow:none;text-align:center;padding:10px 4px;"
            f"animation:nxIn .5s {EASE} both}}"
            "ha-card h3{font-size:16px;font-weight:600;margin:6px 0 4px}"
            f"ha-card p{{color:{MUT};font-size:13px;max-width:34ch;margin:0 auto 6px}}"
            f"{KF}"
        )
    },
}

ACTIVE_LIGHTS = {
    "type": "entity-filter",
    "entities": [
        "light.piece_de_vie",
        "light.cuisine",
        "light.salon_3",
        "light.billard",
        "light.cinema",
        "light.dressing",
        "light.escalier_rez_de_chaussee",
        "light.escalier_1ere_etage",
    ],
    "state_filter": ["on"],
    "card": {"type": "glance", "columns": 4, "show_state": True, "state_color": True},
    "show_empty": False,
    "grid_options": {"columns": "full"},
    "card_mod": glass(0.05, AM),
}


def action_btn(name, icon, accent, entity, service, delay, data=None):
    card = {
        "type": "button",
        "name": name,
        "icon": icon,
        "show_state": False,
        "tap_action": {
            "action": "perform-action",
            "perform_action": service,
            "target": {"entity_id": entity},
        },
        "card_mod": glass(
            delay,
            accent,
            radius=16,
            extra=(
                f"ha-card ha-state-icon{{color:{accent};transition:transform .3s {EASE}}}"
                "ha-card:hover ha-state-icon{transform:scale(1.14)}"
                "ha-card div.name{font-size:12.5px;font-weight:600;letter-spacing:.01em}"
            ),
        ),
    }
    if data:
        card["tap_action"]["data"] = data
    return card


# ── Vue 1 · Accueil ──────────────────────────────────────────────────────────
POWER = "sensor.capteur_de_consommation_electrique_electric_power_consumption"
ENERGY_DAY = "sensor.couloir_capteur_de_consommation_electrique_energie_maison_du_jour"
COST = "sensor.capteur_de_consommation_electrique_electric_energy_consumption_cost"

view_accueil = {
    "title": "Accueil",
    "path": "accueil",
    "icon": "mdi:view-dashboard-outline",
    "type": "sections",
    "max_columns": 4,
    "badges": [
        {"type": "entity", "entity": "person.faure", "show_name": True},
        {"type": "entity", "entity": "person.maryline", "show_name": True},
        {
            "type": "entity",
            "entity": "alarm_control_panel.alarmo",
            "show_name": True,
            "color": "green",
        },
        {
            "type": "entity",
            "entity": "sensor.salon_temperature_exterieure",
            "show_name": True,
            "color": "cyan",
        },
    ],
    "sections": [
        nav_section("accueil"),
        {
            "type": "grid",
            "column_span": 4,
            "cards": [HERO],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Indicateurs clés", "mdi:chart-box-outline"),
                kpi(POWER, "Puissance", "mdi:flash", CY, "cyan", 0.05, 12),
                kpi(ENERGY_DAY, "Énergie du jour", "mdi:home-lightning-bolt", AM, "amber", 0.10, 24),
                kpi(COST, "Coût cumulé", "mdi:currency-eur", GR, "green", 0.15, 48),
                kpi(
                    "sensor.salon_temperature_exterieure",
                    "Extérieur",
                    "mdi:thermometer",
                    VI,
                    "purple",
                    0.20,
                    24,
                ),
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Actions rapides", "mdi:gesture-tap-button"),
                {
                    "type": "grid",
                    "columns": 3,
                    "square": False,
                    "cards": [
                        action_btn("Tout allumer", "mdi:lightbulb-on-outline", AM,
                                   "script.favoris_tout_allumer", "script.turn_on", 0.05),
                        action_btn("Mode nuit", "mdi:weather-night", VI,
                                   "script.favoris_tout_eteindre", "script.turn_on", 0.08),
                        action_btn("Volets", "mdi:window-shutter", BL,
                                   "script.fermer_tous_les_volets", "script.turn_on", 0.11),
                        action_btn("Cinéma", "mdi:movie-open-outline", RD,
                                   "script.cinema_mode_cinema", "script.turn_on", 0.14),
                        action_btn("Récap", "mdi:bullhorn-outline", CY,
                                   "script.recap_maison", "script.turn_on", 0.17),
                        action_btn("Mode absent", "mdi:home-export-outline", GR,
                                   "input_boolean.mode_absent", "input_boolean.toggle", 0.20),
                    ],
                },
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Lumières actives", "mdi:lightbulb-group-outline"),
                ACTIVE_LIGHTS,
                EMPTY_LIGHTS,
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Confort", "mdi:sofa-outline"),
                {
                    "type": "tile",
                    "entity": "climate.salon",
                    "name": "Clim salon",
                    "features": [{"type": "target-temperature"},
                                 {"type": "climate-hvac-modes", "style": "icons"}],
                    "grid_options": {"columns": 6, "rows": 3},
                    "card_mod": skeleton(0.05, CY),
                },
                {
                    "type": "tile",
                    "entity": "climate.cinema",
                    "name": "Clim cinéma",
                    "features": [{"type": "target-temperature"},
                                 {"type": "climate-hvac-modes", "style": "icons"}],
                    "grid_options": {"columns": 6, "rows": 3},
                    "card_mod": skeleton(0.10, VI),
                },
                {
                    "type": "tile",
                    "entity": "cover.tous_les_volets",
                    "name": "Tous les volets",
                    "features": [{"type": "cover-open-close"}, {"type": "cover-position"}],
                    "grid_options": {"columns": 6, "rows": 3},
                    "card_mod": skeleton(0.15, BL),
                },
                {
                    "type": "tile",
                    "entity": "vacuum.roborock_s7_maxv",
                    "name": "Aspirateur",
                    "features": [{"type": "vacuum-commands",
                                  "commands": ["start_pause", "return_home", "locate"]}],
                    "grid_options": {"columns": 6, "rows": 3},
                    "card_mod": skeleton(0.20, GR),
                },
            ],
        },
        {
            "type": "grid",
            "column_span": 4,
            "cards": [
                heading("Machines", "mdi:washing-machine", "subtitle"),
                {
                    "type": "markdown",
                    "text_only": True,
                    "content": (
                        "Les tuiles ci-dessous passent en **squelette scintillant** "
                        "tant que l'appareil ne remonte pas d'état — pas d'écran vide, "
                        "pas de « unavailable » brut."
                    ),
                    "grid_options": {"columns": "full"},
                    "card_mod": {"style": f"ha-card{{color:{MUT};font-size:12.5px;}}"},
                },
                {
                    "type": "tile",
                    "entity": "sensor.machine_a_laver_consommation_electrique",
                    "name": "Lave-linge",
                    "icon": "mdi:washing-machine",
                    "grid_options": {"columns": 4, "rows": 1},
                    "card_mod": skeleton(0.05, CY),
                },
                {
                    "type": "tile",
                    "entity": "binary_sensor.seche_linge_en_marche",
                    "name": "Sèche-linge",
                    "icon": "mdi:tumble-dryer",
                    "grid_options": {"columns": 4, "rows": 1},
                    "card_mod": skeleton(0.10, AM),
                },
                {
                    "type": "tile",
                    "entity": "binary_sensor.voiture_en_charge",
                    "name": "Voiture",
                    "icon": "mdi:ev-station",
                    "grid_options": {"columns": 4, "rows": 1},
                    "card_mod": skeleton(0.15, GR),
                },
            ],
        },
    ],
}

# ── Vue 2 · Énergie ──────────────────────────────────────────────────────────
APEX_BASE = {
    "chart": {
        "background": "transparent",
        "toolbar": {"show": False},
        "zoom": {"enabled": False},
        "parentHeightOffset": 0,
        "fontFamily": "inherit",
        "animations": {
            "enabled": True,
            "easing": "easeinout",
            "speed": 900,
            "animateGradually": {"enabled": True, "delay": 160},
            "dynamicAnimation": {"enabled": True, "speed": 420},
        },
    },
    "grid": {
        "borderColor": "rgba(255,255,255,.06)",
        "strokeDashArray": 4,
        "padding": {"left": 4, "right": 4},
    },
    "dataLabels": {"enabled": False},
    "legend": {"show": False},
    "tooltip": {"theme": "dark", "x": {"format": "dd MMM · HH:mm"}},
    "xaxis": {
        "axisBorder": {"show": False},
        "axisTicks": {"show": False},
        "labels": {"style": {"colors": MUT, "fontSize": "11px"}},
    },
    "yaxis": {"labels": {"style": {"colors": MUT, "fontSize": "11px"}}},
}


def apex(title, series, height=270, delay=0.05, accent=CY, overrides=None):
    cfg = json.loads(json.dumps(APEX_BASE))
    cfg["chart"]["height"] = height
    if overrides:
        for k, v in overrides.items():
            if isinstance(v, dict) and isinstance(cfg.get(k), dict):
                cfg[k].update(v)
            else:
                cfg[k] = v
    return {
        "type": "custom:apexcharts-card",
        "graph_span": "24h",
        "header": {
            "show": True,
            "title": title,
            "show_states": True,
            "colorize_states": True,
        },
        "series": series,
        "apex_config": cfg,
        "grid_options": {"columns": "full"},
        "card_mod": glass(
            delay,
            accent,
            extra=(
                "ha-card #header__title{font-size:15px;font-weight:600;"
                "letter-spacing:-.01em}"
                "ha-card #header__states{opacity:.95}"
            ),
        ),
    }


chart_power = apex(
    "Puissance instantanée · 24 h",
    [
        {
            "entity": POWER,
            "name": "Maison",
            "type": "area",
            "color": CY,
            "stroke_width": 2.5,
            "curve": "smooth",
            "float_precision": 0,
            "group_by": {"func": "avg", "duration": "10min"},
            "show": {"extremas": True},
        }
    ],
    height=280,
    delay=0.05,
    accent=CY,
    overrides={
        "stroke": {"curve": "smooth", "width": 2.5, "lineCap": "round"},
        "fill": {
            "type": "gradient",
            "gradient": {
                "shadeIntensity": 1,
                "opacityFrom": 0.5,
                "opacityTo": 0.02,
                "stops": [0, 88, 100],
            },
        },
    },
)

chart_week = {
    **apex(
        "Énergie quotidienne · 7 jours",
        [
            {
                "entity": ENERGY_DAY,
                "name": "Consommation",
                "type": "column",
                "color": BL,
                "unit": " kWh",
                "float_precision": 1,
                "transform": "return x / 1000;",
                "group_by": {"func": "max", "duration": "1d"},
            }
        ],
        height=260,
        delay=0.10,
        accent=BL,
        overrides={
            "plotOptions": {
                "bar": {"borderRadius": 6, "columnWidth": "46%",
                        "borderRadiusApplication": "end"}
            },
            "fill": {
                "type": "gradient",
                "gradient": {
                    "shade": "dark",
                    "type": "vertical",
                    "gradientToColors": [VI],
                    "opacityFrom": 0.95,
                    "opacityTo": 0.55,
                    "stops": [0, 100],
                },
            },
            "tooltip": {"theme": "dark", "x": {"format": "ddd dd MMM"}},
        },
    ),
    "graph_span": "7d",
    "span": {"start": "day", "offset": "-6d"},
}

chart_gauge = {
    **apex(
        "Charge instantanée",
        [
            {
                "entity": POWER,
                "name": "Maison",
                "color": AM,
                "float_precision": 0,
                "max_value": 9000,
                "show": {"header_color_threshold": True},
            }
        ],
        height=250,
        delay=0.15,
        accent=AM,
        overrides={
            "plotOptions": {
                "radialBar": {
                    "startAngle": -125,
                    "endAngle": 125,
                    "hollow": {"size": "62%"},
                    "track": {"background": "rgba(255,255,255,.06)", "strokeWidth": "100%"},
                    "dataLabels": {
                        "name": {"show": True, "color": MUT, "fontSize": "12px",
                                 "offsetY": 22},
                        "value": {"show": True, "color": "#E6EAF2", "fontSize": "30px",
                                  "fontWeight": 700, "offsetY": -14},
                    },
                }
            },
            "fill": {
                "type": "gradient",
                "gradient": {
                    "shade": "dark",
                    "type": "horizontal",
                    "gradientToColors": [RD],
                    "stops": [0, 100],
                },
            },
            "stroke": {"lineCap": "round"},
            "grid": {"padding": {"top": -10, "bottom": -10}},
        },
    ),
    "chart_type": "radialBar",
    "graph_span": "5min",
}

view_energie = {
    "title": "Énergie",
    "path": "energie",
    "icon": "mdi:lightning-bolt-outline",
    "type": "sections",
    "max_columns": 4,
    "badges": [
        {"type": "entity", "entity": POWER, "show_name": True, "color": "cyan"},
        {"type": "entity", "entity": ENERGY_DAY, "show_name": True, "color": "amber"},
        {"type": "entity", "entity": COST, "show_name": True, "color": "green"},
        {"type": "entity", "entity": "input_number.prix_du_kwh_alpiq",
         "show_name": True, "color": "grey"},
    ],
    "sections": [
        nav_section("energie"),
        {
            "type": "grid",
            "column_span": 3,
            "cards": [heading("Consommation temps réel", "mdi:chart-areaspline"),
                      chart_power],
        },
        {
            "type": "grid",
            "column_span": 1,
            "cards": [heading("Charge", "mdi:gauge"), chart_gauge],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [heading("Historique", "mdi:chart-bar"), chart_week],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Répartition & réglages", "mdi:tune-variant"),
                {
                    "type": "tile",
                    "entity": "input_number.prix_du_kwh_alpiq",
                    "name": "Prix du kWh",
                    "icon": "mdi:cash",
                    "color": "green",
                    "features": [{"type": "numeric-input", "style": "buttons"}],
                    "grid_options": {"columns": 12, "rows": 2},
                },
                {
                    "type": "tile",
                    "entity": "sensor.capteur_de_consommation_electrique_electric_energy_consumption",
                    "name": "Index compteur",
                    "icon": "mdi:counter",
                    "color": "blue",
                    "grid_options": {"columns": 6, "rows": 1},
                },
                {
                    "type": "tile",
                    "entity": "binary_sensor.voiture_en_charge",
                    "name": "Recharge VE",
                    "icon": "mdi:ev-station",
                    "color": "purple",
                    "grid_options": {"columns": 6, "rows": 1},
                },
            ],
        },
    ],
}

# ── Vue 3 · Maison ───────────────────────────────────────────────────────────
AREAS = [
    ("Salon", "salon", "mdi:sofa", CY),
    ("Cuisine", "cuisine", "mdi:stove", AM),
    ("Cinéma", "cinema", "mdi:audio-video", VI),
    ("Billiard", "billiard", "mdi:billiards", GR),
    ("Dressing", "dressing", "mdi:dresser", BL),
    ("Chambre", "chambre", "mdi:bed", RD),
]

view_maison = {
    "title": "Maison",
    "path": "maison",
    "icon": "mdi:home-heart",
    "type": "sections",
    "max_columns": 4,
    "sections": [
        nav_section("maison"),
        {
            "type": "grid",
            "column_span": 2,
            "cards": [heading("Pièces", "mdi:floor-plan")]
            + [
                {
                    "type": "area",
                    "area": aid,
                    "display_type": "compact",
                    "alert_classes": ["motion", "occupancy"],
                    "features": [{"type": "area-controls"}],
                    "navigation_path": f"/{DASH}/maison",
                    "grid_options": {"columns": 6, "rows": 2},
                    "card_mod": glass(0.04 * i, accent),
                }
                for i, (_, aid, _, accent) in enumerate(AREAS)
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Volets & Vélux", "mdi:window-shutter-open"),
                *[
                    {
                        "type": "tile",
                        "entity": e,
                        "features": [{"type": "cover-open-close"}],
                        "grid_options": {"columns": 6, "rows": 2},
                    }
                    for e in (
                        [
                            "cover.volet_cuisine",
                            "cover.volet_dressing",
                            "cover.volet_billard",
                            "cover.volet_cinema",
                            "cover.velux_cuisine",
                            "cover.velux_chambre",
                        ]
                    )
                ],
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Climatisation", "mdi:air-conditioner"),
                *[
                    {
                        "type": "tile",
                        "entity": e,
                        "features": [
                            {"type": "target-temperature"},
                            {"type": "climate-hvac-modes", "style": "icons"},
                        ],
                        "grid_options": {"columns": 6, "rows": 3},
                    }
                    for e in ["climate.salon", "climate.cinema",
                              "climate.chambre", "climate.chambre_daphne"]
                ],
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Ambiances & Média", "mdi:playlist-music-outline"),
                {
                    "type": "grid",
                    "columns": 3,
                    "square": False,
                    "cards": [
                        action_btn("Matin", "mdi:weather-sunset-up", AM,
                                   "script.ambiance_matin", "script.turn_on", 0.04),
                        action_btn("Après-midi", "mdi:weather-sunny", CY,
                                   "script.ambiance_apres_midi", "script.turn_on", 0.07),
                        action_btn("Soirée", "mdi:weather-night", VI,
                                   "script.ambiance_soiree", "script.turn_on", 0.10),
                    ],
                },
                {
                    "type": "tile",
                    "entity": "media_player.tele",
                    "name": "Télé",
                    "features": [{"type": "media-player-volume-slider"}],
                    "grid_options": {"columns": 12, "rows": 2},
                },
                {
                    "type": "tile",
                    "entity": "media_player.ampli_4",
                    "name": "Ampli",
                    "features": [{"type": "media-player-playback"}],
                    "grid_options": {"columns": 12, "rows": 2},
                },
                {
                    "type": "tile",
                    "entity": "input_number.temperature_piscine",
                    "name": "Piscine",
                    "icon": "mdi:pool",
                    "color": "cyan",
                    "features": [{"type": "numeric-input", "style": "slider"}],
                    "grid_options": {"columns": 12, "rows": 2},
                },
            ],
        },
    ],
}

# ── Vue 4 · Sécurité ─────────────────────────────────────────────────────────
CAMS = [
    ("Jardin", "camera.camera_jardin_fluide"),
    ("Terrasse", "camera.terrasse_fluide"),
    ("Porte d'entrée", "camera.porte_d_entree_instantanes_fluide"),
    ("Garage", "camera.garage_live_view"),
]

view_securite = {
    "title": "Sécurité",
    "path": "securite",
    "icon": "mdi:shield-home-outline",
    "type": "sections",
    "max_columns": 4,
    "badges": [
        {"type": "entity", "entity": "alarm_control_panel.alarmo", "show_name": True},
        {"type": "entity", "entity": "binary_sensor.detecteur_fuite_water_leak",
         "show_name": True, "color": "red"},
        {"type": "entity", "entity": "binary_sensor.batterie_faible_maison",
         "show_name": True, "color": "amber"},
    ],
    "sections": [
        nav_section("securite"),
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Alarme", "mdi:shield-lock-outline"),
                {
                    "type": "tile",
                    "entity": "alarm_control_panel.alarmo",
                    "name": "Alarmo",
                    "features": [
                        {
                            "type": "alarm-modes",
                            "modes": ["armed_home", "armed_away", "disarmed"],
                        }
                    ],
                    "grid_options": {"columns": 12, "rows": 3},
                    "card_mod": skeleton(0.05, GR),
                },
                {
                    "type": "tile",
                    "entity": "input_boolean.mode_absent",
                    "name": "Mode absent",
                    "icon": "mdi:home-export-outline",
                    "color": "amber",
                    "features": [{"type": "toggle"}],
                    "grid_options": {"columns": 6, "rows": 2},
                },
                {
                    "type": "tile",
                    "entity": "timer.vigilance_mode_absent",
                    "name": "Vigilance",
                    "icon": "mdi:timer-outline",
                    "color": "purple",
                    "grid_options": {"columns": 6, "rows": 2},
                },
            ],
        },
        {
            "type": "grid",
            "column_span": 2,
            "cards": [
                heading("Détections", "mdi:motion-sensor"),
                *[
                    {
                        "type": "tile",
                        "entity": e,
                        "name": n,
                        "color": "red",
                        "grid_options": {"columns": 6, "rows": 1},
                    }
                    for (n, e) in (
                        [
                            ("Jardin", "binary_sensor.camera_jardin_personne"),
                            ("Terrasse", "binary_sensor.terrasse_personne"),
                            ("Entrée", "binary_sensor.porte_d_entree_personne"),
                            ("Garage", "binary_sensor.garage_motion"),
                            ("Fuite d'eau", "binary_sensor.detecteur_fuite_water_leak"),
                            ("Batterie faible", "binary_sensor.batterie_faible_maison"),
                        ]
                    )
                ],
            ],
        },
        {
            "type": "grid",
            "column_span": 4,
            "cards": [heading("Caméras", "mdi:cctv")]
            + [
                {
                    "type": "picture-entity",
                    "entity": e,
                    "name": n,
                    "camera_view": "auto",
                    "show_state": False,
                    "show_name": True,
                    "grid_options": {"columns": 6, "rows": 4},
                    "card_mod": glass(
                        0.05 * i,
                        CY,
                        extra=(
                            "ha-card{overflow:hidden}"
                            f"ha-card img{{transition:transform .5s {EASE}}}"
                            "ha-card:hover img{transform:scale(1.04)}"
                        ),
                    ),
                }
                for i, (n, e) in enumerate(CAMS)
            ],
        },
        {
            "type": "grid",
            "column_span": 4,
            "cards": [
                heading("Journal", "mdi:history", "subtitle"),
                {
                    "type": "logbook",
                    "target": {
                        "entity_id": [
                            "alarm_control_panel.alarmo",
                            "binary_sensor.camera_jardin_personne",
                            "binary_sensor.terrasse_personne",
                            "binary_sensor.porte_d_entree_personne",
                            "person.faure",
                            "person.maryline",
                        ]
                    },
                    "hours_to_show": 24,
                    "grid_options": {"columns": "full", "rows": 6},
                    "card_mod": glass(0.05, GR),
                },
            ],
        },
    ],
}

config = {"views": [view_accueil, view_energie, view_maison, view_securite]}

if __name__ == "__main__":
    print(json.dumps(config, ensure_ascii=False, indent=1))
