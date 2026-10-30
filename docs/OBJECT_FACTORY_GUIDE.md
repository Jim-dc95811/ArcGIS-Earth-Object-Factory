# ArcGIS Earth Object Factory v0.2 TEST — Quick Operator Guide

## Start

1. Extract the v0.2 TEST package.
2. Double-click `Run_Object_Factory.bat`.
3. Use one of the four main tabs: **Objects**, **Batch**, **Sky Compass**, or **Beacon**.

No third-party Python packages are required.

## Objects

Use this tab for one intentional object.

1. Enter Latitude and Longitude manually, or copy a coordinate pair and click **From Clipboard**.
2. Verify the displayed coordinate.
3. Choose a preset or custom PNG.
4. Set altitude / altitude mode / icon scale as needed.
5. Leave labels off unless you specifically want a permanent visible label.
6. Choose **Info** or **No Popup**.
7. Optionally add a URL and link text.
8. Create the KMZ.

### PNG handling

The source PNG is never modified.

For the KMZ working copy:
- maximum dimension is 256 px
- aspect ratio is preserved
- transparency is preserved
- smaller icons are not unnecessarily enlarged

## Batch

Use this tab to turn an object list into one KMZ.

### Simple shorthand

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

### Full format

```text
type|name|lat|lon|alt_m|icon|description|url|link_text|scale|altitude_mode|tether|popup|label
```

Built-in preset icons can be referenced by type. Custom PNG paths may also be used.

## Sky Compass

1. Enter/copy the center coordinate.
2. Choose radius, altitude, and icon scale.
3. Build the KMZ.
4. Add it to ArcGIS Earth.

The output places N/E/S/W markers around the operating center for horizon orientation.

## Beacon

1. Enter/copy the target coordinate.
2. Choose height, line width, and color.
3. Create the KML.
4. Add it to ArcGIS Earth.

A beacon is designed to remain visually obvious at long range in tilted/horizon view.

## Preferred coordinate workflow

1. Find the desired location in your map/source.
2. Copy the latitude/longitude pair.
3. Click **From Clipboard**.
4. Verify Latitude and Longitude.
5. Create the object.

The factory intentionally does not provide coordinate swapping or ArcGIS-camera pickup controls. Placement remains explicit.

## Popup note

ArcGIS Earth's native KML information box can be visually large. Keep Info content concise. Use No Popup for purely visual objects.

## Link note

An Info object can include a standard hyperlink. This is useful for camera/viewpoint objects, Street View, agency pages, training resources, weather pages, and other external information.

## Self-test

From a command prompt in the extracted folder:

```text
py -3 Object_Factory_v0.2_TEST.py --selftest
```

The self-test checks PNG normalization, original preservation, single objects, hyperlinks, no-popup KML, a 100-object batch, duplicate icon reuse, shorthand parsing, Sky Compass generation, and Beacon generation.
