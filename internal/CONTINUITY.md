# CONTINUITY — ArcGIS Earth + EarthStick + Earth Beacon + Object Factory

**Date:** 2026-10-29  
**Purpose:** This file is written by ChatGPT for future ChatGPT sessions. It is the current reset-proof project state. Read this before proposing changes, rebuilding tools, or interpreting the project from scratch.

> **Update 2026-10-31 — read first.** Several statements below have been superseded since this file was written:
> - **Object Factory v1.0 was commissioned on 2026-10-29** (the accepted v0.2.2 TEST build, promoted without redesign). The integrated GUI is no longer conceptual. See `CHANGELOG.md`.
> - **The umbrella name is now ArcGIS Earth Unlocked**: https://github.com/Jim-dc95811/ArcGIS-Earth-Unlocked
> - The former **Earth-Beacon** repository became this repository (**ArcGIS-Earth-Object-Factory**). The standalone Beacon Maker v1.0 source and docs are preserved under `legacy/Earth_Beacon_v1.0/`. On 2026-10-31 Jim retired it as a separate download (the Factory's Beacon tab makes the same beacon); its release zip remains only in git history.
> - **Object Factory v1.1 released 2026-10-31** (hardening: clipboard reads N/S/E/W and DMS with a readback, overwrite prompt, safe .partial writes, batch header/line-number fixes, clean v1.1 package, unused ArcGIS Earth camera code removed). Outputs identical to v1.0. See `docs/OBJECT_FACTORY_V1.1_CHANGES.md`.
> - The original sections are kept below unchanged as the historical record.

The project has moved beyond EarthStick + Earth Beacon into a broader ArcGIS Earth interaction system built around offline worlds, direct joystick navigation, programmable geographic objects, simple authoring, training, games, classroom use, and public-safety workflows.

Important naming note:
- **EarthStick** and **Earth Beacon** remain accepted product/tool names.
- **Mapworld** was useful as a working concept, but the user considers the name effectively taken/generic and does **not** want to rely on it as the final umbrella brand.
- Current naming direction is to start with **ArcGIS Earth** and add a descriptor. Candidates discussed included ArcGIS Earth Worlds, ArcGIS Earth Interactive, ArcGIS Earth Unlocked, etc. **No final umbrella name has been chosen.**
- `MAPWORLD.md` remains the existing technical format/architecture inventory, but treat “Mapworld” inside it as a working technical term rather than a finalized public brand.

---

# 1. USER / PROJECT INTENT

The user works in public safety/fire-service context and has spent decades around computers/electronics. He is not a traditional programmer, but is a highly capable hands-on operator/analyst who tests relentlessly and trusts measured behavior over theory.

Primary mission:

> **Create new map makers.**

The project is intentionally aimed at ordinary users, firefighters, resource staff, students, teachers, field operators, and decision makers—not only GIS specialists.

The larger philosophy is:

> **Do not make the user learn GIS before they can use geography.**

A joystick, clipboard coordinates, simple object presets, offline basemaps, and clickable objects are all ways of lowering the human-interface barrier without reducing the power of the GIS underneath.

---

# 2. NON-NEGOTIABLE BUILD RULES

Preserve the user’s **Minimal Build Rule**:

- Implement only the requested function unless the user explicitly grants broader design authority.
- Do not rename/restructure accepted products casually.
- Preserve filenames, paths, working behavior, and known-good settings unless a change is specifically justified.
- No “cleanup refactor” of accepted code merely because another structure looks prettier.
- Functional code changes get a new version.
- Do not call a version accepted until the user live-tests it in ArcGIS Earth.
- Distinguish **verified**, **inferred**, and **conceptual** behavior.
- “Unknown” is better than pretending.

Special current authority:

> **The Object Factory is ChatGPT’s factory build.**

The user explicitly gave ChatGPT broad authority to assemble the Object Factory as it sees fit, including building several proof-of-function scripts before tying them together. That does **not** revoke the Minimal Build Rule for accepted EarthStick/Earth Beacon code.

---

# 3. CORE ARCHITECTURE

Current system model:

> **ArcGIS Earth = world + renderer**  
> **EarthStick = movement**  
> **Earth Beacon = long-range navigation / objectives**  
> **GIS layers = objects and meaning**  
> **Python = rules / state / scenario logic**

Stable-world rule:

> **Foundation = stable geography**  
> **Layers = changing information**

Foundation examples:
- offline TPKX imagery
- road/street basemaps
- terrain/elevation
- district-wide Z17/Z18
- local Z20 detail

Changeable content examples:
- parcels
- hydrants
- offices
- photos
- beacons
- clues
- hazards
- staging
- landing zones
- fire perimeters
- routes
- historical overlays
- 3D objects
- sky objects
- scenario objectives

Do not rebuild a giant base map because a hydrant, clue, photo, or scenario object changes.

---

# 4. EARTHSTICK 1.0 — FINISHED / LIVE-ACCEPTED

Repository:
https://github.com/Jim-dc95811/EarthStick

Core idea:

> **Fly the real map.**

EarthStick turns ArcGIS Earth into a directly piloted GIS/map using the Thrustmaster TCA Sidestick Airbus Edition.

Important framing:

> **This is not a flight simulator. It is a real map that you can fly.**

> **Instead of putting the real world into a flight simulator, we put flight controls into the real-world map.**

### Accepted controls
- Stick X = strafe left/right
- Stick Y = forward/reverse
- Twist/RZ = heading
- Physical throttle / Slider0 = travel speed
- POV up/down = camera tilt
- Button 4, red top button = zoom in / descend
- Button 3, black thumb button = zoom out / climb
- Neutral controls = stop / hover

Important operational behavior:

> **Stop. Hover. Think. Then move.**

Neutral input produces a stable working state. The operator can stop, inspect the map, toggle layers, click parcels/features, make a decision, and resume without fighting camera movement.

EarthStick makes horizon view a practical working view rather than a temporary dramatic camera angle.

### Accepted technical behavior
- ArcGIS Earth Automation API GET/PUT camera
- WKID 4326
- Windows WinMM/ctypes, standard library only
- `POLL_HZ = 30.0`
- `DEADZONE = .08`
- `YAW_RATE_DPS = 55`
- `TILT_RATE_DPS = 45`
- Earth radius = 6378137
- idle resync = .50 s
- HTTP timeout = .75 s
- API base = `http://localhost:8000`
- target joystick = `T.A320 Pilot`
- invert twist = false
- invert throttle = true
- fixed 30 Hz loop
- dt capped at .10
- API fault recovery retries camera GET every .25 s
- local authoritative camera state is updated only after successful PUT
- joystick reconnect retry every 1 s
- on reconnect, reread camera and reset timers
- no neutral-before-resume requirement

Speed law:

```python
max_speed = clamp(max(8.0, altitude_m * 0.020), 8.0, 12000.0) * 60.0
min_speed = 0.50
speed = min_speed + (max_speed - min_speed) * throttle**2
```

Zoom behavior:
- `max(2.0, altitude * .75)`
- minimum altitude 1 m

Live-tested on Windows 11 / Python 3.14.5.

Known accepted release reference:
- release commit previously recorded: `f2023e85c9b44b925cf361cf48e2fc0d81beeab1`
- ZIP: `releases/EarthStick_v1.0.zip`
- SHA256: `8b399d70df582c448ed2bfdf532d5dcc17f579187f99a4d165bd06ef1cb0c292`

Do not reinvent or casually change EarthStick 1.0.

---

# 5. EARTH BEACON 1.0 — FINISHED / LIVE-TESTED

Repository:
https://github.com/Jim-dc95811/Earth-Beacon

Core idea:

> **A pin marks a place. A beacon gives you something to aim at.**

Earth Beacon creates a tall vertical KML line anchored to a geographic coordinate, producing a long-range horizon-visible destination inside ArcGIS Earth.

Live behavior already verified:
- clear vertical beacon against horizon
- visible from very long range
- screenshot previously showed approximately 102 km eye altitude with beacon still visible
- user reports visibility from extreme regional distances in favorable views
- near/parallel to ground, vertical line effectively collapses visually and becomes unobtrusive
- layers can be toggled on/off

Default v1.0 beacon:
- height 100 km
- red
- width 6
- `relativeToGround`
- KML output
- optional auto-open

Coordinate sources:
- manual lat/lon
- Windows clipboard
- current ArcGIS Earth camera position through Automation API

Clipboard handling includes lat/lon swap and ambiguity protection.

Useful combination:

> **EarthStick makes horizon flight practical. Earth Beacon makes horizon flight navigable.**

---

# 6. THE BIG UX REALIZATION — ARCGIS EARTH BECOMES A PLACE

Before joystick control, ArcGIS Earth behaves largely like something a user operates.

After joystick control, it becomes somewhere a user can **go**.

Useful project phrase:

> **A $90 joystick didn’t improve ArcGIS Earth. It activated it.**

The joystick acts like water on a dormant desert seed: the imagery, TPKX, parcels, KML, scene layers, API, 3D camera, and GIS datasets were already present, but direct analog navigation makes them connect into one experience.

SpaceMouse is a useful contrast:
- SpaceMouse = manipulate a 3D camera/view
- EarthStick = navigate a geographic world

ArcGIS Earth already had many pieces—TPKX, SpaceMouse support, KML, 3D, Automation API—but they were not organized around a natural “go there” interaction metaphor.

---

# 7. BASEMAPS AS GAME / TRAINING MECHANICS

A major new concept is that changing basemaps can itself be part of the problem-solving mechanic.

Examples:
- imagery to identify a real building, clearing, old runway, shoreline, obstruction
- street map to identify named roads, addresses, route numbers, businesses
- topo to solve ridge/drainage/slope/elevation problems
- hybrid to reconcile ground appearance with labels
- parcel layers to identify ownership/boundaries/access
- historical maps/imagery to determine what used to exist
- current vs older imagery to identify change
- weather/fire/flood/live overlays to determine current viability

Key phrase:

> **The map is not the answer. Choosing the right map is part of the answer.**

This turns GIS literacy into gameplay/training without requiring the user to feel like they are studying GIS software.

The same system can switch back to a conventional flat/2D operational basemap within seconds. The user does not leave the GIS or change applications; only the view/visual language changes.

> **Explore in 3D. Navigate in horizon view. Interact with objects. Flatten back to a standard map whenever needed.**

---

# 8. “MAPWORLD” CONCEPT — INTERNAL ONLY / NAME NOT FINAL

The conceptual idea remains important even though the name is not favored as a final brand.

Same Earth can host different visual/data worlds:
- imagery world
- street-map world
- topo world
- parcel world
- historical world
- weather world
- utility world
- 3D world
- live incident world

Important realization:

> **The mechanics can be universal while the world stays completely local.**

Kansas City, Chicago, Toronto, Jacksonville, or any other place can use the same EarthStick / Beacon / object / scenario mechanics while loading local imagery, roads, parcels, hydrants, history, hazards, photos, and objectives.

Objects can be real or abstract. If something can have a place, shape, state, time, meaning, or rule, it can potentially become a geographic object.

Important later step:

> **Objects can change other objects.**

Python can maintain scenario state and reveal/load/remove/update small object layers without rebuilding foundation maps.

---

# 9. OBJECT FACTORY — CURRENT MAJOR DEVELOPMENT

The Object Factory is now the major active development direction.

Reason for existence:

> **Choose an object → choose where it lives → choose how it appears → choose what it contains/does → create it.**

The user should not have to understand KML syntax, XML, GIS feature-class design, 3D coordinate rules, image optimization, or KMZ packaging.

The Object Factory should feel like simple object authoring, not GIS administration.

### Proposal artifact
A PDF proposal was created in this conversation:
- `ArcGIS_Earth_Object_Factory_Proposal_v0.1.pdf`

It is a design proposal, not an accepted released product.

### Proof-of-function artifact
A separate proof kit was created:
- `Object_Factory_POF_v0.1.zip`

The kit intentionally used multiple independent proof scripts before integration, per user authorization.

The kit included three main proof functions:
1. generic airborne PNG object
2. batch object-list → KMZ generation
3. generated NSEW sky compass

The POF package was conversation-generated and was not yet committed to the GitHub repository at the time of this continuity update.

---

# 10. POF1 — GENERIC AIRBORNE PNG OBJECT — LIVE-PROVEN

User live-tested POF1 in ArcGIS Earth.

Test object:
- a **flying fire-truck PNG** placed in the sky at geographic coordinates/altitude

Observed result:
- object rendered correctly
- fixed location/altitude behavior worked
- icon was clearly visible in the sky
- no-label-until-click behavior worked
- click information worked
- optional tether behavior worked
- the user described the result as essentially perfect except for the oversized ArcGIS Earth information box

Status:

> **POF1 airborne PNG primitive = LIVE-PROVEN**

This proves that the balloon concept generalizes to arbitrary PNG objects such as:
- helicopter
- airplane
- drone
- fire truck
- fuel pump
- hospital symbol
- warning symbol
- bird
- clue icon
- house/home
- staging marker
- water source
- camera
- virtually any transparent PNG

Important distinction:
- PNG object = billboard/symbol-like visual object at geographic altitude
- standalone 3D model = true physical 3D object with world scale/orientation

Both may eventually belong in the factory.

---

# 11. POF2 — BATCH OBJECT LIST → MULTI-OBJECT KMZ — LIVE-PROVEN

User live-tested POF2 in ArcGIS Earth.

Observed behavior:
- one simple object list generated multiple different object types
- different icons worked
- different locations worked
- different information content worked
- resulting objects were packaged into one KMZ
- click-to-reveal behavior worked

A “Mystery Bird” example proved the educational mechanic:

> **see object → guess → click → reveal**

Status:

> **POF2 batch world/object-pack generation = LIVE-PROVEN**

This is a major architectural win because it means a teacher, trainer, or ordinary user can create an entire geographic object set from a simple list rather than manually authoring GIS features one at a time.

Example simple list concept:

```text
fuel,30.410104,-81.922396
heli,30.398210,-81.931440,300
water,30.402778,-81.918620
home,30.385525,-81.930807
```

Presets can supply default icon, altitude, size, visibility, and popup behavior.

---

# 12. POF3 — NSEW SKY COMPASS — LIVE-PROVEN

User live-tested the generated Sky Compass in ArcGIS Earth.

Concept:
- giant **N**, **E**, **S**, **W** visual objects
- positioned far from the operating center
- elevated high in the sky
- used as permanent horizon orientation anchors

The user tested the output and showed the giant directional markers visible in the horizon view.

Status:

> **POF3 generated sky compass = LIVE-PROVEN**

This is not merely decorative. EarthStick makes the horizon a persistent working view, so the sky compass functions like a geographic heads-up orientation system.

Conceptual relationship:

> **Sky Compass = orientation**  
> **Earth Beacon = destination**  
> **EarthStick = movement**

The exact ideal radius/altitude/icon size can continue to be tuned, but the foundation concept works.

---

# 13. THE SKY IS NOW A PROGRAMMABLE INFORMATION LAYER

The balloon/PNG tests produced a major project realization.

User phrase:

> **We own the sky.**

Then:

> **We control the sky.**

Meaning:
ArcGIS Earth’s sky can contain arbitrary geographic symbols/objects that do not need to obey real-world physical constraints.

Possible sky objects:
- helicopters
- balloons
- giant directional letters
- fuel pumps
- warning symbols
- checkpoints
- targets
- route markers
- clue icons
- giant arrows
- observation markers
- floating signs
- camera/viewpoint icons

A floating gas-pump symbol over a real fuel stop can simply mean:

> **Use this fuel stop.**

A floating helicopter can identify an aviation point.

A giant `N` can orient the user.

A bird can become a classroom identification question.

The object itself carries the first layer of meaning.

Preferred information hierarchy:

> **See it → recognize it → click it → understand it.**

For most objects, **no visible label until clicked** is preferred. This prevents sky/world clutter.

---

# 14. OBJECT FACTORY PRESET DIRECTION

The factory should be built around a generic object engine plus presets, not custom code for every icon.

Likely first-class object/preset families:
- Beacon
- Airborne PNG
- Pin / ground icon
- Balloon
- Helicopter
- Fuel Stop
- Hazard
- Bird / lesson object
- Fire Truck
- Hospital / medical
- Water source
- Staging
- Home/Base
- Camera / Viewpoint
- Sky Compass
- later: standalone 3D model
- later: route/line/search-zone objects

Common fields may include:
- object name
- latitude
- longitude
- altitude
- altitude mode
- icon/image
- display size
- label visibility
- popup mode
- popup title/body
- optional tether
- optional URL
- optional local file/photo

3D objects may additionally require:
- scale
- heading
- tilt
- roll
- model file

---

# 15. PNG HANDLING — USER-APPROVED FACTORY RULE

The user explicitly approved automatic PNG normalization.

Factory behavior should be:

1. User selects a PNG.
2. Factory inspects it.
3. User’s original file is **never modified**.
4. Factory makes a working copy for the KMZ.
5. Maximum working dimension = **256 px**.
6. Preserve aspect ratio.
7. Preserve transparency.
8. Do not aggressively upscale smaller source icons; a clean 128×128 source can remain 128×128.
9. Package only the normalized working copy into the KMZ.

This keeps object packs lean without asking users to understand image optimization.

Selection-time information panel should ideally show:
- preview
- dimensions
- file size
- transparency yes/no
- aspect ratio
- simple quality/status message

Possible guidance:
- ideal: 128–256 px
- 512 px: acceptable source, normalize for package
- oversized source: warning, then normalize
- corrupt/non-PNG: reject

These are friendly guardrails, not a GIS lecture.

---

# 16. POPUP BOX ISSUE — ONLY COMMON POF DEFECT SO FAR

POF1 and POF2 both showed the same issue:

> ArcGIS Earth’s native KML information/popup box is visually much larger than desired.

The user otherwise described both proof functions as perfect.

Treat this as a **presentation issue**, not a failure of the object architecture.

Current direction:
- keep popup content concise
- support **Info on Click** and **No Popup** modes
- use short title/body
- avoid unnecessary blank content
- do not make labels permanently visible just to compensate for the popup

The factory should not let the oversized popup block development of the object system.

---

# 17. GOOGLE MAPS → OBJECT LIST — ULTRA-SIMPLE AUTHORING WORKFLOW

A major accessibility insight:

A user can go around Google Maps, right-click locations, copy coordinates, and build an object list in minutes.

Authoring flow:

> **find place → copy coordinate → choose object type → add to list → build KMZ → open in ArcGIS Earth**

This can be done without ArcGIS Pro, QGIS, feature classes, schemas, projections, or manual KML editing.

This is especially powerful for schools.

Students could quickly build:
- landmarks
- history objects
- hazards
- bird/animal lessons
- resource points
- scavenger hunts
- community mapping projects

The educational question becomes:

> **What should we put in the world?**

instead of:

> “How do I operate GIS software?”

---

# 18. CLASSROOM / LESSON OBJECTS

A bird object produced an important lesson pattern.

Example:
1. place a bird PNG at a geographic location/habitat
2. no label
3. student flies toward it
4. student guesses species
5. click reveals answer and information

Loop:

> **See it → inspect it → guess → click → reveal → move on**

The same mechanic works for:
- birds
- trees
- animals
- insects
- clouds
- aircraft
- vehicles
- historical buildings
- road signs
- fire-service equipment
- landmarks

Geography can be part of the lesson: the object may be placed in the habitat/context where the concept makes sense.

This makes the Object Factory potentially a **lesson factory**.

---

# 19. SCAVENGER HUNT / GAME DIRECTION

Existing scavenger-hunt architecture remains active.

Core mapping:

> **world = ArcGIS Earth / real GIS**  
> **movement = EarthStick**  
> **navigation = Earth Beacon / sky objects**  
> **objects = KML/KMZ, GeoJSON, GIS features, PNG/3D objects**  
> **missions = attributes + layers + Python state**  
> **players = whoever has the joystick**

Important mechanic:

> **Knowledge unlocks geography.**

Possible progression:

> find clue → hover → inspect → answer/make decision → acceptable response → next beacon/object appears → fly toward it

Beacons/objects can be rewards as well as navigation aids.

This progression controller is still conceptual unless/until separately built and live-tested.

---

# 20. FIREFIGHTER INCIDENT TRAINING DIRECTION

The scavenger-hunt mechanic translates naturally into serious spatial-decision training.

Possible progression:

> **Dispatch → Recon → Choose access → Locate water → Select staging/LZ → Identify egress → Receive update → Reassess**

Potential objects/layers:
- access routes
- egress routes
- hydrants/water
- staging
- landing zones
- structures
- parcels/ownership
- road choke points
- closures
- jurisdiction
- terrain/obstacles
- hazards
- safety/search areas

Adult scenarios should support multiple defensible answers rather than assume one rigid “correct” decision.

The big advantage is repeatability without repeatedly staging apparatus, personnel, props, travel, and site logistics.

This is not a substitute for hands-on training; it is a geographic familiarization and decision-making environment.

---

# 21. VIEWPOINT / CAMERA OBJECT — NEW MAJOR DIRECTION

A new object class emerged from the clickable-link discussion:

> **Camera / Viewpoint Object**

The geographic object means:

> **There is another way to see this place.**

Possible viewpoint types:
- live webcam
- Street View link
- still photo
- recorded video
- web page
- other online/local visual resource

Important clarification from user:

Do **not** try to force live video to play inside ArcGIS Earth’s own popup.

Preferred architecture:

> **floating camera icon in ArcGIS Earth → click/open → small separate viewer floats on top of ArcGIS Earth**

Possible Camera Viewer behavior:
- always-on-top
- compact movable window
- resize
- close
- refresh
- mute/unmute when relevant
- reuse one viewer window instead of spawning many

ArcGIS Earth remains the geography/rendering environment. The small viewer handles web/video content.

Possible architecture:

> **ArcGIS Earth = geography**  
> **Object Factory = geographic objects**  
> **Camera Viewer = external live/street/photo/video view**

The exact launch/click integration still needs a dedicated proof-of-function.

---

# 22. OFFLINE-FIRST + OPTIONAL ONLINE EXTENSION

One of the strongest recurring patterns is that the system’s core capabilities keep working without internet:
- TPKX worlds
- EarthStick
- Earth Beacon
- Sky Compass
- PNG objects
- batch KMZ object packs
- local photos/info
- training/scenario layers

Internet should enhance objects, not make them useless when connectivity disappears.

Preferred object design:

### Embedded / Offline
- title
- description
- coordinates
- local icon/photo
- instructions
- local reference information

### Optional Online
- URL
- live webcam
- Street View
- current incident page
- weather page
- agency page
- training video
- equipment manual
- other web resource

Core principle:

> **Offline object = useful by itself. Connected object = potentially unlimited extension.**

---

# 23. LIVE WEBCAM / STREET VIEW CONCEPT

A floating camera object could represent either:
- live webcam, or
- a Street View location/panorama link, or
- another viewpoint resource

Examples:
- traffic camera
- beach/weather camera
- fire observation camera
- airport camera
- river/port camera
- facility entrance
- public street-level view

Clicking/opening the object could launch the small always-on-top viewer while the user continues to fly ArcGIS Earth underneath.

This creates a powerful sequence:

> **air view → GIS context → ground/live view → continue navigation**

This feature is conceptual and needs a dedicated POF.

---

# 24. 3D OBJECTS REMAIN AN IMPORTANT FUTURE BRANCH

ArcGIS Earth supports standalone 3D models such as DAE/OBJ/GLTF/FBX/3DS and can geographically position/scale/orient them.

Potential factory objects:
- true 3D helicopter
- tower
- tree
- vehicle
- treasure chest
- sign
- aircraft
- animal
- training prop
- fantasy object

Difference from PNG sky object:
- PNG = lightweight billboard/symbol
- 3D model = real spatial object with physical world scale/orientation

The PNG route should remain the easy/default path. 3D models are a later higher-complexity extension.

---

# 25. 3D GIS / DRAGONFLY MODE

EarthStick has already been used in the public Frankfurt Integrated Mesh scene.

Observed:
- user flew through/around towers
- hover/circle/climb/descend/re-approach worked
- no collision; camera can pass through buildings
- user described experience as flying around “like a dragonfly”

The particular Frankfurt source scene was not visually/performance impressive enough to be the main showcase, but it proved EarthStick can navigate 3D GIS environments.

---

# 26. HARDWARE / PERFORMANCE — IMPORTANT CURRENT EVIDENCE

A firefighter demo laptop is now fully prepared.

Known laptop configuration:
- Dell laptop
- 32 GB RAM
- Intel Core i7-1185G7 @ approximately 3 GHz
- 4 GB graphics allocation/device memory as reported by user

User reports:

> **working like a champ, smooth as ice**

The laptop also opens the map/project files noticeably faster than the home PC.

Home PC comparison:
- user reports only 128 MB graphics versus 4 GB on the Dell

Important conclusion:

> The current operational EarthStick/Beacon/object workflow does **not** require exotic gaming hardware to feel good.

The Dell is especially valuable as a demo platform because it resembles plausible agency/business hardware rather than a laboratory gaming monster.

Heavy 3D scene/mesh work may still benefit substantially from a discrete modern GPU.

---

# 27. GAMING-PC SHOPPING CONCLUSION

Earlier discussion initially drifted too high in price. User correctly pointed out that many sub-$1,000 systems appear to be in the relevant performance ballpark.

Current practical target for an affordable experimentation desktop:
- Windows 11
- RTX 4060 / RTX 5060-class discrete GPU or better
- roughly 8 GB dedicated VRAM
- 32 GB RAM preferred
- 1 TB NVMe or larger
- modern Ryzen 5 / Core i5 or better

This is not a formal requirement; it is a sensible “see what ArcGIS Earth can do with real GPU headroom” target.

A GMKtec M5 Ultra listing was reviewed:
- Ryzen 7 7730U
- 32 GB RAM
- NVMe
- integrated Radeon graphics

Conclusion: good compact general-purpose PC, but **not** the ideal machine for testing the 3D/GPU ceiling because it lacks a true discrete RTX/Radeon-class GPU.

Do not assume expensive hardware is required for the normal operational system—the Dell already disproves that.

---

# 28. FIREFIGHTER DEMO — CURRENT STATUS

A firefighter demonstration is planned for Friday immediately following this continuity date.

Current status:
- Dell demo system fully up
- software/data loaded
- user reports smooth performance
- several dry runs planned/performed
- demo is ready

Purpose:
- judge real firefighter interest
- watch for unsolicited use-case ideas
- see whether people immediately start imagining operational uses

High-value spontaneous questions to listen for:
- Can it show hydrants?
- Can it show our stations?
- Can we use this for preplans?
- Can it show parcel ownership?
- Can we load our imagery?
- Can I put this on my laptop?
- Could we train with this?

Important evaluation question:

> **Does EarthStick merely impress people, or does it immediately make them start inventing uses for it?**

The demo should let the system sell itself: real local map, joystick flight, hover/inspect, parcel/operational layer, basemap changes, beacon navigation, offline capability.

---

# 29. CLASSROOM / MULTI-PILOT CONCEPT

Still active concept:
- one shared ArcGIS Earth display
- many joysticks
- one active pilot at a time
- instructor chooses pilot
- neutral control = safe hover/handoff state

Phrase:

> **One Earth. One classroom. Twenty pilots.**

Possible network USB/Silex architecture was discussed previously, but no classroom selector has been built.

Object Factory makes this classroom direction much stronger because students can also author the world themselves using coordinate lists and simple icons.

---

# 30. FACILITY PHOTOS / AIR-TO-GROUND RECOGNITION

Still important:
- office/station/facility icon
- click → local photo + address + entrance/gate information

Agency-owned still photos are attractive because the agency controls freshness, rights, framing, and operational relevance.

Useful photos:
- front entrance
- apparatus entrance
- gate
- parking/access
- helipad/LZ
- fuel point
- confusing approach feature

Concept phrase:

> **air-to-ground recognition layer**

KMZ remains a strong candidate because it can bundle supporting assets.

---

# 31. BROADER OFFLINE MAP FOUNDATION — STILL VALID

The existing offline map ecosystem remains important and should not be rediscovered from scratch.

Primary path:
- QGIS → MBTiles JPG/75 → Python MBTiles→TPKX converter → ArcGIS Earth

Repository:
https://github.com/Jim-dc95811/QGIS-Mbtile-to-ArcGIS-Earth-TPKX

Verified historical outcomes:
- converter works
- small proof tiles work
- 4 GB MBTiles conversion works
- approximately 40–50 GB MBTiles conversions worked
- resulting TPKX opens in ArcGIS Earth and ArcGIS Pro
- offline TPKX can render extremely quickly
- JPG/75 MBTiles reduced size dramatically versus PNG while retaining useful visual clarity

ArcGIS Earth prefers uncompressed TIFF when using GeoTIFF directly; TPKX remains the stronger large-area operational format.

The foundation-map work is what makes the newer object system especially powerful: the world can remain fully local/offline while objects are layered above it.

---

# 32. CURRENT VERIFIED VS CONCEPTUAL STATUS

## LIVE-PROVEN / ACCEPTED OR FUNCTIONALLY VERIFIED
- EarthStick 1.0 direct joystick flight
- neutral stop/hover
- horizon navigation
- parcel/feature interrogation while flying
- Earth Beacon 1.0 long-range KML beacon
- manual beacon layer show/hide
- Frankfurt 3D EarthStick flight
- offline TPKX world workflow
- airborne PNG object at geographic altitude
- generic flying fire-truck PNG test
- no-label-until-click object behavior
- click information on PNG object
- batch object-list → multi-object KMZ
- Mystery Bird click/reveal example
- generated NSEW Sky Compass
- giant directional sky letters visible in horizon view
- Dell i7-1185G7 / 32 GB / 4 GB-graphics demo machine running the system smoothly

## VERIFIED BUT NEEDS PRESENTATION TUNING
- ArcGIS Earth native KML popup/info box works, but is larger than desired

## DESIGN LOCKED / USER-APPROVED BUT NOT YET INTEGRATED
- preserve source PNG untouched
- normalize KMZ working PNG to max 256 px dimension
- preserve aspect ratio/transparency
- do not unnecessarily upscale small clean images
- no-label default for most world objects
- generic object engine + presets

## CONCEPTUAL / NOT YET BUILT OR NOT YET LIVE-VERIFIED
- integrated Object Factory GUI
- Camera / Viewpoint object launcher
- always-on-top Camera Viewer
- live webcam launch/viewer
- Street View viewpoint launch
- 3D-model object factory branch
- answer-triggered progressive object/beacon reveal
- scenario state controller
- scoring engine
- AI-authored hunt generator
- firefighter GIS Incident Scenario Builder
- classroom joystick selector
- multi-operator/coproilot handoff
- synchronized multi-screen Earth views
- bulk district object generator beyond current POF batch list

Do not blur the above categories.

---

# 33. OBJECT FACTORY BUILD PRIORITY FROM HERE

Because all three risky POF foundations worked, the next step should move from isolated proofs into the first real Object Factory build.

Recommended integration order:

1. shared object schema
2. generic airborne PNG creator
3. PNG inspection + 256 px normalization
4. no-label default
5. concise Info / No Popup modes
6. batch object-list importer
7. preset library
8. Sky Compass generator
9. accepted Beacon functionality
10. KMZ output packaging
11. later: URL / viewpoint object support
12. later: Camera Viewer POF
13. later: standalone 3D model support

Do not overbuild the first integrated factory. The proven primitives are already enough to make a powerful useful product.

---

# 34. IMPORTANT CURRENT PHRASES / FRAMING

Keep these available because they capture the project accurately:

> **Fly the real map.**

> **A pin marks a place. A beacon gives you something to aim at.**

> **Stop. Hover. Think. Then move.**

> **EarthStick makes horizon flight practical. Earth Beacon makes horizon flight navigable.**

> **A $90 joystick didn’t improve ArcGIS Earth. It activated it.**

> **The map is not the answer. Choosing the right map is part of the answer.**

> **See it → recognize it → click it → understand it.**

> **Offline object = useful by itself. Connected object = potentially unlimited extension.**

> **The mechanics can be universal while the world stays completely local.**

> **The world is already built. We just add the objects.**

User phrases worth preserving:

> **We own the sky.**

> **We control the sky.**

> **Sky’s the limit.**

---

# 35. NEXT-SESSION STARTING POINT

If a reset occurs immediately after this file:

1. Do **not** rebuild or redesign EarthStick 1.0.
2. Do **not** rebuild or redesign Earth Beacon 1.0 unless specifically asked.
3. Read `MAPWORLD.md` for the existing ArcGIS Earth format inventory.
4. Treat Object Factory as the active build.
5. Remember that POF1, POF2, and POF3 have all been live-tested successfully.
6. The only common visual complaint from POF1/2 is the oversized native popup box.
7. Preserve the user-approved 256 px PNG normalization rule.
8. The next likely development task is integrating the proven POF components into the first real factory GUI.
9. Keep the architecture offline-first.
10. Treat online/webcam/Street View links as optional object extensions, preferably through a separate small viewer rather than forcing media into ArcGIS Earth’s popup.
11. The Friday firefighter demo system is already up and running smoothly on the Dell laptop.
12. The umbrella public name is **not settled**; use “ArcGIS Earth + …” as the naming direction rather than assuming “Mapworld” is final.

---

# 36. CURRENT ONE-LINE SUMMARY

> **EarthStick makes ArcGIS Earth navigable, Earth Beacon gives it long-range destinations, and the now-proven Object Factory primitives let ordinary users populate both the ground and sky with geographic objects—offline first, with online links opening an effectively unlimited second layer.**
