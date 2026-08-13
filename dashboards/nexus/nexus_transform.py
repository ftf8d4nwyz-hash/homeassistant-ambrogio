CY = "#00E5FF"
TL = "#14F1D9"
AM = "#FFB020"
RD = "#FF3B5C"
MG = "#FF2FB9"
VI = "#8B5CF6"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
s = 20260813
stars = []
for i in range(52):
    s = (s * 1103515245 + 12345) % 2147483648
    x = s % 100
    s = (s * 1103515245 + 12345) % 2147483648
    y = s % 100
    s = (s * 1103515245 + 12345) % 2147483648
    r = 1 + (s % 3)
    s = (s * 1103515245 + 12345) % 2147483648
    col = ["#FFFFFFCC", "#DFF6FFAA", "#00E5FF99", "#FFB02088", "#FF2FB977", "#14F1D999"][s % 6]
    stars.append("radial-gradient(" + str(r) + "px " + str(r) + "px at " + str(x) + "% " + str(y) + "%," + col + ",transparent)")
STARS = ",".join(stars[:30])
STARS2 = ",".join(stars[30:])
KF = "@keyframes nxBoot{0%{opacity:0;transform:translateY(12px) scaleY(.92);filter:brightness(2.4) saturate(1.5)}55%{filter:brightness(1.25)}100%{opacity:1;transform:none;filter:none}}@keyframes nxScan{0%{top:-45%}100%{top:112%}}"
HUD = "ha-card{--ha-card-background:transparent;--primary-text-color:#DFF6FF;--secondary-text-color:#6C89A8;position:relative;overflow:hidden;border-radius:4px;border:1px solid @AC@40;background:linear-gradient(180deg,#0A1020F2,#050912F7),repeating-linear-gradient(0deg,transparent 0 3px,@AC@0A 3px 4px);box-shadow:0 0 24px -11px @AC@,inset 0 0 36px -22px @AC@,0 12px 32px -20px #000000E6;animation:nxBoot .75s cubic-bezier(.2,.8,.2,1) @D@s both;transition:border-color .3s,box-shadow .3s,transform .3s}ha-card:hover{transform:translateY(-2px);border-color:@AC@A6;box-shadow:0 0 34px -8px @AC@,inset 0 0 44px -18px @AC@,0 16px 38px -20px #000}ha-card::before{content:'';position:absolute;inset:5px;pointer-events:none;z-index:3;opacity:.85;background:linear-gradient(@AC@,@AC@) left top/13px 2px no-repeat,linear-gradient(@AC@,@AC@) left top/2px 13px no-repeat,linear-gradient(@AC@,@AC@) right top/13px 2px no-repeat,linear-gradient(@AC@,@AC@) right top/2px 13px no-repeat,linear-gradient(@AC@,@AC@) left bottom/13px 2px no-repeat,linear-gradient(@AC@,@AC@) left bottom/2px 13px no-repeat,linear-gradient(@AC@,@AC@) right bottom/13px 2px no-repeat,linear-gradient(@AC@,@AC@) right bottom/2px 13px no-repeat}ha-card::after{content:'';position:absolute;left:0;right:0;height:38%;top:-45%;pointer-events:none;z-index:2;background:linear-gradient(180deg,transparent,@AC@12 46%,@AC@24 50%,@AC@12 54%,transparent);animation:nxScan 6.5s linear infinite @D@s}ha-card ha-state-icon,ha-card ha-icon,ha-card ha-svg-icon{filter:drop-shadow(0 0 7px @AC@AA)}" + KF
ALERT = "ha-card{{% if is_state(config.entity,'on') %}border-color:#FF3B5CD9;animation:nxAlert 1.15s ease-in-out infinite;{% endif %}}@keyframes nxAlert{0%,100%{box-shadow:0 0 20px -12px #FF3B5C,inset 0 0 26px -20px #FF3B5C}50%{box-shadow:0 0 36px -4px #FF3B5C,inset 0 0 36px -10px #FF3B5C}}"
HDR = "ha-card{--ha-card-background:transparent;background:none;border:none;box-shadow:none;padding:2px 0 0}ha-card h3{margin:0 0 6px;font-size:12px;font-weight:800;letter-spacing:.28em;text-transform:uppercase;color:@AC@;text-shadow:0 0 14px @AC@;font-family:" + MONO + "}ha-card h3::after{content:'';display:block;height:1px;margin-top:7px;background:linear-gradient(90deg,@AC@,@AC@33 38%,transparent 76%)}"
CHIP = "ha-card{--ha-card-background:transparent;position:relative;overflow:hidden;border:none;border-radius:0;clip-path:polygon(11px 0,100% 0,100% calc(100% - 11px),calc(100% - 11px) 100%,0 100%,0 11px);background:linear-gradient(150deg,@BG@);box-shadow:inset 0 0 0 1px @AC@@OP@,inset 0 0 26px -16px @AC@;transition:transform .25s,box-shadow .25s}ha-card:hover{transform:translateY(-2px);box-shadow:inset 0 0 0 1px @AC@,inset 0 0 30px -10px @AC@,0 0 24px -10px @AC@}ha-card ha-state-icon{color:@IC@;filter:drop-shadow(0 0 8px @AC@);transition:color .25s,transform .25s}ha-card:hover ha-state-icon{color:@AC@;transform:scale(1.12)}ha-card div.name{color:@NC@;font-family:" + MONO + ";font-weight:700;font-size:11px;letter-spacing:.16em;text-transform:uppercase}"
BTN = "ha-card ha-state-icon{color:@AC@;filter:drop-shadow(0 0 10px @AC@);transition:transform .3s cubic-bezier(.2,.8,.2,1)}ha-card:hover ha-state-icon{transform:scale(1.18)}ha-card div.name{font-family:" + MONO + ";font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#BFE6F5}"
GRAPH = "ha-card #graph{filter:drop-shadow(0 0 7px @AC@)}ha-card #header__title{font-family:" + MONO + ";font-size:12px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:@AC@;text-shadow:0 0 12px @AC@}ha-card #header__states{filter:drop-shadow(0 0 8px @AC@)}ha-card #state{font-family:" + MONO + ";letter-spacing:.04em}"
RADAR = "ha-card::after{content:'';position:absolute;left:50%;top:56%;width:250px;height:250px;margin:-125px 0 0 -125px;border-radius:50%;background:conic-gradient(from 0deg,transparent 0deg,transparent 296deg,@AC@1A 330deg,@AC@59 358deg,@AC@00 360deg);animation:nxRadar 3.8s linear infinite;pointer-events:none;z-index:1}@keyframes nxRadar{to{transform:rotate(360deg)}}"
CAMX = "ha-card{overflow:hidden}ha-card img{transition:transform .6s cubic-bezier(.2,.8,.2,1);filter:saturate(1.15) contrast(1.06)}ha-card:hover img{transform:scale(1.05)}"
SKEL = "ha-card{{% if states(config.entity) in ['unavailable','unknown','None'] %}--primary-text-color:transparent;--secondary-text-color:transparent;--state-icon-color:transparent;pointer-events:none;background-image:linear-gradient(180deg,#0A1020F2,#050912F7),linear-gradient(100deg,transparent 18%,@AC@2E 40%,transparent 62%);background-size:100% 100%,480px 100%;background-repeat:no-repeat;animation:nxSh 1.5s linear infinite;{% endif %}}@keyframes nxSh{0%{background-position:0 0,-480px 0}to{background-position:0 0,480px 0}}"
POWER = "sensor.capteur_de_consommation_electrique_electric_power_consumption"
ENERGY = "sensor.couloir_capteur_de_consommation_electrique_energie_maison_du_jour"
COST = "sensor.capteur_de_consommation_electrique_electric_energy_consumption_cost"
NAV = [["Passerelle", "mdi:space-station", "accueil", CY], ["Réacteur", "mdi:atom-variant", "energie", AM], ["Modules", "mdi:home-group", "maison", VI], ["Boucliers", "mdi:shield-sun-outline", "securite", TL]]


hud = lambda ac, d, extra="", _H=HUD: {"style": _H.replace("@AC@", ac).replace("@D@", str(d)) + extra.replace("@AC@", ac)}
hdr = lambda t, ac, _H=HDR: {"type": "markdown", "text_only": True, "content": "### ◤ " + t, "grid_options": {"columns": "full"}, "card_mod": {"style": _H.replace("@AC@", ac)}}


navs = {}
for active in ["accueil", "energie", "maison", "securite"]:
    rails = []
    for compact in [False, True]:
        cards = []
        for n in NAV:
            on = n[2] == active
            st = CHIP.replace("@BG@", n[3] + "33,#060C18F5" if on else "#0B1322E6,#050912F2")
            st = st.replace("@OP@", "" if on else "38")
            st = st.replace("@IC@", n[3] if on else "#6C89A8")
            st = st.replace("@NC@", "#EAFBFF" if on else "#6C89A8")
            st = st.replace("@AC@", n[3])
            cards.append({"type": "button", "icon": n[1], "name": n[0], "show_name": not compact, "show_state": False, "tap_action": {"action": "navigate", "navigation_path": "/dashboard-nexus/" + n[2]}, "card_mod": {"style": st}})
        ts = CHIP.replace("@BG@", "#0B1322CC,#050912E6").replace("@OP@", "24").replace("@IC@", "#6C89A8").replace("@NC@", "#6C89A8").replace("@AC@", "#6C89A8")
        cards.append({"type": "button", "icon": "mdi:chevron-double-right" if compact else "mdi:chevron-double-left", "name": "Réduire", "show_name": not compact, "show_state": False, "tap_action": {"action": "toggle"}, "entity": "input_boolean.nexus_navigation_compacte", "card_mod": {"style": ts}})
        rails.append({"type": "grid", "columns": 5, "square": False, "cards": cards, "visibility": [{"condition": "state", "entity": "input_boolean.nexus_navigation_compacte", "state": "on" if compact else "off"}], "grid_options": {"columns": "full"}})
    navs[active] = {"type": "grid", "column_span": 4, "cards": rails}

HEROCSS = "ha-card{--ha-card-background:transparent;position:relative;overflow:hidden;border-radius:6px;border:1px solid " + CY + "45;min-height:196px;background:" + STARS + ",radial-gradient(120% 100% at 8% 0%,#0EA5E933,transparent 58%),radial-gradient(95% 85% at 94% 100%," + MG + "26,transparent 62%),linear-gradient(180deg,#060C18,#02040A);box-shadow:0 0 44px -16px " + CY + ",inset 0 0 70px -34px " + CY + ",0 20px 48px -24px #000}ha-card::before{content:'';position:absolute;inset:-60%;pointer-events:none;opacity:.8;background:" + STARS2 + ";animation:nxDrift 140s linear infinite}ha-card::after{content:'';position:absolute;inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,transparent 0 2px," + CY + "0F 2px 3px),radial-gradient(150% 95% at 50% 128%," + TL + "26,transparent 62%)}ha-card h1{position:relative;z-index:2;margin:2px 0 4px;font-size:34px;font-weight:800;letter-spacing:.05em;text-transform:uppercase;color:#EAFBFF;text-shadow:0 0 20px " + CY + ",0 0 48px " + CY + "66}ha-card h3{position:relative;z-index:2;margin:0 0 8px;font-family:" + MONO + ";font-size:12.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:" + TL + ";text-shadow:0 0 12px " + TL + "}ha-card p{position:relative;z-index:2;margin:0;font-family:" + MONO + ";font-size:11.5px;letter-spacing:.12em;text-transform:uppercase;color:#7FA3C0}@keyframes nxDrift{from{transform:translate3d(0,0,0)}to{transform:translate3d(-22%,14%,0)}}"
HERO = {"type": "markdown", "content": "{% set h = now().hour %}{% set sal = 'Quart de nuit' if h < 6 else ('Bonjour' if h < 12 else ('Bon après-midi' if h < 18 else 'Bonsoir')) %}{% set on = states.light | selectattr('state','eq','on') | list | count %}{% set ici = states.person | selectattr('state','eq','home') | list | count %}{% set t = state_attr('weather.forecast_maison','temperature') %}{% set p = states('" + POWER + "') | int(0) %}# {{ sal }}\n### ◈ Systèmes nominaux · {{ t | round(0) if t is not none else '--' }}°C ext · {{ p }} W\nÉquipage à bord {{ ici }}/2 · {{ on }} module{{ 's' if on > 1 }} éclairé{{ 's' if on > 1 }} · Burtoncourt · {{ now().strftime('%d.%m.%Y — %H:%M') }}", "grid_options": {"columns": "full"}, "card_mod": {"style": HEROCSS}}

TELECSS = "ha-card{--ha-card-background:transparent;position:relative;overflow:hidden;border-radius:4px;border:1px solid " + TL + "40;background:linear-gradient(180deg,#08111FF7,#04080FFA),repeating-linear-gradient(0deg,transparent 0 3px," + TL + "0A 3px 4px);box-shadow:0 0 26px -12px " + TL + ",inset 0 0 40px -24px " + TL + ";animation:nxBoot .8s cubic-bezier(.2,.8,.2,1) .1s both}ha-card::after{content:'';position:absolute;left:0;right:0;height:36%;top:-45%;pointer-events:none;background:linear-gradient(180deg,transparent," + TL + "14 48%,transparent);animation:nxScan 7s linear infinite}ha-card pre,ha-card code{background:none;border:none;padding:0;margin:0;font-family:" + MONO + ";font-size:11.5px;line-height:1.85;letter-spacing:.06em;color:" + TL + ";text-shadow:0 0 10px " + TL + "80;white-space:pre-wrap}" + KF
TELE = {"type": "markdown", "content": "{% set p = states('" + POWER + "') | int(0) %}{% set n = [ (p // 1000), 9 ] | min %}{% set e = states('" + ENERGY + "') | float(0) / 1000 %}{% set det = states.binary_sensor | selectattr('state','eq','on') | list | count %}{% set lum = states.light | selectattr('state','eq','on') | list | count %}```\nALIMENTATION ..... {{ '%5d'|format(p) }} W  {{ '▓' * n }}{{ '░' * (9 - n) }}\nÉNERGIE / JOUR ... {{ '%5.1f'|format(e) }} kWh\nCOÛT CUMULÉ ...... {{ '%5.2f'|format(states('" + COST + "') | float(0)) }} EUR\nRÉSEAU WAN ....... {{ 'EN LIGNE' if is_state('binary_sensor.freebox_v9_r1_etat_du_reseau_etendu_wan','on') else 'ACTIF' }}\nCAPTEURS ......... {{ det }} SIGNAUX ACTIFS\nÉCLAIRAGE ........ {{ lum }} MODULE(S)\nBOUCLIERS ........ {{ 'ARMÉS' if not is_state('alarm_control_panel.alarmo','disarmed') else 'AU REPOS' }}\n```", "grid_options": {"columns": "full"}, "card_mod": {"style": TELECSS}}

EMPTY = {"type": "markdown", "content": "### ⬡ Tous les modules en veille\nAucun éclairage actif à bord. Les secteurs alimentés apparaîtront ici automatiquement.", "grid_options": {"columns": "full"}, "card_mod": {"style": "ha-card{--ha-card-background:transparent;{% if states.light | selectattr('state','eq','on') | list | count > 0 %}display:none;{% endif %}background:linear-gradient(180deg,#080E1AB3,#04070ECC);border:1px dashed " + CY + "3D;border-radius:4px;box-shadow:none;text-align:center;padding:14px 6px}ha-card h3{font-family:" + MONO + ";font-size:12px;font-weight:800;letter-spacing:.2em;text-transform:uppercase;color:" + CY + "B3;text-shadow:0 0 12px " + CY + "80;margin:4px 0 6px}ha-card p{font-family:" + MONO + ";font-size:11px;letter-spacing:.08em;color:#5F7C99;max-width:44ch;margin:0 auto 6px}"}}

KPI = [[POWER, "Alimentation", "mdi:flash", CY, "cyan", 12], [ENERGY, "Énergie / jour", "mdi:atom-variant", AM, "amber", 24], [COST, "Coût cumulé", "mdi:currency-eur", TL, "teal", 48], ["sensor.salon_temperature_exterieure", "Coque ext.", "mdi:thermometer", MG, "pink", 24]]
kpi_cards = [hdr("Indicateurs primaires", CY)]
for i, k in enumerate(KPI):
    kpi_cards.append({"type": "tile", "entity": k[0], "name": k[1], "icon": k[2], "color": k[4], "features_position": "bottom", "features": [{"type": "trend-graph", "hours_to_show": k[5]}], "grid_options": {"columns": 6, "rows": 2}, "card_mod": hud(k[3], round(0.06 * i, 2), SKEL)})

ACTS = [["Éclairage max", "mdi:lightbulb-on-outline", AM, "script.favoris_tout_allumer", "script.turn_on"], ["Mode nuit", "mdi:weather-night", VI, "script.favoris_tout_eteindre", "script.turn_on"], ["Sas / volets", "mdi:window-shutter", CY, "script.fermer_tous_les_volets", "script.turn_on"], ["Holodeck", "mdi:movie-open-outline", MG, "script.cinema_mode_cinema", "script.turn_on"], ["Rapport", "mdi:radio-tower", TL, "script.recap_maison", "script.turn_on"], ["Hors-bord", "mdi:rocket-launch-outline", RD, "input_boolean.mode_absent", "input_boolean.toggle"]]
act_btns = []
for i, a in enumerate(ACTS):
    act_btns.append({"type": "button", "name": a[0], "icon": a[1], "show_state": False, "tap_action": {"action": "perform-action", "perform_action": a[4], "target": {"entity_id": a[3]}}, "card_mod": hud(a[2], round(0.05 * i, 2), BTN)})

CONF = [["climate.salon", "Clim salon", CY], ["climate.cinema", "Clim holodeck", VI], ["cover.tous_les_volets", "Sas principal", TL], ["vacuum.roborock_s7_maxv", "Drone d'entretien", AM]]
conf_cards = [hdr("Support-vie", TL)]
for i, c in enumerate(CONF):
    f = [{"type": "target-temperature"}, {"type": "climate-hvac-modes", "style": "icons"}]
    if c[0].startswith("cover"):
        f = [{"type": "cover-open-close"}, {"type": "cover-position"}]
    if c[0].startswith("vacuum"):
        f = [{"type": "vacuum-commands", "commands": ["start_pause", "return_home", "locate"]}]
    conf_cards.append({"type": "tile", "entity": c[0], "name": c[1], "features": f, "grid_options": {"columns": 6, "rows": 3}, "card_mod": hud(c[2], round(0.06 * i, 2), SKEL)})

MACH = [["sensor.machine_a_laver_consommation_electrique", "Recycleur", "mdi:washing-machine", CY], ["binary_sensor.seche_linge_en_marche", "Déshydrateur", "mdi:tumble-dryer", AM], ["binary_sensor.voiture_en_charge", "Navette", "mdi:ev-station", TL]]
mach_cards = [hdr("Soutes", MG)]
for i, m in enumerate(MACH):
    mach_cards.append({"type": "tile", "entity": m[0], "name": m[1], "icon": m[2], "grid_options": {"columns": 4, "rows": 1}, "card_mod": hud(m[3], round(0.06 * i, 2), SKEL)})

v_accueil = {"title": "Passerelle", "path": "accueil", "icon": "mdi:space-station", "type": "sections", "max_columns": 4, "badges": [{"type": "entity", "entity": "person.faure", "show_name": True}, {"type": "entity", "entity": "person.maryline", "show_name": True}, {"type": "entity", "entity": "alarm_control_panel.alarmo", "show_name": True, "color": "teal"}, {"type": "entity", "entity": "sensor.salon_temperature_exterieure", "show_name": True, "color": "cyan"}], "sections": [navs["accueil"], {"type": "grid", "column_span": 4, "cards": [HERO]}, {"type": "grid", "column_span": 2, "cards": kpi_cards}, {"type": "grid", "column_span": 2, "cards": [hdr("Télémétrie", TL), TELE]}, {"type": "grid", "column_span": 2, "cards": [hdr("Commandes rapides", AM), {"type": "grid", "columns": 3, "square": False, "cards": act_btns}]}, {"type": "grid", "column_span": 2, "cards": [hdr("Secteurs éclairés", AM), {"type": "entity-filter", "entities": ["light.piece_de_vie", "light.cuisine", "light.salon_3", "light.billard", "light.cinema", "light.dressing", "light.escalier_rez_de_chaussee", "light.escalier_1ere_etage"], "state_filter": ["on"], "card": {"type": "glance", "columns": 4, "show_state": True, "state_color": True}, "show_empty": False, "grid_options": {"columns": "full"}, "card_mod": hud(AM, 0.05)}, EMPTY]}, {"type": "grid", "column_span": 2, "cards": conf_cards}, {"type": "grid", "column_span": 2, "cards": mach_cards}]}

APEX = {"chart": {"background": "transparent", "toolbar": {"show": False}, "zoom": {"enabled": False}, "parentHeightOffset": 0, "fontFamily": MONO, "foreColor": "#6C89A8", "animations": {"enabled": True, "easing": "easeinout", "speed": 1100, "animateGradually": {"enabled": True, "delay": 190}, "dynamicAnimation": {"enabled": True, "speed": 450}}}, "grid": {"borderColor": "#FFFFFF0F", "strokeDashArray": 3, "padding": {"left": 4, "right": 4}}, "dataLabels": {"enabled": False}, "legend": {"show": False}, "tooltip": {"theme": "dark", "x": {"format": "dd MMM · HH:mm"}}, "xaxis": {"axisBorder": {"show": False}, "axisTicks": {"show": False}, "labels": {"style": {"colors": "#6C89A8", "fontSize": "10px", "letterSpacing": "1px"}}}, "yaxis": {"labels": {"style": {"colors": "#6C89A8", "fontSize": "10px"}}}}
c_area = {}
for k in APEX:
    c_area[k] = APEX[k]
c_area["chart"] = {}
for k in APEX["chart"]:
    c_area["chart"][k] = APEX["chart"][k]
c_area["chart"]["height"] = 290
c_area["stroke"] = {"curve": "smooth", "width": 3, "lineCap": "round"}
c_area["fill"] = {"type": "gradient", "gradient": {"shadeIntensity": 1, "opacityFrom": 0.55, "opacityTo": 0.02, "stops": [0, 88, 100]}}
c_area["markers"] = {"size": 0, "strokeWidth": 0, "hover": {"size": 5}}
c_bar = {}
for k in APEX:
    c_bar[k] = APEX[k]
c_bar["chart"] = {}
for k in APEX["chart"]:
    c_bar["chart"][k] = APEX["chart"][k]
c_bar["chart"]["height"] = 270
c_bar["tooltip"] = {"theme": "dark", "x": {"format": "ddd dd MMM"}}
c_bar["plotOptions"] = {"bar": {"borderRadius": 3, "columnWidth": "42%", "borderRadiusApplication": "end"}}
c_bar["fill"] = {"type": "gradient", "gradient": {"shade": "dark", "type": "vertical", "gradientToColors": [MG], "opacityFrom": 1, "opacityTo": 0.45, "stops": [0, 100]}}
c_gau = {}
for k in APEX:
    c_gau[k] = APEX[k]
c_gau["chart"] = {}
for k in APEX["chart"]:
    c_gau["chart"][k] = APEX["chart"][k]
c_gau["chart"]["height"] = 262
c_gau["grid"] = {"padding": {"top": -12, "bottom": -12}}
c_gau["stroke"] = {"lineCap": "round"}
c_gau["plotOptions"] = {"radialBar": {"startAngle": -130, "endAngle": 130, "hollow": {"size": "60%"}, "track": {"background": "#FFFFFF0D", "strokeWidth": "100%"}, "dataLabels": {"name": {"show": True, "color": "#6C89A8", "fontSize": "10px", "offsetY": 24}, "value": {"show": True, "color": "#EAFBFF", "fontSize": "32px", "fontWeight": 800, "offsetY": -12}}}}
c_gau["fill"] = {"type": "gradient", "gradient": {"shade": "dark", "type": "horizontal", "gradientToColors": [RD], "stops": [0, 100]}}

v_energie = {"title": "Réacteur", "path": "energie", "icon": "mdi:atom-variant", "type": "sections", "max_columns": 4, "badges": [{"type": "entity", "entity": POWER, "show_name": True, "color": "cyan"}, {"type": "entity", "entity": ENERGY, "show_name": True, "color": "amber"}, {"type": "entity", "entity": COST, "show_name": True, "color": "teal"}, {"type": "entity", "entity": "input_number.prix_du_kwh_alpiq", "show_name": True, "color": "grey"}], "sections": [navs["energie"], {"type": "grid", "column_span": 3, "cards": [hdr("Flux du réacteur · 24 h", CY), {"type": "custom:apexcharts-card", "graph_span": "24h", "header": {"show": True, "title": "Puissance instantanée", "show_states": True, "colorize_states": True}, "series": [{"entity": POWER, "name": "Coque", "type": "area", "color": CY, "stroke_width": 3, "curve": "smooth", "float_precision": 0, "group_by": {"func": "avg", "duration": "10min"}, "show": {"extremas": True}}], "apex_config": c_area, "grid_options": {"columns": "full"}, "card_mod": hud(CY, 0.05, GRAPH)}]}, {"type": "grid", "column_span": 1, "cards": [hdr("Charge", AM), {"type": "custom:apexcharts-card", "chart_type": "radialBar", "graph_span": "5min", "header": {"show": True, "title": "Charge", "show_states": True, "colorize_states": True}, "series": [{"entity": POWER, "name": "Coque", "color": AM, "float_precision": 0, "max_value": 9000, "show": {"header_color_threshold": True}}], "apex_config": c_gau, "grid_options": {"columns": "full"}, "card_mod": hud(AM, 0.1, GRAPH + RADAR)}]}, {"type": "grid", "column_span": 2, "cards": [hdr("Cycles · 7 jours", VI), {"type": "custom:apexcharts-card", "graph_span": "7d", "span": {"start": "day", "offset": "-6d"}, "header": {"show": True, "title": "Énergie quotidienne", "show_states": True, "colorize_states": True}, "series": [{"entity": ENERGY, "name": "Consommation", "type": "column", "color": VI, "unit": " kWh", "float_precision": 1, "transform": "return x / 1000;", "group_by": {"func": "max", "duration": "1d"}}], "apex_config": c_bar, "grid_options": {"columns": "full"}, "card_mod": hud(VI, 0.15, GRAPH)}]}, {"type": "grid", "column_span": 2, "cards": [hdr("Paramètres", TL), {"type": "tile", "entity": "input_number.prix_du_kwh_alpiq", "name": "Tarif kWh", "icon": "mdi:cash", "color": "teal", "features": [{"type": "numeric-input", "style": "buttons"}], "grid_options": {"columns": 12, "rows": 2}, "card_mod": hud(TL, 0.05)}, {"type": "tile", "entity": "sensor.capteur_de_consommation_electrique_electric_energy_consumption", "name": "Index", "icon": "mdi:counter", "color": "cyan", "grid_options": {"columns": 6, "rows": 1}, "card_mod": hud(CY, 0.1, SKEL)}, {"type": "tile", "entity": "binary_sensor.voiture_en_charge", "name": "Navette", "icon": "mdi:ev-station", "color": "purple", "grid_options": {"columns": 6, "rows": 1}, "card_mod": hud(VI, 0.15, SKEL)}]}]}

AREAS = [["salon", CY], ["cuisine", AM], ["cinema", MG], ["billiard", TL], ["dressing", VI], ["chambre", RD]]
area_cards = [hdr("Modules d'habitation", VI)]
for i, a in enumerate(AREAS):
    area_cards.append({"type": "area", "area": a[0], "display_type": "compact", "alert_classes": ["motion", "occupancy"], "features": [{"type": "area-controls"}], "grid_options": {"columns": 6, "rows": 2}, "card_mod": hud(a[1], round(0.05 * i, 2))})
cover_cards = [hdr("Sas & hublots", CY)]
for i, e in enumerate(["cover.volet_cuisine", "cover.volet_dressing", "cover.volet_billard", "cover.volet_cinema", "cover.velux_cuisine", "cover.velux_chambre"]):
    cover_cards.append({"type": "tile", "entity": e, "features": [{"type": "cover-open-close"}], "grid_options": {"columns": 6, "rows": 2}, "card_mod": hud(CY, round(0.05 * i, 2), SKEL)})
clim_cards = [hdr("Régulation thermique", TL)]
for i, e in enumerate(["climate.salon", "climate.cinema", "climate.chambre", "climate.chambre_daphne"]):
    clim_cards.append({"type": "tile", "entity": e, "features": [{"type": "target-temperature"}, {"type": "climate-hvac-modes", "style": "icons"}], "grid_options": {"columns": 6, "rows": 3}, "card_mod": hud(TL, round(0.06 * i, 2), SKEL)})
AMB = [["Aube", "mdi:weather-sunset-up", AM, "script.ambiance_matin"], ["Zénith", "mdi:weather-sunny", CY, "script.ambiance_apres_midi"], ["Crépuscule", "mdi:weather-night", VI, "script.ambiance_soiree"]]
amb_btns = []
for i, a in enumerate(AMB):
    amb_btns.append({"type": "button", "name": a[0], "icon": a[1], "show_state": False, "tap_action": {"action": "perform-action", "perform_action": "script.turn_on", "target": {"entity_id": a[3]}}, "card_mod": hud(a[2], round(0.05 * i, 2), BTN)})
media_cards = [hdr("Ambiances & signaux", MG), {"type": "grid", "columns": 3, "square": False, "cards": amb_btns}, {"type": "tile", "entity": "media_player.tele", "name": "Écran principal", "features": [{"type": "media-player-volume-slider"}], "grid_options": {"columns": 12, "rows": 2}, "card_mod": hud(MG, 0.08, SKEL)}, {"type": "tile", "entity": "media_player.ampli_4", "name": "Acoustique", "features": [{"type": "media-player-playback"}], "grid_options": {"columns": 12, "rows": 2}, "card_mod": hud(VI, 0.12, SKEL)}, {"type": "tile", "entity": "input_number.temperature_piscine", "name": "Bassin", "icon": "mdi:pool", "color": "cyan", "features": [{"type": "numeric-input", "style": "slider"}], "grid_options": {"columns": 12, "rows": 2}, "card_mod": hud(CY, 0.16)}]
v_maison = {"title": "Modules", "path": "maison", "icon": "mdi:home-group", "type": "sections", "max_columns": 4, "sections": [navs["maison"], {"type": "grid", "column_span": 2, "cards": area_cards}, {"type": "grid", "column_span": 2, "cards": cover_cards}, {"type": "grid", "column_span": 2, "cards": clim_cards}, {"type": "grid", "column_span": 2, "cards": media_cards}]}

alarm_cards = [hdr("Contrôle des boucliers", TL), {"type": "tile", "entity": "alarm_control_panel.alarmo", "name": "Bouclier principal", "features": [{"type": "alarm-modes", "modes": ["armed_home", "armed_away", "disarmed"]}], "grid_options": {"columns": 12, "rows": 3}, "card_mod": hud(TL, 0.05, SKEL)}, {"type": "tile", "entity": "input_boolean.mode_absent", "name": "Hors-bord", "icon": "mdi:rocket-launch-outline", "color": "amber", "features": [{"type": "toggle"}], "grid_options": {"columns": 6, "rows": 2}, "card_mod": hud(AM, 0.1)}, {"type": "tile", "entity": "timer.vigilance_mode_absent", "name": "Vigilance", "icon": "mdi:timer-sand", "color": "purple", "grid_options": {"columns": 6, "rows": 2}, "card_mod": hud(VI, 0.14)}]
DETS = [["Jardin", "binary_sensor.camera_jardin_personne"], ["Terrasse", "binary_sensor.terrasse_personne"], ["Sas d'entrée", "binary_sensor.porte_d_entree_personne"], ["Hangar", "binary_sensor.garage_motion"], ["Fuite fluide", "binary_sensor.detecteur_fuite_water_leak"], ["Cellule faible", "binary_sensor.batterie_faible_maison"]]
det_cards = [hdr("Détecteurs de proximité", RD)]
for i, d in enumerate(DETS):
    det_cards.append({"type": "tile", "entity": d[1], "name": d[0], "color": "red", "grid_options": {"columns": 6, "rows": 1}, "card_mod": hud(RD, round(0.05 * i, 2), ALERT)})
CAMS = [["Jardin", "camera.camera_jardin_fluide"], ["Terrasse", "camera.terrasse_fluide"], ["Sas d'entrée", "camera.porte_d_entree_instantanes_fluide"], ["Hangar", "camera.garage_live_view"]]
cam_cards = [hdr("Optiques externes", CY)]
for i, c in enumerate(CAMS):
    cam_cards.append({"type": "picture-entity", "entity": c[1], "name": c[0], "camera_view": "auto", "show_state": False, "show_name": True, "grid_options": {"columns": 6, "rows": 4}, "card_mod": hud(CY, round(0.06 * i, 2), CAMX)})
log_cards = [hdr("Journal de bord", TL), {"type": "logbook", "target": {"entity_id": ["alarm_control_panel.alarmo", "binary_sensor.camera_jardin_personne", "binary_sensor.terrasse_personne", "binary_sensor.porte_d_entree_personne", "person.faure", "person.maryline"]}, "hours_to_show": 24, "grid_options": {"columns": "full", "rows": 6}, "card_mod": hud(TL, 0.05)}]
v_secu = {"title": "Boucliers", "path": "securite", "icon": "mdi:shield-sun-outline", "type": "sections", "max_columns": 4, "badges": [{"type": "entity", "entity": "alarm_control_panel.alarmo", "show_name": True}, {"type": "entity", "entity": "binary_sensor.detecteur_fuite_water_leak", "show_name": True, "color": "red"}, {"type": "entity", "entity": "binary_sensor.batterie_faible_maison", "show_name": True, "color": "amber"}], "sections": [navs["securite"], {"type": "grid", "column_span": 2, "cards": alarm_cards}, {"type": "grid", "column_span": 2, "cards": det_cards}, {"type": "grid", "column_span": 4, "cards": cam_cards}, {"type": "grid", "column_span": 4, "cards": log_cards}]}

config["views"] = [v_accueil, v_energie, v_maison, v_secu]
