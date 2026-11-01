# ArcGIS Earth Object Factory v1.1 - User Manual

> **v1.1 (2026-10-31):** file names below are updated for v1.1. New behavior: From Clipboard understands N/S/E/W letters and degrees-minutes-seconds and states how it read the coordinate; the factory asks before replacing a file, keeps the previous file if a build fails, and names the line of any batch-list problem. See [OBJECT_FACTORY_V1.1_CHANGES.md](OBJECT_FACTORY_V1.1_CHANGES.md).

A printable copy of this manual is available as [ArcGIS_Earth_Object_Factory_v1.1_User_Manual.pdf](ArcGIS_Earth_Object_Factory_v1.1_User_Manual.pdf).

Create geographic objects without hand-writing KML.

**Coordinates + PNG -> Object Factory -> KMZ/KML -> ArcGIS Earth**

v1.0 was commissioned on October 29, 2026. Airborne PNG objects, batch object sets, the N/E/S/W Sky Compass and the Beacon were live-proven in ArcGIS Earth. v1.1 (October 31, 2026) is a hardening release: everything it creates is identical to v1.0.

> **Core PNG rule:** the original PNG is never modified. Packaged icon copies are normalized to a maximum dimension of 256 px while preserving aspect ratio and transparency.

---

## 1. Quick Start

Object Factory is a Windows Python/Tkinter application. Normal use does not require ArcGIS Pro, QGIS, Pillow, or other third-party Python packages.

### What you need

- Windows with Python 3 installed, including Tkinter.
- ArcGIS Earth desktop to view the generated KML/KMZ files.
- PNG images only when you want custom icons. Preset icons are included.

### Start the factory

1. Download [`ArcGIS_Earth_Object_Factory_v1.1.zip`](../releases/ArcGIS_Earth_Object_Factory_v1.1.zip) and extract it to a normal folder. It contains an `Object_Factory_v1.1` folder.
2. Keep `Object_Factory_v1.1.py`, `Run_Object_Factory.bat`, and the `icons` folder together.
3. Double-click `Run_Object_Factory.bat`.
4. Choose **Objects**, **Batch**, **Sky Compass**, or **Beacon**.
5. Create the output and open the resulting KML/KMZ in ArcGIS Earth.

### Fastest first test

Open **Objects**, choose the **firetruck** preset, enter a known coordinate, leave labels off, add short Info text, press **CREATE OBJECT KMZ**, and open the KMZ (saved to your Desktop by default) in ArcGIS Earth. This mirrors the live-proven first Object Factory primitive.

### Main package files

- `Object_Factory_v1.1.py` - main application.
- `Run_Object_Factory.bat` - Windows launcher.
- `icons/` - 11 object presets plus N/E/S/W compass PNGs.
- `sample_objects.txt` - full-format batch example.
- `simple_objects.txt` - shorthand batch example.
- `SAMPLE_Object_Set.kmz`, `SAMPLE_Linked_Camera.kmz`, `SAMPLE_Sky_Compass.kmz`, `SAMPLE_Beacon.kml` - ready-made outputs to open in ArcGIS Earth.
- `README.txt` - quick start and release summary.

Every output path has a **Browse** button. By default, files are saved to your Desktop.

---

## 2. Main Window and Coordinate Entry

The factory uses one object-generation engine behind four task tabs: **Objects**, **Batch**, **Sky Compass** and **Beacon**. A status line at the bottom reports what the factory just did.

### Coordinate entry

**Manual** - type decimal latitude and longitude directly.

**From Clipboard** - reads coordinates copied from Google Maps or other text. Google Maps' `30.40098, -81.93471` (latitude first) is the reference format. N/S/E/W letters (`30.4009768°N 81.9347098°W`) and degrees-minutes-seconds (`30°24'03.5"N 81°56'05.0"W`) are also understood. The line under the button states exactly what was read, e.g. `Read as Latitude 30.400980 N, Longitude 81.934710 W`.

### Google Maps workflow

1. Right-click a location in Google Maps.
2. Click the coordinate pair to copy it.
3. Return to Object Factory and press **From Clipboard**.
4. Check the `Read as Latitude ... Longitude ...` line.
5. Create the object.

Latitude must be between -90 and 90. Longitude must be between -180 and 180. The factory validates these ranges before output is built.

---

## 3. Objects Tab - Create One Geographic Object

Use **Objects** for one floating or ground-level PNG object. The factory creates one KMZ containing the KML and the normalized icon copy.

### Typical workflow

1. Choose a preset or **Browse** to your own PNG. The PNG inspection box shows its size and what will be packaged.
2. Enter the object name and coordinate.
3. Set altitude, altitude mode, and icon scale.
4. Normally leave **Show label** off.
5. Turn on **Show tether** only when you want a visible line to the ground.
6. Choose **Info** or **None** for popup behavior.
7. Enter optional Info text and hyperlink.
8. Choose the output KMZ path (default `ArcGIS_Earth_Object.kmz` on your Desktop). If the file already exists, the factory asks before replacing it.
9. Press **CREATE OBJECT KMZ**.

### Field reference

- **Preset** - loads a built-in icon and starting altitude/scale. All fields remain editable.
- **Object name** - KML Placemark name.
- **Latitude / Longitude** - geographic anchor point.
- **PNG icon** - preset or custom transparent PNG. Source is never modified.
- **Altitude (m)** - altitude value in meters.
- **Altitude mode** - `relativeToGround`, `absolute`, or `clampToGround`.
- **Icon scale** - KML icon scale.
- **Popup** - `Info` or `None`.
- **Show tether** - adds a vertical line from ground to the object.
- **Show label** - continuously displays the object name. Default is off.
- **Info text** - short text shown after clicking.
- **Link text / URL** - optional standard hyperlink in the KML information.
- **Output KMZ** - output path.

---

## 4. PNG Handling, Altitude, Labels, and Links

### Automatic PNG normalization

When you select a PNG, the factory inspects its dimensions and packaged size. Oversized source images are reduced for the KMZ. Smaller clean icons are not needlessly enlarged.

Locked behavior:

- Maximum packaged dimension: **256 px**.
- Aspect ratio is preserved.
- Transparency is preserved.
- The source PNG remains byte-for-byte untouched.
- A wide helicopter stays wide; a tall object stays tall.
- A clean 128 x 128 icon may remain 128 x 128.
- Batch mode reuses a normalized icon rather than packing duplicate copies unnecessarily.

### Altitude modes

- **relativeToGround** - altitude above terrain. Normal choice for floating icons and sky objects.
- **absolute** - absolute elevation. Use only when intentional.
- **clampToGround** - places the object on the ground surface.

### Labels and click information

The project default is **no permanent label** for most objects. The icon carries the first layer of meaning; click only when more information is needed.

> **See it -> recognize it -> click it -> understand it.**

### Hyperlinks

Enter link text such as `OPEN LIVE CAMERA`, `STREET VIEW`, `FACILITY PAGE`, or `OPEN MAP`, then enter a normal URL. The factory writes a standard HTML hyperlink into the KML description.

The factory writes the link structure; browser-launch behavior depends on ArcGIS Earth and Windows/browser configuration.

---

## 5. Preset Library

Presets are convenience starting points. Every preset feeds the same generic PNG-object engine.

| Preset | Default altitude | Scale | Typical meaning |
|---|---:|---:|---|
| object | 150 m | 1.4 | generic object / pin |
| helicopter | 300 m | 1.5 | aviation marker |
| fuel | 150 m | 1.4 | fuel stop |
| bird | 120 m | 1.4 | lesson / wildlife object |
| hazard | 200 m | 1.5 | warning / hazard |
| home | 200 m | 1.5 | home / base |
| staging | 150 m | 1.5 | staging point |
| water | 150 m | 1.5 | water source |
| firetruck | 150 m | 1.5 | apparatus / fire-service point |
| camera | 180 m | 1.5 | viewpoint / camera |
| medical | 180 m | 1.5 | hospital / medical point |

In batch lists, these alternative names also work: `pin` (object), `heli` (helicopter), `gas` / `gas_pump` (fuel), `warning` (hazard), `base` (home), `truck` (firetruck), `viewpoint` (camera), `hospital` (medical). An unrecognized type becomes a generic `object`.

---

## 6. Batch Tab

Use **Batch** to create many objects in one KMZ. This is the fastest path for classrooms, training scenarios, operational object packs, or any repeated coordinate list.

### Batch workflow

1. **Browse** to the object list (a `.txt` file). The default is the included `sample_objects.txt`.
2. Press **VALIDATE LIST**. The summary line reports how many objects were read, or names the line with a problem.
3. Choose the output KMZ (default `Object_Set.kmz` on your Desktop).
4. Press **CREATE OBJECT SET**.

Two list formats are supported:

### Shorthand format

```text
type,lat,lon[,alt_m][,name]
```

```text
fuel,30.410104,-81.922396
heli,30.398210,-81.931440,300
bird,30.402778,-81.918620,120,Mystery Bird
home,30.385525,-81.930807
```

The preset supplies icon, normal altitude, and scale when omitted. Without a name, the object is named after its type.

### Full pipe-delimited format

```text
type|name|lat|lon|alt_m|icon|description|url|link_text|scale|altitude_mode|tether|popup|label
fuel|Fuel Stop|30.410104|-81.922396|150||Use this fuel stop.|||1.4|relativeToGround|no|Info|no
camera|Viewpoint|30.394120|-81.927300|180||Another way to see this place.|https://www.google.com/maps|OPEN MAP|1.5|relativeToGround|no|Info|no
```

Blank lines and lines beginning with `#` may be used for readability and are ignored.

The integrated self-test generated a **100-object batch KMZ** and verified duplicate-icon reuse.

---

## 7. Full Batch Field Reference

- `type` - preset name or alias.
- `name` - object name.
- `lat` / `lon` - coordinate.
- `alt_m` - altitude in meters.
- `icon` - optional custom PNG path. Blank uses the preset icon; a relative path is looked up beside the list file.
- `description` - Info text.
- `url` - optional URL.
- `link_text` - hyperlink text.
- `scale` - KML icon scale.
- `altitude_mode` - `relativeToGround`, `absolute`, or `clampToGround`.
- `tether` - yes/no, true/false, 1/0, on/off.
- `popup` - `Info` or `None`.
- `label` - yes/no. Normally no.

Use `sample_objects.txt` for the full format and `simple_objects.txt` for the shorthand format.

---

## 8. Sky Compass

Sky Compass creates four giant geographic PNG markers - **N, E, S, W** - around a center point. It was designed for EarthStick horizon flight, where the letters act as persistent orientation landmarks in the sky.

Default starting values:

- Radius: **100 km**.
- Altitude AGL: **20,000 m**.
- Icon scale: **6**.
- Output: one `Sky_Compass.kmz` containing all four markers.

### Create a Sky Compass

1. Set the center manually or with **From Clipboard**.
2. Set the radius.
3. Set altitude AGL.
4. Set icon scale.
5. Choose the output KMZ (default `Sky_Compass.kmz` on your Desktop).
6. Press **CREATE SKY COMPASS** and open the KMZ in ArcGIS Earth.

The POF3 N/E/S/W geometry was live-tested successfully. Radius, altitude, and scale remain adjustable because the best values depend on the operating area and preferred view.

> **Sky Compass = orientation. Earth Beacon = destination. EarthStick = movement.**

---

## 9. Beacon Tab

Beacon preserves the accepted Earth Beacon geometry: a tall vertical KML line anchored to a geographic point so the destination remains visible from long range in an oblique/horizon view.

### Standard starting values

- Height: **100 km**.
- Line width: **6**.
- Default color: **Red**.
- Available colors: Red, Yellow, Cyan, Green, Magenta, White, Orange.
- Beacon name: **EarthStick Beacon** (shown as the label at the base).
- Output: KML (default `EarthStick_Beacon.kml` on your Desktop).

### Standard workflow

1. Enter a beacon name and the destination coordinate, manually or with **From Clipboard**.
2. Keep 100 km height and width 6 for the accepted baseline unless you intentionally want another presentation.
3. Choose color.
4. Press **CREATE BEACON KML**.
5. Open the KML in ArcGIS Earth.

Earth Beacon geometry is already live-tested and accepted. The Factory tab preserves it rather than redesigning it.

---

## 10. Using Factory Output in ArcGIS Earth

- KMZ/KML objects appear under **My Data**.
- Toggle the whole layer on/off from the Data panel.
- Most factory objects are intended to show an icon without a permanent label.
- Click an **Info** object to open its information.
- Objects with links expose the hyperlink through KML information content.
- ArcGIS Earth can edit KML object information after creation through object Properties / Info.

A generated object is therefore not locked. You can edit its Rich Text or HTML information in ArcGIS Earth without rebuilding the foundation map.

> **Offline object = useful by itself. Connected object = potentially unlimited extension.**

### Camera / Viewpoint objects

A camera object is a geographic camera PNG plus an optional link. It can point to a live webcam, Street View, photo page, video, or normal web resource. A separate always-on-top mini Camera Viewer is a future concept and is **not** part of the factory.

### Native popup size

ArcGIS Earth presents KML information in a relatively large native panel. This is viewer behavior. Keep Info text concise or choose `Popup = None` for purely visual objects.

---

## 11. Troubleshooting and Verification

### Factory does not start

Confirm Python 3 is installed and includes Tkinter. Run the BAT from the extracted folder so the `icons` folder remains beside the Python script.

### PNG not ready

Confirm the file is a readable PNG. The factory intentionally does not require Pillow and does not accept other icon formats.

### Object too small or large

Adjust **Icon scale** and recreate the KMZ.

### Object too high or low

Check **Altitude** and **Altitude mode**. `relativeToGround` is the normal floating-object setting.

### Large popup

Use concise Info text or `Popup = None`. Popup size is an ArcGIS Earth presentation behavior.

### Batch validation problem

The message names the line (and, for header lists, the object), e.g. `Line 4: latitude '30.4O' is not a number.` Line numbers count every line in the file, including comments and blank lines. Also check the delimiter, header spelling (`lat` and `lon` columns), icon paths, and that shorthand lines contain at least type, latitude, and longitude.

### Clipboard coordinates not accepted

The message explains why. Copy just one coordinate pair; extra numbers such as `Pin 1:` are rejected. If necessary, enter the coordinate manually.

### Operational verification checklist

1. Create a known firetruck and confirm placement, Info text, and click behavior.
2. Select an oversized PNG and verify the source remains unchanged.
3. Create an object with a harmless URL and confirm the link appears.
4. Choose `Popup = None` and inspect the result.
5. Load `sample_objects.txt` and inspect mixed objects.
6. Load `simple_objects.txt` and inspect the shorthand objects.
7. Recreate the Sky Compass and inspect N/E/S/W behavior.
8. Create a standard 100 km red Beacon and confirm accepted geometry remains unchanged.

### Developer self-test

```text
py -3 Object_Factory_v1.1.py --selftest
```

The self-test covers PNG normalization/original preservation, single-object KMZ creation, hyperlink output, no-popup KML style, a 100-object batch, duplicate-icon reuse, shorthand parsing, Sky Compass generation, and Beacon generation.

> **Release rule:** Object Factory v1.1 is the stable accepted baseline. Future functional changes receive a new version and should preserve known-good behavior unless the change specifically targets it.

---

## 12. Operating Philosophy

Object Factory is deliberately not a GIS editor. It is a simple object-authoring bridge into ArcGIS Earth.

> **Find a place -> copy coordinates -> choose an object -> create it -> open ArcGIS Earth.**

Project rules:

- Foundation maps stay stable; small information layers change.
- The icon carries the first layer of meaning.
- Most objects stay unlabeled until clicked.
- Original PNGs are never modified.
- Offline capability comes first; online links add an optional second layer.
- Presets simplify common tasks, but all presets use the same generic object engine.
- The sky is a programmable information layer, not empty background.

> **See it -> recognize it -> click it -> understand it.**

> **The world is already built. We just add the objects.**

---

## Related Project Family

Object Factory is part of **ArcGIS Earth Unlocked**:

https://github.com/Jim-dc95811/ArcGIS-Earth-Unlocked

The umbrella connects the offline-map foundation, EarthStick navigation, Object Factory authoring, PointLayer public point data, and Parcel100 parcel intelligence while keeping each specialized tool independent.
