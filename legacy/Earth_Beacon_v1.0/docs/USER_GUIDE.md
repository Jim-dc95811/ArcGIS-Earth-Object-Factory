# Earth Beacon — User Guide

## Purpose

Earth Beacon creates a tall vertical KML marker at a geographic coordinate. The marker is designed to remain easy to see from long distance in ArcGIS Earth's tilted 3D view.

## Start the program

1. Extract `Beacon_Maker_v1.0.zip`.
2. Double-click `Beacon_Maker.bat`.
3. The Beacon Maker window opens.

No third-party Python packages are required.

## Choose a coordinate

### Manual

Enter latitude and longitude directly into their fields.

### Windows clipboard

Copy a coordinate pair, then click **From Windows Clipboard**.

Examples:

```text
30.123, -81.456
-81.456 30.123
Latitude: 30.123 Longitude: -81.456
```

The **Clipboard order** selector can be set to:

- Auto
- Lat, Lon
- Lon, Lat

If both numbers are legal in either order, Auto interprets them as Latitude, Longitude and reports that the pair is ambiguous. Verify the result or click **Swap Lat/Lon**.

### ArcGIS Earth

Enable the ArcGIS Earth Automation API, then click **From ArcGIS Earth**.

Beacon Maker reads the current ArcGIS Earth camera coordinates from:

```text
http://localhost:8000/arcgisearth/camera
```

## Configure the beacon

- **Beacon name** — label shown in the KML
- **Height (km)** — vertical height above local ground
- **Line width** — visual width of the KML line
- **Color** — red, yellow, cyan, green, magenta, white, or orange

The default is a red 100 km beacon with width 6.

## Create the KML

1. Click **Create Beacon KML**.
2. Choose a filename and save location.
3. If **Open KML after saving** is checked, Windows opens the KML using the associated application.
4. In ArcGIS Earth, the target appears as a labeled base point with a vertical pillar extending upward.

## Practical use

The beacon is intended to be visually obvious at distance. Use it as a temporary destination, incident marker, staging location, route checkpoint, home position, parcel target, or other long-range reference.

Multiple KML beacon files can be created when several targets are needed. Different colors can distinguish different purposes.

## Troubleshooting

### Clipboard pair is backwards

Click **Swap Lat/Lon**, or set **Clipboard order** explicitly before reading the clipboard.

### ArcGIS Earth button cannot connect

Confirm:

- ArcGIS Earth desktop is running
- Automation API is enabled under Advanced settings
- the API is still using `http://localhost:8000`

Manual and clipboard coordinate entry do not require the ArcGIS Earth API.

### KML saves but does not open automatically

The KML itself was still created. Open it manually from File Explorer or add it from ArcGIS Earth.

### Beacon is hard to see

Try a larger line width, a different color, or a taller height.
