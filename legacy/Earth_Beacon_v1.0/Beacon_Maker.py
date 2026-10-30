#!/usr/bin/env python3
'''
EarthStick Beacon Maker 1.0

Creates a vertical KML beacon for ArcGIS Earth.
Coordinates can be entered manually, read from the Windows clipboard,
or read from the current ArcGIS Earth camera position.

Standard-library only.
'''

from __future__ import annotations

import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from xml.sax.saxutils import escape

VERSION = "1.0"
CAMERA_URL = "http://localhost:8000/arcgisearth/camera"
HTTP_TIMEOUT = 1.0

COLORS = {
    "Red": "ff0000ff",
    "Yellow": "ff00ffff",
    "Cyan": "ffffff00",
    "Green": "ff00ff00",
    "Magenta": "ffff00ff",
    "White": "ffffffff",
    "Orange": "ff0088ff",
}

FLOAT_RE = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)")


class CoordinateError(ValueError):
    pass


def validate_lat_lon(lat: float, lon: float) -> tuple[float, float]:
    if not (math.isfinite(lat) and math.isfinite(lon)):
        raise CoordinateError("Coordinates must be finite numbers.")
    if not -90.0 <= lat <= 90.0:
        raise CoordinateError("Latitude must be between -90 and 90.")
    if not -180.0 <= lon <= 180.0:
        raise CoordinateError("Longitude must be between -180 and 180.")
    return lat, lon


def parse_clipboard_coordinates(text: str, order: str = "Auto") -> tuple[float, float, str]:
    '''
    Returns (latitude, longitude, interpretation_message).

    Supported examples:
      30.123, -81.456
      -81.456 30.123
      Latitude: 30.123 Longitude: -81.456
      lat=30.123 lon=-81.456
    '''
    if not text or not text.strip():
        raise CoordinateError("The clipboard is empty.")

    source = text.strip()

    lat_match = re.search(
        r"\b(?:lat|latitude)\b\s*[:=]?\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        source,
        re.IGNORECASE,
    )
    lon_match = re.search(
        r"\b(?:lon|lng|long|longitude)\b\s*[:=]?\s*([-+]?(?:\d+(?:\.\d*)?|\.\d+))",
        source,
        re.IGNORECASE,
    )

    if lat_match and lon_match:
        lat = float(lat_match.group(1))
        lon = float(lon_match.group(1))
        validate_lat_lon(lat, lon)
        return lat, lon, "Clipboard labels identified latitude and longitude."

    numbers = [float(x) for x in FLOAT_RE.findall(source)]
    if len(numbers) < 2:
        raise CoordinateError("Could not find two decimal coordinates in the clipboard.")

    a, b = numbers[0], numbers[1]

    if order == "Lat, Lon":
        lat, lon = a, b
        validate_lat_lon(lat, lon)
        return lat, lon, "Clipboard interpreted as Latitude, Longitude."

    if order == "Lon, Lat":
        lon, lat = a, b
        validate_lat_lon(lat, lon)
        return lat, lon, "Clipboard interpreted as Longitude, Latitude."

    a_can_lat = -90.0 <= a <= 90.0
    b_can_lat = -90.0 <= b <= 90.0
    a_can_lon = -180.0 <= a <= 180.0
    b_can_lon = -180.0 <= b <= 180.0

    if not (a_can_lon and b_can_lon):
        raise CoordinateError("Clipboard coordinates are outside valid longitude range.")

    if not a_can_lat and b_can_lat:
        lon, lat = a, b
        validate_lat_lon(lat, lon)
        return lat, lon, "Auto-detected Longitude, Latitude by numeric range."

    if a_can_lat and not b_can_lat:
        lat, lon = a, b
        validate_lat_lon(lat, lon)
        return lat, lon, "Auto-detected Latitude, Longitude by numeric range."

    if a_can_lat and b_can_lat:
        lat, lon = a, b
        validate_lat_lon(lat, lon)
        return (
            lat,
            lon,
            "Ambiguous pair: interpreted as Latitude, Longitude. "
            "Verify the values or click Swap Lat/Lon.",
        )

    raise CoordinateError("Could not determine a valid latitude/longitude pair.")


def get_arcgis_camera_coordinates() -> tuple[float, float]:
    req = urllib.request.Request(
        CAMERA_URL,
        method="GET",
        headers={"Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as response:
            raw = response.read().decode("utf-8")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
        raise CoordinateError(f"Could not reach ArcGIS Earth Automation API: {exc}") from exc

    try:
        camera = json.loads(raw)
        pos = camera["position"]
        lon = float(pos["x"])
        lat = float(pos["y"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        raise CoordinateError(f"Unexpected ArcGIS Earth camera response: {exc}") from exc

    sr = pos.get("spatialReference") or {}
    wkid = sr.get("wkid")
    if wkid not in (None, 4326, "4326"):
        raise CoordinateError(f"ArcGIS Earth camera is not reporting WKID 4326 (reported {wkid}).")

    validate_lat_lon(lat, lon)
    return lat, lon


def build_kml(
    name: str,
    lat: float,
    lon: float,
    height_m: float,
    width: float,
    color_kml: str,
) -> str:
    validate_lat_lon(lat, lon)

    if not math.isfinite(height_m) or height_m <= 0:
        raise ValueError("Beacon height must be greater than zero.")
    if not math.isfinite(width) or width <= 0:
        raise ValueError("Line width must be greater than zero.")

    safe_name = escape(name.strip() or "EarthStick Beacon")

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>{safe_name}</name>
    <Style id="beaconStyle">
      <LineStyle>
        <color>{color_kml}</color>
        <width>{width:g}</width>
      </LineStyle>
      <IconStyle>
        <scale>1.1</scale>
      </IconStyle>
    </Style>
    <Placemark>
      <name>{safe_name}</name>
      <styleUrl>#beaconStyle</styleUrl>
      <MultiGeometry>
        <Point>
          <altitudeMode>relativeToGround</altitudeMode>
          <coordinates>{lon:.8f},{lat:.8f},0</coordinates>
        </Point>
        <LineString>
          <tessellate>0</tessellate>
          <altitudeMode>relativeToGround</altitudeMode>
          <coordinates>
            {lon:.8f},{lat:.8f},0
            {lon:.8f},{lat:.8f},{height_m:.3f}
          </coordinates>
        </LineString>
      </MultiGeometry>
    </Placemark>
  </Document>
</kml>
'''


class BeaconMaker(tk.Tk):
    def __init__(self, smoke_test: bool = False):
        super().__init__()
        self.title(f"EarthStick Beacon Maker {VERSION}")
        self.resizable(False, False)

        self.lat_var = tk.StringVar()
        self.lon_var = tk.StringVar()
        self.name_var = tk.StringVar(value="EarthStick Beacon")
        self.height_var = tk.StringVar(value="100")
        self.width_var = tk.StringVar(value="6")
        self.color_var = tk.StringVar(value="Red")
        self.order_var = tk.StringVar(value="Auto")
        self.open_var = tk.BooleanVar(value=True)
        self.status_var = tk.StringVar(value="Enter coordinates, use Clipboard, or read ArcGIS Earth.")

        self._build_ui()

        if smoke_test:
            self.after(600, self.destroy)

    def _build_ui(self):
        pad = {"padx": 8, "pady": 5}

        frame = ttk.Frame(self, padding=12)
        frame.grid(row=0, column=0, sticky="nsew")

        ttk.Label(frame, text="Beacon name").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.name_var, width=34).grid(
            row=0, column=1, columnspan=2, sticky="ew", **pad
        )

        ttk.Label(frame, text="Latitude").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.lat_var, width=22).grid(
            row=1, column=1, sticky="ew", **pad
        )

        ttk.Label(frame, text="Longitude").grid(row=2, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.lon_var, width=22).grid(
            row=2, column=1, sticky="ew", **pad
        )

        ttk.Button(frame, text="Swap Lat/Lon", command=self.swap_coordinates).grid(
            row=1, column=2, rowspan=2, sticky="nsew", **pad
        )

        source_box = ttk.LabelFrame(frame, text="Get coordinates")
        source_box.grid(row=3, column=0, columnspan=3, sticky="ew", padx=8, pady=8)

        ttk.Button(
            source_box, text="From Windows Clipboard", command=self.from_clipboard
        ).grid(row=0, column=0, padx=7, pady=7)

        ttk.Button(
            source_box, text="From ArcGIS Earth", command=self.from_arcgis
        ).grid(row=0, column=1, padx=7, pady=7)

        ttk.Label(source_box, text="Clipboard order").grid(
            row=1, column=0, sticky="e", padx=7, pady=5
        )
        ttk.Combobox(
            source_box,
            textvariable=self.order_var,
            values=("Auto", "Lat, Lon", "Lon, Lat"),
            state="readonly",
            width=12,
        ).grid(row=1, column=1, sticky="w", padx=7, pady=5)

        ttk.Separator(frame, orient="horizontal").grid(
            row=4, column=0, columnspan=3, sticky="ew", padx=8, pady=8
        )

        ttk.Label(frame, text="Height (km)").grid(row=5, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.height_var, width=14).grid(
            row=5, column=1, sticky="w", **pad
        )

        ttk.Label(frame, text="Line width").grid(row=6, column=0, sticky="w", **pad)
        ttk.Entry(frame, textvariable=self.width_var, width=14).grid(
            row=6, column=1, sticky="w", **pad
        )

        ttk.Label(frame, text="Color").grid(row=7, column=0, sticky="w", **pad)
        ttk.Combobox(
            frame,
            textvariable=self.color_var,
            values=tuple(COLORS.keys()),
            state="readonly",
            width=12,
        ).grid(row=7, column=1, sticky="w", **pad)

        ttk.Checkbutton(
            frame,
            text="Open KML after saving",
            variable=self.open_var,
        ).grid(row=8, column=0, columnspan=3, sticky="w", padx=8, pady=5)

        ttk.Button(
            frame,
            text="Create Beacon KML",
            command=self.create_beacon,
        ).grid(row=9, column=0, columnspan=3, sticky="ew", padx=8, pady=(10, 7), ipady=5)

        ttk.Label(
            frame,
            textvariable=self.status_var,
            wraplength=440,
            justify="left",
        ).grid(row=10, column=0, columnspan=3, sticky="w", padx=8, pady=(5, 2))

    def _set_coordinates(self, lat: float, lon: float):
        self.lat_var.set(f"{lat:.8f}".rstrip("0").rstrip("."))
        self.lon_var.set(f"{lon:.8f}".rstrip("0").rstrip("."))

    def swap_coordinates(self):
        lat = self.lat_var.get().strip()
        lon = self.lon_var.get().strip()
        self.lat_var.set(lon)
        self.lon_var.set(lat)
        self.status_var.set("Latitude and longitude fields swapped.")

    def from_clipboard(self):
        try:
            text = self.clipboard_get()
            lat, lon, message = parse_clipboard_coordinates(text, self.order_var.get())
            self._set_coordinates(lat, lon)
            self.status_var.set(message)
        except (tk.TclError, CoordinateError) as exc:
            messagebox.showerror("Clipboard coordinates", str(exc), parent=self)
            self.status_var.set(str(exc))

    def from_arcgis(self):
        try:
            lat, lon = get_arcgis_camera_coordinates()
            self._set_coordinates(lat, lon)
            self.status_var.set("Coordinates read from current ArcGIS Earth camera position.")
        except CoordinateError as exc:
            messagebox.showerror("ArcGIS Earth", str(exc), parent=self)
            self.status_var.set(str(exc))

    def create_beacon(self):
        try:
            lat = float(self.lat_var.get().strip())
            lon = float(self.lon_var.get().strip())
            validate_lat_lon(lat, lon)

            height_km = float(self.height_var.get().strip())
            width = float(self.width_var.get().strip())
            if not math.isfinite(height_km) or height_km <= 0:
                raise ValueError("Height must be greater than zero.")
            if not math.isfinite(width) or width <= 0:
                raise ValueError("Line width must be greater than zero.")

            kml = build_kml(
                name=self.name_var.get(),
                lat=lat,
                lon=lon,
                height_m=height_km * 1000.0,
                width=width,
                color_kml=COLORS[self.color_var.get()],
            )
        except (ValueError, CoordinateError) as exc:
            messagebox.showerror("Beacon values", str(exc), parent=self)
            return

        default_name = re.sub(
            r"[^A-Za-z0-9._-]+",
            "_",
            self.name_var.get().strip() or "EarthStick_Beacon",
        ).strip("_") or "EarthStick_Beacon"

        path = filedialog.asksaveasfilename(
            parent=self,
            title="Save beacon KML",
            defaultextension=".kml",
            initialfile=default_name + ".kml",
            filetypes=[("KML files", "*.kml"), ("All files", "*.*")],
        )
        if not path:
            return

        try:
            Path(path).write_text(kml, encoding="utf-8", newline="\n")
        except OSError as exc:
            messagebox.showerror("Save beacon", f"Could not save KML:\n{exc}", parent=self)
            return

        self.status_var.set(f"Beacon created: {path}")

        if self.open_var.get():
            try:
                if os.name == "nt":
                    os.startfile(path)  # type: ignore[attr-defined]
                else:
                    self.status_var.set(
                        f"Beacon created: {path} — automatic opening is Windows-only."
                    )
            except OSError as exc:
                messagebox.showwarning(
                    "Beacon saved",
                    f"The KML was saved, but Windows could not open it automatically:\n{exc}",
                    parent=self,
                )


def run_selftest() -> None:
    tests = [
        ("30.123,-81.456", "Auto", 30.123, -81.456),
        ("-120.5 35.2", "Auto", 35.2, -120.5),
        ("Latitude: 30.123 Longitude: -81.456", "Auto", 30.123, -81.456),
        ("30.123,-81.456", "Lat, Lon", 30.123, -81.456),
        ("-81.456,30.123", "Lon, Lat", 30.123, -81.456),
    ]
    for text, order, exp_lat, exp_lon in tests:
        lat, lon, _ = parse_clipboard_coordinates(text, order)
        assert abs(lat - exp_lat) < 1e-12
        assert abs(lon - exp_lon) < 1e-12

    kml = build_kml("Test Beacon", 30.0, -81.0, 100000.0, 6.0, COLORS["Red"])
    assert "-81.00000000,30.00000000,0" in kml
    assert "-81.00000000,30.00000000,100000.000" in kml
    assert "<color>ff0000ff</color>" in kml

    print("Beacon Maker self-test PASS")


def main():
    if "--selftest" in sys.argv:
        run_selftest()
        return

    smoke = "--smoke-test" in sys.argv
    app = BeaconMaker(smoke_test=smoke)
    app.mainloop()


if __name__ == "__main__":
    main()
