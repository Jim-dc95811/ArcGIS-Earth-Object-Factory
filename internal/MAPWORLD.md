# MAPWORLD — Technical Continuity for Future ChatGPT

**Date established:** 2026-10-27  
**Primary application:** ArcGIS Earth desktop, current 3.0 / 3.0.1-era behavior  
**Repository:** `Jim-dc95811/Earth-Beacon`  
**Purpose:** This file is written by ChatGPT for future ChatGPT sessions. It is a technical working reference for the emerging **Mapworld** idea: treating ArcGIS Earth not merely as a GIS viewer, but as a virtual world into which stable foundation maps, GIS features, clickable objects, media, 3D objects, beacons, scenarios, and eventually live or rule-driven content can be introduced.

This is not a marketing document. It is a continuity and architecture document. Future ChatGPT should use it to avoid rediscovering the same format questions and to distinguish verified ArcGIS Earth capabilities from concepts that still need testing.

---

## 1. THE MAPWORLD TECHNICAL IDEA

The working architectural concept is:

> **ArcGIS Earth = world + renderer**  
> **EarthStick = movement**  
> **Earth Beacon = long-range navigation / objectives**  
> **GIS layers = objects and meaning**  
> **Python = rules / state / scenario logic**

The foundation map does **not** need to be rebuilt whenever operational or game/training content changes.

Preferred separation:

> **Foundation = stable geography**  
> **Layers = changing information**

Examples of stable foundation content:
- offline imagery TPKX
- road/street basemaps
- terrain/elevation
- wide-area Z17/Z18 coverage
- local Z20 detail packages

Examples of changeable Mapworld content:
- parcels
- hydrants
- offices
- clue points
- photos
- fire perimeters
- landing zones
- staging areas
- beacons
- routes
- historical overlays
- 3D models
- scenario objectives
- temporary hazards

The design question is therefore not simply:

> “What files can ArcGIS Earth open?”

It is:

> **“Which ArcGIS Earth format is the best container for this kind of Mapworld object?”**

---

## 2. CURRENT OFFICIAL LOCAL-FILE SUPPORT

ArcGIS Earth currently documents support for the following local formats/content types:

- KML / KMZ
- Shapefile
- Mobile geodatabase
- CSV / TXT with coordinates or addresses
- GPX
- GeoJSON
- Raster files
- Standalone 3D models
- OGC 3D Tiles
- Gaussian splat `.3tz`
- Tile package `.tpk` / `.tpkx`
- Vector tile package `.vtpk`
- Scene layer package `.spk` / `.slpk`
- Mobile map package `.mmpk`
- Mobile scene package `.mspk`
- GeoPackage `.gpkg`

ArcGIS Earth 3.0 also uses:
- `.aescx` for Global Scene and Local Scene projects
- `.aemvx` for Movie projects

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

ArcGIS Earth 3.0 / 3.0.1 release information:
https://doc.arcgis.com/en/arcgis-earth/get-started/what-s-new.htm

---

## 3. MAPWORLD FORMAT MATRIX

### 3.1 KML / KMZ — best simple presentation-object format

**Extensions:** `.kml`, `.kmz`

**What it can provide:**
- point placemarks
- lines
- polygons
- ground overlays
- screen overlays
- network links
- tracks and multitracks
- models
- folders / hierarchy
- descriptions / popup information
- time-aware content

ArcGIS Earth allows KML/KMZ editing and can edit popup contents through the Info properties. KMZ is especially attractive because it can package supporting content with the KML.

**Mapworld strengths:**
- very easy to create with Python
- excellent for a small number of highly intentional objects
- natural for Earth Beacon
- supports 3D geometry behavior
- good for icons, labels, simple descriptions, links, media references
- KMZ can bundle assets
- easy to inspect and debug
- can be manually edited inside ArcGIS Earth

**Weaknesses:**
- not a serious relational/database format
- large numbers of features can become cumbersome
- not ideal for big agency datasets
- styling and hierarchy can become complicated in giant KML trees
- network-link behavior can introduce refresh/performance issues

**Best Mapworld fits:**
- Earth Beacon
- one clickable object
- one office icon with a photo/instructions
- clue point
- finish marker
- home marker
- simple route/tour
- historical annotation
- small scenario layer
- object with a rich popup

**Canonical example:**

> **State office icon → click → photo + address + entrance information**

For a simple “click the object and see a picture/info” requirement, **KMZ should be one of the first formats tested.**

Official KML documentation inside ArcGIS Earth:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm#ESRI_SECTION1_20F2AE2EA05D45BDB57F8FD7CC126E46

---

### 3.2 GeoJSON — best lightweight programmatically generated vector-object format

**Extensions:** `.geojson`, `.json`

**What it can provide:**
- points
- lines
- polygons
- feature properties / attributes

ArcGIS Earth supports GeoJSON from local files or URLs. GeoJSON supports ArcGIS Earth labeling and attribute-table workflows.

**Mapworld strengths:**
- extremely simple Python generation
- plain text
- easy to inspect manually
- easy to generate dynamically
- arbitrary feature attributes
- suitable for clue points, objectives, incidents, parcels, temporary objects
- ArcGIS Earth can label GeoJSON features
- ArcGIS Earth can expose GeoJSON attributes in attribute tables

**Weaknesses:**
- not designed to bundle images or arbitrary supporting files
- styling is not a core portable GeoJSON capability
- huge single GeoJSON files can become inefficient
- not a multi-layer database container

**Best Mapworld fits:**
- scavenger-hunt clue layers
- scenario points
- objective markers
- temporary hazard polygons
- search zones
- fire perimeter snapshots
- Python-generated operational layers
- simple game/training state objects

**Mapworld rule of thumb:**

> If Python needs to create or replace a simple vector layer quickly, **GeoJSON is a first-choice prototype format.**

Official ArcGIS Earth GeoJSON support:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

Label support:
https://doc.arcgis.com/en/arcgis-earth/use/apply-label.htm

---

### 3.3 CSV / TXT — best simple point-list format

**Extensions:** `.csv`, `.txt`

**What it can provide:**
- point locations from latitude/longitude
- point locations from addresses/geocoding
- fields/attributes
- configurable popup fields

ArcGIS Earth allows the user to select which CSV/TXT fields appear in feature popups.

**Mapworld strengths:**
- easiest format for non-GIS users
- Excel-friendly
- human-readable
- easy for Python and ordinary office workflows
- labels supported
- attributes supported
- very good for point inventories

**Weaknesses:**
- mostly a point-data solution
- no rich geometry model
- no embedded media
- no real multi-layer structure

**Best Mapworld fits:**
- office list
- facility list
- hydrant list
- checkpoint list
- classroom target list
- simple point inventory
- quick proof-of-concept object set

**Rule of thumb:**

> If a normal human could reasonably maintain the object list in Excel, CSV deserves consideration.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.4 Shapefile — best legacy/existing-agency vector interchange format

**Typical files:** `.shp`, `.shx`, `.dbf`, `.prj`, etc.

**What it can provide:**
- points
- lines
- polygons
- feature attributes

ArcGIS Earth supports shapefile labeling and attribute tables.

**Mapworld strengths:**
- nearly universal GIS interchange
- enormous amount of existing agency/public data already available this way
- good for established GIS datasets
- attributes and labels work well

**Weaknesses:**
- not really one file
- old DBF field limitations
- awkward as a modern game/scenario authoring format
- no natural media bundling
- less pleasant to hand-author than GeoJSON

**Best Mapworld fits:**
- parcels from existing agencies
- hydrants
- roads
- boundaries
- infrastructure
- forestry/land-management layers
- existing GIS source data that already arrives as shapefile

**Rule of thumb:**

> Shapefile is often something Mapworld should **consume**, not something a new Mapworld authoring tool should necessarily generate by default.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.5 Mobile geodatabase — structured Esri offline vector database

**Extension:** typically `.geodatabase`

**What it can provide:**
- structured feature classes
- attribute tables
- multiple related datasets depending on source design

ArcGIS Earth supports mobile geodatabases as local data and supports their attribute tables.

**Mapworld strengths:**
- one structured database
- better data organization than loose text/shapefile files
- good for substantial offline operational datasets
- suitable for serious agency data collections

**Weaknesses:**
- more Esri-specific
- more engineering/authoring overhead
- less transparent than GeoJSON/CSV
- not a presentation-first format

**Best Mapworld fits:**
- large offline operational object databases
- mature agency datasets
- district-scale structured feature collections

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.6 GeoPackage — high-value candidate for complete Mapworld object/scenario packs

**Extension:** `.gpkg`

**What it can provide conceptually:**
- multiple vector datasets
- tables
- raster/tile content depending on package design
- one SQLite-based OGC container

ArcGIS Earth supports GeoPackage as local content in a **Global Scene**. It is not currently supported as a local-file content type in a **Local Scene**.

**Mapworld strengths:**
- open OGC format
- single-file portability
- SQLite foundation
- strong candidate for packaging a full hunt/scenario database
- potentially excellent Python tooling
- can keep multiple logical datasets together

**Weaknesses / unknowns:**
- exact ArcGIS Earth popup behavior for all desired Mapworld uses still needs live testing
- image/media relationships need live testing
- ArcGIS Earth styling behavior may not preserve every styling concept expected from other GIS software
- not currently supported in Local Scene

**Best Mapworld fits to test:**
- entire scavenger hunt
- incident-training scenario package
- facility/object database
- district operational object pack
- multi-table scenario state/reference data

**Important:**

Do not permanently choose GeoPackage over GeoJSON/KMZ until a prototype verifies the exact popup, labeling, media, performance, and editing behavior needed.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

Scene-type matrix:
https://doc.arcgis.com/en/arcgis-earth/use/feature-availability-by-scene-type.htm

---

### 3.7 GPX — route/track/history format

**Extension:** `.gpx`

**What it can provide:**
- waypoints
- tracks
- routes
- timestamps

ArcGIS Earth imports GPX into KML-style layers and supports time animation.

**Mapworld strengths:**
- natural GPS interchange format
- excellent for recorded travel
- time-aware tracks
- routes and waypoints
- broadly understood by GPS applications

**Weaknesses:**
- specialized
- not a general object/scenario database
- ArcGIS Earth effectively transforms it into KML behavior after import

**Best Mapworld fits:**
- flight/player breadcrumb history
- patrol history
- vehicle track replay
- route familiarization
- “where did we travel?”
- time-based movement demonstrations

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.8 Raster files — maps/images/surfaces, not intelligent objects

ArcGIS Earth documents support for a range of raster formats including GeoTIFF, IMG, JPEG, PNG, JPEG2000, MrSID, NITF, DTED, SRTM and others.

Raster can be used as:
- operational layer
- basemap layer
- elevation layer

**Mapworld strengths:**
- direct image/map representation
- good for historical maps
- good for aerial imagery
- good for elevation/terrain
- useful for before/after comparison

**Weaknesses:**
- pixels are not individually intelligent objects
- no feature-level attributes
- changing one object generally means changing/rebuilding imagery

**Best Mapworld fits:**
- historical maps
- scanned incident maps
- aerial photographs
- elevation surfaces
- overlays where pixel display matters more than feature intelligence

**Rule of thumb:**

> Raster is part of the **world surface**, not usually the best container for interactive Mapworld objects.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.9 TPK / TPKX — primary offline raster foundation-world format

**Extensions:** `.tpk`, `.tpkx`

ArcGIS Earth supports tile packages as basemap or terrain content.

**Mapworld strengths:**
- excellent offline performance
- multizoom tile pyramid
- one package
- proven in the user's workflow at very large sizes
- ArcGIS Earth renders TPKX extremely well
- ideal for stable foundation imagery

**Weaknesses:**
- frozen pixels
- no individual feature intelligence
- no popup attributes for objects encoded in the image
- changing operational information requires a separate overlay, not editing the TPKX

**Best Mapworld fit:**

> **FOUNDATION WORLD**

This remains the preferred architecture for large offline imagery/road-map coverage while smaller operational/object layers sit above it.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.10 VTPK — offline vector-tile foundation display

**Extension:** `.vtpk`

**What it can provide:**
- prebuilt vector-tile cartography
- roads
- labels
- stylized basemap content

**Mapworld strengths:**
- scalable crisp cartography
- efficient display
- excellent foundation-map role

**Weaknesses:**
- vector tiles are primarily rendered cartographic content, not an ideal set of individually interactive game/scenario objects
- editing requires rebuilding/repackaging

**Best Mapworld fits:**
- offline road-map foundation
- label foundation
- cartographic backdrop

Official support list:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.11 Standalone 3D models — extremely important Mapworld object type

**Supported formats documented by ArcGIS Earth:**
- `.3ds`
- `.dae`
- `.fbx`
- `.obj`
- `.gltf`

ArcGIS Earth can place standalone 3D models geographically and allows editing of:
- name
- position
- altitude mode
- scale
- heading
- tilt
- roll
- fly-to view

**Crucial capability:** ArcGIS Earth allows a 3D model to have a **Rich Text / HTML description that appears in a popup when the model is clicked.**

This makes standalone 3D models one of the most interesting Mapworld object types.

**Mapworld strengths:**
- object can visibly exist in the world rather than merely appear as a symbol
- geographically placeable
- can be rotated/scaled
- clickable
- rich-text/HTML popup
- ArcGIS Earth can export the placed model as KMZ

**Weaknesses:**
- poor choice for enormous numbers of independent models
- model preparation matters
- texture/asset packaging needs testing per model format
- performance depends on model complexity

**Best Mapworld fits:**
- treasure chest
- question-mark object
- fire engine
- aircraft
- tower
- tree
- landmark
- historical object
- instructional prop
- fantasy object
- dragon
- alien object
- training target
- 3D “pickup” object

**Very important future experiment:**

> Place a simple GLTF/DAE object in ArcGIS Earth, attach a rich popup, and determine whether it is practical as a scavenger-hunt clue or game-object primitive.

Official 3D-model documentation:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.12 Scene Layer Package — high-volume 3D GIS

**Extensions:** `.slpk`, `.spk`

ArcGIS Earth supports scene layer packages containing:
- point scene layers
- point clouds
- 3D objects
- integrated mesh
- building scene layers

**Mapworld strengths:**
- designed for large 3D datasets
- far more scalable than loose standalone models
- good for cities, forests, infrastructure, meshes, point clouds
- suitable for mass 3D rather than one-off props

**Weaknesses:**
- more complicated creation pipeline
- generally needs ArcGIS Pro or specialized tools/workflows
- less convenient for rapidly generated clue/object content
- some scene-layer types differ between Global and Local Scene support

**Best Mapworld fits:**
- 3D city
- forest inventory visualization
- many 3D infrastructure objects
- integrated-mesh environment
- point cloud
- BIM/building content

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

Scene-type support:
https://doc.arcgis.com/en/arcgis-earth/use/feature-availability-by-scene-type.htm

---

### 3.13 OGC 3D Tiles — open large-scale 3D world/object format

**Local forms documented by ArcGIS Earth:** `.json`, `.3tz`, and support for batched `.b3dm` content within 3D Tiles structures.

ArcGIS Earth describes 3D Tiles as suitable for visualizing:
- continuous meshes
- discrete 3D objects

**Mapworld strengths:**
- open OGC ecosystem
- designed to stream/render large amounts of 3D content
- works for meshes or collections of objects
- can come from non-Esri tooling
- `.3tz` supported in both Global and Local Scene

**Weaknesses:**
- more engineering than KML/GeoJSON
- not necessarily the easiest path for feature-level popup/game semantics
- needs testing if Mapworld wants each discrete object to behave as an interactive object rather than merely rendered 3D content

**Best Mapworld fits:**
- city models
- photogrammetric environments
- large collections of 3D objects
- external/open 3D ecosystems
- future large-scale custom worlds

Official ArcGIS Earth source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

OGC 3D Tiles standard:
https://www.ogc.org/standard/3dtiles/

---

### 3.14 Gaussian splat `.3tz` — photorealistic captured local world

ArcGIS Earth 3.0 added Gaussian splat support.

**Current important limitation:**

> Gaussian splat layers are **Local Scene only**.

**Mapworld strengths:**
- highly realistic capture of complicated real environments
- useful where traditional meshes struggle with vegetation, reflective surfaces, fine detail, etc.

**Weaknesses:**
- Local Scene only
- heavy GPU/storage requirements are likely
- more of a captured environment than an object database
- current EarthStick/Beacon work is primarily Global Scene oriented

**Best Mapworld fits:**
- facility capture
- campus/site capture
- detailed training area
- photorealistic local scene

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

Release notes:
https://doc.arcgis.com/en/arcgis-earth/get-started/what-s-new.htm

---

### 3.15 MMPK — complete portable 2D map package

**Extension:** `.mmpk`

**Conceptual role:** package a complete map and its supported data for offline use.

**Mapworld strengths:**
- one portable package
- useful for delivering a self-contained authored map
- offline capable

**Weaknesses:**
- heavier than independent lightweight overlays
- less flexible than the current “stable foundation + replaceable object layers” philosophy
- user has already observed that TPKX is often smaller/faster for pure imagery delivery

**Best Mapworld fits:**
- finished offline map package
- deliver a preassembled map where bundling is more important than rapidly swapping object layers

Official support list:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.16 MSPK — complete portable 2D/3D scene package

**Extension:** `.mspk`

ArcGIS Earth documents MSPK as an offline package that can contain scenes, operational layers, basemap, elevation, KML/KMZ, scene layers and locators.

**Important behavior:** packaged data is effectively treated as a package; ArcGIS Earth documents that the user cannot remove/reorder individual layers inside it or add more data to the package itself. Removing the package removes the package as a unit.

**Mapworld strengths:**
- closest local-file concept to shipping a preassembled 3D world
- can include multiple content types
- offline
- can include locators

**Weaknesses:**
- less modular
- package contents are comparatively rigid/read-only inside Earth
- rebuilding is heavier than replacing a small independent layer

**Best Mapworld fits:**
- finished training world
- finished demonstration world
- city/facility scene distributed as one unit

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

### 3.17 ArcGIS Earth project `.aescx` — saves the world assembly/state

ArcGIS Earth 3.0 introduced projects. Global Scene and Local Scene projects use `.aescx`.

A project keeps the working scene, including data, views and project settings, so work can be resumed later.

**Mapworld strengths:**
- saves how the world is assembled
- saves layers/views/settings rather than only one data source
- useful for scenario setups
- useful for classroom/demo presets
- potentially useful as “load this Mapworld configuration”

**Weaknesses:**
- should not automatically be assumed to embed every referenced source file
- project state and data packaging are different concepts

**Best Mapworld fits:**
- saved scenario configuration
- classroom starting state
- demonstration starting state
- personal Mapworld setup

Official source:
https://doc.arcgis.com/en/arcgis-earth/get-started/what-s-new.htm

---

### 3.18 Movie project `.aemvx` — scripted presentation/time sequence, not object storage

ArcGIS Earth 3.0 uses `.aemvx` for Movie projects.

Movie can combine camera movement, maps, layers, text, images, drawings and audio on a timeline.

**Mapworld strengths:**
- scripted presentation
- narrated geographic story
- controlled demonstration
- may eventually be useful for training introductions or scenario playback

**Weaknesses:**
- not a general object database
- primarily presentation/timeline oriented

**Best Mapworld fits:**
- demo videos
- guided tours
- scenario intro
- historical narration

Official source:
https://doc.arcgis.com/en/arcgis-earth/get-started/what-s-new.htm

---

## 4. FORMAT ROLES — THE SIMPLE ARCHITECTURE

Future ChatGPT should remember this shorthand:

| Mapworld role | First formats to consider |
| --- | --- |
| Stable offline imagery foundation | **TPKX** |
| Stable offline road/label foundation | **TPKX / VTPK** |
| One simple clickable object | **KML/KMZ** |
| Icon + picture + instructions | **KMZ** |
| Earth Beacon | **KML** |
| Quickly generated vector objects | **GeoJSON** |
| Human-maintained point list | **CSV** |
| Existing agency vector dataset | **Shapefile / GeoPackage / mobile geodatabase** |
| Entire scenario/object database | **GeoPackage** (prototype/test first) |
| One/few true 3D clickable objects | **Standalone 3D model / KMZ** |
| Thousands/millions of 3D objects | **SLPK / 3D Tiles** |
| Photorealistic captured local environment | **3D Tiles / Gaussian splat** |
| Whole prebuilt offline 2D world | **MMPK** |
| Whole prebuilt offline 3D world | **MSPK** |
| Save world configuration/state | **AESCX** |
| GPS route/track/history | **GPX** |
| Scripted presentation | **AEMVX Movie project** |

The most useful conceptual distinction is:

> **KML/KMZ = presentation-first**  
> **GeoJSON = generation-first**  
> **GeoPackage / mobile geodatabase = storage-first**  
> **TPKX / VTPK = foundation-display-first**  
> **SLPK / 3D Tiles = mass-3D-first**

---

## 5. GLOBAL SCENE VS LOCAL SCENE — DO NOT FORGET THIS

ArcGIS Earth 3.0 introduced Local Scene, but Local Scene does **not** support everything the Global Scene supports.

Important current examples from Esri's scene-type matrix:

### Global Scene supports local files including:
- KML/KMZ
- GeoPackage
- raster
- TPK/TPKX
- VTPK
- SLPK/SPK where the layer type is supported
- MMPK/MSPK where supported
- `.3tz` 3D Tiles

### Local Scene restrictions include:
- KML/KMZ: not supported
- GeoPackage: not supported
- raster local files: not supported
- ordinary `.dae` standalone model: not supported
- package support depends on whether contained layer types are Local Scene compatible
- `.3tz` 3D Tiles: supported
- building scene layers: Local Scene supported
- Gaussian splat: Local Scene supported

This matters because the current EarthStick/Earth Beacon world is fundamentally a **Global Scene / globe** concept.

Do not casually recommend Local Scene formats without checking whether the rest of the Mapworld architecture still works there.

Official matrix:
https://doc.arcgis.com/en/arcgis-earth/use/feature-availability-by-scene-type.htm

---

## 6. LABELING AND ATTRIBUTE TABLES

ArcGIS Earth currently documents dynamic labeling support for:
- shapefile
- CSV/TXT
- GeoJSON
- feature services

Source:
https://doc.arcgis.com/en/arcgis-earth/use/apply-label.htm

ArcGIS Earth currently documents attribute-table support for:
- shapefile
- CSV/TXT
- GeoJSON
- feature services
- mobile geodatabase

Attribute tables allow sorting, selecting, filtering, zooming to features, and exporting selected rows to KMZ or CSV.

Source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

This makes GeoJSON, shapefile, CSV and mobile geodatabases especially important where Mapworld needs **inspectable feature data**, not merely pretty symbols.

---

## 7. TIME-AWARE OBJECTS

ArcGIS Earth supports time animation when time-aware layers are present. The documentation specifically discusses temporal KML/KMZ layers, feature services and image services.

This opens a separate Mapworld category:

> **Objects do not merely have location; they can have time.**

Possible future uses:
- moving incident perimeter
- vehicle history
- aircraft track
- historical timeline
- wildfire progression
- flood progression
- route replay
- animal migration
- “what did this place look like at this time?”

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

## 8. LIVE / SERVICE-BASED MAPWORLD CONTENT

This file began as a local-file inventory, but future Mapworld work must remember that ArcGIS Earth also supports live/services content.

Documented service categories include:
- ArcGIS map service
- image service
- feature service
- scene service
- vector tile service
- stream service
- web scene
- web map
- WMS
- WMTS
- WFS
- KML URL/service
- Survey123 forms

ArcGIS Earth also supports automatic refresh for several service/layer types.

This is where Mapworld can eventually move from:

> **static objects**

toward:

> **objects that change while the operator is flying through the world**

Potential future examples:
- live unit locations
- weather
- live incident perimeter
- stream/sensor objects
- refreshed road closures
- feature-service scenario state
- live crew/resource layers

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

## 9. SURVEY123 AND HTML WINDOWS — FUTURE INTERACTION OPTIONS

ArcGIS Earth documentation includes:
- Survey123 integration
- HTML windows

Survey123 can interact with records and can connect surveys to other selected layers/features.

This could matter if future Mapworld requires structured forms, inspections, answers, or data collection rather than only passive popups.

Do not assume Survey123 or HTML windows solve the scavenger-hunt/game-state problem until tested, but they belong on the future interaction list.

Official source:
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

---

## 10. AUTOMATION/API RELATIONSHIP

The file-format system and the Automation API should be treated as two different layers of the architecture.

File/data formats answer:

> **“What can exist in the world?”**

Automation answers:

> **“What can an external program ask Earth to do or report?”**

EarthStick already proves that an external Python program can use ArcGIS Earth's Automation API to read and update camera state.

Future Mapworld scenario logic may therefore be split:

- ArcGIS Earth renders world/data
- EarthStick controls movement
- small files/layers carry objects
- Python tracks game/training state
- Python reveals/replaces/loads objects or beacons when rules are satisfied

Important limitation from current research: do **not** assume ArcGIS Earth exposes a general event stream for every user click/feature selection. Selection/click detection requires separate investigation before designing the game engine around it.

Future technical research target:

> Determine exactly which Automation API endpoints can read layer/graphic state, add/remove/update graphics/layers, take snapshots, and whether any supported mechanism can report which feature/object the user selected.

ArcGIS Earth documentation home:
https://doc.arcgis.com/en/arcgis-earth/

---

## 11. MAPWORLD OBJECT DECISION TREE

When inventing a new object, future ChatGPT should ask these questions in order:

### A. Is it part of the stable visual world?
Use:
- TPKX
- VTPK
- raster
- terrain

### B. Is it one/few intentional clickable objects?
First test:
- KML/KMZ
- standalone 3D model

### C. Is it hundreds/thousands of simple dynamically generated vector objects?
First test:
- GeoJSON

### D. Is it a human-maintained point list?
First test:
- CSV

### E. Is it a large existing GIS dataset?
Use/consider:
- shapefile
- GeoPackage
- mobile geodatabase
- feature service

### F. Does it need multiple datasets in one portable scenario database?
Prototype:
- GeoPackage
- mobile geodatabase

### G. Does it need to physically appear as a real 3D object?
Few objects:
- GLTF / DAE / OBJ / FBX / 3DS

Large collections:
- SLPK
- 3D Tiles

### H. Does the whole world need to be delivered as one preassembled package?
Consider:
- MMPK for 2D-centric map
- MSPK for 2D/3D scene

### I. Does it need time/history?
Consider:
- GPX
- time-aware KML
- time-aware service data

### J. Does it need live updating?
Consider:
- feature service
- stream service
- KML network link
- WFS
- other refresh-capable services

---

## 12. HIGH-VALUE MAPWORLD PROTOTYPES TO TEST

Do not build all of these at once. These are focused experiments that would answer major architecture questions.

### Prototype 1 — KMZ photo object
Create one office placemark with:
- custom icon
- name
- JPEG photo
- address
- phone
- entrance/gate note

Goal:
- verify best offline self-contained picture-popup behavior

### Prototype 2 — GeoJSON clue layer
Create 10 points containing:
- clue ID
- question
- answer
- hint
- points
- next objective

Goal:
- verify labels, popups, attribute inspection, performance, and Python authoring simplicity

### Prototype 3 — GeoPackage hunt
Put several logical hunt/scenario layers into one GPKG.

Goal:
- determine whether one portable database is better than multiple GeoJSON/KML files for scenario authoring

### Prototype 4 — clickable 3D treasure chest
Place a simple `.gltf` or `.dae` model with a rich popup.

Goal:
- prove whether a true 3D object can function as a scavenger-hunt pickup/clue object

### Prototype 5 — answer → beacon reveal
Keep the foundation map unchanged.

Goal:
- small Python controller accepts an answer and reveals/loads the next KML beacon

This tests the progression idea:

> **Knowledge unlocks geography.**

### Prototype 6 — live/refresh object
Use one refreshable source/service.

Goal:
- demonstrate an object changing while EarthStick remains in the same world

---

## 13. VERIFIED VS CONCEPTUAL

### VERIFIED / DOCUMENTED
- ArcGIS Earth supports the local formats listed in Section 2.
- KML/KMZ can contain/edit a wide variety of KML geometry/content types.
- GeoJSON loads from local file/URL.
- GeoJSON, shapefile, CSV/TXT and feature services support dynamic labels.
- GeoJSON, shapefile, CSV/TXT, feature services and mobile geodatabases support attribute tables.
- GPX imports to KML-style layers and supports time behavior.
- raster can be operational, basemap or elevation content.
- TPK/TPKX can be used as basemap or terrain content.
- standalone 3D models support position, scale, heading, tilt, roll and rich-text/HTML popup descriptions.
- 3D Tiles can represent continuous meshes or discrete 3D objects.
- MSPK packages offline 2D/3D scene content and is comparatively rigid/read-only as a package.
- ArcGIS Earth 3.0 introduced Global/Local Scene projects `.aescx` and Movie `.aemvx`.
- Local Scene has significant content limitations compared with Global Scene.

### LIVE-TESTED BY USER IN THE PROJECT ECOSYSTEM
- TPKX works extremely well as offline ArcGIS Earth foundation imagery.
- Earth Beacon KML works as a very tall long-range vertical navigation marker.
- EarthStick works as direct joystick-driven ArcGIS Earth movement.
- parcel/feature interrogation can be performed while stopping/hovering with EarthStick.
- integrated-mesh 3D content can be flown through with EarthStick.

### CONCEPTUAL / NEEDS TESTING
- KMZ as the preferred self-contained offline facility-photo object
- GeoJSON as the final scavenger-hunt format
- GeoPackage as a complete scenario container
- true 3D models as clickable game/training objects
- answer-triggered automated beacon reveal
- automated object/layer state transitions
- automated detection of which ArcGIS Earth feature the user clicked
- large-scale game-like scenario engine

Do not silently upgrade conceptual items to “working” in future sessions.

---

## 14. SOURCE LINKS — KEEP THESE WITH THE FILE

Primary ArcGIS Earth sources used to establish this continuity file:

### Add and edit data / supported local formats / KML / GeoJSON / raster / 3D models / packages / services / attribute tables
https://doc.arcgis.com/en/arcgis-earth/use/add-data.htm

### Dynamic labeling support
https://doc.arcgis.com/en/arcgis-earth/use/apply-label.htm

### Global Scene vs Local Scene feature/content matrix
https://doc.arcgis.com/en/arcgis-earth/use/feature-availability-by-scene-type.htm

### ArcGIS Earth 3.0 / 3.0.1 new project formats and Local Scene additions
https://doc.arcgis.com/en/arcgis-earth/get-started/what-s-new.htm

### ArcGIS Earth documentation root
https://doc.arcgis.com/en/arcgis-earth/

### OGC 3D Tiles standard
https://www.ogc.org/standard/3dtiles/

### OGC GeoPackage standard
https://www.ogc.org/standard/geopackage/

### OGC KML standard
https://www.ogc.org/standard/kml/

Future ChatGPT should re-check the official ArcGIS Earth documentation when ArcGIS Earth versions change. The format matrix is based on the 3.0 / 3.0.1-era documentation current on 2026-10-27.

---

## 15. CURRENT MAPWORLD SUMMARY

The important discovery is not that ArcGIS Earth supports many GIS formats. The important discovery is that those formats form a usable **object hierarchy**:

> **TPKX/VTPK/raster build the world.**  
> **GeoJSON/shapefile/CSV/databases populate it with intelligent features.**  
> **KML/KMZ provides expressive clickable presentation objects and beacons.**  
> **Standalone 3D models create literal objects inside the world.**  
> **SLPK/3D Tiles scale that concept to large 3D environments.**  
> **AESCX saves the assembled world.**  
> **Python can potentially provide the rules that make objects appear, disappear, change, or unlock.**

That is the technical foundation of **Mapworld**.

When resuming this line of thought, do not begin by asking “what game should we make?” Begin by asking:

> **What kind of object do we want to exist, and which ArcGIS Earth container gives that object the behavior we need?**
