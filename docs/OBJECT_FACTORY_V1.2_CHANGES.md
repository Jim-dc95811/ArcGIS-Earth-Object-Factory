# ArcGIS Earth Object Factory v1.2 - change document

**Released:** 2026-11-02
**Type:** feature release (Jim's request): Hide above, altitude in feet, popup never blank, roomier layout.
**Download:** [`releases/ArcGIS_Earth_Object_Factory_v1.2.zip`](../releases/ArcGIS_Earth_Object_Factory_v1.2.zip) - **Source:** [`source/Object_Factory_v1.2.py`](../source/Object_Factory_v1.2.py)

Sky Compass, Beacon, PNG handling, presets and the coordinate reader are unchanged.

## What changed

### 1. Hide above (ft) - stop icons cluttering the view

**v1.1:** every object was always drawn. From high above a city, many objects became a pile of giant icons.

**v1.2:** the Objects tab has **Hide above (ft)**, and Batch lists accept an optional last column, `hide_above_ft`. The object shows only while you are within about that distance of it. Looking straight down, the number matches the **eye alt** ArcGIS Earth shows at the bottom of the map. Blank = always visible, as in v1.1.

How it works: the object (and its tether) goes into a KML folder with a **Region**: an invisible 300 m cube centred on the object, and a **minLodPixels** cutoff. ArcGIS Earth draws the folder only while that cube covers at least that many pixels on screen, i.e. while you are close enough. The cutoff = 1,790,000 / Hide above (ft) pixels (for example 3,000 ft -> 597).

How it was worked out (Jim's ArcGIS Earth, 2026-11-02):

- **Calibration:** six cameras with cutoffs 16 to 256 pixels. Climbing straight down, each doubling of eye alt (5,618 / 10,019 / 18,610 / 37,210 / 74,433 / 148,895 ft) removed exactly one more camera, which fixed the constant to within about ±25%.
- **Check:** a camera set to Hide above 40,000 ft disappeared near 40,000 ft (Jim: "yes it does").
- **Flat vs cube:** a flat box vanished edge-on when flying low (it looks like a sheet of paper seen from the side). A 300 m cube did not: at 162 ft eye alt, the cube set to 20,000 ft stayed visible about 4.9 miles away and was gone at about 5.3 miles, while the flat box was already gone at 4.9 miles. v1.2 uses the cube. Sideways, it reaches about a third farther than the number typed.

The cutoff is approximate. A smaller ArcGIS Earth window hides objects a little sooner.

### 2. Altitude in feet (Objects tab)

**Altitude (ft)** replaces Altitude (m) on the Objects tab, matching Hide above and ArcGIS Earth's eye alt. The factory converts to metres inside the KML. Preset altitudes are shown in feet, rounded to 10 ft (camera: 590 ft = 179.8 m). **Batch lists keep `alt_m` in metres,** so existing lists work unchanged.

### 3. Popup never blank

**v1.1:** with Popup = Info but no Info text and no URL, the object had nothing to show, so clicking it only selected it.

**v1.2:** in that case the popup shows the object's name. Popup = None still means no popup.

### 4. Layout

The description now sits on the title line, the title and tabs are slightly smaller and rows are slightly closer, so **CREATE OBJECT KMZ** and the status line fit on a maximised window (Jim's screenshot of TEST2).

## Verification

- **Live acceptance:** Jim Gaddy built objects with the v1.2 test builds and checked them in ArcGIS Earth on 2026-11-02: Hide above cutoff (40,000 ft), flat vs cube from low altitude, popups inside the Hide above folder, and a live FL511 camera popup on a v1.2 object ("target acquired").
- **Regression against v1.1** (Tk stand-in, same inputs, `tools/test-rigs/object_factory_test_v12.py` in ArcGIS Earth Unlocked): 32 of 32 checks pass. Sky Compass, Beacon and every object with Info text, a URL or Popup = None are byte-identical to v1.1. The only difference with Hide above blank is the name added to otherwise empty Info popups.
- **Hide above checks:** one folder and one 300 x 300 x 300 m cube per object, tether inside the folder, the cube placed correctly for all three altitude modes, bad values (`high`, `-10`) rejected with the line number, blank and 0 = always visible.
- **Built-in self-test** extended with Hide above, cube and name-popup checks.
- **Not verified:** the cutoff on other screens and window sizes.

## Checksums

| File | SHA-256 |
|---|---|
| `Object_Factory_v1.2.py` | `1310743e2f129d70dd85291efe1922c2f275bedbb9a91f45759d5925b4640ff9` |
| `ArcGIS_Earth_Object_Factory_v1.2.zip` | `531d4e0e54e38a0608052ba4140c51534101e40a16d75af6842532701c2fe1c4` |

`releases/ArcGIS_Earth_Object_Factory_v1.1.zip` and `source/Object_Factory_v1.1.py` stay in the repository so existing links keep working.
