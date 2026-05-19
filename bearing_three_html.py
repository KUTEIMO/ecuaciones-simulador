# -*- coding: utf-8 -*-
"""
Vista 3D del rodamiento magnético con Three.js (HTML embebido en Streamlit).

Three.js r128 vía <script> global: los iframes de Streamlit suelen dejar el lienzo
a 0×0 con `height:100%` y los ES modules + CDN fallan sin mensaje claro.
"""

from __future__ import annotations

import json
from typing import Any

import numpy as np


def _resample_uniform(
    x: np.ndarray, y: np.ndarray, t: np.ndarray, max_pts: int
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Remuestreo uniforme en tiempo (evita saltos al mover el deslizador)."""
    n = int(len(t))
    if n <= max_pts:
        return x.astype(float), y.astype(float), t.astype(float)
    tq = np.linspace(float(t[0]), float(t[-1]), max_pts)
    xq = np.interp(tq, t, x)
    yq = np.interp(tq, t, y)
    return xq.astype(float), yq.astype(float), tq.astype(float)


def _apply_frame_height(html: str, frame_height: int) -> str:
    h = int(max(360, min(900, frame_height)))
    return html.replace("__FRAME_H__px", str(h) + "px").replace("__FRAME_H__", str(h))


# Radio de la holgura en la escena 3D [m] (anillo rojo = límite físico)
_RING_SCENE_M = 0.048


def scene_coords(
    x_m: np.ndarray,
    y_m: np.ndarray,
    clearance_m: float,
) -> tuple[np.ndarray, np.ndarray, float, float]:
    """
    Escala posiciones para que |desplazamiento| = holgura coincida con el anillo rojo.
    Así el eje permanece dentro del cojinete cuando |x| < holgura, y sale solo si la física lo exige.
    """
    x_m = np.asarray(x_m, dtype=float)
    y_m = np.asarray(y_m, dtype=float)
    clr = max(float(clearance_m), 1e-12)
    scale = _RING_SCENE_M / clr
    return x_m * scale, y_m * scale, _RING_SCENE_M, scale


def visual_gain_for_orbit(
    x_m: np.ndarray,
    y_m: np.ndarray,
    clearance_m: float,
    stable: bool,
) -> float:
    """Amplifica el render 3D si |r|_max es pequeño frente a la holgura."""
    if not stable:
        return 1.0
    r_max = float(np.max(np.hypot(np.asarray(x_m), np.asarray(y_m))))
    clr = max(float(clearance_m), 1e-12)
    if r_max < 0.2 * clr:
        return float(min(4.5, max(1.0, 0.65 * clr / max(r_max, 1e-15))))
    return 1.0


def build_bearing_viewer_html(
    x_m: np.ndarray,
    y_m: np.ndarray,
    t_s: np.ndarray,
    clearance_m: float,
    state: str,
    spin_omega: float,
    start_pct: float = 35.0,
    max_trail_pts: int = 4000,
    frame_height: int = 520,
    case_label: str = "",
    case_id: str = "III",
    expo_tag: str = "",
    alpha_re: float = -3.0,
    beta_im: float = 1.0,
    clearance_um: float = 320.0,
    unstable: bool = False,
    visual_gain: float = 1.0,
) -> str:
    x_m = np.asarray(x_m, dtype=float)
    y_m = np.asarray(y_m, dtype=float)
    t_s = np.asarray(t_s, dtype=float)
    tx, ty, c_vis, scene_scale = scene_coords(x_m, y_m, clearance_m)
    vg = float(max(1.0, min(5.0, visual_gain)))
    tx_d = tx * vg
    ty_d = ty * vg
    tx_d, ty_d, ttl = _resample_uniform(tx_d, ty_d, t_s, max_trail_pts)
    tx, ty, _ = _resample_uniform(tx, ty, t_s, max_trail_pts)
    st = state if state in ("stable", "marginal", "danger") else "stable"
    fh = int(max(360, min(900, frame_height)))
    payload: dict[str, Any] = {
        "tx": tx_d.astype(float).tolist(),
        "ty": ty_d.astype(float).tolist(),
        "txTrue": tx.astype(float).tolist(),
        "tyTrue": ty.astype(float).tolist(),
        "tt": ttl.astype(float).tolist(),
        "visualGain": vg,
        "cVis": float(c_vis),
        "state": st,
        "Rout": 0.10,
        "Rin": 0.056,
        "rShaft": 0.022,
        "zDisk": 0.18,
        "Rblade": 0.09,
        "spinOmega": float(spin_omega),
        "sceneScale": float(scene_scale),
        "startPct": float(np.clip(start_pct, 0.0, 100.0)),
        "frameH": fh,
        "caseLabel": case_label[:120],
        "caseId": case_id,
        "expoTag": (expo_tag or case_label)[:80],
        "alphaRe": float(alpha_re),
        "betaIm": float(beta_im),
        "clearanceUm": float(clearance_um),
        "unstable": bool(unstable),
    }
    blob = json.dumps(payload, separators=(",", ":"))
    html = _BEARING_HTML_TEMPLATE.replace("__BEARING_JSON__", blob)
    return _apply_frame_height(html, fh)


_BEARING_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width,initial-scale=1"/>
  <style>
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; height: 100%; font-family: system-ui, sans-serif; background: #05070c; }
    #wrap {
      position: relative;
      width: 100%;
      height: __FRAME_H__px;
      overflow: hidden;
      background: #05070c;
    }
    #cv { position: absolute; left: 0; right: 0; top: 58px; bottom: 52px; }
    #cv canvas { display: block; width: 100% !important; height: 100% !important; }
    #hud {
      position: absolute; left: 0; right: 0; bottom: 0; height: 52px; z-index: 6;
      padding: 8px 10px; color: #e8eefc;
      background: rgba(5,8,14,0.96);
      border-top: 1px solid rgba(255,255,255,0.08);
      font-size: 12px;
    }
    #hud label { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; height: 100%; }
    #scrub { flex: 1; min-width: 120px; accent-color: #5dade2; }
    #readout { opacity: 0.92; white-space: nowrap; font-variant-numeric: tabular-nums; }
    #err {
      position: absolute; left: 8px; top: 8px; z-index: 7; max-width: 92%;
      padding: 8px 10px; border-radius: 6px; background: rgba(120,20,20,0.92);
      color: #fff; font-size: 12px; display: none;
    }
    #banner {
      position: absolute; left: 8px; top: 8px; right: 8px; z-index: 5;
      padding: 6px 10px; border-radius: 6px;
      background: rgba(15, 35, 65, 0.88); color: #e8eefc;
      font-size: 11px; line-height: 1.35; pointer-events: none;
      border: 1px solid rgba(120, 160, 200, 0.35);
    }
    #banner strong { color: #90caf9; }
  </style>
</head>
<body>
<div id="wrap" data-h="__FRAME_H__">
  <div id="err"></div>
  <div id="banner"></div>
  <div id="cv"></div>
  <div id="hud">
    <label>
      <span style="min-width:7.5em">Instante <strong>t</strong></span>
      <input type="range" id="scrub" min="0" max="1000" value="350" step="1"/>
      <span id="readout"></span>
    </label>
  </div>
</div>
<script type="application/json" id="bearingParams">__BEARING_JSON__</script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js" crossorigin="anonymous"></script>
<script>
(function () {
  function showErr(msg) {
    var el = document.getElementById('err');
    el.style.display = 'block';
    el.textContent = msg;
  }
  if (typeof THREE === 'undefined') { showErr('No se cargó Three.js (red/CDN bloqueado).'); return; }

  var P = {};
  try {
    P = JSON.parse(document.getElementById('bearingParams').textContent);
  } catch (e) {
    showErr('JSON inválido: ' + e.message);
    return;
  }

  var tx = P.tx, ty = P.ty, tt = P.tt;
  var txT = P.txTrue || tx, tyT = P.tyTrue || ty;
  var n = (tx && tx.length) ? tx.length : 0;
  if (!n) { showErr('Trayectoria vacía.'); return; }

  var spinOm = P.spinOmega || 0;
  var sc = P.sceneScale || 1;
  var storageKey = 'bearingScrub_' + (P.expoTag || P.caseId || 'default');

  var PAL = {
    stable:   { st: 0x34495e, sh: 0x27ae60, hub: 0x2980b9, bl: 0x85c1e9, em: 0x1f618d },
    marginal: { st: 0x9a7d0a, sh: 0xf39c12, hub: 0xd68910, bl: 0xf9e79f, em: 0xb9770e },
    danger:   { st: 0x78281f, sh: 0xe74c3c, hub: 0xc0392b, bl: 0xfadbd8, em: 0x922b21 },
  };
  var col = PAL[P.state] || PAL.stable;

  function phong(hex) {
    return new THREE.MeshPhongMaterial({ color: hex, shininess: 60, specular: 0x555555 });
  }

  var cv = document.getElementById('cv');
  var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  cv.appendChild(renderer.domElement);

  var scene = new THREE.Scene();
  scene.background = new THREE.Color(0x0a0e18);
  scene.fog = new THREE.Fog(0x0a0e18, 0.35, 2.2);

  var camera = new THREE.PerspectiveCamera(42, 1, 0.01, 20);
  camera.position.set(0.34, 0.36, 0.42);

  var controls = null;
  try {
    if (typeof THREE.OrbitControls === 'function') {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.06;
      controls.target.set(0, 0, 0.04);
    }
  } catch (e) {
    showErr('OrbitControls: ' + e.message);
  }

  scene.add(new THREE.AmbientLight(0xffffff, 0.55));
  var L1 = new THREE.DirectionalLight(0xffffff, 1.0);
  L1.position.set(0.9, 1.0, 0.7);
  scene.add(L1);
  var L2 = new THREE.DirectionalLight(0xaaccff, 0.5);
  L2.position.set(-0.9, -0.5, -0.2);
  scene.add(L2);

  var group = new THREE.Group();
  scene.add(group);

  var stMat = phong(col.st);
  for (var i = 0; i < 7; i++) {
    var z = -0.028 + i * (0.056 / 6);
    var tor = new THREE.Mesh(new THREE.TorusGeometry(P.Rout, 0.012, 18, 64), stMat);
    tor.position.z = z;
    group.add(tor);
  }

  var shellGeo = new THREE.CylinderGeometry(P.Rout + 0.012, P.Rout + 0.012, 0.075, 40, 1, true);
  var shell = new THREE.Mesh(shellGeo, phong(col.st));
  shell.material.side = THREE.DoubleSide;
  shell.rotation.x = Math.PI / 2;
  group.add(shell);

  var emMat = phong(col.em);
  for (var k = 0; k < 4; k++) {
    var ang = (k * Math.PI) / 2;
    var r1 = P.Rin * 0.86;
    var r2 = P.Rout * 0.9;
    var box = new THREE.Mesh(new THREE.BoxGeometry(0.018, 0.028, (r2 - r1)), emMat);
    var mid = (r1 + r2) * 0.5;
    box.position.set(mid * Math.cos(ang), mid * Math.sin(ang), 0);
    box.rotation.z = ang;
    group.add(box);
  }

  var gap = new THREE.Mesh(
    new THREE.TorusGeometry(P.cVis, 0.0025, 12, 80),
    new THREE.MeshBasicMaterial({ color: 0xe74c3c, transparent: true, opacity: 0.92 })
  );
  gap.position.z = 0.001;
  group.add(gap);

  var gapInner = new THREE.Mesh(
    new THREE.TorusGeometry(P.Rin * 0.92, 0.0012, 8, 64),
    new THREE.MeshBasicMaterial({ color: 0x5dade2, transparent: true, opacity: 0.35 })
  );
  gapInner.position.z = 0.0005;
  group.add(gapInner);

  var shaftGeo = new THREE.CylinderGeometry(P.rShaft, P.rShaft, 0.36, 36);
  shaftGeo.rotateX(Math.PI / 2);
  var shaft = new THREE.Mesh(shaftGeo, phong(col.sh));
  group.add(shaft);

  var hub = new THREE.Mesh(new THREE.CylinderGeometry(0.032, 0.032, 0.022, 32), phong(col.hub));
  hub.rotation.x = Math.PI / 2;
  group.add(hub);

  var bladeRoot = new THREE.Group();
  group.add(bladeRoot);

  var blMat = phong(col.bl);
  var nBl = 8;
  for (var bi = 0; bi < nBl; bi++) {
    var a0 = (bi * 2 * Math.PI) / nBl;
    var blade = new THREE.Mesh(new THREE.BoxGeometry(P.Rblade, 0.014, 0.04), blMat);
    blade.position.set((P.Rblade * 0.52) * Math.cos(a0), (P.Rblade * 0.52) * Math.sin(a0), 0);
    blade.rotation.z = a0;
    bladeRoot.add(blade);
  }

  var mark = new THREE.Mesh(new THREE.OctahedronGeometry(0.012, 0), phong(0xf39c12));
  group.add(mark);

  var trailPts = [];
  for (var ti = 0; ti < n; ti++) { trailPts.push(tx[ti], ty[ti], 0.004); }
  var trailGeo = new THREE.BufferGeometry();
  trailGeo.setAttribute('position', new THREE.Float32BufferAttribute(trailPts, 3));
  var trailCol = (P.state === 'danger') ? 0xe74c3c : ((P.state === 'marginal') ? 0xf39c12 : 0x5dade2);
  var trail = new THREE.Line(trailGeo, new THREE.LineBasicMaterial({ color: trailCol, transparent: true, opacity: 0.9 }));
  group.add(trail);

  var banner = document.getElementById('banner');
  var ar = P.alphaRe || 0, bi = P.betaIm || 0;
  var poleTxt = (bi > 0.01) ? (ar.toFixed(2) + ' \u00B1 ' + bi.toFixed(2) + 'i') : ar.toFixed(2);
  var stabTxt = P.unstable ? 'INESTABLE (Re(s)>0)' :
    ((ar < -0.001) ? 'ESTABLE (Re(s)<0)' : 'REVISAR polos');
  var tipoRaiz = 'Tipo ra\u00edz ' + (P.caseId || '?');
  banner.innerHTML = '<strong>' + (P.expoTag || tipoRaiz) + '</strong> \u00B7 ' + tipoRaiz +
    ' \u00B7 ' + stabTxt + ' \u00B7 s \u2248 ' + poleTxt +
    ' \u00B7 holgura ' + (P.clearanceUm || 0).toFixed(0) + ' \u00b5m (anillo rojo)';

  var readout = document.getElementById('readout');
  var scrub = document.getElementById('scrub');
  var tMax = tt[n - 1];

  function posAtFrac(frac) {
    if (n <= 1) {
      return { ox: tx[0], oy: ty[0], oxT: txT[0], oyT: tyT[0], t: tt[0] };
    }
    var tq = Math.max(tt[0], Math.min(tMax, frac * tMax));
    if (tq <= tt[0]) {
      return { ox: tx[0], oy: ty[0], oxT: txT[0], oyT: tyT[0], t: tt[0] };
    }
    if (tq >= tt[n - 1]) {
      return { ox: tx[n - 1], oy: ty[n - 1], oxT: txT[n - 1], oyT: tyT[n - 1], t: tt[n - 1] };
    }
    for (var j = 0; j < n - 1; j++) {
      if (tq >= tt[j] && tq <= tt[j + 1]) {
        var dt = tt[j + 1] - tt[j];
        var w = dt > 1e-15 ? (tq - tt[j]) / dt : 0;
        return {
          ox: tx[j] * (1 - w) + tx[j + 1] * w,
          oy: ty[j] * (1 - w) + ty[j + 1] * w,
          oxT: txT[j] * (1 - w) + txT[j + 1] * w,
          oyT: tyT[j] * (1 - w) + tyT[j + 1] * w,
          t: tq
        };
      }
    }
    return { ox: tx[n - 1], oy: ty[n - 1], oxT: txT[n - 1], oyT: tyT[n - 1], t: tt[n - 1] };
  }

  var scrubTimer = null;

  function applyFrac(frac) {
    var p = posAtFrac(frac);
    shaft.position.set(p.ox, p.oy, 0);
    hub.position.set(p.ox, p.oy, P.zDisk);
    bladeRoot.position.set(p.ox, p.oy, P.zDisk);
    bladeRoot.rotation.z = spinOm * p.t;
    mark.position.set(p.ox, p.oy, 0);
    var xum = (p.oxT / sc) * 1e6;
    var yum = (p.oyT / sc) * 1e6;
    var rad = Math.sqrt(xum * xum + yum * yum);
    var clr = P.clearanceUm || 1;
    var pct = (rad / clr * 100).toFixed(0);
    var warn = (rad > clr * 1.02) ? '  | FUERA de holgura' : '  | dentro de holgura';
    readout.textContent = 't = ' + p.t.toFixed(4) + ' s  |  x = ' + xum.toFixed(1) +
      ' \u00b5m  |  y = ' + yum.toFixed(1) + ' \u00b5m  |  |r| = ' + rad.toFixed(1) +
      ' \u00b5m (' + pct + '%)' + warn;
  }

  var frac0 = P.startPct / 100;
  try {
    var stored = localStorage.getItem(storageKey);
    if (stored !== null && stored !== '') {
      var f = parseFloat(stored);
      if (!isNaN(f) && f >= 0 && f <= 1) frac0 = f;
    }
  } catch (e) {}
  frac0 = Math.max(0, Math.min(1, frac0));
  scrub.value = String(Math.round(frac0 * 1000));
  applyFrac(frac0);
  scrub.addEventListener('input', function () {
    var f = Number(scrub.value) / 1000;
    applyFrac(f);
    if (scrubTimer) clearTimeout(scrubTimer);
    scrubTimer = setTimeout(function () {
      try { localStorage.setItem(storageKey, String(f)); } catch (e) {}
    }, 80);
  });

  function resize() {
    var w = Math.max(200, cv.clientWidth);
    var h = Math.max(200, cv.clientHeight);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h, false);
  }
  window.addEventListener('resize', resize);
  resize();

  function tick() {
    requestAnimationFrame(tick);
    if (controls) controls.update();
    renderer.render(scene, camera);
  }
  tick();
})();
</script>
</body>
</html>
"""
