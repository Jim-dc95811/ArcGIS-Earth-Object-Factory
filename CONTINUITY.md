# Earth Beacon — Continuity

## Current accepted version

**Beacon Maker v1.0** is the accepted baseline.

Release package:

```text
releases/Beacon_Maker_v1.0.zip
```

SHA-256:

```text
d53559ac33b84c148f97e14094a6a6f8249583ea068f1606ecf1add7f4b68535
```

## Accepted behavior

Coordinate sources:

- manual latitude / longitude
- Windows clipboard
- current ArcGIS Earth camera coordinates

Beacon output:

- standard KML 2.2
- base Point plus vertical LineString
- `relativeToGround`
- default height 100 km
- default width 6
- default red
- user-selectable height, width, and color

Clipboard behavior:

- labeled coordinates are recognized directly
- range is used to infer order when possible
- ambiguous unlabeled pairs are identified to the operator
- Swap Lat/Lon is available

## Live verification

v1.0 generated a functioning KML beacon that loaded in ArcGIS Earth and remained clearly visible in a long-range tilted 3D view at roughly 102 km eye altitude.

Proof image:

```text
assets/Earth_Beacon_ArcGIS_Earth.jpg
```

## Modification rules

1. Preserve the accepted v1.0 behavior unless a change is explicitly requested.
2. Make one functional change at a time when practical.
3. Give functional changes a new version number.
4. Do not silently change coordinate interpretation, KML altitude mode, default height, default width, colors, API URL, or output geometry.
5. Run the built-in self-test after code changes.
6. A changed release is not accepted until its KML is live-tested in ArcGIS Earth.
7. Keep Earth Beacon independent from EarthStick; integration should not be required for either utility to work.
8. Prefer operational simplicity over feature accumulation.

## Companion project

EarthStick:

https://github.com/Jim-dc95811/EarthStick

EarthStick and Earth Beacon complement each other but remain separate applications.
