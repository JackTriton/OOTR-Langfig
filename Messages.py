from __future__ import annotations
from collections.abc import Callable, Iterable, Sequence
from typing import TYPE_CHECKING, Optional, Any, Dict, Tuple, List
from math import ceil
import json

if TYPE_CHECKING:
    from Rom import Rom
    from World import World

def try_find_last(source_list: Sequence[Any], sought_element: Any) -> Optional[int]:
    for reverse_index, element in enumerate(reversed(source_list)):
        if element == sought_element:
            return len(source_list) - 1 - reverse_index
    return None


def find_last(source_list: Sequence[Any], sought_element: Any) -> int:
    last = try_find_last(source_list, sought_element)
    if last is None:
        raise Exception(f"Element {sought_element} not found in sequence {source_list}.")
    return last

ENG_TEXT_START: int = 0x92D000
JPN_TEXT_START: int = 0x8EB000
ENG_TEXT_SIZE_LIMIT: int = 0x39000
JPN_TEXT_SIZE_LIMIT: int = 0x3B000

JPN_TABLE_START: int = 0xB808AC
ENG_TABLE_START: int = 0xB849EC
CREDITS_TABLE_START: int = 0xB88C0C

JPN_TABLE_SIZE: int = ENG_TABLE_START - JPN_TABLE_START
ENG_TABLE_SIZE: int = CREDITS_TABLE_START - ENG_TABLE_START

EXTENDED_TABLE_START: int = JPN_TABLE_START  # start writing entries to the jp table instead of english for more space
EXTENDED_TABLE_SIZE: int = JPN_TABLE_SIZE + ENG_TABLE_SIZE  # 0x8360 bytes, 4204 entries

EXTENDED_TEXT_START: int = JPN_TABLE_START  # start writing text to the jp table instead of english for more space
EXTENDED_TEXT_SIZE_LIMIT: int = JPN_TEXT_SIZE_LIMIT + ENG_TEXT_SIZE_LIMIT  # 0x74000 bytes

if TYPE_CHECKING:
    from Rom import Rom
    from World import World

CONTROL_CODES: dict[int, tuple[str, int, Callable[[Any], str]]] = {
    0x00: ('pad', 0, lambda _: '<pad>' ),
    0x01: ('line-break', 0, lambda _: '\n' ),
    0x02: ('end', 0, lambda _: '' ),
    0x04: ('box-break', 0, lambda _: '\n▼\n' ),
    0x05: ('color', 1, lambda d: '<color ' + "{:02x}".format(d) + '>' ),
    0x06: ('gap', 1, lambda d: '<' + str(d) + 'px gap>' ),
    0x07: ('goto', 2, lambda d: '<goto ' + "{:04x}".format(d) + '>' ),
    0x08: ('instant', 0, lambda _: '<allow instant text>' ),
    0x09: ('un-instant', 0, lambda _: '<disallow instant text>' ),
    0x0A: ('keep-open', 0, lambda _: '<keep open>' ),
    0x0B: ('event', 0, lambda _: '<event>' ),
    0x0C: ('box-break-delay', 1, lambda d: '\n▼<wait ' + str(d) + ' frames>\n' ),
    0x0E: ('fade-out', 1, lambda d: '<fade after ' + str(d) + ' frames?>' ),
    0x0F: ('name', 0, lambda _: '<name>' ),
    0x10: ('ocarina', 0, lambda _: '<ocarina>' ),
    0x12: ('sound', 2, lambda d: '<play SFX ' + "{:04x}".format(d) + '>' ),
    0x13: ('icon', 1, lambda d: '<icon ' + "{:02x}".format(d) + '>' ),
    0x14: ('speed', 1, lambda d: '<delay each character by ' + str(d) + ' frames>' ),
    0x15: ('background', 3, lambda d: '<set background to ' + "{:06x}".format(d) + '>' ),
    0x16: ('marathon', 0, lambda _: '<marathon time>' ),
    0x17: ('race', 0, lambda _: '<race time>' ),
    0x18: ('points', 0, lambda _: '<points>' ),
    0x19: ('skulltula', 0, lambda _: '<skulltula count>' ),
    0x1A: ('unskippable', 0, lambda _: '<text is unskippable>' ),
    0x1B: ('two-choice', 0, lambda _: '<start two choice>' ),
    0x1C: ('three-choice', 0, lambda _: '<start three choice>' ),
    0x1D: ('fish', 0, lambda _: '<fish weight>' ),
    0x1E: ('high-score', 1, lambda d: '<high-score ' + "{:02x}".format(d) + '>' ),
    0x1F: ('time', 0, lambda _: '<current time>' ),
    0xF0: ('silver_rupee', 1, lambda d: '<silver rupee count ' + "{:02x}".format(d) + '>' ),
    0xF1: ('key_count', 1, lambda d: '<key count ' + "{:02x}".format(d) + '>' ),
    0xF2: ('outgoing_item_filename', 0, lambda _: '<outgoing item filename>' ),
    0xF3: ('farores_wind_destination', 0, lambda _: '<farores_wind_destination>' ),
}

CONTROL_CHARS_JP: dict[str, tuple[str, str|int, int, int]] = {
    '　':('pad', '　', 0,0x00),
    '&':('line-break', 0x0A, 0,0x01),
    '｝':('end', '｝', 0,0x02),
    '^':('box-break', '▼', 0,0x04),
    '#':('color', 0x0B, 1,0x05),
    '☞':('gap', 0x86C7, 1, 0x06),
    '⇒':('goto', '⇒', 2,0x07),
    '♂':('instant', '♂', 0,0x08),
    '♀':('un-instant', '♀', 0,0x09),
    '☜':('keep-open', 0x86C8,0,0x0A),
    '◆':('event', '◆', 0,0x0B),
    '▲':('box-break-delay', '▲', 1,0x0C),
    '◇':('fade-out', '◇', 1,0x0E),
    '@':('name', 0x874F,0,0x0F),
    'Å':('ocarina',0x81F0,0,0x10),
    '♭':('sound', '♭', 2,0x12),
    '★':('icon', '★', 1,0x13),
    '☝':('speed', 0x86C9, 1, 0x14),
    '〠':('background',0x86B3,3,0x15),
    '大⃝':('marathon',0x8791,0,0x16),
    '小⃝':('race',0x8792,0,0x17),
    '㊘':('points',0x879B,0,0x18),
    '♠':('skulltula',0x86A3,0,0x19),
    '☆':('unskippable', '☆', 0,0x1A),
    '⊂':('two-choice', '⊂', 0,0x1B),
    '∈':('three-choice', '∈', 0,0x1C),
    '♣':('fish',0x86A4,0,0x1D),
    '♤':('highscore',0x869F,1,0x1E),
    '■':('time', '■', 0, 0x1F),
    '㍓':('silver_rupee', 0x87F0, 1, 0xF0),
    '♧':('key_count', 0x87F1, 1, 0xF1),
    '★':('outgoing_item_filename', 0x87F2, 0, 0xF2),
    '▷':('farores_wind_destination', 0x87F3, 0, 0xF3),
}

CC_PARSE_JP: Dict[int, Tuple[str, int, Callable[[Any], str]]] = {}

for _k, (name_jp, byte, ext_len_jp, code) in CONTROL_CHARS_JP.items():
    byte_key = byte if isinstance(byte, int) else int.from_bytes(byte.encode("cp932"))
    try:
        print_fmt = CONTROL_CODES[code][2]
    except KeyError:
        raise ValueError(f"The Value respondes with {name_jp!r} doesn't exist in CONTROL_CODES[{code:#04x}]")
    CC_PARSE_JP[byte_key] = (name_jp, ceil(ext_len_jp / 2), print_fmt)

# Maps unicode characters to corresponding bytes in OOTR's character set.
CHARACTER_MAP: dict[str, int] = {
    'Ⓐ': 0x9F,
    'Ⓑ': 0xA0,
    'Ⓒ': 0xA1,
    'Ⓛ': 0xA2,
    'Ⓡ': 0xA3,
    'Ⓩ': 0xA4,
    '⯅': 0xA5,
    '⯆': 0xA6,
    '⯇': 0xA7,
    '⯈': 0xA8,
    chr(0xA9): 0xA9,  # Down arrow   -- not sure what best supports this
    chr(0xAA): 0xAA,  # Analog stick -- not sure what best supports this
}
# Support other ways of directly specifying controller inputs in OOTR's character set.
# (This is backwards-compatibility support for ShadowShine57's previous patch.)
CHARACTER_MAP.update(tuple((chr(v), v) for v in CHARACTER_MAP.values()))

# Characters 0x20 thru 0x7D map perfectly.  range() excludes the last element.
CHARACTER_MAP.update((chr(c), c) for c in range(0x20, 0x7e))

# Other characters, source: https://wiki.cloudmodding.com/oot/Text_Format
CHARACTER_MAP.update((c, ix) for ix, c in enumerate(
        (
            '\u203e'             # 0x7f
            'ÀîÂÄÇÈÉÊËÏÔÖÙÛÜß'   # 0x80 .. #0x8f
            'àáâäçèéêëïôöùûü'    # 0x90 .. #0x9e
        ),
        start=0x7f
))

SPECIAL_CHARACTERS: dict[int, str] = {
    0x9F: '[A]',
    0xA0: '[B]',
    0xA1: '[C]',
    0xA2: '[L]',
    0xA3: '[R]',
    0xA4: '[Z]',
    0xA5: '[C Up]',
    0xA6: '[C Down]',
    0xA7: '[C Left]',
    0xA8: '[C Right]',
    0xA9: '[Triangle]',
    0xAA: '[Control Stick]',
}

SCJP: dict[int, str] = {k + 0x8300: v for k, v in SPECIAL_CHARACTERS.items()}

"""
JP Coding Guide
Create template for each messages using pickler.py
"""

REVERSE_MAP: list[str] = list(chr(x) for x in range(256))

for char, byte in CHARACTER_MAP.items():
    SPECIAL_CHARACTERS.setdefault(byte, char)
    REVERSE_MAP[byte] = char

try:
    CHARACTER_MAP_JP,REVERSE_MAP_JP=json.load(open("./jp_char_map.otrx",mode="r+"))
except:
    CHARACTER_MAP_JP: Dict[str, int] = {}
    for cp in range(0x110000):
        ch = chr(cp)
        try:
            b = ch.encode("cp932")
        except UnicodeEncodeError:
            continue                       # skip characters not in the JP font

        if len(b) == 1:                    # single-byte (same as US ASCII & half-width kana)
            code = b[0]
        else:                              # two-byte sequence: high byte first
            code = (b[0] << 8) | b[1]
        CHARACTER_MAP_JP[ch] = code

    # 2. add the controller glyphs explicitly (Greek Α … Μ)
    for sjis_code, token in SCJP.items():
        glyph = bytes([(sjis_code >> 8) & 0xFF, sjis_code & 0xFF]).decode("cp932")
        CHARACTER_MAP_JP[glyph] = sjis_code

    REVERSE_MAP_JP: List[str] = ["\uFFFD"] * 0x10000     # default U+FFFD for gaps

    #  regular characters …
    for ch, code in CHARACTER_MAP_JP.items():
        if code < 0x10000:
            REVERSE_MAP_JP[code] = ch

    #  … then override with tokens for special controller inputs
    for code, token in SCJP.items():
        if code < 0x10000:
            REVERSE_MAP_JP[code] = token
    json.dump([CHARACTER_MAP_JP,REVERSE_MAP_JP],open("./jp_char_map.otrx",mode="w"))

COLOR_MAP: dict[str, str] = {
    'White':      ['\x40',"00"],
    'Red':        ['\x41',"01"],
    'Green':      ['\x42',"02"],
    'Blue':       ['\x43',"03"],
    'Light Blue': ['\x44',"04"],
    'Pink':       ['\x45',"05"],
    'Yellow':     ['\x46',"06"],
    'Black':      ['\x47',"07"],
}

# convert byte array to an integer
def bytes_to_int(data: bytes, signed: bool = False) -> int:
    return int.from_bytes(data, byteorder='big', signed=signed)


# convert int to an array of bytes of the given width
def int_to_bytes(num: int, width: int, signed: bool = False) -> bytes:
    return int.to_bytes(num, width, byteorder='big', signed=signed)

class TextCodeJP:
    def __init__(self, code: int, data: int) -> None:
        self.code: int = code
        if code in CC_PARSE_JP:
            self.type = CC_PARSE_JP[code][0]
        else:
            self.type = 'character'
        self.data: int = data

    def display(self) -> str:
        if self.code in CC_PARSE_JP:
            return CC_PARSE_JP[self.code][2](self.data)
        elif self.code in SCJP:
            return SCJP[self.code]
        else:
            return int_to_bytes(self.code,2).decode("cp932")

    def get_python_string(self) -> str:
        if self.code in CC_PARSE_JP:
            ret = ''
            data = self.data
            for _ in range(0, CC_PARSE_JP[self.code][1]):
                ret = f'\\x{data & 0xFFFF:04X}{ret}'
                data = data >> 16
            ret = f'\\x{self.code:04X}{ret}'
            return ret
        elif self.code in SCJP:
            return f'\\x{self.code:04X}'
        else:
            return int_to_bytes(self.code,2).decode("cp932")

    def get_string(self) -> str:
        if self.code in CC_PARSE_JP:
            ret = ''
            subdata = self.data
            for _ in range(0, CC_PARSE_JP[self.code][1]):
                ret = chr(subdata & 0xFFFF) + ret
                subdata = subdata >> 16
            ret = chr(self.code) + ret
            return ret
        else:
            # raise ValueError(repr(REVERSE_MAP))
            return REVERSE_MAP_JP[self.code]

    def size(self) -> int:
        size = 1
        if self.code in CONTROL_CODES:
            size += CONTROL_CODES[self.code][1]
        return size

    # writes the code to the given offset, and returns the offset of the next byte
    def write(self, rom: Rom, text_start: int, offset: int) -> int:
        rom.write_bytes(text_start + offset, int_to_bytes(self.code,2))

        extra_bytes = 0
        if self.code in CC_PARSE_JP:
            extra_bytes = CC_PARSE_JP[self.code][1]*2
            bytes_to_write = int_to_bytes(self.data, extra_bytes)
            rom.write_bytes(text_start + offset + 2, bytes_to_write)

        return offset + 2 + extra_bytes

    __str__ = __repr__ = display

def display_code_list(codes: list[TextCodeJP]) -> str:
    message = ""
    for code in codes:
        message += str(code)
    return message

def jp_encode(text):
    result=[];c="";q=0;it=iter(text)
    for ch in it:
        if q!=0:
            c+=ch
            q-=1
            if len(c)==4 or (q==0 and c!=""):
                result.append(int(f"{c}",16))
                c=""
        else:
            if ch in CONTROL_CHARS_JP.keys():
                _,h,q,d=CONTROL_CHARS_JP[ch]
                if q%2==1: c+="0C" if ch=="#" else "00"
                q*=2
                if type(h)==int:result.append(h)
                else:result.append(int.from_bytes(h.encode("cp932")))
            else: result.append(int.from_bytes(ch.encode("cp932")))
    return result

def parse_control_codes(text: list[int] | bytearray | str) -> list[TextCodeJP]:
    if isinstance(text, list):
        text_bytes = text
    elif isinstance(text, bytearray):
        text_bytes = list(text)
    else:
        text_bytes = jp_encode(text)

    text_codes = []
    index = 0
    while index < len(text_bytes):
        next_char = text_bytes[index]
        data = 0
        index += 1
        if next_char in CC_PARSE_JP:
            extra_bytes = CC_PARSE_JP[next_char][1]
            if extra_bytes > 0:
                dt=[]
                for x in text_bytes[index: index + extra_bytes]:
                    dt+=[x>>8&0xFF,x&0xFF]
                data = bytes_to_int(dt)
                index += extra_bytes
        text_code = TextCodeJP(next_char, data)
        text_codes.append(text_code)
        if text_code.code == 0x8170:  # message end code
            break

    return text_codes

class MessageJP:
    def __init__(self, raw_text: list[int] | bytearray | str, index: int, id: int, opts: int, offset: int, length: int) -> None:
        if isinstance(raw_text, str):
            raw_text = jp_encode(raw_text)
        elif not isinstance(raw_text, bytearray):
            raw_text = bytearray(raw_text)

        self.raw_text: bytearray = raw_text

        self.index: int = index
        self.id: int = id
        self.opts: int = opts  # Textbox type and y position
        self.box_type: int = (self.opts & 0xF0) >> 4
        self.position: int = (self.opts & 0x0F)
        self.offset: int = offset
        self.length: int = length

        self.has_goto: bool = False
        self.has_keep_open: bool = False
        self.has_event: bool = False
        self.has_fade: bool = False
        self.has_ocarina: bool = False
        self.has_two_choice: bool = False
        self.has_three_choice: bool = False
        self.ending: Optional[TextCodeJP] = None

        self.text_codes: list[TextCodeJP] = []
        self.text: str = ''
        self.unpadded_length: int = 0
        self.parse_text()

    def display(self) -> str:
        meta_data = [
            "#" + str(self.index),
            "ID: 0x" + "{:04x}".format(self.id),
            "Offset: 0x" + "{:06x}".format(self.offset),
            "Length: 0x" + "{:04x}".format(self.unpadded_length) + "/0x" + "{:04x}".format(self.length),
            "Box Type: " + str(self.box_type),
            "Postion: " + str(self.position)
        ]
        return ', '.join(meta_data) + '\n' + self.text

    def get_python_string(self) -> str:
        ret = ''
        for code in self.text_codes:
            ret = ret + code.get_python_string()
        return ret

    # check if this is an unused message that just contains it's own id as text
    def is_id_message(self) -> bool:
        if self.unpadded_length != 5 or self.id == 0xFFFC:
            return False
        for i in range(4):
            code = self.text_codes[i].code
            if not (
                    code in range(ord('0'), ord('9')+1)
                    or code in range(ord('A'), ord('F')+1)
                    or code in range(ord('a'), ord('f')+1)
            ):
                return False
        return True

    def parse_text(self) -> None:
        self.text_codes = parse_control_codes(self.raw_text)

        index = 0
        for text_code in self.text_codes:
            index += text_code.size()
            if text_code.code == 0x8170:  # message end code
                break
            if text_code.code == 0x81CB:  # goto
                self.has_goto = True
                self.ending = text_code
            if text_code.code == 0x86C8:  # keep-open
                self.has_keep_open = True
                self.ending = text_code
            if text_code.code == 0x819F:  # event
                self.has_event = True
                self.ending = text_code
            if text_code.code == 0x819E:  # fade out
                self.has_fade = True
                self.ending = text_code
            if text_code.code == 0x81F0:  # ocarina
                self.has_ocarina = True
                self.ending = text_code
            if text_code.code == 0x81BC:  # two choice
                self.has_two_choice = True
            if text_code.code == 0x81B8:  # three choice
                self.has_three_choice = True
        self.text = display_code_list(self.text_codes)
        self.unpadded_length = index

    def is_basic(self) -> bool:
        return not (self.has_goto or self.has_keep_open or self.has_event or self.has_fade or self.has_ocarina or self.has_two_choice or self.has_three_choice)

    # computes the size of a message, including padding
    def size(self) -> int:
        size = 0

        for code in self.text_codes:
            size += code.size()

        size = (size + 3) & -4 # align to nearest 4 bytes

        return size

    # applies whatever transformations we want to the dialogs
    def transform(self, replace_ending: bool = False, ending: Optional[TextCodeJP] = None,
                  always_allow_skip: bool = True, speed_up_text: bool = True) -> None:
        ending_codes = [0x8170, 0x81CB, 0x86C8, 0x819F, 0x819E, 0x81F0]
        box_breaks = [0x81A5, 0x81A3]
        slows_text = [0x8189, 0x818A, 0x86C9]
        slow_icons = [0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x04, 0x02]

        text_codes = []
        instant_text_code = TextCodeJP(0x8189, 0)

        # # speed the text
        if speed_up_text:
            text_codes.append(instant_text_code) # allow instant

        # write the message
        for code in self.text_codes:
            # ignore ending codes if it's going to be replaced
            if replace_ending and code.code in ending_codes:
                pass
            # ignore the "make unskippable flag"
            elif always_allow_skip and code.code == 0x8199:
                pass
            # ignore anything that slows down text
            elif speed_up_text and code.code in slows_text:
                pass
            elif speed_up_text and code.code in box_breaks:
                # some special cases for text that needs to be on a timer
                if (self.id == 0x605A or  # twinrova transformation
                    self.id == 0x706C or  # rauru ending text
                    self.id == 0x70DD or  # ganondorf ending text
                    self.id in (0x706F, 0x7091, 0x7092, 0x7093, 0x7094, 0x7095, 0x7070)  # zelda ending text
                ):
                    text_codes.append(code)
                    text_codes.append(instant_text_code)  # allow instant
                else:
                    text_codes.append(TextCodeJP(0x81A5, 0))  # un-delayed break
                    text_codes.append(instant_text_code)  # allow instant
            elif speed_up_text and code.code == 0x819A and code.data in slow_icons:
                text_codes.append(code)
                text_codes.pop(find_last(text_codes, instant_text_code))  # remove last instance of instant text
                text_codes.append(instant_text_code)  # allow instant
            else:
                text_codes.append(code)

        if replace_ending:
            if ending:
                if speed_up_text and ending.code == 0x81F0:  # ocarina
                    text_codes.append(TextCodeJP(0x818A, 0))  # disallow instant text
                text_codes.append(ending)  # write special ending
            text_codes.append(TextCodeJP(0x8170, 0))  # write end code

        self.text_codes = text_codes

    # writes a Message back into the rom, using the given index and offset to update the table
    # returns the offset of the next message
    def write(self, rom: Rom, index: int, text_start: int, offset: int, bank: int) -> int:
        # construct the table entry
        id_bytes = int_to_bytes(self.id, 2)
        offset_bytes = int_to_bytes(offset, 3)
        entry = id_bytes + bytes([self.opts, 0x00, bank]) + offset_bytes
        # write it back
        entry_offset = EXTENDED_TABLE_START + 8 * index
        rom.write_bytes(entry_offset, entry)

        for code in self.text_codes:
            offset = code.write(rom, text_start, offset)

        while offset % 4 > 0:
            offset = TextCodeJP(0x00, 0).write(rom, text_start, offset) # pad to 4 byte align

        return offset

    # read a single message from rom
    @classmethod
    def from_rom(cls, rom: Rom, index: int, eng: bool = True) -> MessageJP:
        if eng:
            table_start = ENG_TABLE_START
            text_start = ENG_TEXT_START
        else:
            table_start = JPN_TABLE_START
            text_start = JPN_TEXT_START
        entry_offset = table_start + 8 * index
        entry = rom.read_bytes(entry_offset, 8)
        next = rom.read_bytes(entry_offset + 8, 8)

        id = bytes_to_int(entry[0:2])
        opts = entry[2]
        offset = bytes_to_int(entry[5:8])
        length = bytes_to_int(next[5:8]) - offset

        raw_text = rom.read_bytes(text_start + offset, length)

        return cls(raw_text, index, id, opts, offset, length)

    @classmethod
    def from_string(cls, text: str, id: int = 0, opts: int = 0x00) -> MessageJP:
        bytes = text + "\x02"
        return cls(bytes, 0, id, opts, 0, len(bytes) + 1)

    @classmethod
    def from_bytearray(cls, text: bytearray, id: int = 0, opts: int = 0x00) -> MessageJP:
        bytes = list(text) + [0x02]
        return cls(bytes, 0, id, opts, 0, len(bytes) + 1)

    __str__ = __repr__ = display

a="☞8A#02〠012345ありがとう"

ax=MessageJP(a,1,1,1,1,1)
ax.transform()
print(ax.text_codes)
