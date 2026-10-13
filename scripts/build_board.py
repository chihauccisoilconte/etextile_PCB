"""Place assigned footprints on an unrouted two-layer PCB."""
from design import *
import os
import sys
import xml.etree.ElementTree as ET
import pcbnew as k

E = PROJECT / "hardware"
target = E / f"{NAME}.kicad_pcb"
if target.exists() and "--regenerate" not in sys.argv:
    raise SystemExit("PCB exists. Check for manual edits before --regenerate.")
netlist = PROJECT / "docs/validation/netlist.xml"
if not netlist.exists():
    raise SystemExit("Export the KiCad XML netlist before building the PCB.")

board = k.BOARD()
board.SetCopperLayerCount(2)
board.GetDesignSettings().SetBoardThickness(k.FromMM(1.6))
v = lambda x, y: k.VECTOR2I(k.FromMM(x), k.FromMM(y))
net_items = {}
pin_nets = {}
for xmlnet in ET.parse(netlist).findall(".//nets/net"):
    name = xmlnet.get("name")
    if name not in net_items:
        item = k.NETINFO_ITEM(board, name)
        board.Add(item)
        net_items[name] = item
    for node in xmlnet.findall("node"):
        pin_nets[node.get("ref"), node.get("pin")] = net_items[name]

stock = Path(os.environ["KICAD_STOCK_DATA_HOME"]) / "footprints"
for part in PARTS:
    library, footprint = part["fp"].split(":", 1)
    directory = E / "EtaxTile.pretty" if library == "EtaxTile" else stock / f"{library}.pretty"
    fp = k.FootprintLoad(str(directory), footprint)
    if fp is None:
        raise RuntimeError(f"Cannot load {part['fp']}")
    fp.Models().clear()
    fp.SetReference(part["ref"])
    fp.SetValue(part["value"])
    fp.SetFPID(k.LIB_ID(library, footprint))
    fp.Value().SetVisible(False)
    if part["ref"] == "U1":
        fp.SetField("Manufacturer", "Seeed Studio")
        fp.GetField("Manufacturer").SetVisible(False)
        fp.SetField("Datasheet", "https://wiki.seeedstudio.com/xiao_esp32s3_getting_started/")
        fp.GetField("Datasheet").SetVisible(False)
    fp.Reference().SetTextSize(v(0.85, 0.85))
    fp.Reference().SetTextThickness(k.FromMM(0.13))
    fp.Reference().SetLayer(k.F_SilkS)
    board.Add(fp)
    fp.SetPosition(v(*part["xy"]))
    path = k.KIID_PATH()
    import uuid
    uid = lambda key: str(uuid.uuid5(uuid.NAMESPACE_URL, NAME + "/" + key))
    path.push_back(k.KIID(uid("root")))
    path.push_back(k.KIID(uid(part["ref"])))
    fp.SetPath(path)
    for pad in fp.Pads():
        item = pin_nets.get((part["ref"], pad.GetNumber()))
        if item:
            pad.SetNet(item)

def line(a, z, layer, width=0.15):
    shape = k.PCB_SHAPE(board)
    shape.SetShape(k.SHAPE_T_SEGMENT)
    shape.SetStart(v(*a))
    shape.SetEnd(v(*z))
    shape.SetLayer(layer)
    shape.SetWidth(k.FromMM(width))
    board.Add(shape)

width, height = 125, 83
for a, z in [((0, 0), (width, 0)), ((width, 0), (width, height)),
             ((width, height), (0, height)), ((0, height), (0, 0))]:
    line(a, z, k.Edge_Cuts)

def label(value, x, y, size=0.95):
    txt = k.PCB_TEXT(board)
    txt.SetText(value)
    txt.SetPosition(v(x, y))
    txt.SetTextSize(v(size, size))
    txt.SetTextThickness(k.FromMM(0.13))
    txt.SetLayer(k.F_SilkS)
    board.Add(txt)

for value, x, y in [
    ("XIAO ESP32-S3 SMD", 29, 48),
    ("BAT1", 51, 7), ("BAT2", 64, 7), ("BOOST", 78, 7),
    ("BOOST SRC", 95, 7), ("LED SRC", 109, 7),
    ("LED1", 51, 27), ("LED2", 64, 27),
    ("SENSOR I2C", 78, 27), ("SENSOR GPIO", 95, 27),
    ("D0-D10", 111, 26), ("3V3/GND", 51, 51),
    ("LED/GND", 78, 51), ("USB5/GND", 95, 51),
    ("ETAXTILE REV A - UNROUTED", 63, 79),
]:
    label(value, x, y)

# The square pad is pin 1 on each standard 2.54 mm header. Keep each
# connector's electrical meaning visible when using loose Dupont leads.
short_names = {
    "J1": ["+", "-"], "J2": ["+", "-"],
    "J3": ["VIN", "GND", "5V"],
    "J4": ["BAT1", "IN", "BAT2"],
    "J5": ["USB", "LED", "BST"],
    "J6": ["V+", "D6", "GND"],
    "J7": ["V+", "D7", "GND"],
    "J8": ["3V3", "GND", "SDA", "SCL"],
    "J9": ["3V3", "GND", "D0", "D1"],
    "J10": [f"D{i}" for i in range(11)],
}
for part in PARTS:
    names = short_names.get(part["ref"])
    if names:
        x, y = part["xy"]
        for i, name in enumerate(names):
            label(name, x + (7.1 if part["ref"] == "J10" else 4.7),
                  y + i * 2.54, 0.85)

board.BuildConnectivity()
k.SaveBoard(str(target), board)
print(f"Created {target.name}: {len(PARTS)} footprints, 0 tracks/vias, 0 zones")
