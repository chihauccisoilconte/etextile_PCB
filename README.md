# EtaxTile board

Editable KiCad 10 working files for an EtaxTile XIAO ESP32-S3 board. The saved PCB is 31.35 × 36.1 mm with 9 footprints and 160 track segments. It does **not** match the saved schematic: the current KiCad check reports 22 schematic-parity issues. These files are not a fabrication release.

Open [`hardware/etaxtile-board.kicad_pro`](hardware/etaxtile-board.kicad_pro) in KiCad. The project-local symbol and footprint libraries live beside it so KiCad can resolve them through `${KIPRJMOD}`.

## Repository guide

| Path | Contents |
| --- | --- |
| [`hardware/`](hardware/) | Editable schematic, PCB, project file, and local libraries |
| [`docs/design-notes.md`](docs/design-notes.md) | Historical design intent, source attribution, and unresolved decisions; not a current build guide |
| [`docs/images/`](docs/images/) | Schematic and PCB previews |
| [`docs/validation/`](docs/validation/) | Current KiCad ERC/DRC reports and generated XML netlist |
| [`scripts/`](scripts/) | Source scripts used to generate the initial design |
| [`STATUS.md`](STATUS.md) | Latest project state and next design decisions |

There is no fabrication package, assembly BOM, or firmware yet. Fabrication and assembly files will be added after the schematic and PCB are reconciled, the parts are selected, and the board is checked for manufacture.

## Editing and reuse

The KiCad files are the editable design sources. The scripts in `scripts/` describe an earlier 125 × 83 mm connector-board concept and do not reproduce the current saved PCB. Both builders refuse to overwrite existing files unless passed `--regenerate`; using that option would overwrite current design work. If developing that older concept separately, `build_schematic.py` writes the schematic and project files, and `build_board.py` reads a KiCad XML netlist at `docs/validation/netlist.xml`.

This repository is a private working draft. No open-source license has been selected or granted. A future public open-source hardware release will need an explicit license, BOM, assembly information, and design files corresponding to a tested revision.
