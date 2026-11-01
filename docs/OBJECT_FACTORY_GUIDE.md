# ArcGIS Earth Object Factory v1.1 - Quick Operator Guide

## Start

1. Download and extract [`ArcGIS_Earth_Object_Factory_v1.1.zip`](../releases/ArcGIS_Earth_Object_Factory_v1.1.zip).
2. Double-click `Run_Object_Factory.bat`.
3. Use **Objects**, **Batch**, **Sky Compass**, or **Beacon**.

No third-party Python packages are required.

For the full guide, use the **[v1.1 User Manual](OBJECT_FACTORY_USER_MANUAL.md)** ([PDF](ArcGIS_Earth_Object_Factory_v1.1_User_Manual.pdf)).

## Objects

1. Enter Latitude and Longitude manually, or right-click the spot in Google Maps, click the coordinate to copy it, and click **From Clipboard**.
2. Check the `Read as Latitude ... Longitude ...` line under the button.
3. Choose a preset or custom PNG.
4. Set altitude / altitude mode / icon scale if needed.
5. Leave labels off unless you intentionally want a permanent label.
6. Choose **Info** or **None** for the popup.
7. Enter optional multiline **Info text**.
8. Optionally add Link text and a URL.
9. Press **CREATE OBJECT KMZ**. If the file already exists, the factory asks before replacing it.

Built-in presets:

`object, helicopter, fuel, bird, hazard, home, staging, water, firetruck, camera, medical`

### PNG handling

The source PNG is never modified.

For the KMZ working copy:
- maximum dimension is 256 px
- aspect ratio is preserved
- transparency is preserved
- smaller icons are not unnecessarily enlarged

## Batch

Simple shorthand:

```text
fuel,30.410104,-81.922396
helicopter,30.398210,-81.931440,300
bird,30.402778,-81.918620,120,Mystery Bird
home,30.385525,-81.930807
```

Format:

```text
type,lat,lon[,alt_m][,name]
```

Then press **VALIDATE LIST** and **CREATE OBJECT SET**.

Full format:

```text
type|name|lat|lon|alt_m|icon|description|url|link_text|scale|altitude_mode|tether|popup|label
```

## Sky Compass

1. Enter/copy the center coordinate.
2. Choose radius, altitude, and icon scale.
3. Press **CREATE SKY COMPASS**.
4. Add it to ArcGIS Earth.

## Beacon

1. Enter a beacon name and enter/copy the target coordinate.
2. Choose height, line width, and color.
3. Press **CREATE BEACON KML**.
4. Add it to ArcGIS Earth.

## Popup note

ArcGIS Earth's native KML information box can be visually large. Keep Info content concise. Use `Popup = None` for purely visual objects.

## Self-test

```text
py -3 Object_Factory_v1.1.py --selftest
```

The self-test checks PNG normalization, original preservation, single objects, hyperlinks, no-popup KML, a 100-object batch, duplicate icon reuse, shorthand parsing, Sky Compass generation, and Beacon generation.
