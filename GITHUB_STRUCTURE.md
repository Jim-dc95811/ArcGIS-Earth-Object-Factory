# GitHub Structure — ArcGIS Earth Unlocked

**Date:** 2026-10-29

This file records the intended public GitHub organization for the ArcGIS Earth project family.

## Master umbrella

Preferred umbrella name:

> **ArcGIS Earth Unlocked**

Intended public repository name:

`ArcGIS-Earth-Unlocked`

Purpose:
- explain the complete system
- route users to the correct specialized tool
- contain architecture/workflow documentation rather than production code
- show how offline maps, navigation, operational GIS, and objects work together

The current master system document is temporarily stored here as:

`ARCGIS_EARTH_UNLOCKED.md`

When the separate umbrella repository exists, that document should become its primary README/system map.

## Object Factory home

Current GitHub repository name:

`Earth-Beacon`

Intended repository name:

`ArcGIS-Earth-Object-Factory`

The content of the repository has already been reorganized around **ArcGIS Earth Object Factory**.

Earth Beacon is preserved as:
- a factory tab/capability
- a standalone accepted v1.0 release
- exact legacy source/documentation under `legacy/Earth_Beacon_v1.0/`

The root is now reserved for active Object Factory source, examples, current documentation, continuity, and architecture.

## Public project roles

### Foundation maps

#### `QGIS-Mbtile-to-ArcGIS-Earth-TPKX`
Build/convert compatible raster MBTiles into large offline TPKX worlds and organize production through Master 4.

#### `ArcGIS-Earth-Offline-Maps-Chartplotting`
Preserve the earlier ArcGIS Pro/TPKX production, mobile/offline, chartplotting, extent, and field-tracker workflow.

### Navigation

#### `EarthStick`
Direct joystick navigation through the ArcGIS Earth camera.

> **Fly the real map.**

### Object authoring / experimentation

#### intended `ArcGIS-Earth-Object-Factory`
Current repo: `Earth-Beacon`

Creates intentional geographic objects:
- PNG objects
- batch object packs
- Sky Compass
- Beacon
- hyperlinks/viewpoints
- future scenario/3D/camera experiments

New experimental object concepts should normally begin here. Spin out a separate repo only when a capability becomes independently useful and mature.

### Operational GIS data

#### `Point-Maps`
PointLayer: ingest/query public ArcGIS point services and produce offline KMZ/GeoJSON datasets.

#### `Parcel100`
Produce manageable clickable offline parcel GeoJSON cells from public ArcGIS parcel services.

## Architecture rule

Do not combine all projects into one giant application merely because they cooperate.

Keep each specialized tool focused:

```text
Foundation maps  -> what the world looks like
Operational data -> what databases know about the world
EarthStick       -> how the user moves through the world
Object Factory   -> what intentional objects/meaning are placed in the world
ArcGIS Earth     -> renderer / common environment
```

## Current account-level limitations

The connected GitHub tool can edit repository contents and history but does not currently expose repository creation or rename controls.

Therefore these two account-level operations remain pending:

1. Rename `Earth-Beacon` → `ArcGIS-Earth-Object-Factory`.
2. Create public repo `ArcGIS-Earth-Unlocked`.

After those operations, update all ecosystem links to the final URLs and move/copy the umbrella README/system map into the new umbrella repository.

## Binary release assets

The exact Object Factory v0.2 TEST Python source is mirrored in this repository and its Git blob SHA was verified against the tested local source.

The tested operator package also includes preset PNG assets and documentation. The current GitHub connector cannot safely upload those binary release assets. Until they are uploaded separately, the tested packaged ZIP remains the canonical runnable distribution and the repository remains the exact source/documentation home.

Do not imply that `Code -> Download ZIP` is the same as the tested Object Factory operator package until the preset icon bundle/release asset is present.
