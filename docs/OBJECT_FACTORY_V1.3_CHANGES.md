# Object Factory v1.3 - One obvious file (2026-11-06)

## Why

Jim's packaging rule for every tool: *one obvious .bat file to click, and everything else under a system folder.* Jim chose to keep the samples, moved into System Files.

## The folder after Extract All

```
Object_Factory_v1.3\
   Run_Object_Factory.bat     <- double-click this
   System Files\              <- Object_Factory_v1.3.py, icons\, sample_objects.txt, simple_objects.txt,
                                 SAMPLE_Object_Set.kmz, SAMPLE_Linked_Camera.kmz, SAMPLE_Sky_Compass.kmz, SAMPLE_Beacon.kml
```

`README.txt` is gone (the manual is on the GitHub page).

## What changed

- The launcher starts `System Files\Object_Factory_v1.3.py`.
- The program finds its icons and sample lists beside itself, so moving them together needed no code change; only the version text is 1.3.

## What did not change

Everything the factory makes. Checked here, v1.2 against v1.3: both sample object lists (identical apart from the short folder code in each icon's name inside the KMZ, which depends on where the program sits on disk - it differs between any two PCs in v1.2 too), the Sky Compass, the Beacon and a single object with tether, Info popup, link and Hide above - all identical.

## Files

- `archive/ArcGIS_Earth_Object_Factory_v1.3.zip` (folder `Object_Factory_v1.3/`) SHA-256 `cd1c1a755b04df606d48f62aabba9e37a0cbb5b1afcb0e34e9125a268dd03621`
- `archive/source/Object_Factory_v1.3.py` SHA-256 `676a258e5e7aaeb2ca7cee97e5b5c37c1fe7d8d6c59aa7c3dc5647705ffd2e12`
- v1.2 and v1.1 zips and sources kept.
