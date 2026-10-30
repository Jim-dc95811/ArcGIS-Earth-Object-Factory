# ArcGIS Earth Unlocked

**Offline worlds, direct navigation, operational GIS, and programmable geographic objects — all inside ArcGIS Earth.**

This is the master system map for the public project family.

The projects began as separate solutions to separate problems: making huge offline maps, carrying them into the field, interrogating parcels, converting public point services, navigating ArcGIS Earth with a joystick, and creating long-range beacons. They now fit together as one coherent architecture.

> **The world is already built. We add the maps, movement, data, and objects.**

## The system

```text
                    ARCGIS EARTH UNLOCKED

     FOUNDATION              OPERATIONAL DATA
  offline TPKX worlds      parcels / public points
          |                         |
          +------------+------------+
                       |
                       v
                 ARCGIS EARTH
                       ^
                       |
         +-------------+-------------+
         |                           |
      NAVIGATION                  OBJECTS
      EarthStick              Object Factory
         |                   beacons / icons /
         |                   sky compass / links
         +-------------+-------------+
                       |
                       v
             interactive real geography
```

## Start with what you want to do

| I want to... | Start here |
|---|---|
| Make large offline zoomable ArcGIS Earth maps | [QGIS MBTiles → TPKX](https://github.com/Jim-dc95811/QGIS-Mbtile-to-ArcGIS-Earth-TPKX) |
| Work with the older offline-map/chartplotting/field-tracker toolset | [ArcGIS Earth Offline Maps & Chartplotting](https://github.com/Jim-dc95811/ArcGIS-Earth-Offline-Maps-Chartplotting) |
| Fly/navigate ArcGIS Earth with a joystick | [EarthStick](https://github.com/Jim-dc95811/EarthStick) |
| Put beacons, sky objects, icons, links, or object sets into Earth | [ArcGIS Earth Object Factory](https://github.com/Jim-dc95811/Earth-Beacon) |
| Turn public ArcGIS point services into offline KMZ/GeoJSON layers | [Point Maps / PointLayer](https://github.com/Jim-dc95811/Point-Maps) |
| Build offline clickable parcel layers | [Parcel100](https://github.com/Jim-dc95811/Parcel100) |

## 1. Foundation maps

### QGIS MBTiles → ArcGIS Earth TPKX

Repository: [QGIS-Mbtile-to-ArcGIS-Earth-TPKX](https://github.com/Jim-dc95811/QGIS-Mbtile-to-ArcGIS-Earth-TPKX)

Primary role:

> **Build the durable offline world.**

The converter turns compatible raster MBTiles into TPKX without rebuilding the raster tile pyramid. The surrounding Master 4 workflow provides deterministic geographic organization for large-area production.

Typical use:
- wide-area Z17/Z18 overview
- local Z20 detail
- imagery, road, hybrid, or other authorized raster tile sources
- ArcGIS Earth desktop/mobile offline viewing

### ArcGIS Earth Offline Maps & Chartplotting

Repository: [ArcGIS-Earth-Offline-Maps-Chartplotting](https://github.com/Jim-dc95811/ArcGIS-Earth-Offline-Maps-Chartplotting)

This preserves the earlier ArcGIS Pro/TPKX production, extent, Android/mobile, chartplotting, and PRAVE/ME tracking work. It remains useful historical and operational tooling rather than being folded into the newer MBTiles converter.

## 2. Navigation

### EarthStick

Repository: [EarthStick](https://github.com/Jim-dc95811/EarthStick)

Core idea:

> **Fly the real map.**

EarthStick gives direct joystick control to the ArcGIS Earth camera through the Automation API.

It changes the human relationship to the viewer:

> **Before the joystick, ArcGIS Earth is something you operate. After the joystick, it becomes somewhere you go.**

Neutral controls create a stable working state:

> **Stop. Hover. Think. Then move.**

## 3. Objects and authoring

### ArcGIS Earth Object Factory

Current repository: [Earth-Beacon / Object Factory](https://github.com/Jim-dc95811/Earth-Beacon)

The repository began as Earth Beacon and evolved into the active object-authoring lab.

Current factory primitives:
- generic PNG objects at geographic coordinates/altitudes
- batch object sets
- Sky Compass
- Earth Beacon
- labels off by default
- clickable information
- optional web links
- automatic PNG normalization for lean KMZ files

Core information flow:

> **See it → recognize it → click it → understand it.**

Core connectivity rule:

> **Offline object = useful by itself. Connected object = potentially unlimited extension.**

Future object work can include:
- live-camera/viewpoint launchers
- Street View links
- scenario triggers
- 3D models
- fly-through checkpoints
- classroom/training object sets

New experimental object ideas should normally begin here. Only spin them into a separate repository when they become large, stable, and independently useful.

## 4. Operational GIS data

### Point Maps / PointLayer

Repository: [Point-Maps](https://github.com/Jim-dc95811/Point-Maps)

Primary role:

> **Turn a public ArcGIS point service into a clean offline layer.**

PointLayer reads public FeatureServer/MapServer point layers, lets the user choose useful attributes, and creates KMZ/GeoJSON output.

Examples:
- hydrants
- fire stations
- shelters
- towers
- gates
- AEDs
- hospitals
- helipads

PointLayer is a data-ingestion/production tool. It should remain separate from Object Factory, which creates intentional user-authored objects.

### Parcel100

Repository: [Parcel100](https://github.com/Jim-dc95811/Parcel100)

Primary role:

> **Add clickable property intelligence beside the imagery.**

Parcel100 creates manageable offline GeoJSON parcel cells from public ArcGIS parcel services.

Useful field pairing:

```text
TPKX    = what the ground looks like
GeoJSON = what the parcel database knows about the ground
```

## 5. The architecture rule

The system should keep expensive durable geography separate from frequently changing information.

> **Foundation = stable geography**  
> **Layers = changing information**

Foundation:
- imagery
- roads
- terrain
- TPKX

Changeable layers/objects:
- parcels
- hydrants
- offices
- photos
- clues
- hazards
- beacons
- staging
- landing zones
- scenario objectives
- sky objects

Do not rebuild a massive foundation map because one operational object changed.

## 6. Offline first

A recurring project result is that the strongest pieces do not require internet at the incident/training/use location:

- TPKX foundation maps
- EarthStick
- Earth Beacon
- Sky Compass
- Object Factory KMZ/KML
- local photos/instructions
- Parcel100 GeoJSON
- PointLayer KMZ/GeoJSON

When internet exists, objects can extend outward through links to:
- live webcams
- Street View
- weather
- incident dashboards
- agency pages
- training videos
- equipment manuals

Online services are enhancements, not the foundation.

## 7. Basemaps can be part of the problem

ArcGIS Earth can change the visual language without changing geographic position.

A training/game problem may require the user to realize that the current map is the wrong tool:
- imagery for visual recognition
- street map for names/routes
- topo for drainage/ridges/elevation
- parcels for ownership/access
- historical maps for change
- live overlays for current conditions

Key idea:

> **The map is not the answer. Choosing the right map is part of the answer.**

## 8. Public safety and classroom directions

The same architecture supports very different use cases.

Public safety:
- pre-incident familiarization
- parcel/ownership context
- hydrants/water
- staging/LZ/egress exercises
- facility recognition
- offline incident mapping

Classroom:
- local geography
- bird/tree/animal identification
- history scavenger hunts
- coordinate literacy
- basemap problem solving
- student-authored object worlds

The common principle is accessibility:

> **Do not make the user learn GIS before they can use geography.**

## 9. Project boundaries

Each repository keeps one clear job. Do not collapse the ecosystem into a giant application simply because the pieces cooperate.

- EarthStick stays navigation.
- Object Factory stays intentional object authoring and experimentation.
- PointLayer stays public point-service ingestion.
- Parcel100 stays parcel production.
- TPKX projects stay foundation-map production.

The umbrella explains the relationship; it does not replace the specialized tools.

## 10. Independence

These are independent projects. ArcGIS, ArcGIS Pro, and ArcGIS Earth are Esri products and trademarks. The projects are not Esri products or official Esri distributions.

Third-party imagery, data, icons, services, URLs, and other content remain subject to their respective rights, terms, and accuracy limitations.
