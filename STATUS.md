# Current status

Stage: editable connector-board draft, placement complete, routing pending.

## 2026-09-28

Created `electronics/etaxtile-board.kicad_pro`, schematic, two-layer 125 × 83 mm PCB, project-local symbols and Seeed XIAO ESP32-S3 SMD footprint. U1 and thirteen 2.54 mm headers have schematic footprints and board placement. J1 powers the XIAO through underside BAT1+/GND pads. J2 supports a separate battery for an off-board 5 V boost; grounds are common. J4 selects the boost battery, J5 selects USB or boost for LED_PWR. J6/J7 are two LED outputs, J8/J9 are provisional sensor ports, J10 exposes D0–D10 and J11–J13 provide extra power and ground connections. The calligraphy project's ESP32-C3 layout was used only as reference; Seeed's ESP32-S3 footprint/pad map was used for U1.

Checks: KiCad 10.0.6 ERC 0. DRC 0 geometry violations, 54 intentional open connections and 0 schematic-parity issues. Board has 0 tracks/vias/zones. Schematic and PCB plots exported; PNG previews inspected. No physical or LED-current validation.

Open decisions: user message ended at “connections for 2,” without naming the devices. J8/J9 are generic sensor ports pending that detail. Confirm LED type, length and peak current; source battery capacity, boost module and 2.54 mm shunt/header hardware accordingly. Board outline, connector positions and mounting pattern are provisional. After the required interfaces and current are known, finalize power widths, route, repeat ERC/DRC and check physical fit.
