# Earth Beacon

**Turn any coordinate into a horizon-visible 3D beacon for ArcGIS Earth.**

A normal map pin is useful when you are close to it. From far away, it disappears into the map.

Earth Beacon creates a vertical KML pillar at the target coordinate so the location remains visually obvious from great distance.

> **A pin marks a place. A beacon gives you something to aim at.**

![Earth Beacon live in ArcGIS Earth](assets/Earth_Beacon_ArcGIS_Earth.jpg)

The screenshot above is a live ArcGIS Earth test with the eye at roughly **102 km altitude**. The red beacon remains clearly visible on the horizon.

## What it does

Beacon Maker v1.0 creates a standard KML file containing:

- a geographic point at the target location
- a vertical `LineString` rising from that point
- configurable beacon height
- configurable line width
- selectable beacon color
- a visible label at the target

The resulting `.kml` can be opened directly in ArcGIS Earth.

Earth Beacon does not modify ArcGIS Earth. It simply generates a small KML overlay using standard KML 3D geometry.

## Coordinate sources

You can create a beacon from:

1. **Manual latitude / longitude entry**
2. **Windows clipboard**
3. **The current ArcGIS Earth camera coordinates** through the local Automation API

Clipboard examples accepted by v1.0 include:

```text
30.123, -81.456
-81.456 30.123
Latitude: 30.123 Longitude: -81.456
lat=30.123 lon=-81.456
```

When an unlabeled pair is geographically ambiguous, Beacon Maker tells you how it interpreted the numbers and provides a **Swap Lat/Lon** button instead of silently pretending certainty.

## Default beacon

The default v1.0 beacon is:

- **100 km tall**
- **red**
- **line width 6**
- KML altitude mode: `relativeToGround`

Available colors include red, yellow, cyan, green, magenta, white, and orange.

## Download

The official tested package is:

[`releases/Beacon_Maker_v1.0.zip`](releases/Beacon_Maker_v1.0.zip)

SHA-256:

```text
d53559ac33b84c148f97e14094a6a6f8249583ea068f1606ecf1add7f4b68535
```

The ZIP contains exactly:

- `Beacon_Maker.py`
- `Beacon_Maker.bat`
- `README.txt`

No third-party Python packages are required.

## Quick start

1. Install Python 3 on Windows.
2. Extract `Beacon_Maker_v1.0.zip`.
3. Double-click `Beacon_Maker.bat`.
4. Enter coordinates, copy coordinates to the Windows clipboard, or use **From ArcGIS Earth**.
5. Choose the beacon height, width, and color.
6. Click **Create Beacon KML**.
7. Save the `.kml` file.
8. If **Open KML after saving** is checked, Windows will open it using the associated KML application.

For ArcGIS Earth camera pickup, enable the **Automation API** in ArcGIS Earth. Beacon Maker uses the default local endpoint:

```text
http://localhost:8000/arcgisearth/camera
```

## Why this is useful

Earth Beacon is deliberately simple. Its purpose is long-range visual orientation.

Possible uses include:

- destination beacon
- incident location
- staging area
- landing-zone reference
- home base
- parcel or tract target
- route checkpoint
- any location that must remain visually obvious while navigating the globe

The beacon can be especially useful in a tilted 3D view where an ordinary point marker may be hidden by distance, terrain, or visual clutter.

## EarthStick companion use

Earth Beacon works independently, but it pairs naturally with [EarthStick](https://github.com/Jim-dc95811/EarthStick).

EarthStick makes the ArcGIS Earth camera directly flyable with a joystick. Earth Beacon gives that flyable map a long-range visual destination:

> **Drop a beacon anywhere on Earth, then fly the real map toward it.**

The two projects remain intentionally separate utilities.

## How it works

The core KML geometry is intentionally uncomplicated. The base and top vertices use the same longitude and latitude, while the top vertex has a large altitude value:

```xml
<LineString>
  <altitudeMode>relativeToGround</altitudeMode>
  <coordinates>
    -81.00000000,30.00000000,0
    -81.00000000,30.00000000,100000
  </coordinates>
</LineString>
```

That creates a geographic vertical line extending upward from the target.

This is standard KML geometry. Earth Beacon's value is turning that geometry into a fast operational beacon workflow.

## Verified status

**Beacon Maker v1.0 is live-verified in ArcGIS Earth.**

Verified behavior:

- GUI launches on Windows
- KML beacon is generated
- generated beacon loads in ArcGIS Earth
- vertical red pillar renders correctly
- label/base point render correctly
- beacon remains visible from long range in tilted 3D view
- clipboard parser self-test passes
- KML generation self-test passes

The v1.0 source and release package are the accepted baseline for this repository.

## Repository map

- `Beacon_Maker.py` — Beacon Maker v1.0
- `Beacon_Maker.bat` — Windows launcher
- `releases/Beacon_Maker_v1.0.zip` — official tested package
- `assets/Earth_Beacon_ArcGIS_Earth.jpg` — live ArcGIS Earth proof screenshot
- `docs/USER_GUIDE.md` — operating guide
- `docs/TECHNICAL_NOTES.md` — KML/API implementation notes
- `CHANGELOG.md` — release record
- `CONTINUITY.md` — accepted project state and modification rules
- `LICENSE` — MIT License

## Scope

Earth Beacon is a visual map-navigation aid. It is not a certified aviation, maritime, surveying, dispatch, or safety-of-life navigation system.

## License

MIT License. See [`LICENSE`](LICENSE).
