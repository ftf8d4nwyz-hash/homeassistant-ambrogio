/*
 * Matrix History Card — journal écrit "style Matrix" pour Home Assistant
 * v2 : chaque ligne DÉFILE horizontalement (marquee) à vitesse lente pour
 * laisser le temps de lire. Pluie de code, lueur verte, effet terminal,
 * enrichissement coût / eau / énergie par appareil + bandeau live.
 *
 * Options principales :
 *   scroll: true|false     -> activer le défilement (défaut true)
 *   direction: "ltr"|"rtl" -> sens du défilement (défaut "ltr" = gauche→droite)
 *   speed: <px/seconde>     -> vitesse (défaut 28 ; plus petit = plus lent)
 */

const KATA =
  "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモ0123456789";

const STATE_FR = {
  on: "MARCHE", off: "ARRET", home: "A LA MAISON", not_home: "ABSENT",
  open: "OUVERT", opened: "OUVERT", closed: "FERME", closing: "FERMETURE",
  opening: "OUVERTURE", locked: "VERROUILLE", unlocked: "DEVERROUILLE",
  docked: "A LA BASE", cleaning: "NETTOYAGE", returning: "RETOUR BASE",
  charging: "EN CHARGE", paused: "PAUSE", idle: "REPOS", playing: "LECTURE",
  heat: "CHAUFFAGE", cool: "CLIM", heat_cool: "AUTO", auto: "AUTO",
  disarmed: "DESARME", armed_away: "ARME ABSENT", armed_home: "ARME PRESENT",
  armed_night: "ARME NUIT", triggered: "ALARME !", detected: "DETECTE",
  clear: "RAS", unavailable: "INDISPO", unknown: "INCONNU",
};

function glyphFor(entity_id, state) {
  const d = (entity_id || "").split(".")[0];
  const on = state === "on" || state === "home" || state === "open" ||
    state === "playing" || state === "cleaning" || state === "charging" ||
    state === "detected";
  const map = {
    binary_sensor: on ? "◉" : "○",
    person: state === "home" ? "☗" : "☖",
    device_tracker: state === "home" ? "☗" : "☖",
    light: on ? "☀" : "☼",
    switch: on ? "▮" : "▯",
    lock: state === "locked" ? "▣" : "▢",
    cover: state === "open" ? "▤" : "▥",
    climate: "❋", vacuum: "⌬",
    alarm_control_panel: state === "triggered" ? "✷" : "⛨",
    media_player: "♫", automation: "λ", script: "λ", sensor: "≡",
  };
  return map[d] || "»";
}

class MatrixHistoryCard extends HTMLElement {
  setConfig(config) {
    this._config = Object.assign(
      {
        title: "SYSTEME // JOURNAL",
        count: 12, hours: 96,
        scroll: true, direction: "ltr", speed: 28,
        entities: [], context: {}, stats: [],
      },
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
  }

  getCardSize() { return 10; }

  connectedCallback() {
    if (!this._root) this._build();
    this._startRain();
    this._clock = setInterval(() => this._tickClock(), 1000);
    this._mo = new ResizeObserver(() => this._setupMarquee());
    this._mo.observe(this);
  }

  disconnectedCallback() {
    this._stopRain();
    if (this._clock) clearInterval(this._clock);
    if (this._mo) { this._mo.disconnect(); this._mo = null; }
    (this._anims || []).forEach((a) => { try { a.cancel(); } catch (e) {} });
    this._anims = [];
  }

  _build() {
    this._root = this.attachShadow({ mode: "open" });
    this._root.innerHTML = `
      <style>
        :host { display:block; }
        ha-card {
          position:relative; overflow:hidden; border:1px solid #00ff41;
          background:#000; box-shadow:0 0 18px rgba(0,255,65,.35),
            inset 0 0 40px rgba(0,255,65,.06);
          font-family:"Courier New",monospace; color:#00ff41;
        }
        canvas.rain { position:absolute; inset:0; width:100%; height:100%;
          opacity:.30; pointer-events:none; }
        .scan { position:absolute; inset:0; pointer-events:none; z-index:2;
          background:repeating-linear-gradient(0deg,
            rgba(0,0,0,0) 0px, rgba(0,0,0,0) 2px,
            rgba(0,255,65,.05) 3px, rgba(0,0,0,0) 4px);
          animation:flick 3.5s infinite; }
        @keyframes flick { 0%,97%{opacity:1} 98%{opacity:.7} 100%{opacity:1} }
        .wrap { position:relative; z-index:3; padding:14px 16px 16px; }
        .hd { display:flex; align-items:center; justify-content:space-between;
          border-bottom:1px dashed rgba(0,255,65,.5); padding-bottom:8px;
          margin-bottom:10px; gap:10px; }
        .ttl { font-weight:bold; letter-spacing:2px; text-transform:uppercase;
          text-shadow:0 0 8px #00ff41; font-size:15px; }
        .ttl .cur { animation:blink 1s steps(2) infinite; }
        @keyframes blink { 0%,50%{opacity:1} 51%,100%{opacity:0} }
        .clk { font-size:12px; opacity:.85; white-space:nowrap; }
        .log { list-style:none; margin:0; padding:0;
          max-height:520px; overflow-y:auto; overflow-x:hidden; }
        .log::-webkit-scrollbar{width:6px}
        .log::-webkit-scrollbar-thumb{background:#00ff41;border-radius:3px}
        .row { display:grid; grid-template-columns:auto 1fr; gap:10px;
          align-items:center; padding:6px 0;
          border-bottom:1px solid rgba(0,255,65,.12);
          animation:fade .5s ease both; }
        @keyframes fade { from{opacity:0} to{opacity:1} }
        .gly { font-size:16px; text-shadow:0 0 8px #00ff41; width:1em;
          text-align:center; }
        .mar { position:relative; overflow:hidden; }
        .move { display:inline-block; white-space:nowrap; will-change:transform;
          font-size:13px; }
        .nm { color:#9dffb0; text-shadow:0 0 4px rgba(0,255,65,.6);
          font-weight:bold; }
        .st { color:#00ff41; text-transform:uppercase; letter-spacing:1px; }
        .ctx { color:#5cff8a; }
        .ctx b { color:#eaffef; }
        .tm { color:#00ff41; opacity:.8; }
        .sep { opacity:.5; padding:0 8px; }
        .foot { margin-top:12px; padding-top:10px;
          border-top:1px dashed rgba(0,255,65,.5);
          display:grid; grid-template-columns:repeat(auto-fit,minmax(120px,1fr));
          gap:8px; }
        .cell { border:1px solid rgba(0,255,65,.35); padding:6px 8px;
          background:rgba(0,255,65,.05); }
        .cell .cl { font-size:10px; opacity:.75; text-transform:uppercase;
          letter-spacing:1px; white-space:nowrap; overflow:hidden;
          text-overflow:ellipsis; }
        .cell .cv { font-size:16px; font-weight:bold; text-shadow:0 0 8px #00ff41; }
        .empty { padding:24px 4px; opacity:.7; font-size:13px; }
      </style>
      <ha-card>
        <canvas class="rain"></canvas>
        <div class="scan"></div>
        <div class="wrap">
          <div class="hd">
            <span class="ttl"></span>
            <span class="clk"></span>
          </div>
          <ul class="log"></ul>
          <div class="foot"></div>
        </div>
      </ha-card>`;
    this._canvas = this._root.querySelector("canvas.rain");
    this._logEl = this._root.querySelector(".log");
    this._footEl = this._root.querySelector(".foot");
    this._render();
    if (this.isConnected) {
      this._startRain();
      if (!this._clock) this._clock = setInterval(() => this._tickClock(), 1000);
    }
  }

  _tickClock() {
    const c = this._root && this._root.querySelector(".clk");
    if (c) c.textContent = "> " + new Date().toLocaleTimeString("fr-FR") + " _";
  }

  async _fetchEvents() {
    const hass = this._hass, cfg = this._config;
    if (!hass) return;
    const start = new Date(Date.now() - cfg.hours * 3600000).toISOString();
    let ev = null;
    try {
      ev = await hass.callWS({
        type: "logbook/get_events",
        start_time: start,
        entity_ids: cfg.entities.length ? cfg.entities : undefined,
      });
    } catch (e) { ev = null; }
    let rows;
    if (Array.isArray(ev) && ev.length) {
      rows = ev.filter((x) => x.entity_id || x.name).map((x) => ({
        when: (x.when || 0) * 1000,
        eid: x.entity_id || "",
        name: x.name || (x.entity_id || "").split(".")[1],
        state: x.state, message: x.message,
      }));
    } else {
      rows = cfg.entities.map((eid) => hass.states[eid]).filter(Boolean).map((s) => ({
        when: new Date(s.last_changed).getTime(),
        eid: s.entity_id,
        name: (s.attributes && s.attributes.friendly_name) || s.entity_id,
        state: s.state,
      }));
    }
    rows.sort((a, b) => b.when - a.when);
    this._events = rows.slice(0, cfg.count);
    this._render();
  }

  _relTime(ms) {
    const s = Math.max(0, Math.floor((Date.now() - ms) / 1000));
    if (s < 60) return "il y a " + s + "s";
    const m = Math.floor(s / 60);
    if (m < 60) return "il y a " + m + "min";
    const h = Math.floor(m / 60);
    if (h < 24) return "il y a " + h + "h";
    return "il y a " + Math.floor(h / 24) + "j";
  }

  _stateLabel(r) {
    if (r.state != null && r.state !== "")
      return STATE_FR[r.state] || String(r.state).toUpperCase();
    if (r.message) return String(r.message).toUpperCase();
    return "";
  }

  _ctxFor(eid) {
    const hass = this._hass;
    const list = (this._config.context || {})[eid];
    if (!list || !hass) return "";
    const parts = [];
    for (const c of list) {
      const s = hass.states[c.entity];
      if (!s || s.state === "unknown" || s.state === "unavailable") continue;
      let unit = c.unit || (s.attributes && s.attributes.unit_of_measurement) || "";
      if (unit === "EUR") unit = "€";
      parts.push((c.label ? c.label + " " : "") + "<b>" + s.state + " " + unit + "</b>");
    }
    return parts.join(" · ");
  }

  _render() {
    if (!this._root) return;
    const cfg = this._config;
    const ttl = this._root.querySelector(".ttl");
    if (ttl) ttl.innerHTML = cfg.title + ' <span class="cur">█</span>';
    this._tickClock();

    if (this._logEl) {
      if (!this._events) {
        this._logEl.innerHTML = '<li class="empty">> chargement du flux…</li>';
      } else if (!this._events.length) {
        this._logEl.innerHTML = '<li class="empty">> aucun évènement récent</li>';
      } else {
        this._logEl.innerHTML = this._events.map((r) => {
          const gly = glyphFor(r.eid, r.state);
          const ctx = this._ctxFor(r.eid);
          const d = new Date(r.when);
          const abs = d.toLocaleString("fr-FR", {
            weekday: "short", day: "2-digit", month: "2-digit",
            hour: "2-digit", minute: "2-digit", second: "2-digit",
          });
          const line =
            '<span class="nm">' + this._esc(r.name) + '</span>' +
            '<span class="sep">::</span>' +
            '<span class="st">' + this._esc(this._stateLabel(r)) + '</span>' +
            (ctx ? '<span class="sep">//</span><span class="ctx">' + ctx + '</span>' : '') +
            '<span class="sep">·</span>' +
            '<span class="tm">🕒 ' + this._relTime(r.when) + ' · ' + this._esc(abs) + '</span>';
          return '<li class="row"><span class="gly">' + gly +
            '</span><span class="mar"><span class="move">' + line +
            '</span></span></li>';
        }).join("");
      }
    }
    this._updateStats();
    // (re)lance le défilement une fois la mise en page effectuée
    requestAnimationFrame(() => requestAnimationFrame(() => this._setupMarquee()));
  }

  _setupMarquee() {
    if (!this._logEl) return;
    (this._anims || []).forEach((a) => { try { a.cancel(); } catch (e) {} });
    this._anims = [];
    const cfg = this._config;
    if (cfg.scroll === false) return;
    const speed = Math.max(6, Number(cfg.speed) || 28); // px/s
    const rtl = cfg.direction === "rtl";
    this._logEl.querySelectorAll(".move").forEach((m) => {
      const cont = m.parentElement;
      const w = m.scrollWidth, cw = cont.clientWidth;
      if (!cw || w <= cw + 4) { m.style.transform = "none"; return; }
      const dur = ((w + cw) / speed) * 1000;
      const from = rtl ? cw : -w;
      const to = rtl ? -w : cw;
      const a = m.animate(
        [{ transform: `translateX(${from}px)` },
         { transform: `translateX(${to}px)` }],
        { duration: dur, iterations: Infinity, easing: "linear" }
      );
      this._anims.push(a);
    });
  }

  _updateStats() {
    if (!this._footEl || !this._hass) return;
    this._footEl.innerHTML = (this._config.stats || []).map((c) => {
      const s = this._hass.states[c.entity];
      let v = s ? s.state : "—";
      let unit = c.unit || (s && s.attributes && s.attributes.unit_of_measurement) || "";
      if (unit === "EUR") unit = "€";
      const label = c.label || (s && s.attributes && s.attributes.friendly_name) || c.entity;
      return '<div class="cell"><div class="cl">' + this._esc(label) +
        '</div><div class="cv">' + this._esc(v) +
        (unit ? " " + this._esc(unit) : "") + "</div></div>";
    }).join("");
  }

  _esc(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  _startRain() {
    if (!this._canvas || this._raf) return;
    const cv = this._canvas, ctx = cv.getContext("2d");
    let cols, drops, fs;
    const resize = () => {
      const r = cv.getBoundingClientRect();
      cv.width = Math.max(1, r.width); cv.height = Math.max(1, r.height);
      fs = 14; cols = Math.ceil(cv.width / fs);
      drops = new Array(cols).fill(0).map(() => Math.random() * -50);
    };
    resize();
    this._ro = new ResizeObserver(resize); this._ro.observe(cv);
    let last = 0;
    const step = (t) => {
      this._raf = requestAnimationFrame(step);
      if (t - last < 55) return;
      last = t;
      ctx.fillStyle = "rgba(0,0,0,0.09)";
      ctx.fillRect(0, 0, cv.width, cv.height);
      ctx.font = fs + "px monospace";
      for (let i = 0; i < cols; i++) {
        const ch = KATA[Math.floor(Math.random() * KATA.length)];
        const x = i * fs, y = drops[i] * fs;
        ctx.fillStyle = "#aaffcc"; ctx.fillText(ch, x, y);
        ctx.fillStyle = "#00ff41"; ctx.fillText(ch, x, y - fs);
        if (y > cv.height && Math.random() > 0.975) drops[i] = 0;
        drops[i] += 1;
      }
    };
    this._raf = requestAnimationFrame(step);
  }

  _stopRain() {
    if (this._raf) cancelAnimationFrame(this._raf);
    this._raf = null;
    if (this._ro) this._ro.disconnect();
    this._ro = null;
  }
}

customElements.define("matrix-history-card", MatrixHistoryCard);
window.customCards = window.customCards || [];
window.customCards.push({
  type: "matrix-history-card",
  name: "Matrix History Card",
  description: "Journal écrit défilant style Matrix (logbook + coûts/énergie).",
});
console.info("%c MATRIX-HISTORY-CARD v2 ", "background:#000;color:#00ff41");
