# EtaxTile board — XIAO ESP32-S3 connector carrier

Open `electronics/etaxtile-board.kicad_pro` in KiCad 10. The project contains an editable schematic, a placed two-layer 125 × 83 mm PCB, assigned footprints and a project-local XIAO ESP32-S3 SMD footprint. All other fitted parts are ordinary 2.54 mm through-hole headers, suitable for soldered wires, Dupont leads or a chosen compatible spring-contact receptacle. The square header pad is pin 1. The board is currently **unrouted** while the two unspecified connections and LED current are clarified.

## Interfaces

| Connector | Pins in order |
| --- | --- |
| J1, BAT1 | 1 BAT1+ (protected 1S LiPo), 2 GND |
| J2, BAT2 | 1 BAT2+ (optional separate protected 1S LiPo), 2 GND |
| J3, external 5 V boost | 1 boost input, 2 GND, 3 regulated 5 V output |
| J4, boost input selector | 1 BAT1+, 2 boost input, 3 BAT2+ |
| J5, LED supply selector | 1 USB 5 V, 2 LED_PWR, 3 boost 5 V |
| J6/J7, LED strings 1/2 | 1 LED_PWR, 2 D6/D7 data, 3 GND |
| J8, sensor 1 | 1 3V3, 2 GND, 3 SDA/D4, 4 SCL/D5 |
| J9, sensor 2 | 1 3V3, 2 GND, 3 D0, 4 D1 |
| J10, GPIO breakout | 1–11: XIAO D0–D10 |
| J11 | four alternating 3V3/GND pairs |
| J12 | three alternating LED_PWR/GND pairs |
| J13 | two alternating USB_5V/GND pairs |

J8 and J9 are provisional generic ports because the phrase “connections for 2” did not identify the two devices. Both LED string outputs are also present. All eleven XIAO GPIO signals remain exposed on J10, including those used on J6–J9.

## Power arrangement

BAT1+ connects to the XIAO's underside VBAT pad 23; GND connects to underside pad 24. The XIAO is soldered as an SMD module. BAT2+ stays electrically separate from BAT1+; their negative terminals share board GND. With an external 5 V boost connected to J3, fit **one** shunt on J4: pins 1–2 for BAT1 or 2–3 for BAT2. Fit **one** shunt on J5: pins 1–2 for USB 5 V or 2–3 for the boost output. Do not fit both positions on either selector. A LiPo is never connected directly to LED_PWR as a supposed 5 V source.

The XIAO 5 V pin carries USB power and has no 5 V output in battery operation, per [Seeed's XIAO ESP32-S3 documentation](https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/). The external boost, battery protection, selector shunts and LED strings are not supplied by this project. Confirm the boost's input range and current rating for the chosen battery and LEDs. The 2.54 mm battery headers are unkeyed, so verify polarity at assembly. The XIAO data pins use 3.3 V logic; a 5 V LED strip may require an external level shifter. The sensor ports are 3.3 V only. USB_5V and LED_PWR are separate named rails until J5 is bridged.

## Source and checks

The XIAO SMD footprint is a project-local copy of [Seeed's XIAO Series KiCad footprints](https://files.seeedstudio.com/wiki/XIAO-KiCad-Library/New_XIAO_Series_Footprints.zip). Its F.Silkscreen graphics were moved to F.Fab because the supplied outline crossed its own solder pads. Pin numbers and copper geometry were retained. The adjacent [calligraphy-based Acid Skate project](../skateboard-acid/electronics/README.md) supplied layout context, but its ESP32-C3 battery footprint was not reused for the ESP32-S3.

KiCad 10.0.6 ERC: 0 violations. PCB DRC: 0 geometry violations, 0 schematic-parity issues and 54 expected unconnected items because the PCB is unrouted. Schematic and PCB SVG plots were exported; PNG previews were inspected. No hardware, 5 V strip compatibility, connector fit, thermal capacity or enclosure fit was tested. Board dimensions and placement are provisional; no mounting pattern has been specified.

The source scripts in `scripts/` can regenerate the schematic and PCB after checking for manual edits. `build_schematic.py` writes the schematic and project files; export its KiCad XML netlist to `exports/netlist.xml` before running `build_board.py`. Both scripts refuse to overwrite existing files unless passed `--regenerate`.
