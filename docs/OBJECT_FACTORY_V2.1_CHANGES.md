# Object Factory 2.1 - what changed (2026-11-08)

> 🤖 **Using AI assistance?** Have the agent read the [CLAUDE.md](https://github.com/Jim-dc95811/ArcGIS-Earth-Unlocked/blob/main/CLAUDE.md) file first.

A re-hardening release. **Objects made from good input are exactly the same as in 2.0** (checked: 48 single-object combinations, both sample lists, a 100-object list, Sky Compass and Beacon). Only bad or unusual input is handled better. Live-tested by Jim on 2026-11-08.

| # | Before (2.0) | Now (2.1) |
|---|---|---|
| 1 | A batch list saved from Excel as plain **CSV** stopped with a `'utf-8' codec` error if any name had an accent (Café, Señor, Ñ). | Excel's plain CSV (Windows-1252) and "Unicode Text" (UTF-16) lists are read. Names come out right in ArcGIS Earth. |
| 2 | In a `\|` list, a quote mark that opened a description and never closed (`"Behind the gate`) **silently swallowed the next row** - one object fewer, no message. | In `\|` lists a quote mark is just a character, so every row stays. In comma (Excel) lists, quotes still work the Excel way; a quote that never closes stops with a message naming the line. |
| 3 | Rows Excel leaves behind after you clear cells (`,,,,`) stopped the list with "latitude and longitude are required". | Empty rows are skipped. Error messages still name the real line in the file. |
| 4 | A word in a number box gave `could not convert string to float: 'thirty'`. `nan`, a scale of 0 or less, and a Sky Compass radius of 0 were accepted and made broken or invisible objects. | Plain messages that name the box: *Altitude (ft): 'thirty' is not a number.* Those values are refused. `1,500` in a feet box still reads as 1500. |
| 5 | Default output = `C:\Users\<you>\Desktop`, which on PCs where OneDrive moved the Desktop is a folder you never see. | The default output is the Desktop Windows really shows (OneDrive or not). |
| 6 | The window opened 790 px tall and would not shrink below 700 - on a small laptop the CREATE button could sit under the taskbar. | The window opens to fit the screen, and a tab that does not fit gets a scroll bar (mouse wheel works). On a big screen nothing looks different. |
| 7 | From Clipboard with a picture on the clipboard gave a programmer error. | *The clipboard has no text. Copy a latitude, longitude pair first.* |

Test rig: [`object_factory_test_v21.py`](https://github.com/Jim-dc95811/ArcGIS-Earth-Unlocked/blob/main/tools/test-rigs/object_factory_test_v21.py) (2.0 vs 2.1, ALL PASS). The program's own `--selftest` gained the Excel, quote-mark and number-box checks.
