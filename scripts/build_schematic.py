"""Generate the editable EtaxTile schematic from design.py; refuses overwrite."""
from design import *
import json
import sys
import uuid

E = PROJECT / "hardware"
target = E / f"{NAME}.kicad_sch"
if target.exists() and "--regenerate" not in sys.argv:
    raise SystemExit("Schematic exists. Check for manual edits before --regenerate.")

uid = lambda key: str(uuid.uuid5(uuid.NAMESPACE_URL, NAME + "/" + key))
q = lambda value: json.dumps(str(value))
root = uid("root")
font = '(effects (font (size 1 1)))'

def layout(part):
    count = len(part["pins"])
    left = (count + 1) // 2
    return [(n + 1, -17.78, (left - 1) * 1.27 - n * 2.54, 0)
            for n in range(left)] + [
            (n + 1, 17.78, (count - left - 1) * 1.27 - (n-left) * 2.54, 180)
            for n in range(left, count)]

def lib_symbol(part, local=False):
    ref = part["ref"]
    count = len(part["pins"])
    height = max(3.81, ((count + 1) // 2) * 1.27 + 1.27)
    name = ref if local else "EtaxTile:" + ref
    out = (f'(symbol {q(name)} (pin_names (offset 0.6)) (in_bom yes) (on_board yes) '
           f'(property "Reference" {q(ref[0])} (at 0 {height+2.54} 0) {font}) '
           f'(property "Value" {q(part["value"])} (at 0 {height+5.08} 0) {font}) '
           f'(symbol "{ref}_0_1" (rectangle (start -12.7 {height}) '
           f'(end 12.7 {-height}) (stroke (width 0.254) (type default)) '
           '(fill (type background)))) '
           f'(symbol "{ref}_1_1" ')
    for number, x, y, angle in layout(part):
        name = part["pins"][number-1]
        out += (f'(pin passive line (at {x} {y} {angle}) (length 5.08) '
                f'(name {q(name)} {font}) (number "{number}" {font}))')
    return out + '))'

lib = ''.join(lib_symbol(part) for part in PARTS)
sheet = (f'(kicad_sch (version 20250114) (generator "eeschema") '
         f'(uuid {root}) (paper "A2") '
         '(title_block (title "EtaxTile XIAO ESP32-S3 connector board") '
         '(date "2026-09-28") (rev "A") '
         '(comment 1 "Two LED outputs, two sensor ports; 2.54 mm headers")) '
         f'(lib_symbols {lib})')
for part in PARTS:
    ref = part["ref"]
    x, y = (round(value / 1.27) * 1.27 for value in part["sch"])
    x, y = round(x, 5), round(y, 5)
    count = len(part["pins"])
    h = max(3.81, ((count + 1) // 2) * 1.27 + 1.27)
    sheet += (f'(symbol (lib_id "EtaxTile:{ref}") (at {x} {y} 0) '
              f'(unit 1) (in_bom yes) (on_board yes) (dnp no) (uuid {uid(ref)}) '
              f'(property "Reference" "{ref}" (at {x} {y-h-3.81} 0) {font}) '
              f'(property "Value" {q(part["value"])} (at {x} {y-h-1.27} 0) {font}) '
              f'(property "Footprint" {q(part["fp"])} (at {x} {y} 0) '
              '(effects (font (size 1 1)) hide))')
    if ref == "U1":
        sheet += (f'(property "Manufacturer" "Seeed Studio" (at {x} {y} 0) '
                  '(effects (font (size 1 1)) hide)) '
                  f'(property "Datasheet" "https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/" '
                  f'(at {x} {y} 0) (effects (font (size 1 1)) hide))')
    for n in range(1, count+1):
        sheet += f'(pin "{n}" (uuid {uid(ref+"/pin/"+str(n))}))'
    sheet += (f'(instances (project "{NAME}" (path "/{root}" '
              f'(reference "{ref}") (unit 1)))))')
    for n, dx, dy, angle in layout(part):
        px, py = round(x+dx, 5), round(y-dy, 5)
        net = part["nets"][n-1]
        if net is None:
            sheet += f'(no_connect (at {px} {py}) (uuid {uid(ref+"/nc/"+str(n))}))'
            continue
        ex = round(px+(-7.62 if angle == 0 else 7.62), 5)
        sheet += (f'(wire (pts (xy {px} {py}) (xy {ex} {py})) '
                  f'(stroke (width 0) (type default)) (uuid {uid(ref+"/w/"+str(n))})) '
                  f'(label {q(net)} (at {ex} {py} {180 if angle == 0 else 0}) '
                  '(effects (font (size 0.9 0.9)) (justify left bottom)) '
                  f'(uuid {uid(ref+"/l/"+str(n))}))')
sheet += (f'(text "J4: jumper 1-2 for BAT1 or 2-3 for BAT2 into an external 5V boost. '
          'J5: jumper 1-2 for USB 5V or 2-3 for boost 5V. Never fit both. '
          'BAT1 connects only to XIAO underside VBAT; BAT2 positive stays separate. '
          'Battery negatives share GND. LED DATA is 3.3V logic: check strip compatibility or use external level shifter." '
          f'(at 25 365 0) (effects (font (size 1.1 1.1)) (justify left)) '
          f'(uuid {uid("notes")})))')
target.write_text(sheet)
(E / "EtaxTile.kicad_sym").write_text(
    '(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor") '
    + ''.join(lib_symbol(part, True) for part in PARTS) + ')')
(E / "sym-lib-table").write_text(
    '(sym_lib_table (version 7) (lib (name "EtaxTile") (type "KiCad") '
    '(uri "${KIPRJMOD}/EtaxTile.kicad_sym") (options "") '
    '(descr "EtaxTile local symbols")))')
(E / "fp-lib-table").write_text(
    '(fp_lib_table (version 7) (lib (name "EtaxTile") (type "KiCad") '
    '(uri "${KIPRJMOD}/EtaxTile.pretty") (options "") '
    '(descr "Seeed XIAO ESP32-S3 SMD footprint")))')
(E / f"{NAME}.kicad_pro").write_text(json.dumps({
    "meta": {"filename": f"{NAME}.kicad_pro", "version": 1},
    "board": {"design_settings": {"rules": {"min_clearance": 0.2,
             "min_track_width": 0.2, "min_via_diameter": 0.6}}},
    "net_settings": {"classes": [{"name": "Default", "clearance": 0.2,
             "track_width": 0.25, "via_diameter": 0.6, "via_drill": 0.3,
             "microvia_diameter": 0.3, "microvia_drill": 0.1,
             "bus_width": 12, "wire_width": 6}]}
}, indent=2))
print(f"Created {target.name} with {len(PARTS)} assigned components")
