"""EtaxTile connector-first prototype specification; dimensions in mm."""
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
NAME = "etaxtile-board"

# Pin order matches Seeed's XIAO-ESP32-S3-SMD footprint and symbol library.
XIAO_PINS = ["D0/GPIO1", "D1/GPIO2", "D2/GPIO3", "D3/GPIO4",
             "D4/SDA/GPIO5", "D5/SCL/GPIO6", "D6/GPIO43", "D7/GPIO44",
             "D8/GPIO7", "D9/GPIO8", "D10/GPIO9", "3V3_OUT", "GND",
             "USB_5V", "MTDI", "MTDO", "EN", "GND", "MTMS", "MTCK",
             "USB_DN", "USB_DP", "BAT1+", "GND", "PAD"]
XIAO_NETS = [f"D{i}" for i in range(11)] + ["3V3", "GND", "USB_5V"] + [None]*3 + ["GND"] + [None]*4 + ["BAT1+", "GND", None]

PARTS = [
    dict(ref="U1", value="Seeed XIAO ESP32-S3", pins=XIAO_PINS, nets=XIAO_NETS,
         fp="EtaxTile:XIAO-ESP32-S3-SMD", xy=(24, 28), sch=(75, 105), kind="xiao"),
    dict(ref="J1", value="BAT1 1S LiPo", pins=["+", "-"], nets=["BAT1+", "GND"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", xy=(51, 12), sch=(185, 50)),
    dict(ref="J2", value="BAT2 1S LiPo optional", pins=["+", "-"], nets=["BAT2+", "GND"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical", xy=(64, 12), sch=(185, 82)),
    dict(ref="J3", value="External 5V boost", pins=["VIN", "GND", "VOUT_5V"], nets=["BOOST_IN", "GND", "BOOST_5V"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", xy=(78, 12), sch=(185, 118)),
    dict(ref="J4", value="Boost input selector", pins=["BAT1", "BOOST_IN", "BAT2"], nets=["BAT1+", "BOOST_IN", "BAT2+"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", xy=(95, 12), sch=(185, 157)),
    dict(ref="J5", value="LED supply selector", pins=["USB_5V", "LED_PWR", "BOOST_5V"], nets=["USB_5V", "LED_PWR", "BOOST_5V"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", xy=(108, 12), sch=(185, 196)),
    dict(ref="J6", value="LED string 1", pins=["V+", "DATA", "GND"], nets=["LED_PWR", "D6", "GND"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", xy=(51, 31), sch=(185, 235)),
    dict(ref="J7", value="LED string 2", pins=["V+", "DATA", "GND"], nets=["LED_PWR", "D7", "GND"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical", xy=(64, 31), sch=(185, 274)),
    dict(ref="J8", value="Sensor 1 I2C", pins=["3V3", "GND", "SDA", "SCL"], nets=["3V3", "GND", "D4", "D5"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", xy=(78, 31), sch=(335, 50)),
    dict(ref="J9", value="Sensor 2 GPIO", pins=["3V3", "GND", "SIG_A", "SIG_B"], nets=["3V3", "GND", "D0", "D1"],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", xy=(95, 31), sch=(335, 91)),
    dict(ref="J10", value="All XIAO GPIO", pins=[f"D{i}" for i in range(11)], nets=[f"D{i}" for i in range(11)],
         fp="Connector_PinHeader_2.54mm:PinHeader_1x11_P2.54mm_Vertical", xy=(110, 30), sch=(335, 145)),
    dict(ref="J11", value="3V3 / GND expansion", pins=["3V3", "GND"]*4, nets=["3V3", "GND"]*4,
         fp="Connector_PinHeader_2.54mm:PinHeader_1x08_P2.54mm_Vertical", xy=(51, 55), sch=(335, 207)),
    dict(ref="J12", value="LED_PWR / GND expansion", pins=["LED_PWR", "GND"]*3, nets=["LED_PWR", "GND"]*3,
         fp="Connector_PinHeader_2.54mm:PinHeader_1x06_P2.54mm_Vertical", xy=(78, 55), sch=(335, 261)),
    dict(ref="J13", value="USB 5V / GND expansion", pins=["USB_5V", "GND"]*2, nets=["USB_5V", "GND"]*2,
         fp="Connector_PinHeader_2.54mm:PinHeader_1x04_P2.54mm_Vertical", xy=(95, 55), sch=(335, 306)),
]

for part in PARTS:
    assert len(part["pins"]) == len(part["nets"])
