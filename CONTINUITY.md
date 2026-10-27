# CONTINUITY — EarthStick + Earth Beacon
**Date:** 2026-10-27  
**Purpose:** Preserve the exact current state, live-tested facts, published repositories, and new concepts from this session.

---

## 1. CORE PROJECT STATE

### EarthStick 1.0 — FINISHED / LIVE-ACCEPTED
Repository: https://github.com/Jim-dc95811/EarthStick

EarthStick turns ArcGIS Earth into a directly piloted map using the Thrustmaster TCA Sidestick Airbus Edition.

Core public idea:

> **Fly the real map.**

EarthStick is not a flight simulator. The actual ArcGIS Earth GIS/map becomes the world being flown.

### Accepted controls
- Stick X = strafe left/right
- Stick Y = forward/reverse
- Twist = heading
- Physical throttle = travel speed
- POV up/down = camera tilt
- Red top button = zoom in / descend
- Black thumb button = zoom out / climb
- Neutral controls = stop / hover

### Important behavioral fact
Neutral input is not merely “nothing happens.” It creates a useful operational state:

> **Stop. Hover. Think. Then move.**

This is one of the most important EarthStick advantages over keyboard/mouse or SpaceMouse control. The operator can stop completely, inspect the map, change layers, decide what to do next, and continue without fighting the camera.

### Operational insight
Keyboard/mouse or SpaceMouse control consumes attention maintaining camera attitude, horizon, heading, speed and position.

EarthStick reduces that camera-control workload enough that the operator can actually **observe the GIS while moving through it**.

---

## 2. EARTH BEACON 1.0 — FINISHED / LIVE-TESTED

Repository: https://github.com/Jim-dc95811/Earth-Beacon

Earth Beacon creates a tall vertical KML line at a geographic coordinate so the location remains visible from very long distances in an oblique ArcGIS Earth view.

Core public idea:

> **A pin marks a place. A beacon gives you something to aim at.**

Earth Beacon uses standard KML 3D geometry. The geometry itself is not claimed as a new invention. The unusual part is using the vertical line intentionally as a long-range visual navigation/homing marker inside ArcGIS Earth.

### Live-tested behavior
User created the beacon and tested it in ArcGIS Earth successfully.

Observed live behavior:
- Red vertical beacon clearly visible against the horizon.
- Screenshot showed approximately 102 km eye altitude while the beacon remained plainly visible.
- The beacon is useful from very long distance.
- When oriented essentially parallel to the ground at/near the beacon, the vertical line becomes effectively invisible.
- This is desirable behavior: obvious while approaching, unobtrusive when working close to the destination.

### Beacon Maker v1.0
Coordinate input methods:
- Manual latitude / longitude
- Windows clipboard
- Current ArcGIS Earth camera position through Automation API

Clipboard handling supports:
- comma-separated coordinates
- whitespace-separated coordinates
- labeled latitude/longitude
- ambiguous coordinate pairs are flagged rather than silently treated as certain
- Swap Lat/Lon button

Default beacon:
- 100 km tall
- red
- line width 6
- `relativeToGround`
- KML output
- optional automatic open after creation

The v1.0 source/package was live-tested before the GitHub page was built.

---

## 3. EARTHSTICK + EARTH BEACON — THE IMPORTANT COMBINATION

Earth Beacon by itself is a clever geographic marker.

EarthStick gives it operational purpose.

The combination is:

> **EarthStick = movement**  
> **Earth Beacon = destination**  
> **GIS layers = meaning**

Or:

> **Drop a beacon anywhere on Earth, then fly the real map toward it.**

Before EarthStick, a horizon-visible KML pillar had limited practical value because ordinary ArcGIS Earth navigation requires too much camera manipulation.

With EarthStick, the operator can:
1. acquire the beacon visually
2. fly toward it
3. stop/hover anywhere
4. inspect the map
5. change layers
6. resume flight
7. arrive without losing orientation

This creates a simple visual navigation language inside ArcGIS Earth.

---

## 4. CURRENT HIGH-VALUE BEACON USES

### Fixed facilities
Possible district-wide persistent beacon layer for:
- offices
- fire stations
- yards
- dispatch locations
- training sites
- staging areas
- landing zones
- other fixed operational facilities

Concept name:

> **District Beacon Network**

This would allow an operator to answer visually:

> “Where is that facility from here?”

without calculating a bearing or searching a flat map.

### Incident / operational targets
Potential beacons for:
- incident locations
- staging
- ICP
- landing zones
- parcel / tract targets
- search sectors
- inspection points
- home base

### Feature-derived beacons
Any existing GIS point feature could theoretically generate a beacon.

Example discussed:
- fire hydrants

Potential encoding:
- blue = hydrant
- green = tested / available
- yellow = limited
- red = out of service
- height/color could encode attributes

Important design insight:
Do **not** display enormous beacons for every feature across a huge region at once. Use an AOI, incident radius, selected grid, filtered subset, or similar visibility logic to avoid visual spaghetti.

---

## 5. BEACON TOURS — “FOLLOW THE RAINBOW”

A sequence of differently colored beacons can become a visual route/tour without drawing a continuous route line.

Example concept:
- red
- orange
- yellow
- green
- cyan
- blue
- magenta

Operator simply flies from one visible beacon to the next.

Phrase:

> **Follow the rainbow.**

Potential uses:
- helicopter route familiarization
- district familiarization
- wildfire/disaster walkthroughs
- utility corridor inspections
- river/coastline tours
- historical tours
- forestry tracts
- scenic tours
- training routes
- presentations where the instructor wants the viewer to visit a series of specific locations

Possible future utility:

> **Earth Beacon Tour Maker**

Potential input:
- list of coordinates
- optional names
- automatic sequential colors
- one generated KML containing the complete tour

Not built yet.

---

## 6. MULTI-OPERATOR / COPILOT CONCEPT

EarthStick controls ArcGIS Earth through its Automation API.

Infrastructure insight:
If ArcGIS Earth instances/endpoints can be independently addressed, the same control stream could theoretically be sent to more than one Earth display or transferred between operators.

Possible roles:
- primary operator
- copilot / relief operator
- local expert
- instructor

### Port-pilot analogy
A local expert could temporarily take control of the map exactly like a harbor/port pilot takes temporary navigational responsibility aboard a ship.

They do not replace the main operator. They bring local knowledge for a specific geographic area.

Examples:
- district staff who know one county extremely well
- forester who knows a tract
- utility worker who knows a corridor
- fire officer who knows a response area
- emergency manager with local knowledge

They could say while actually flying the shared map:
- “That road washes out.”
- “That gate is usually locked.”
- “Come in from this side.”
- “That is our tract.”
- “That crossing is the one you want.”

Concept phrase:

> **Local pilotage for the map.**

No multi-user control software has been built yet.

---

## 7. MULTIPLE ARCGIS EARTH DISPLAYS — INFRASTRUCTURE IDEA

ArcGIS Earth Automation API uses a configurable base URL; the default is `http://localhost:8000`.

Theoretical architecture:

- Earth display 1 = imagery
- Earth display 2 = roads / labels
- Earth display 3 = parcels / operational GIS
- all displays receive the same camera state

This could create a multi-screen GIS cockpit where all views move together but each screen carries different layers.

Important status:
- Multiple networked computers/endpoints are conceptually straightforward.
- Multiple simultaneous ArcGIS Earth processes on one Windows machine using separate API ports has **not been live-tested**.
- Do not treat that specific same-PC behavior as proven.

---

## 8. CLASSROOM CONCEPT

One ArcGIS Earth instance appears on a shared classroom screen.

Each student has a joystick.

Only one joystick has control authority at a time.

Instructor selects the active pilot through a small GUI.

Basic control model:
- Student 1 — available
- Student 2 — available
- Student 3 — PILOT
- Student 4 — available
- Instructor takeover
- Stop / hover
- next pilot

Handoff sequence:

> **fly → release controls → hover → transfer authority → next student flies**

Because neutral input means stop/hover, EarthStick is unusually well suited for controlled handoffs.

### Educational value
Students would not feel like they were being taught GIS software.

They would feel like they were:

> **taking turns flying the world**

While doing so they learn:
- spatial orientation
- distance and scale
- terrain recognition
- landmarks
- roads
- jurisdictions
- layer interpretation
- map-to-world recognition
- route selection
- observation before movement

Possible classroom challenges:
- fly to the next beacon
- find the county line
- identify location with labels off
- follow a river
- find a facility using imagery only
- navigate a route by a sequence of beacons

Phrase:

> **One Earth. One classroom. Twenty pilots.**

No classroom selector GUI has been built yet.

---

## 9. CLASSROOM USB INFRASTRUCTURE CONCEPT

Silex Technology network USB/device-server products were discussed as a practical way to bring many student USB joysticks back to one central Windows computer.

Possible architecture:

Student joysticks  
→ network USB / Silex device servers  
→ central Windows PC  
→ Python joystick-selector GUI  
→ EarthStick control engine  
→ ArcGIS Earth  
→ classroom display/projector

Preferred software concept:
- Windows sees all joysticks
- Python enumerates them
- instructor chooses which joystick ID is currently listened to
- all non-selected joysticks are ignored
- USB connections do not need to be physically switched for every student handoff if all devices can remain available to Windows

Possible GUI:
- student name
- joystick/device status
- TAKE CONTROL
- ACTIVE PILOT
- INSTRUCTOR
- STOP/HOVER

This architecture is only conceptual. It has not been built or live-tested.

---

## 10. ROUTE FAMILIARIZATION / HELICOPTER USE

Important conceptual use:

An experienced helicopter pilot could use EarthStick to rehearse a route through real GIS/map imagery.

Useful sequence:
1. labels/borders/roads/operational layers ON
2. fly the intended route and learn names/features intellectually
3. switch to imagery only
4. fly the same route again
5. verify visual recognition without textual cues
6. optionally re-enable only mission-relevant overlays

This creates:

> **annotated pass → visual pass**

and a learn/remove-cues/verify-recognition loop.

Earth Beacon adds visible destinations and route legs to that process.

Do not turn this into unnecessary aviation disclaimer language when the user is discussing conceptual map familiarization rather than asking for real flight instructions.

---

## 11. “GTA OF MAPWORLD” CONCEPT

User description:

> **“It’s the GTA of mapworld.”**

Useful meaning behind the joke:
- free roaming
- stop anywhere
- choose destinations
- follow beacons
- switch labels/imagery
- turn GIS layers on/off
- inspect features
- continue moving

Difference from a game:
- the world is the real GIS/map
- the features and layers carry real operational meaning

Useful framing:

> **In a game, the world exists to support the game.  
> Here, the real map is the world.**

---

## 12. IMPORTANT PRESENTATION / PHILOSOPHY

EarthStick should not be described merely as a joystick hack.

Its deeper value is:

> **continuous map observation under direct analog control**

The operator can actually study the map while moving through it.

Earth Beacon should not be described merely as a vertical KML line.

Its deeper value is:

> **turning a geographic coordinate into a long-range visual destination**

Together they form an operational system.

---

## 13. VERIFIED VS NOT YET VERIFIED

### VERIFIED
- EarthStick 1.0 live-tested and accepted.
- Neutral controls stop/hover.
- EarthStick provides clean direct map flight in ArcGIS Earth.
- Earth Beacon v1.0 creates a working vertical KML beacon.
- Beacon visible from very long range.
- User observed it becomes effectively invisible when viewed parallel to the ground.
- Clipboard coordinate import works in Beacon Maker.
- ArcGIS Earth camera coordinate import exists in Beacon Maker.
- Earth Beacon repository published.
- EarthStick repository published.

### CONCEPTUAL / NOT BUILT
- Beacon Tour Maker
- district bulk beacon generator
- automatic GIS feature → beacon conversion
- hydrant beacon generator
- beacon filtering by AOI/radius
- multi-operator EarthStick
- copilot control handoff
- classroom joystick selector
- Silex classroom joystick network
- synchronized multiple ArcGIS Earth displays
- multiple ArcGIS Earth instances on same PC using different API ports

Do not accidentally present these concepts as finished products.

---

## 14. CURRENT REPOSITORIES

### EarthStick
https://github.com/Jim-dc95811/EarthStick

### Earth Beacon
https://github.com/Jim-dc95811/Earth-Beacon

Related broader mapping ecosystem may include Parcel100, MBTiles→TPKX, offline ArcGIS Earth map generation and other tools, but those were not changed during this particular session.

---

## 15. NEXT-SESSION STARTING POINT

When resuming, do not reinvent EarthStick or Earth Beacon.

Both current v1.0 products are accepted.

The most fertile next directions are:

1. **Earth Beacon Tour Maker / Follow the Rainbow**
2. **bulk beacons from GIS point datasets**
3. **district facility beacon network**
4. **hydrant beacons with controlled visibility**
5. **classroom joystick-selector architecture**
6. **copilot/local-pilot control handoff**
7. **multi-screen synchronized ArcGIS Earth views**

Before building anything, preserve the Minimal Build Rule:
- implement only the requested function
- do not refactor accepted tools without approval
- preserve working filenames/paths/behavior
- make new versions for functional code changes
- do not call a version accepted until it is live-tested in ArcGIS Earth

---

## 16. CURRENT ONE-LINE SUMMARY

> **EarthStick lets you fly the real map. Earth Beacon gives you something to fly toward.**
