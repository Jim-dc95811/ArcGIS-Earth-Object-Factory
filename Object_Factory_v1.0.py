#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import os
import re
import shutil
import sys
import tempfile
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from xml.sax.saxutils import escape as xml_escape

APP = "ArcGIS Earth Object Factory"
VERSION = "1.0"
CAMERA_URL = "http://localhost:8000/arcgisearth/camera"
HTTP_TIMEOUT = 1.0
EARTH_R = 6371008.8
MAX_ICON_DIM = 256

COLORS = {
    "Red": "ff0000ff",
    "Yellow": "ff00ffff",
    "Cyan": "ffffff00",
    "Green": "ff00ff00",
    "Magenta": "ffff00ff",
    "White": "ffffffff",
    "Orange": "ff0088ff",
}

PRESET_ALIASES = {
    "heli": "helicopter",
    "helicopter": "helicopter",
    "fuel": "fuel",
    "gas": "fuel",
    "gas_pump": "fuel",
    "bird": "bird",
    "hazard": "hazard",
    "warning": "hazard",
    "home": "home",
    "base": "home",
    "staging": "staging",
    "water": "water",
    "firetruck": "firetruck",
    "truck": "firetruck",
    "camera": "camera",
    "viewpoint": "camera",
    "medical": "medical",
    "hospital": "medical",
    "object": "object",
    "pin": "object",
}

PRESET_DEFAULTS = {
    "object":      {"alt": 150.0, "scale": 1.4},
    "helicopter":  {"alt": 300.0, "scale": 1.5},
    "fuel":        {"alt": 150.0, "scale": 1.4},
    "bird":        {"alt": 120.0, "scale": 1.4},
    "hazard":      {"alt": 200.0, "scale": 1.5},
    "home":        {"alt": 200.0, "scale": 1.5},
    "staging":     {"alt": 150.0, "scale": 1.5},
    "water":       {"alt": 150.0, "scale": 1.5},
    "firetruck":   {"alt": 150.0, "scale": 1.5},
    "camera":      {"alt": 180.0, "scale": 1.5},
    "medical":     {"alt": 180.0, "scale": 1.5},
}

FLOAT_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)")


def app_dir() -> Path:
    return Path(__file__).resolve().parent


def icon_dir() -> Path:
    return app_dir() / "icons"


def boolish(value, default=False) -> bool:
    if value is None or str(value).strip() == "":
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}


def validate_lat_lon(lat: float, lon: float) -> tuple[float, float]:
    if not (math.isfinite(lat) and math.isfinite(lon)):
        raise ValueError("Coordinates must be finite numbers.")
    if not -90 <= lat <= 90:
        raise ValueError("Latitude must be between -90 and 90.")
    if not -180 <= lon <= 180:
        raise ValueError("Longitude must be between -180 and 180.")
    return lat, lon


def parse_clipboard_coordinates(text: str, order: str = "Auto") -> tuple[float, float, str]:
    if not text or not text.strip():
        raise ValueError("The clipboard is empty.")
    source = text.strip()
    lat_match = re.search(r"\b(?:lat|latitude)\b\s*[:=]?\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))", source, re.I)
    lon_match = re.search(r"\b(?:lon|lng|long|longitude)\b\s*[:=]?\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))", source, re.I)
    if lat_match and lon_match:
        lat, lon = float(lat_match.group(1)), float(lon_match.group(1))
        validate_lat_lon(lat, lon)
        return lat, lon, "Clipboard labels identified latitude and longitude."
    nums = [float(x) for x in FLOAT_RE.findall(source)]
    if len(nums) < 2:
        raise ValueError("Could not find two decimal coordinates in the clipboard.")
    a, b = nums[0], nums[1]
    if order == "Lat, Lon":
        validate_lat_lon(a, b); return a, b, "Clipboard interpreted as Latitude, Longitude."
    if order == "Lon, Lat":
        validate_lat_lon(b, a); return b, a, "Clipboard interpreted as Longitude, Latitude."
    a_lat, b_lat = -90 <= a <= 90, -90 <= b <= 90
    if not (-180 <= a <= 180 and -180 <= b <= 180):
        raise ValueError("Clipboard coordinates are outside valid longitude range.")
    if not a_lat and b_lat:
        validate_lat_lon(b, a); return b, a, "Auto-detected Longitude, Latitude by numeric range."
    if a_lat and not b_lat:
        validate_lat_lon(a, b); return a, b, "Auto-detected Latitude, Longitude by numeric range."
    if a_lat and b_lat:
        validate_lat_lon(a, b)
        return a, b, "Ambiguous pair: interpreted as Latitude, Longitude. Verify coordinates before creation."
    raise ValueError("Could not determine a valid latitude/longitude pair.")


def get_arcgis_camera_coordinates() -> tuple[float, float]:
    req = urllib.request.Request(CAMERA_URL, method="GET", headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        raise ValueError(f"Could not reach ArcGIS Earth Automation API: {exc}") from exc
    try:
        camera = json.loads(raw)
        pos = camera["position"]
        lon, lat = float(pos["x"]), float(pos["y"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Unexpected ArcGIS Earth camera response: {exc}") from exc
    sr = pos.get("spatialReference") or {}
    wkid = sr.get("wkid")
    if wkid not in (None, 4326, "4326"):
        raise ValueError(f"ArcGIS Earth camera is not reporting WKID 4326 (reported {wkid}).")
    validate_lat_lon(lat, lon)
    return lat, lon


def preset_key(value: str) -> str:
    raw = (value or "object").strip().lower().replace(" ", "_")
    return PRESET_ALIASES.get(raw, raw if raw in PRESET_DEFAULTS else "object")


def preset_icon(value: str) -> Path:
    key = preset_key(value)
    p = icon_dir() / f"{key}.png"
    if p.exists():
        return p
    return icon_dir() / "object.png"


def png_info(path: Path, master=None) -> tuple[int, int, int, bool]:
    p = Path(path)
    if p.suffix.lower() != ".png":
        raise ValueError("Object Factory accepts PNG icons only.")
    if not p.is_file():
        raise FileNotFoundError(p)
    im = tk.PhotoImage(master=master, file=str(p))
    return im.width(), im.height(), p.stat().st_size, True


def normalize_png(source: Path, dest: Path, master=None, max_dim: int = MAX_ICON_DIM) -> dict:
    """Standard-library/Tk normalization. Original file is never modified.

    Tk PhotoImage preserves PNG transparency. If a source is over max_dim, use integer
    subsampling so the packaged working copy is <= max_dim while preserving aspect ratio.
    Smaller sources are copied unchanged and are never upscaled.
    """
    source, dest = Path(source), Path(dest)
    if source.suffix.lower() != ".png":
        raise ValueError(f"PNG required: {source.name}")
    if not source.is_file():
        raise FileNotFoundError(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    im = tk.PhotoImage(master=master, file=str(source))
    w, h = im.width(), im.height()
    if w <= 0 or h <= 0:
        raise ValueError(f"Invalid PNG dimensions: {source}")
    factor = max(1, math.ceil(max(w, h) / max_dim))
    if factor == 1:
        shutil.copy2(source, dest)
        out_w, out_h = w, h
    else:
        small = im.subsample(factor, factor)
        small.write(str(dest), format="png")
        out_w, out_h = small.width(), small.height()
    return {"source_w": w, "source_h": h, "out_w": out_w, "out_h": out_h, "factor": factor}


def description_html(description: str, url: str = "", link_text: str = "OPEN LINK") -> str:
    parts = []
    if description and description.strip():
        for line in description.strip().splitlines():
            parts.append(html.escape(line))
        body = "<br/>".join(parts)
    else:
        body = ""
    if url and url.strip():
        link = f'<a href="{html.escape(url.strip(), quote=True)}">{html.escape((link_text or "OPEN LINK").strip())}</a>'
        body = f"{body}<br/><br/>{link}" if body else link
    return body


def object_style(style_id: str, icon_href: str, scale: float, show_label: bool, popup_mode: str) -> str:
    label_scale = "1.0" if show_label else "0.0"
    balloon = "<BalloonStyle><displayMode>hide</displayMode></BalloonStyle>" if popup_mode.lower() == "none" else ""
    return f'''  <Style id="{style_id}">
    <IconStyle><scale>{scale:g}</scale><Icon><href>{xml_escape(icon_href)}</href></Icon></IconStyle>
    <LabelStyle><scale>{label_scale}</scale></LabelStyle>
    {balloon}
  </Style>'''


def object_placemark(name: str, lat: float, lon: float, altitude_m: float, style_id: str,
                     altitude_mode: str = "relativeToGround", description: str = "", url: str = "",
                     link_text: str = "OPEN LINK", tether: bool = False, popup_mode: str = "Info") -> str:
    validate_lat_lon(lat, lon)
    if altitude_mode not in {"relativeToGround", "absolute", "clampToGround"}:
        raise ValueError(f"Unsupported altitude mode: {altitude_mode}")
    safe_name = xml_escape(name.strip() or "Object")
    desc = ""
    if popup_mode.lower() != "none":
        body = description_html(description, url, link_text)
        if body:
            desc = f"\n    <description><![CDATA[{body}]]></description>"
    if altitude_mode == "clampToGround":
        coord_alt = 0
    else:
        coord_alt = altitude_m
    tether_kml = ""
    if tether and altitude_mode != "clampToGround":
        tether_kml = f'''
  <Placemark>
    <name>{safe_name} tether</name>
    <Style><LineStyle><color>ff4040ff</color><width>2</width></LineStyle><LabelStyle><scale>0</scale></LabelStyle><BalloonStyle><displayMode>hide</displayMode></BalloonStyle></Style>
    <LineString><altitudeMode>{altitude_mode}</altitudeMode><coordinates>{lon},{lat},0 {lon},{lat},{altitude_m}</coordinates></LineString>
  </Placemark>'''
    pm = f'''  <Placemark>
    <name>{safe_name}</name>
    <styleUrl>#{style_id}</styleUrl>{desc}
    <Point><altitudeMode>{altitude_mode}</altitudeMode><coordinates>{lon},{lat},{coord_alt}</coordinates></Point>
  </Placemark>'''
    return pm + tether_kml


def create_single_object_kmz(output_path: Path, icon_path: Path, name: str, lat: float, lon: float,
                             altitude_m: float, scale: float, altitude_mode: str, description: str,
                             url: str, link_text: str, tether: bool, show_label: bool, popup_mode: str,
                             master=None) -> Path:
    output_path = Path(output_path)
    if output_path.suffix.lower() != ".kmz":
        output_path = output_path.with_suffix(".kmz")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        norm = td / "icon.png"
        normalize_png(icon_path, norm, master=master)
        style = object_style("objectStyle", "icons/icon.png", scale, show_label, popup_mode)
        pm = object_placemark(name, lat, lon, altitude_m, "objectStyle", altitude_mode,
                              description, url, link_text, tether, popup_mode)
        kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{xml_escape(name.strip() or "Object")}</name>
{style}
{pm}
</Document>
</kml>'''
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("doc.kml", kml)
            z.write(norm, "icons/icon.png")
    return output_path


def parse_batch_rows(path: Path) -> list[dict]:
    path = Path(path)
    lines = [ln for ln in path.read_text(encoding="utf-8-sig").splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
    if not lines:
        return []
    first = lines[0].lower()
    has_header = "lat" in first and "lon" in first and ("," in first or "|" in first)
    rows = []
    if has_header:
        delim = "|" if "|" in lines[0] else ","
        reader = csv.DictReader(lines, delimiter=delim)
        for idx, row in enumerate(reader, start=2):
            clean = {str(k).strip().lower(): (v.strip() if v else "") for k, v in row.items() if k}
            if not clean.get("lat") or not clean.get("lon"):
                raise ValueError(f"Line {idx}: latitude and longitude are required.")
            typ = clean.get("type", "object") or "object"
            key = preset_key(typ)
            defaults = PRESET_DEFAULTS.get(key, PRESET_DEFAULTS["object"])
            name = clean.get("name") or key.replace("_", " ").title()
            rows.append({
                "type": key,
                "name": name,
                "lat": float(clean["lat"]),
                "lon": float(clean["lon"]),
                "alt_m": float(clean.get("alt_m") or clean.get("alt") or defaults["alt"]),
                "icon": clean.get("icon", ""),
                "description": clean.get("description", ""),
                "url": clean.get("url", ""),
                "link_text": clean.get("link_text", "OPEN LINK") or "OPEN LINK",
                "scale": float(clean.get("scale") or defaults["scale"]),
                "altitude_mode": clean.get("altitude_mode", "relativeToGround") or "relativeToGround",
                "tether": boolish(clean.get("tether"), False),
                "popup": clean.get("popup", "Info") or "Info",
                "label": boolish(clean.get("label"), False),
            })
    else:
        # Simple shorthand: type,lat,lon[,alt_m][,name]
        for idx, ln in enumerate(lines, start=1):
            delim = "|" if "|" in ln else ","
            parts = [p.strip() for p in ln.split(delim)]
            if len(parts) < 3:
                raise ValueError(f"Line {idx}: shorthand requires type,lat,lon[,alt_m][,name].")
            typ, lat, lon = parts[0], float(parts[1]), float(parts[2])
            key = preset_key(typ)
            defaults = PRESET_DEFAULTS.get(key, PRESET_DEFAULTS["object"])
            alt = float(parts[3]) if len(parts) >= 4 and parts[3] else defaults["alt"]
            name = parts[4] if len(parts) >= 5 and parts[4] else key.replace("_", " ").title()
            rows.append({
                "type": key, "name": name, "lat": lat, "lon": lon, "alt_m": alt,
                "icon": "", "description": "", "url": "", "link_text": "OPEN LINK",
                "scale": defaults["scale"], "altitude_mode": "relativeToGround",
                "tether": False, "popup": "Info", "label": False,
            })
    for r in rows:
        validate_lat_lon(r["lat"], r["lon"])
    return rows


def resolve_row_icon(row: dict, list_path: Path) -> Path:
    if row.get("icon"):
        p = Path(row["icon"])
        if not p.is_absolute():
            p = Path(list_path).parent / p
        return p
    return preset_icon(row.get("type", "object"))


def create_batch_kmz(list_path: Path, output_path: Path, master=None) -> tuple[Path, int]:
    rows = parse_batch_rows(list_path)
    if not rows:
        raise ValueError("Object list is empty.")
    output_path = Path(output_path)
    if output_path.suffix.lower() != ".kmz":
        output_path = output_path.with_suffix(".kmz")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        asset_by_key = {}
        asset_files = {}
        styles = []
        placemarks = []
        for i, row in enumerate(rows, start=1):
            src = resolve_row_icon(row, list_path)
            if src.suffix.lower() != ".png":
                raise ValueError(f"{row['name']}: icon must be PNG ({src})")
            if not src.exists():
                raise FileNotFoundError(f"{row['name']}: icon not found: {src}")
            key = str(src.resolve()).lower()
            if key not in asset_by_key:
                digest = hashlib.sha1(key.encode("utf-8")).hexdigest()[:8]
                arc = f"icons/{len(asset_by_key)+1:03d}_{src.stem}_{digest}.png"
                norm = td / Path(arc).name
                normalize_png(src, norm, master=master)
                asset_by_key[key] = arc
                asset_files[arc] = norm
            arc = asset_by_key[key]
            sid = f"s{i}"
            styles.append(object_style(sid, arc, row["scale"], row["label"], row["popup"]))
            placemarks.append(object_placemark(row["name"], row["lat"], row["lon"], row["alt_m"], sid,
                                               row["altitude_mode"], row["description"], row["url"],
                                               row["link_text"], row["tether"], row["popup"]))
        docname = xml_escape(Path(list_path).stem)
        kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
  <name>{docname}</name>
{chr(10).join(styles)}
{chr(10).join(placemarks)}
</Document>
</kml>'''
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("doc.kml", kml)
            for arc, norm in asset_files.items():
                z.write(norm, arc)
    return output_path, len(rows)


def destination(lat_deg: float, lon_deg: float, bearing_deg: float, distance_m: float) -> tuple[float, float]:
    lat, lon, br = math.radians(lat_deg), math.radians(lon_deg), math.radians(bearing_deg)
    a = distance_m / EARTH_R
    lat2 = math.asin(math.sin(lat)*math.cos(a) + math.cos(lat)*math.sin(a)*math.cos(br))
    lon2 = lon + math.atan2(math.sin(br)*math.sin(a)*math.cos(lat), math.cos(a)-math.sin(lat)*math.sin(lat2))
    lon2 = (lon2 + 3*math.pi) % (2*math.pi) - math.pi
    return math.degrees(lat2), math.degrees(lon2)


def create_sky_compass_kmz(output_path: Path, center_lat: float, center_lon: float, radius_km: float,
                           altitude_m: float, icon_scale: float) -> Path:
    validate_lat_lon(center_lat, center_lon)
    output_path = Path(output_path)
    if output_path.suffix.lower() != ".kmz":
        output_path = output_path.with_suffix(".kmz")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    defs = [("N", 0), ("E", 90), ("S", 180), ("W", 270)]
    styles, pms = [], []
    for i, (letter, bearing) in enumerate(defs, start=1):
        lat, lon = destination(center_lat, center_lon, bearing, radius_km*1000)
        arc = f"icons/{letter}.png"
        sid = f"s{i}"
        styles.append(object_style(sid, arc, icon_scale, False, "Info"))
        pms.append(object_placemark(letter, lat, lon, altitude_m, sid, "relativeToGround",
                                    f"{letter} sky compass marker; {radius_km:g} km from center.", "", "", False, "Info"))
    kml = f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document><name>Sky Compass</name>
{chr(10).join(styles)}
{chr(10).join(pms)}
</Document></kml>'''
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("doc.kml", kml)
        for letter, _ in defs:
            src = icon_dir() / f"{letter}.png"
            if not src.exists():
                raise FileNotFoundError(src)
            z.write(src, f"icons/{letter}.png")
    return output_path


def build_beacon_kml(name: str, lat: float, lon: float, height_m: float, width: float, color_kml: str) -> str:
    validate_lat_lon(lat, lon)
    if not math.isfinite(height_m) or height_m <= 0:
        raise ValueError("Beacon height must be greater than zero.")
    if not math.isfinite(width) or width <= 0:
        raise ValueError("Line width must be greater than zero.")
    safe_name = xml_escape(name.strip() or "EarthStick Beacon")
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{safe_name}</name>
    <Style id="beaconStyle">
      <LineStyle><color>{color_kml}</color><width>{width:g}</width></LineStyle>
      <IconStyle><scale>1.1</scale></IconStyle>
    </Style>
    <Placemark>
      <name>{safe_name}</name>
      <styleUrl>#beaconStyle</styleUrl>
      <MultiGeometry>
        <Point><altitudeMode>relativeToGround</altitudeMode><coordinates>{lon:.8f},{lat:.8f},0</coordinates></Point>
        <LineString><tessellate>0</tessellate><altitudeMode>relativeToGround</altitudeMode><coordinates>
          {lon:.8f},{lat:.8f},0
          {lon:.8f},{lat:.8f},{height_m:.3f}
        </coordinates></LineString>
      </MultiGeometry>
    </Placemark>
  </Document>
</kml>
'''


def create_beacon_kml(output_path: Path, name: str, lat: float, lon: float, height_km: float, width: float, color_name: str) -> Path:
    output_path = Path(output_path)
    if output_path.suffix.lower() != ".kml":
        output_path = output_path.with_suffix(".kml")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_beacon_kml(name, lat, lon, height_km*1000.0, width, COLORS[color_name]), encoding="utf-8")
    return output_path


def open_path(path: Path):
    try:
        if os.name == "nt":
            os.startfile(str(path))
        elif sys.platform == "darwin":
            os.system(f'open "{path}"')
        else:
            os.system(f'xdg-open "{path}" >/dev/null 2>&1 &')
    except Exception:
        pass


class CoordinateMixin:
    def clipboard_coords(self, lat_var, lon_var, status_var, order="Auto"):
        try:
            text = self.clipboard_get()
            lat, lon, msg = parse_clipboard_coordinates(text, order)
            lat_var.set(f"{lat:.12f}".rstrip("0").rstrip("."))
            lon_var.set(f"{lon:.12f}".rstrip("0").rstrip("."))
            status_var.set(msg)
        except Exception as e:
            messagebox.showerror(APP, str(e))


class ObjectFactory(tk.Tk, CoordinateMixin):
    def __init__(self, smoke_test=False):
        super().__init__()
        self.title(f"{APP} {VERSION}")
        self.geometry("980x790")
        self.minsize(900, 700)
        self.status = tk.StringVar(value="Factory ready. Object Factory v1.0 commissioned for ArcGIS Earth.")
        self.preview_image = None
        self._build_ui()
        if smoke_test:
            self.after(1000, self.destroy)

    def _build_ui(self):
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)
        header = ttk.Frame(root)
        header.pack(fill="x")
        ttk.Label(header, text="ArcGIS Earth Object Factory", font=("Segoe UI", 19, "bold")).pack(side="left")
        ttk.Label(header, text=f"v{VERSION}", font=("Segoe UI", 10)).pack(side="left", padx=(8,0), pady=(8,0))
        ttk.Label(root, text="Create geographic objects without hand-writing KML. Original PNG files are never modified.").pack(anchor="w", pady=(2,8))
        style = ttk.Style(self)
        style.configure("Factory.TNotebook.Tab", font=("Segoe UI", 12, "bold"), foreground="#005EA8", padding=(18, 9))
        style.map("Factory.TNotebook.Tab", foreground=[("selected", "#003B73"), ("active", "#004F8C")])
        self.nb = ttk.Notebook(root, style="Factory.TNotebook")
        self.nb.pack(fill="both", expand=True)
        self.object_tab = ttk.Frame(self.nb, padding=10)
        self.batch_tab = ttk.Frame(self.nb, padding=10)
        self.compass_tab = ttk.Frame(self.nb, padding=10)
        self.beacon_tab = ttk.Frame(self.nb, padding=10)
        self.nb.add(self.object_tab, text="Objects")
        self.nb.add(self.batch_tab, text="Batch")
        self.nb.add(self.compass_tab, text="Sky Compass")
        self.nb.add(self.beacon_tab, text="Beacon")
        self._build_object_tab()
        self._build_batch_tab()
        self._build_compass_tab()
        self._build_beacon_tab()
        ttk.Separator(root).pack(fill="x", pady=(8,5))
        ttk.Label(root, textvariable=self.status, wraplength=930).pack(anchor="w")

    def _coord_buttons(self, parent, row, latv, lonv, statusv):
        f = ttk.Frame(parent)
        f.grid(row=row, column=1, columnspan=3, sticky="w", pady=(2,6))
        ttk.Button(f, text="From Clipboard", command=lambda:self.clipboard_coords(latv, lonv, statusv)).pack(side="left")

    def _build_object_tab(self):
        t = self.object_tab
        t.columnconfigure(1, weight=1); t.columnconfigure(3, weight=1)
        self.ov = {
            "preset": tk.StringVar(value="object"), "name": tk.StringVar(value="Airborne Object"),
            "lat": tk.StringVar(value="30.385524823620624"), "lon": tk.StringVar(value="-81.93080672778036"),
            "alt": tk.StringVar(value="150"), "scale": tk.StringVar(value="1.4"),
            "mode": tk.StringVar(value="relativeToGround"), "icon": tk.StringVar(value=str(preset_icon("object"))),
            "popup": tk.StringVar(value="Info"), "link_text": tk.StringVar(value="OPEN LINK"), "url": tk.StringVar(),
            "tether": tk.BooleanVar(value=False), "label": tk.BooleanVar(value=False),
            "out": tk.StringVar(value=str(Path.home()/"Desktop"/"ArcGIS_Earth_Object.kmz")),
            "png_info": tk.StringVar(value="Select a PNG. Packaged copy will be <=256 px; original remains untouched."),
            "coord_status": tk.StringVar(value="Enter coordinates manually or use From Clipboard."),
        }
        r=0
        ttk.Label(t,text="Single Object",font=("Segoe UI",15,"bold")).grid(row=r,column=0,columnspan=4,sticky="w",pady=(0,8));r+=1
        ttk.Label(t,text="Preset").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4)
        presets=["object","helicopter","fuel","bird","hazard","home","staging","water","firetruck","camera","medical"]
        cb=ttk.Combobox(t,textvariable=self.ov["preset"],values=presets,state="readonly");cb.grid(row=r,column=1,sticky="ew",pady=4);cb.bind("<<ComboboxSelected>>",self.on_preset)
        ttk.Label(t,text="Object name").grid(row=r,column=2,sticky="w",padx=(16,8),pady=4);ttk.Entry(t,textvariable=self.ov["name"]).grid(row=r,column=3,sticky="ew",pady=4);r+=1
        ttk.Label(t,text="Latitude").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["lat"]).grid(row=r,column=1,sticky="ew",pady=4)
        ttk.Label(t,text="Longitude").grid(row=r,column=2,sticky="w",padx=(16,8),pady=4);ttk.Entry(t,textvariable=self.ov["lon"]).grid(row=r,column=3,sticky="ew",pady=4);r+=1
        self._coord_buttons(t,r,self.ov["lat"],self.ov["lon"],self.ov["coord_status"]);r+=1
        ttk.Label(t,textvariable=self.ov["coord_status"],foreground="#555").grid(row=r,column=1,columnspan=3,sticky="w",pady=(0,6));r+=1
        ttk.Label(t,text="PNG icon").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["icon"]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=4);ttk.Button(t,text="Browse",command=self.pick_icon).grid(row=r,column=3,sticky="e",pady=4);r+=1
        infof=ttk.Frame(t); infof.grid(row=r,column=1,columnspan=3,sticky="ew",pady=(0,8)); infof.columnconfigure(1,weight=1)
        self.preview_label=ttk.Label(infof);self.preview_label.grid(row=0,column=0,rowspan=2,padx=(0,10))
        ttk.Label(infof,text="PNG inspection",font=("Segoe UI",10,"bold")).grid(row=0,column=1,sticky="w")
        ttk.Label(infof,textvariable=self.ov["png_info"],wraplength=650).grid(row=1,column=1,sticky="w")
        self.after(100,self.refresh_png_info);r+=1
        ttk.Label(t,text="Altitude (m)").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["alt"]).grid(row=r,column=1,sticky="ew",pady=4)
        ttk.Label(t,text="Altitude mode").grid(row=r,column=2,sticky="w",padx=(16,8),pady=4);ttk.Combobox(t,textvariable=self.ov["mode"],values=("relativeToGround","absolute","clampToGround"),state="readonly").grid(row=r,column=3,sticky="ew",pady=4);r+=1
        ttk.Label(t,text="Icon scale").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["scale"]).grid(row=r,column=1,sticky="ew",pady=4)
        ttk.Label(t,text="Popup").grid(row=r,column=2,sticky="w",padx=(16,8),pady=4);ttk.Combobox(t,textvariable=self.ov["popup"],values=("Info","None"),state="readonly").grid(row=r,column=3,sticky="ew",pady=4);r+=1
        flags=ttk.Frame(t);flags.grid(row=r,column=1,columnspan=3,sticky="w",pady=4);ttk.Checkbutton(flags,text="Show tether",variable=self.ov["tether"]).pack(side="left",padx=(0,18));ttk.Checkbutton(flags,text="Show label",variable=self.ov["label"]).pack(side="left");r+=1
        ttk.Label(t,text="Info text").grid(row=r,column=0,sticky="nw",padx=(0,8),pady=4);self.object_desc=tk.Text(t,height=2,wrap="word");self.object_desc.grid(row=r,column=1,columnspan=3,sticky="ew",pady=4);r+=1
        ttk.Label(t,text="Link text").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["link_text"]).grid(row=r,column=1,sticky="ew",pady=4)
        ttk.Label(t,text="URL").grid(row=r,column=2,sticky="w",padx=(16,8),pady=4);ttk.Entry(t,textvariable=self.ov["url"]).grid(row=r,column=3,sticky="ew",pady=4);r+=1
        ttk.Label(t,text="Output KMZ").grid(row=r,column=0,sticky="w",padx=(0,8),pady=4);ttk.Entry(t,textvariable=self.ov["out"]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=4);ttk.Button(t,text="Browse",command=self.pick_object_out).grid(row=r,column=3,sticky="e",pady=4);r+=1
        outf=ttk.Frame(t);outf.grid(row=r,column=0,columnspan=4,sticky="ew",pady=(8,12));outf.columnconfigure(0,weight=1);ttk.Button(outf,text="CREATE OBJECT KMZ",command=self.create_object).grid(row=0,column=0,sticky="e",ipadx=20,ipady=5)

    def on_preset(self,_evt=None):
        key=preset_key(self.ov["preset"].get());d=PRESET_DEFAULTS.get(key,PRESET_DEFAULTS["object"]);self.ov["icon"].set(str(preset_icon(key)));self.ov["alt"].set(f"{d['alt']:g}");self.ov["scale"].set(f"{d['scale']:g}");self.refresh_png_info()

    def pick_icon(self):
        p=filedialog.askopenfilename(filetypes=[("PNG image","*.png")]);
        if p:self.ov["icon"].set(p);self.refresh_png_info()

    def refresh_png_info(self):
        try:
            p=Path(self.ov["icon"].get());im=tk.PhotoImage(master=self,file=str(p));w,h=im.width(),im.height();size=p.stat().st_size
            factor=max(1,math.ceil(max(w,h)/MAX_ICON_DIM));ow=math.ceil(w/factor);oh=math.ceil(h/factor)
            status="Excellent" if max(w,h)<=256 else "Will normalize for KMZ"
            self.ov["png_info"].set(f"{p.name} — {w}×{h}px — {size/1024:.1f} KB — transparency preserved — {status}. Packaged copy ≈ {ow}×{oh}px; source untouched.")
            prev=im
            pf=max(1,math.ceil(max(w,h)/72));
            if pf>1:prev=im.subsample(pf,pf)
            self.preview_image=prev;self.preview_label.configure(image=prev)
        except Exception as e:
            self.ov["png_info"].set(f"PNG not ready: {e}");self.preview_label.configure(image="");self.preview_image=None

    def pick_object_out(self):
        p=filedialog.asksaveasfilename(defaultextension=".kmz",filetypes=[("KMZ","*.kmz")]);
        if p:self.ov["out"].set(p)

    def create_object(self):
        try:
            p=create_single_object_kmz(Path(self.ov["out"].get()),Path(self.ov["icon"].get()),self.ov["name"].get(),float(self.ov["lat"].get()),float(self.ov["lon"].get()),float(self.ov["alt"].get()),float(self.ov["scale"].get()),self.ov["mode"].get(),self.object_desc.get("1.0","end").strip(),self.ov["url"].get(),self.ov["link_text"].get(),self.ov["tether"].get(),self.ov["label"].get(),self.ov["popup"].get(),master=self)
            self.status.set(f"Created object: {p}")
            messagebox.showinfo(APP,f"Created:\n{p}\n\nOriginal PNG was not modified.")
        except Exception as e:messagebox.showerror(APP,str(e))

    def _build_batch_tab(self):
        t=self.batch_tab;t.columnconfigure(1,weight=1)
        here=app_dir();self.bv={"list":tk.StringVar(value=str(here/"sample_objects.txt")),"out":tk.StringVar(value=str(Path.home()/"Desktop"/"Object_Set.kmz")),"summary":tk.StringVar(value="Load a header-based list or simple shorthand list.")}
        ttk.Label(t,text="Batch Object Set",font=("Segoe UI",15,"bold")).grid(row=0,column=0,columnspan=3,sticky="w",pady=(0,8))
        ttk.Label(t,text="Simple shorthand: type,lat,lon[,alt_m][,name]   —   Full list supports icon, description, hyperlink, scale, tether, popup, and labels.",wraplength=850).grid(row=1,column=0,columnspan=3,sticky="w",pady=(0,12))
        ttk.Label(t,text="Object list").grid(row=2,column=0,sticky="w",padx=(0,8),pady=5);ttk.Entry(t,textvariable=self.bv["list"]).grid(row=2,column=1,sticky="ew",pady=5);ttk.Button(t,text="Browse",command=self.pick_batch_list).grid(row=2,column=2,padx=(8,0),pady=5)
        ttk.Button(t,text="VALIDATE LIST",command=self.validate_batch).grid(row=3,column=1,sticky="w",pady=(2,8));ttk.Label(t,textvariable=self.bv["summary"],wraplength=700).grid(row=4,column=1,columnspan=2,sticky="w",pady=(0,12))
        ttk.Label(t,text="Output KMZ").grid(row=5,column=0,sticky="w",padx=(0,8),pady=5);ttk.Entry(t,textvariable=self.bv["out"]).grid(row=5,column=1,sticky="ew",pady=5);ttk.Button(t,text="Browse",command=self.pick_batch_out).grid(row=5,column=2,padx=(8,0),pady=5)
        fmt=ttk.LabelFrame(t,text="Full header format",padding=10);fmt.grid(row=6,column=0,columnspan=3,sticky="nsew",pady=12);t.rowconfigure(6,weight=1);fmt.columnconfigure(0,weight=1)
        header="type|name|lat|lon|alt_m|icon|description|url|link_text|scale|altitude_mode|tether|popup|label"
        ttk.Label(fmt,text=header,font=("Consolas",9),wraplength=820).grid(row=0,column=0,sticky="w")
        ttk.Label(fmt,text="Blank icon = preset icon. Relative icon paths are resolved beside the list file. PNGs are normalized to <=256 px inside the KMZ; originals remain untouched.",wraplength=820).grid(row=1,column=0,sticky="w",pady=(8,0))
        f=ttk.Frame(t);f.grid(row=7,column=0,columnspan=3,sticky="ew",pady=(8,0));f.columnconfigure(0,weight=1);ttk.Button(f,text="CREATE OBJECT SET",command=self.create_batch).grid(row=0,column=0,sticky="e",ipadx=20,ipady=5)

    def pick_batch_list(self):
        p=filedialog.askopenfilename(filetypes=[("Object lists","*.txt *.csv"),("All files","*.*")]);
        if p:self.bv["list"].set(p);self.validate_batch()
    def pick_batch_out(self):
        p=filedialog.asksaveasfilename(defaultextension=".kmz",filetypes=[("KMZ","*.kmz")]);
        if p:self.bv["out"].set(p)
    def validate_batch(self):
        try:
            rows=parse_batch_rows(Path(self.bv["list"].get()));types={r['type'] for r in rows};self.bv["summary"].set(f"Valid: {len(rows)} objects. Presets/types: {', '.join(sorted(types)) or 'object'}.")
        except Exception as e:self.bv["summary"].set(f"Problem: {e}")
    def create_batch(self):
        try:
            p,n=create_batch_kmz(Path(self.bv["list"].get()),Path(self.bv["out"].get()),master=self);self.status.set(f"Created batch object set: {p} ({n} objects)")
            messagebox.showinfo(APP,f"Created {n} objects:\n{p}")
        except Exception as e:messagebox.showerror(APP,str(e))

    def _build_compass_tab(self):
        t=self.compass_tab;t.columnconfigure(1,weight=1)
        self.cv={"lat":tk.StringVar(value="30.385524823620624"),"lon":tk.StringVar(value="-81.93080672778036"),"radius":tk.StringVar(value="100"),"alt":tk.StringVar(value="20000"),"scale":tk.StringVar(value="6"),"out":tk.StringVar(value=str(Path.home()/"Desktop"/"Sky_Compass.kmz")),"coord_status":tk.StringVar(value="Center coordinates for N/E/S/W generation.")}
        ttk.Label(t,text="Sky Compass",font=("Segoe UI",15,"bold")).grid(row=0,column=0,columnspan=3,sticky="w",pady=(0,8));ttk.Label(t,text="Creates giant N/E/S/W PNG markers around a center point using the live-proven POF3 geometry.",wraplength=800).grid(row=1,column=0,columnspan=3,sticky="w",pady=(0,12))
        r=2
        for k,l in [("lat","Center latitude"),("lon","Center longitude")]:ttk.Label(t,text=l).grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.cv[k]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        self._coord_buttons(t,r,self.cv["lat"],self.cv["lon"],self.cv["coord_status"]);r+=1;ttk.Label(t,textvariable=self.cv["coord_status"],foreground="#555").grid(row=r,column=1,columnspan=2,sticky="w",pady=(0,8));r+=1
        for k,l in [("radius","Radius (km)"),("alt","Altitude AGL (m)"),("scale","Icon scale")]:ttk.Label(t,text=l).grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.cv[k]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        ttk.Label(t,text="Output KMZ").grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.cv["out"]).grid(row=r,column=1,sticky="ew",pady=5);ttk.Button(t,text="Browse",command=self.pick_compass_out).grid(row=r,column=2,padx=(8,0),pady=5);r+=1
        f=ttk.Frame(t);f.grid(row=r,column=0,columnspan=3,sticky="ew",pady=(12,0));f.columnconfigure(0,weight=1);ttk.Button(f,text="CREATE SKY COMPASS",command=self.create_compass).grid(row=0,column=0,sticky="e",ipadx=20,ipady=5)
    def pick_compass_out(self):
        p=filedialog.asksaveasfilename(defaultextension=".kmz",filetypes=[("KMZ","*.kmz")]);
        if p:self.cv["out"].set(p)
    def create_compass(self):
        try:
            p=create_sky_compass_kmz(Path(self.cv["out"].get()),float(self.cv["lat"].get()),float(self.cv["lon"].get()),float(self.cv["radius"].get()),float(self.cv["alt"].get()),float(self.cv["scale"].get()));self.status.set(f"Created Sky Compass: {p}")
            messagebox.showinfo(APP,f"Created:\n{p}")
        except Exception as e:messagebox.showerror(APP,str(e))

    def _build_beacon_tab(self):
        t=self.beacon_tab;t.columnconfigure(1,weight=1)
        self.ev={"name":tk.StringVar(value="EarthStick Beacon"),"lat":tk.StringVar(value="30.385524823620624"),"lon":tk.StringVar(value="-81.93080672778036"),"height":tk.StringVar(value="100"),"width":tk.StringVar(value="6"),"color":tk.StringVar(value="Red"),"out":tk.StringVar(value=str(Path.home()/"Desktop"/"EarthStick_Beacon.kml")),"coord_status":tk.StringVar(value="Accepted Beacon Maker behavior integrated here.")}
        ttk.Label(t,text="Earth Beacon",font=("Segoe UI",15,"bold")).grid(row=0,column=0,columnspan=3,sticky="w",pady=(0,8));ttk.Label(t,text="Accepted Earth Beacon geometry preserved: a long-range vertical KML destination marker.").grid(row=1,column=0,columnspan=3,sticky="w",pady=(0,12))
        r=2
        ttk.Label(t,text="Beacon name").grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.ev["name"]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        for k,l in [("lat","Latitude"),("lon","Longitude")]:ttk.Label(t,text=l).grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.ev[k]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        self._coord_buttons(t,r,self.ev["lat"],self.ev["lon"],self.ev["coord_status"]);r+=1;ttk.Label(t,textvariable=self.ev["coord_status"],foreground="#555").grid(row=r,column=1,columnspan=2,sticky="w",pady=(0,8));r+=1
        ttk.Label(t,text="Height (km)").grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.ev["height"]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        ttk.Label(t,text="Line width").grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.ev["width"]).grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        ttk.Label(t,text="Color").grid(row=r,column=0,sticky="w",pady=5);ttk.Combobox(t,textvariable=self.ev["color"],values=tuple(COLORS.keys()),state="readonly").grid(row=r,column=1,columnspan=2,sticky="ew",pady=5);r+=1
        ttk.Label(t,text="Output KML").grid(row=r,column=0,sticky="w",pady=5);ttk.Entry(t,textvariable=self.ev["out"]).grid(row=r,column=1,sticky="ew",pady=5);ttk.Button(t,text="Browse",command=self.pick_beacon_out).grid(row=r,column=2,padx=(8,0),pady=5);r+=1
        f=ttk.Frame(t);f.grid(row=r,column=0,columnspan=3,sticky="ew",pady=(12,0));f.columnconfigure(0,weight=1);ttk.Button(f,text="CREATE BEACON KML",command=self.create_beacon).grid(row=0,column=0,sticky="e",ipadx=20,ipady=5)
    def pick_beacon_out(self):
        p=filedialog.asksaveasfilename(defaultextension=".kml",filetypes=[("KML","*.kml")]);
        if p:self.ev["out"].set(p)
    def create_beacon(self):
        try:
            p=create_beacon_kml(Path(self.ev["out"].get()),self.ev["name"].get(),float(self.ev["lat"].get()),float(self.ev["lon"].get()),float(self.ev["height"].get()),float(self.ev["width"].get()),self.ev["color"].get());self.status.set(f"Created Beacon: {p}")
            messagebox.showinfo(APP,f"Created:\n{p}")
        except Exception as e:messagebox.showerror(APP,str(e))


def selftest():
    root = tk.Tk(); root.withdraw()
    here = app_dir()
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        # 1. Normalization: large and wide PNG; original untouched.
        large=tk.PhotoImage(master=root,width=900,height=300);large.put("#ff0000",to=(0,0,900,300));src=td/"wide.png";large.write(str(src),format="png");before=hashlib.sha256(src.read_bytes()).hexdigest();norm=td/"norm.png";ni=normalize_png(src,norm,master=root);after=hashlib.sha256(src.read_bytes()).hexdigest();assert before==after and max(ni["out_w"],ni["out_h"])<=256 and ni["out_w"]>ni["out_h"]
        # 2. Single object + hyperlink + hidden label.
        out1=td/"one.kmz";create_single_object_kmz(out1,preset_icon("helicopter"),"Test",30.1,-81.1,300,1.5,"relativeToGround","Desc","https://example.com","OPEN",False,False,"Info",master=root)
        with zipfile.ZipFile(out1) as z:
            k=z.read("doc.kml").decode();assert "https://example.com" in k and "<scale>0.0</scale>" in k and "icons/icon.png" in z.namelist()
        # 3. No-popup style emitted.
        outnp=td/"none.kmz";create_single_object_kmz(outnp,preset_icon("object"),"NoPopup",30.1,-81.1,100,1.4,"relativeToGround","","","",False,False,"None",master=root)
        with zipfile.ZipFile(outnp) as z: assert "<displayMode>hide</displayMode>" in z.read("doc.kml").decode()
        # 4. 100-object stress pack with duplicate icon reuse.
        lst=td/"stress.txt";lines=["type|name|lat|lon|alt_m|icon|description|url|link_text|scale|altitude_mode|tether|popup|label"]
        for i in range(100):lines.append(f"fuel|Fuel {i}|30.{100000+i}|-81.{200000+i}|150||Object {i}|||1.4|relativeToGround|no|Info|no")
        lst.write_text("\n".join(lines),encoding="utf-8");out2=td/"stress.kmz";_,n=create_batch_kmz(lst,out2,master=root);assert n==100
        with zipfile.ZipFile(out2) as z:
            names=z.namelist();assert names.count("doc.kml")==1 and len([x for x in names if x.startswith("icons/")])==1
        # 5. Shorthand parser.
        sh=td/"short.txt";sh.write_text("fuel,30.410104,-81.922396\nheli,30.39821,-81.93144,300,Helicopter 1\n",encoding="utf-8");assert len(parse_batch_rows(sh))==2
        # 6. Sky compass.
        comp=td/"comp.kmz";create_sky_compass_kmz(comp,30.3855,-81.9308,100,20000,6)
        with zipfile.ZipFile(comp) as z:
            k=z.read("doc.kml").decode();assert all(f"<name>{x}</name>" in k for x in "NESW")
        # 7. Beacon accepted geometry.
        b=td/"b.kml";create_beacon_kml(b,"Beacon",30.2,-81.2,100,6,"Red");text=b.read_text();assert "100000.000" in text and "relativeToGround" in text
    root.destroy()
    print("OBJECT FACTORY SELFTEST PASS")


def main():
    ap=argparse.ArgumentParser(add_help=False);ap.add_argument("--selftest",action="store_true");ap.add_argument("--smoke-test",action="store_true");ns,_=ap.parse_known_args()
    if ns.selftest:selftest();return
    ObjectFactory(smoke_test=ns.smoke_test).mainloop()

if __name__=="__main__":
    main()
