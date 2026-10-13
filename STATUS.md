# Current status

Stage: editable draft; saved schematic and routed PCB are out of sync. Not ready for fabrication.

## 2026-10-13

Created a standalone project Git repository and uploaded the KiCad sources, scripts, and previews to the private GitHub repository at https://github.com/chihauccisoilconte/etextile_PCB. Local KiCad history, editor state, and Python caches are excluded. The electrical and mechanical open decisions below remain unchanged.

Reorganized the repository: editable KiCad files are in `hardware/`, historical design notes, regenerated previews and current reports are in `docs/`, and older-concept generators remain in `scripts/`. Removed unused template folders. The native KiCad files were moved unchanged, and the generator paths were updated. A fresh ERC/DRC run found one ERC power-pin error, eight DRC warnings, one reported unconnected item, and 22 schematic-parity issues. The saved PCB is 31.35 × 36.1 mm with 9 footprints and 160 track segments; the earlier 125 × 83 mm unrouted description does not match it. Resolve the schematic/PCB mismatch before making a fabrication package. Licensing, BOM and assembly documentation are still pending.

## 2026-09-28

Created `electronics/etaxtile-board.kicad_pro`, schematic, two-layer 125 × 83 mm PCB, project-local symbols and Seeed XIAO ESP32-S3 SMD footprint. U1 and thirteen 2.54 mm headers have schematic footprints and board placement. J1 powers the XIAO through underside BAT1+/GND pads. J2 supports a separate battery for an off-board 5 V boost; grounds are common. J4 selects the boost battery, J5 selects USB or boost for LED_PWR. J6/J7 are two LED outputs, J8/J9 are provisional sensor ports, J10 exposes D0–D10 and J11–J13 provide extra power and ground connections. The calligraphy project's ESP32-C3 layout was used only as reference; Seeed's ESP32-S3 footprint/pad map was used for U1.

Checks: KiCad 10.0.6 ERC 0. DRC 0 geometry violations, 54 intentional open connections and 0 schematic-parity issues. Board has 0 tracks/vias/zones. Schematic and PCB plots exported; PNG previews inspected. No physical or LED-current validation.

Open decisions: user message ended at “connections for 2,” without naming the devices. J8/J9 are generic sensor ports pending that detail. Confirm LED type, length and peak current; source battery capacity, boost module and 2.54 mm shunt/header hardware accordingly. Board outline, connector positions and mounting pattern are provisional. After the required interfaces and current are known, finalize power widths, route, repeat ERC/DRC and check physical fit.
