# ArcGIS Earth Object Factory v1.1 - change document

**Released:** 2026-10-31
**Type:** hardening release. Coordinate reading, file safety, batch-list checks and packaging.
**Download:** [`releases/ArcGIS_Earth_Object_Factory_v1.1.zip`](../releases/ArcGIS_Earth_Object_Factory_v1.1.zip) - **Source:** [`source/Object_Factory_v1.1.py`](../source/Object_Factory_v1.1.py)

**What it makes is unchanged.** Objects, batch object sets, the Sky Compass and Earth Beacons are generated exactly as in v1.0. So are PNG normalization (original never modified, packaged copy no larger than 256 px), the 11 presets, popup and label behavior, links, tethers, and the Sky Compass and Beacon geometry.

## What changed

### 1. From Clipboard reads coordinates correctly and says how it read them

**v1.0:** N/S/E/W letters were ignored and degrees-minutes-seconds were misread:

| Clipboard text | v1.0 result | v1.1 result |
|---|---|---|
| `30.4009768, -81.9347098` (Google Maps right-click) | correct | correct (unchanged) |
| `30.4009768°N 81.9347098°W` | longitude +81.93 (Tibet) | correct |
| `30°24'03.5"N 81°56'05.0"W` | lat 30, lon 24 (Libya) | correct |
| `Pin 1: 30.40, -81.93` | lat 1, lon 30.40 | rejected: copy just the coordinate pair |

The "Ambiguous pair... verify" warning also appeared for every normal Florida coordinate, so it was easy to ignore.

**v1.1:**
- N/S/E/W letters before or after the number, and degrees-minutes-seconds, are understood. Contradictions such as two latitudes, minutes of 60 or more, or a sign that disagrees with its letter are rejected with a plain reason.
- The line under the button states exactly what was read, e.g. `Read as Latitude 30.400977 N, Longitude 81.934710 W (latitude first, the Google Maps order). Check before creating.`
- The Google Maps right-click copy is the reference format.

### 2. Asks before replacing an existing file

Each tab offers a fixed default output on the Desktop (`Object_Set.kmz`, `Sky_Compass.kmz`, and so on).

**v1.0** silently replaced the earlier file each time. **v1.1** asks `... already exists. Replace it?` and defaults to No.

### 3. A failed build keeps the previous file

**v1.0** wrote straight into the output file. A failure part-way destroyed the previous file and left a broken one: with the `W.png` icon missing, a Sky Compass KMZ came out holding only N, E and S.

**v1.1** builds every output as `<name>.partial` and replaces the real file only when the build succeeds. The Sky Compass also checks for its four letter icons first and names any that are missing.

### 4. Batch lists: header detection fixed

**v1.0** treated a shorthand list as a header-style list whenever its first line contained the letters "lat" and "lon" anywhere. A first object named `Palatka Colony Staging` failed with `Line 2: latitude and longitude are required.`

**v1.1** recognizes a header only when `lat` and `lon` are actual column names.

### 5. Batch errors name the line

**v1.0:** `could not convert string to float: '30.4O'`.

**v1.1:** `Line 4: latitude '30.4O' is not a number.` Header-style lists also give the object name, e.g. `Line 3 (B): ...`. Line numbers count every line in the file, including comments and blank lines, so they match what you see in Notepad. An invalid `altitude_mode` is now reported with its line when the list is read.

### 6. Proper release package

**v1.0** was published as `ArcGIS_Earth_Object_Factory_v0.2.2_TEST.zip`. That package contained the TEST-named program, which showed "0.2.2 TEST", a TEST checklist and leftover `__pycache__` files.

**v1.1** ships as `ArcGIS_Earth_Object_Factory_v1.1.zip` with a clean `Object_Factory_v1.1` folder:
- `Object_Factory_v1.1.py` and `Run_Object_Factory.bat`
- the icons, the sample lists and outputs
- a `README.txt` written for this release

The source is also published at `source/Object_Factory_v1.1.py`.

### Also

- The unused ArcGIS Earth camera-coordinate code, left behind when its buttons were removed in v0.2, was deleted. Clipboard coordinates from Google Maps are the intended method.
- The built-in self-test gained checks for the new clipboard reader, header detection, line numbers and safe output.

## Verification

- **Live acceptance:** Jim Gaddy built objects with the v1.1 test package, including a new Earth Beacon ("Bald beacon") and a Sky Compass, and confirmed them working in ArcGIS Earth on 2026-10-31.
- **Output regression (25 checks, all passed):**
  - batch sets (both sample lists and a 100-object list covering every altitude mode, popup, tether and label combination), single objects in all three altitude modes with Info and No Popup, the Sky Compass, and Beacons in all 7 colors were byte-identical to v1.0;
  - failure cases (missing compass icon, missing batch icon, disk full while writing) kept the previous file;
  - the "Palatka Colony" list was read correctly;
  - batch errors named the right line.
- **Clipboard reader:** 20 formats checked, including Google Maps pairs, N/S/E/W in either position, degrees-minutes-seconds, and southern/eastern hemispheres.
- **Not run on Windows:** the extended `--selftest`. Tkinter could not be installed in the test environment, so the GUI and PNG normalization were exercised only by Jim's live use.

## Checksums

| File | SHA-256 |
|---|---|
| `Object_Factory_v1.1.py` | `f94a2034a9e3348d81a2a2061619201fd795d36930c2b64797ebb2611f5b6b70` |
| `ArcGIS_Earth_Object_Factory_v1.1.zip` | `927ed4bf589395708a171784503ca8338380c1746860200c4a4bd2db12f0608b` |
| v1.0 `Object_Factory_v1.0.py` (commit `b65a54c`) | `e77e1866e7a87b9824ed6bb1cd0f830f52adb1a2872efe48ede13a581018aa00` |

The v0.2.2 TEST zip that carried v1.0 remains in the repository history. The v1.0 PDF User Manual still describes the workflow; this document lists what v1.1 adds.
