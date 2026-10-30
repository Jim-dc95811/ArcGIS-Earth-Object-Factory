# Changelog

## Object Factory v1.0 - 2026-10-29

First commissioned Object Factory release.

v1.0 is the accepted v0.2.2 TEST build promoted without feature redesign after live ArcGIS Earth verification.

- Single-object PNG/KMZ creation.
- 11 built-in object presets retained.
- Manual coordinates and **From Clipboard** workflow.
- Original PNG preservation and automatic <=256 px packaged normalization.
- `relativeToGround`, `absolute`, and `clampToGround` modes.
- Optional tether and label.
- Visible multiline Info text.
- Optional hyperlink in KML Info content.
- Info / No Popup modes.
- Batch object-list -> KMZ generation.
- 100-object batch self-test and duplicate-icon reuse.
- NSEW Sky Compass generator.
- Earth Beacon generator.
- Protected Create Object button area and visible Info-text field retained from the accepted v0.2.2 layout.
- v1.0 PDF User Manual published.

v1.0 source SHA-256:

`e77e1866e7a87b9824ed6bb1cd0f830f52adb1a2872efe48ede13a581018aa00`

## Object Factory v0.2 TEST - 2026-10-29

Integrated Object Factory UX simplification pass.

- Removed **From ArcGIS Earth** coordinate-source controls from the factory.
- Removed **Swap Lat/Lon**.
- Removed **Open after creation**.
- Kept manual coordinate entry and **From Clipboard** as the normal placement workflow.
- Strengthened the four main tabs: Objects, Batch, Sky Compass, Beacon.
- Preserved the working v0.1 object/KMZ generation behavior.
- Preserved PNG normalization to a maximum 256 px working dimension without modifying source images.
- Preserved optional hyperlink output.
- Preserved batch duplicate-icon reuse and 100-object self-test.

## Object Factory v0.1 TEST - 2026-10-29

First integrated factory build from three separately live-tested proof-of-function scripts.

- Objects tab
- Batch object-list tab
- Sky Compass tab
- Earth Beacon tab
- preset icon library
- PNG normalization
- labels off by default
- Info / No Popup modes
- optional hyperlink output
- batch stress test

## Proof-of-function stage - 2026-10-29

- **POF1:** generic airborne PNG object - live-tested in ArcGIS Earth.
- **POF2:** batch object-list -> multi-object KMZ - live-tested.
- **POF3:** generated NSEW Sky Compass - live-tested.

## Earth Beacon v1.0

Original standalone Beacon Maker accepted and live-tested in ArcGIS Earth.

The standalone release remains preserved at:

`releases/Beacon_Maker_v1.0.zip`

Earth Beacon subsequently became one of the main Object Factory tools rather than being discarded.
