/*
 * Matrix History Card — journal d'activité NÉON CYBERPUNK pour HA
 * v4 : cyan + magenta, halos néon, scanlines discrètes. Une ligne par
 * appareil (dernier état), icônes claires, pastilles d'état néon, étiquettes
 * coût/énergie/eau, horloge live + bandeau de valeurs. Lisible avant tout.
 *
 * Options : title, count, hours, unique(true), entities[], context{}, stats[]
 */

const STATE_FR = {
  on: "Marche", off: "Arrêt", home: "À la maison", not_home: "Absent",
  open: "Ouvert", opened: "Ouvert", closed: "Fermé", closing: "Fermeture",
  opening: "Ouverture", locked: "Verrouillé", unlocked: "Déverrouillé",
  docked: "À la base", cleaning: "Nettoyage", returning: "Retour base",
  charging: "En charge", paused: "Pause", idle: "Repos", playing: "Lecture",
  heat: "Chauffage", cool: "Clim", heat_cool: "Auto", auto: "Auto",
  disarmed: "Désarmé", armed_away: "Armé absent", armed_home: "Armé présent",
  armed_night: "Armé nuit", triggered: "ALARME", detected: "Détecté",
  clear: "RAS", unavailable: "Indispo", unknown: "Inconnu",
};

function stateKind(eid, s) {
  if (s === "triggered") return "alarm";
  if (["charging", "playing", "cleaning", "opening", "closing", "returning"]
      .includes(s)) return "busy";
  if (["on", "home", "open", "detected", "heat", "cool", "heat_cool",
       "armed_away", "armed_home", "armed_night", "unlocked"].includes(s))
    return "on";
  if (["off", "not_home", "closed", "docked", "idle", "disarmed", "locked",
       "paused", "clear"].includes(s)) return "off";
  if (["unavailable", "unknown"].includes(s)) return "dim";
  return "neutral";
}

function iconFor(eid, s) {
  const id = (eid || "").toLowerCase();
  const on = ["on", "home", "open", "detected", "charging", "playing",
    "cleaning"].includes(s);
  const kw = [
    ["lave_linge", "🧺"], ["machine_a_laver", "🧺"],
    ["seche_linge", "♨️"], ["seche-linge", "♨️"],
    ["voiture", "🚗"], ["charge", "🔌"], ["deshumidificateur", "💨"],
    ["roborock", "🤖"], ["vacuum", "🤖"], ["aspirateur", "🤖"],
    ["porte", "🚪"], ["presence", "👁️"], ["mouvement", "👁️"],
    ["ding", "🔔"], ["sonnette", "🔔"], ["alarm", on ? "🚨" : "🛡️"],
    ["volet", "🪟"], ["thermostat", "🌡️"], ["piscine", "🏊"],
    ["lumiere", on ? "💡" : "🔅"], ["light", on ? "💡" : "🔅"],
  ];
  for (const [k, ic] of kw) if (id.includes(k)) return ic;
  const dom = id.split(".")[0];
  const byDom = {
    binary_sensor: on ? "🟢" : "⚪", person: s === "home" ? "🏠" : "🚶",
    device_tracker: s === "home" ? "🏠" : "🚶", light: on ? "💡" : "🔅",
    switch: on ? "🔛" : "⭕", lock: s === "locked" ? "🔒" : "🔓",
    cover: "🪟", climate: "🌡️", vacuum: "🤖",
    alarm_control_panel: on ? "🚨" : "🛡️", media_player: "🎵",
    sensor: "📊", automation: "⚙️", script: "⚙️",
  };
  return byDom[dom] || "•";
}

function unitIcon(u) {
  if (u === "€" || u === "EUR") return "💶";
  if (/kwh|wh/i.test(u)) return "⚡";
  if (/^l$|litre|m³|m3/i.test(u)) return "💧";
  return "";
}

class MatrixHistoryCard extends HTMLElement {
  setConfig(config) {
    this._config = Object.assign(
      { title: "Journal d'activité", count: 10, hours: 96, unique: true,
        entities: [], context: {}, stats: [] },
      config || {}
    );
    this._events = null;
    this._lastFetch = 0;
    if (this._root) this._render();
  }

  set hass(hass) {
    this._hass = hass;
    const now = Date.now();
    if (!this._events || now - this._lastFetch > 60000) {
      this._lastFetch = now;
      this._fetchEvents();
    }
    this._updateStats();
    this._paintTimes();
  }

  getCardSize() { return 8; }

  connectedCallback() {
    if (!this._root) this._build();
    this._clock = setInterval(() => { this._tickClock(); this._paintTimes(); },
      1000);
  }
  disconnectedCallback() { if (this._clock) clearInterval(this._clock); }

  _build() {
    this._root = this.attachShadow({ mode: "open" });
    this._root.innerHTML = `
      <style>
        :host { display:block; }
        ha-card {
          --cy:#00eaff; --mg:#ff2bd6; --pu:#b388ff; --yl:#ffe45e;
          position:relative; overflow:hidden; border-radius:14px;
          background:
            radial-gradient(120% 80% at 0% 0%, rgba(255,43,214,.10), transparent 60%),
            radial-gradient(120% 80% at 100% 100%, rgba(0,234,255,.12), transparent 60%),
            linear-gradient(160deg,#0b0618 0%,#100a22 55%,#080510 100%);
          border:1px solid rgba(0,234,255,.35);
          box-shadow:0 0 22px rgba(255,43,214,.22), 0 0 42px rgba(0,234,255,.15),
            inset 0 0 34px rgba(162,89,255,.08);
          color:#e9f6ff;
          font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif;
        }
        ha-card::before { content:""; position:absolute; inset:0; z-index:1;
          pointer-events:none; opacity:.5;
          background:repeating-linear-gradient(0deg,
            rgba(0,0,0,0) 0, rgba(0,0,0,0) 2px,
            rgba(0,234,255,.035) 3px, rgba(0,0,0,0) 4px); }
        .bar { position:relative; z-index:2; height:3px;
          background:linear-gradient(90deg,transparent,var(--cy),var(--mg),
            var(--yl),transparent); background-size:250% 100%;
          animation:slide 5s linear infinite;
          box-shadow:0 0 12px rgba(0,234,255,.6); }
        @keyframes slide { to { background-position:250% 0; } }
        .hd,.list,.foot { position:relative; z-index:2; }
        .hd { display:flex; align-items:center; justify-content:space-between;
          padding:14px 16px 10px; gap:12px; }
        .tt { display:flex; align-items:center; gap:9px; font-weight:800;
          font-size:15px; letter-spacing:2px; text-transform:uppercase;
          color:var(--cy); text-shadow:0 0 10px rgba(0,234,255,.7); }
        .tt .dot { width:9px; height:9px; border-radius:50%;
          background:var(--mg); box-shadow:0 0 12px var(--mg),0 0 4px #fff;
          animation:pulse 1.6s ease-in-out infinite; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }
        .clk { font-variant-numeric:tabular-nums; font-size:13px;
          font-family:ui-monospace,Menlo,Consolas,monospace; color:var(--mg);
          text-shadow:0 0 8px rgba(255,43,214,.6); white-space:nowrap; }
        .list { padding:2px 8px 6px; }
        .row { display:grid; grid-template-columns:auto 1fr auto; gap:12px;
          align-items:center; padding:11px 8px; border-radius:10px;
          animation:in .35s ease both; }
        .row:hover { background:rgba(0,234,255,.05);
          box-shadow:inset 0 0 0 1px rgba(0,234,255,.2); }
        .row + .row { border-top:1px solid rgba(179,136,255,.18); }
        @keyframes in { from{opacity:0;transform:translateY(4px)} to{opacity:1} }
        .ic { width:38px; height:38px; border-radius:9px; display:grid;
          place-items:center; font-size:20px; background:rgba(0,234,255,.06);
          border:1px solid rgba(0,234,255,.35);
          box-shadow:0 0 10px rgba(0,234,255,.2), inset 0 0 8px rgba(0,234,255,.08); }
        .mid { min-width:0; }
        .l1 { display:flex; align-items:center; gap:8px; flex-wrap:wrap; }
        .nm { font-weight:650; font-size:14px; color:#eaf6ff;
          text-shadow:0 0 6px rgba(0,234,255,.15); }
        .pill { font-size:11px; font-weight:800; letter-spacing:.5px;
          padding:2px 10px; border-radius:6px; text-transform:uppercase;
          white-space:nowrap; border:1px solid transparent; }
        .k-on{color:#00eaff;background:rgba(0,234,255,.10);
          border-color:rgba(0,234,255,.5);box-shadow:0 0 10px rgba(0,234,255,.35)}
        .k-busy{color:#c9a9ff;background:rgba(179,136,255,.12);
          border-color:rgba(179,136,255,.5);box-shadow:0 0 10px rgba(179,136,255,.3)}
        .k-off{color:#8aa0b6;background:rgba(138,160,182,.10);
          border-color:rgba(138,160,182,.3)}
        .k-alarm{color:#ff2bd6;background:rgba(255,43,214,.14);
          border-color:rgba(255,43,214,.6);box-shadow:0 0 14px rgba(255,43,214,.5);
          animation:blink 1s steps(2) infinite}
        @keyframes blink{50%{opacity:.5}}
        .k-dim{color:#6b7785;background:rgba(107,119,133,.1)}
        .k-neutral{color:var(--yl);background:rgba(255,228,94,.1);
          border-color:rgba(255,228,94,.35)}
        .chips { display:flex; flex-wrap:wrap; gap:6px; margin-top:6px; }
        .chip { font-size:11.5px; color:#bfefff; background:rgba(0,234,255,.06);
          border:1px solid rgba(0,234,255,.28); padding:2px 8px; border-radius:6px;
          white-space:nowrap; box-shadow:0 0 8px rgba(0,234,255,.12); }
        .chip b { color:#eaffff; text-shadow:0 0 6px rgba(0,234,255,.5); }
        .tm { text-align:right; white-space:nowrap; }
        .tm .rel { font-size:12.5px; font-weight:800; color:var(--mg);
          text-shadow:0 0 8px rgba(255,43,214,.5); }
        .tm .abs { display:block; font-size:10.5px; color:#7a86a8; margin-top:2px; }
        .empty { padding:26px 12px; color:#8b98a5; font-size:13px;
          text-align:center; }
        .foot { display:grid; gap:8px; padding:10px 14px 15px;
          grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
          border-top:1px solid rgba(0,234,255,.18); margin-top:4px; }
        .cell { border-radius:10px; padding:9px 11px;
          background:linear-gradient(160deg,rgba(0,234,255,.06),rgba(255,43,214,.05));
          border:1px solid rgba(0,234,255,.3);
          box-shadow:inset 0 0 12px rgba(0,234,255,.06); }
        .cell .cl { font-size:10.5px; color:#8fa6c4; text-transform:uppercase;
          letter-spacing:.6px; white-space:nowrap; overflow:hidden;
          text-overflow:ellipsis; }
        .cell .cv { font-size:17px; font-weight:800; margin-top:3px;
          color:#eaffff; text-shadow:0 0 10px rgba(0,234,255,.4); }
        @media (max-width:520px){
          .row{grid-template-columns:auto 1fr; }
          .tm{grid-column:2; text-align:left; margin-top:4px; }
        }
      </style>
      <ha-card>
        <div class="bar"></div>
        <div class="hd"><div class="tt"><span class="dot"></span>
          <span class="ttx"></span></div><div class="clk"></div></div>
        <div class="list"></div>
        <div class="foot"></div>
      </ha-card>`;
    this._listEl = this._root.querySelector(".list");
    this._footEl = this._root.querySelector(".foot");
    this._render();
    if (!this._clock)
      this._clock = setInterval(() => { this._tickClock(); this._paintTimes(); },
        1000);
  }

  _tickClock() {
    const c = this._root && this._root.querySelector(".clk");
    if (c) c.textContent = new Date().toLocaleTimeString("fr-FR");
  }

  async _fetchEvents() {
    const hass = this._hass, cfg = this._config;
    if (!hass) return;
    const start = new Date(Date.now() - cfg.hours * 3600000).toISOString();
    let ev = null;
    try {
      ev = await hass.callWS({ type: "logbook/get_events", start_time: start,
        entity_ids: cfg.entities.length ? cfg.entities : undefined });
    } catch (e) { ev = null; }
    let rows;
    if (Array.isArray(ev) && ev.length) {
      rows = ev.filter((x) => x.entity_id || x.name).map((x) => ({
        when: (x.when || 0) * 1000, eid: x.entity_id || "",
        name: x.name || (x.entity_id || "").split(".")[1],
        state: x.state, message: x.message }));
    } else {
      rows = cfg.entities.map((e) => hass.states[e]).filter(Boolean).map((s) => ({
        when: new Date(s.last_changed).getTime(), eid: s.entity_id,
        name: (s.attributes && s.attributes.friendly_name) || s.entity_id,
        state: s.state }));
    }
    rows.sort((a, b) => b.when - a.when);
    if (cfg.unique !== false) {
      const seen = new Set();
      rows = rows.filter((r) => {
        const k = r.eid || r.name;
        if (seen.has(k)) return false; seen.add(k); return true;
      });
    }
    this._events = rows.slice(0, cfg.count);
    this._render();
  }

  _relTime(ms) {
    const s = Math.max(0, Math.floor((Date.now() - ms) / 1000));
    if (s < 60) return "à l'instant";
    const m = Math.floor(s / 60);
    if (m < 60) return "il y a " + m + " min";
    const h = Math.floor(m / 60);
    if (h < 24) return "il y a " + h + " h";
    return "il y a " + Math.floor(h / 24) + " j";
  }

  _stateLabel(r) {
    if (r.state != null && r.state !== "")
      return STATE_FR[r.state] || String(r.state);
    if (r.message) return String(r.message);
    return "";
  }

  _chips(eid) {
    const hass = this._hass;
    const list = (this._config.context || {})[eid];
    if (!list || !hass) return "";
    const out = [];
    for (const c of list) {
      const s = hass.states[c.entity];
      if (!s || s.state === "unknown" || s.state === "unavailable") continue;
      let u = c.unit || (s.attributes && s.attributes.unit_of_measurement) || "";
      if (u === "EUR") u = "€";
      const ic = unitIcon(u);
      out.push('<span class="chip">' + (ic ? ic + " " : "") +
        (c.label ? this._esc(c.label) + " " : "") +
        "<b>" + this._esc(s.state) + (u ? " " + this._esc(u) : "") + "</b></span>");
    }
    return out.length ? '<div class="chips">' + out.join("") + "</div>" : "";
  }

  _render() {
    if (!this._root) return;
    const tt = this._root.querySelector(".ttx");
    if (tt) tt.textContent = this._config.title;
    this._tickClock();
    if (this._listEl) {
      if (!this._events)
        this._listEl.innerHTML = '<div class="empty">Chargement…</div>';
      else if (!this._events.length)
        this._listEl.innerHTML =
          '<div class="empty">Aucun évènement récent</div>';
      else
        this._listEl.innerHTML = this._events.map((r, i) => {
          const kind = stateKind(r.eid, r.state);
          const abs = new Date(r.when).toLocaleString("fr-FR", {
            weekday: "short", day: "2-digit", month: "2-digit",
            hour: "2-digit", minute: "2-digit" });
          return '<div class="row" style="animation-delay:' + (i * 30) +
            'ms"><div class="ic">' + iconFor(r.eid, r.state) +
            '</div><div class="mid"><div class="l1"><span class="nm">' +
            this._esc(r.name) + '</span><span class="pill k-' + kind + '">' +
            this._esc(this._stateLabel(r)) + "</span></div>" +
            this._chips(r.eid) + '</div><div class="tm"><span class="rel" ' +
            'data-t="' + r.when + '">' + this._relTime(r.when) +
            '</span><span class="abs">' + abs + "</span></div></div>";
        }).join("");
    }
    this._updateStats();
  }

  _paintTimes() {
    if (!this._listEl) return;
    this._listEl.querySelectorAll(".rel").forEach((el) => {
      const t = Number(el.getAttribute("data-t"));
      if (t) el.textContent = this._relTime(t);
    });
  }

  _updateStats() {
    if (!this._footEl || !this._hass) return;
    this._footEl.innerHTML = (this._config.stats || []).map((c) => {
      const s = this._hass.states[c.entity];
      let v = s ? s.state : "—";
      let u = c.unit || (s && s.attributes && s.attributes.unit_of_measurement) || "";
      if (u === "EUR") u = "€";
      const label = c.label || (s && s.attributes && s.attributes.friendly_name)
        || c.entity;
      return '<div class="cell"><div class="cl">' + this._esc(label) +
        '</div><div class="cv">' + this._esc(v) +
        (u ? " " + this._esc(u) : "") + "</div></div>";
    }).join("");
  }

  _esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
}

if (!customElements.get("matrix-history-card"))
  customElements.define("matrix-history-card", MatrixHistoryCard);
window.customCards = window.customCards || [];
window.customCards.push({ type: "matrix-history-card",
  name: "Matrix History Card",
  description: "Journal d'activité néon cyberpunk (logbook + coûts/énergie)." });
console.info("%c MATRIX-HISTORY-CARD v4 ", "background:#0b0618;color:#00eaff");
