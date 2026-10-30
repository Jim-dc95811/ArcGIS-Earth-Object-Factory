# ArcGIS Earth Object Factory

**Put objects into the real map.**

ArcGIS Earth Object Factory is a Windows/Python authoring tool for creating geographic objects that open directly in **ArcGIS Earth**. It grew from the original Earth Beacon experiment into a general factory for sky objects, ground objects, batch object sets, horizon navigation markers, and clickable information.

The goal is deliberately simple:

> **Choose an object → choose where it lives → choose what it shows → create it.**

No ArcGIS Pro project, QGIS project, KML hand-editing, or GIS database design is required for normal object creation.

## Current build

**ArcGIS Earth Object Factory v0.2 TEST**

The v0.2 build is the current owner-tested factory build. It keeps the live-proven object-generation behavior from the earlier proof-of-function tests while simplifying the GUI.

### Distribution note

The exact tested Python source is mirrored at the repository root as [`Object_Factory_v0.2_TEST.py`](Object_Factory_v0.2_TEST.py).

The **canonical runnable distribution** is the tested `ArcGIS_Earth_Object_Factory_v0.2_TEST.zip`, which also contains the preset PNG library, launcher, samples, and test checklist. The GitHub connector used during this reorganization can write source/documentation but cannot safely publish the binary ZIP/PDF/icon bundle, so **do not treat `Code → Download ZIP` of this repository as the packaged Object Factory release yet**.

This distinction is intentional: the public source mirror is exact, while the tested packaged distribution remains the accepted operator package until the binary release assets are uploaded separately.

The repository is currently still named `Earth-Beacon` because repository rename controls are not exposed through the connected GitHub tool. The intended repository name is **`ArcGIS-Earth-Object-Factory`**. See [`GITHUB_STRUCTURE.md`](GITHUB_STRUCTURE.md).

The active factory is organized around four tabs:

### Objects
Create one geographic PNG object at a time.

- manual latitude/longitude or **From Clipboard**
- built-in object presets
- custom transparent PNG support
- `relativeToGround`, `absolute`, or `clampToGround`
- adjustable icon scale
- optional vertical tether
- labels off by default
- Info popup or No Popup
- optional clickable hyperlink
- KMZ output

### Batch
Turn a simple text/CSV list into one object-set KMZ.

Kid-simple shorthand works:

```text
fuel,30.410104,-81.922396
helicopter,30.398210,-81.931440,300
bird,30.402778,-81.918620,120,Mystery Bird
home,30.385525,-81.930807
```

A full header format is also supported when altitude mode, scale, links, popup behavior, labels, tethers, descriptions, and custom icons need to be controlled per object.

### Sky Compass
Generate giant **N / E / S / W** horizon markers around a chosen center.

The Sky Compass was live-tested in ArcGIS Earth and gives EarthStick pilots a persistent visual orientation system in horizon view.

### Beacon
The original Earth Beacon geometry is now built into the factory.

A beacon turns a coordinate into a tall horizon-visible vertical KML target:

> **A pin marks a place. A beacon gives you something to aim at.**

## PNG normalization

The factory handles icon optimization automatically.

When a PNG is selected:

- the original file is never modified
- aspect ratio is preserved
- transparency is preserved
- images larger than 256 px are reduced for the packaged KMZ
- smaller clean icons are not unnecessarily enlarged
- duplicate source icons in a batch are packaged once and reused

This keeps object packs small without asking the operator to understand image optimization.

## Object presets

Current built-in preset families in the packaged distribution include:

- generic object
- helicopter
- fuel
- bird
- hazard
- home/base
- staging
- water
- fire truck
- camera/viewpoint
- medical

These are presets over one shared object engine, not separate hard-coded programs. A gas pump, bird, helicopter, or camera is simply a different geographic object definition.

## Clickable objects and links

Most objects are intended to remain visually clean with **no visible label until clicked**.

A useful information hierarchy is:

> **See it → recognize it → click it → understand it.**

Info objects can include a concise description and an optional web hyperlink. This creates a clean offline-first model:

> **Offline object = useful by itself. Connected object = potentially unlimited extension.**

Future Camera/Viewpoint work can use those links to open live webcams, Street View, still photos, recorded video, or other location-specific resources in a separate viewer while ArcGIS Earth remains underneath.

## Live-proven foundations

The development sequence intentionally proved the risky pieces separately before integration.

- **POF1:** arbitrary airborne PNG object — live-proven in ArcGIS Earth
- **POF2:** batch object list → multi-object KMZ — live-proven
- **POF3:** generated NSEW Sky Compass — live-proven
- **Earth Beacon:** long-range vertical KML navigation marker — live-proven

The v0.2 factory integrates those ideas into one GUI.

## Fast coordinate workflow

The preferred authoring loop is intentionally ordinary-person friendly:

1. Find a location in the map/source you are using.
2. Copy its latitude/longitude pair.
3. Click **From Clipboard** in Object Factory.
4. Verify Latitude and Longitude.
5. Choose the object/preset.
6. Create the KMZ/KML.
7. Add it to ArcGIS Earth.

This makes it practical to create an object list in minutes from ordinary map coordinates.

## Classroom and training possibilities

The same primitives can support very different worlds:

- bird/tree/animal identification lessons
- local-history hunts
- scavenger hunts
- route familiarization
- firefighter incident scenarios
- staging/LZ/water-source training
- floating fuel or facility markers
- giant sky-compass references
- camera/viewpoint objects
- future 3D objects

The world is the real geography; the factory adds objects and meaning.

## Relationship to EarthStick

[EarthStick](https://github.com/Jim-dc95811/EarthStick) provides direct joystick navigation through ArcGIS Earth.

Useful combination:

> **EarthStick = movement**  
> **Sky Compass = orientation**  
> **Earth Beacon = destination**  
> **Object Factory = objects and meaning**

## ArcGIS Earth Unlocked ecosystem

Object Factory is the active object-authoring and experimentation center in the broader **ArcGIS Earth Unlocked** project family.

- **Foundation maps:** [QGIS MBTiles → ArcGIS Earth TPKX](https://github.com/Jim-dc95811/QGIS-Mbtile-to-ArcGIS-Earth-TPKX)
- **Offline field-map workflows:** [ArcGIS Earth Offline Maps & Chartplotting](https://github.com/Jim-dc95811/ArcGIS-Earth-Offline-Maps-Chartplotting)
- **Navigation:** [EarthStick](https://github.com/Jim-dc95811/EarthStick)
- **Operational point layers:** [Point Maps / PointLayer](https://github.com/Jim-dc95811/Point-Maps)
- **Parcel intelligence:** [Parcel100](https://github.com/Jim-dc95811/Parcel100)
- **Objects / navigation markers / experiments:** this repository

Read the full system map: **[ArcGIS Earth Unlocked](ARCGIS_EARTH_UNLOCKED.md)**.

## Earth Beacon legacy

This repository began as **Earth Beacon**. The standalone accepted Beacon Maker v1.0 is preserved rather than discarded:

- [Beacon Maker v1.0 release](releases/Beacon_Maker_v1.0.zip)
- legacy standalone source/documentation is preserved under `legacy/Earth_Beacon_v1.0/`

The Beacon concept did not disappear; it became one of the four main Object Factory tools.

## Documentation / project brain

- [Object Factory quick guide](docs/OBJECT_FACTORY_GUIDE.md)
- [ArcGIS Earth Unlocked master system map](ARCGIS_EARTH_UNLOCKED.md)
- [GitHub organization / intended repository structure](GITHUB_STRUCTURE.md)
- [CONTINUITY.md](CONTINUITY.md) — current live-tested project state and next-session handoff
- [MAPWORLD.md](MAPWORLD.md) — technical ArcGIS Earth format/object inventory; “Mapworld” is an internal working term, not the final public umbrella name
- [CHANGELOG.md](CHANGELOG.md)

## Requirements

- Windows
- Python 3 with Tkinter (standard Windows Python install)
- ArcGIS Earth desktop for use/testing of generated files

Object Factory v0.2 TEST uses the Python standard library and Tkinter. No Pillow installation is required.

## Independence and data responsibility

This is an independent project and is not an Esri product or official Esri distribution. ArcGIS, ArcGIS Pro, and ArcGIS Earth are Esri products and trademarks.

Users remain responsible for the rights, accuracy, currency, and suitability of imagery, icons, URLs, agency data, public services, and other third-party content they place into their own object packs.

## License

MIT License. See [`LICENSE`](LICENSE).
