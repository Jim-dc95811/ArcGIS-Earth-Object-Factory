# Earth Beacon — Technical Notes

## Accepted baseline

Beacon Maker v1.0 is the accepted live-tested baseline.

It is a Windows/Python standard-library utility with no third-party Python dependencies.

## Coordinate handling

Latitude is validated to `-90..90` and longitude to `-180..180`.

Clipboard parsing accepts labeled forms and raw decimal pairs. In Auto mode, numeric range is used when it can prove the order. When both values are valid latitudes, the pair is inherently ambiguous; v1.0 interprets it as Latitude, Longitude and warns the operator.

## ArcGIS Earth Automation API

The optional **From ArcGIS Earth** function sends an HTTP GET to:

```text
http://localhost:8000/arcgisearth/camera
```

It reads:

- `position.x` as longitude
- `position.y` as latitude

WKID 4326 is expected when the spatial reference is explicitly reported.

The API request uses a 1-second timeout. API failure does not prevent manual or clipboard operation.

## KML geometry

Each beacon is a KML `Placemark` containing a `MultiGeometry`:

- base `Point`
- vertical `LineString`

Both use `relativeToGround` altitude mode.

The line has two vertices at identical longitude/latitude:

```text
longitude,latitude,0
longitude,latitude,height_m
```

This is intentionally standard KML 2.2 geometry rather than a proprietary ArcGIS format.

## KML color format

KML uses `aabbggrr` byte order, not ordinary RGB hex notation.

Examples used by v1.0:

- Red: `ff0000ff`
- Yellow: `ff00ffff`
- Cyan: `ffffff00`
- Green: `ff00ff00`
- Magenta: `ffff00ff`
- White: `ffffffff`
- Orange: `ff0088ff`

## Default geometry

- height: 100 km / 100,000 m
- width: 6
- color: red

The height is user-configurable and converted from kilometers to meters before writing KML.

## Tested package

Official release:

```text
releases/Beacon_Maker_v1.0.zip
```

SHA-256:

```text
d53559ac33b84c148f97e14094a6a6f8249583ea068f1606ecf1add7f4b68535
```

Source SHA-256:

```text
2304bce131502a42aac76f2448e3dc07b03dece5f9976dfb1db53b07d2b60c88
```

Launcher SHA-256:

```text
bf6220002b0b9475755b3c32deefc50be717752e5fc30f00eb57772794d8ddf9
```

## Verification

Local code verification:

- Python compile: PASS
- built-in self-test: PASS

Live ArcGIS Earth verification:

- generated KML opened successfully
- vertical beacon rendered successfully
- label/base marker rendered successfully
- beacon remained visible from long-range tilted view

## Design rule

Keep the utility small. A future feature should solve a clear operational need and should not disturb the accepted coordinate parser or KML geometry without a new version and live ArcGIS Earth test.
