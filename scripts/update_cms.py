#!/usr/bin/env python3
import os
import struct
import json
import re

CMS_DIR = 'framerusercontent.com/cms'

# Replacement rules for CMS text and JSON fields
REPLACEMENTS = [
    # Full phrases
    ("Research: Alethia's Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Research: Prakriti's Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Research: Alethia’s Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Research: Prakriti’s Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Alethia's Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Prakriti's Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Alethia’s Atmospheric-based Measurement, Reporting, and Verification approach.",
     "Prakriti’s Atmospheric-based Measurement, Reporting, and Verification approach."),
    ("Alethia’s Atmospheric‑Based Measurement, Reporting, and Verification Approach",
     "Prakriti’s Atmospheric‑Based Measurement, Reporting, and Verification Approach"),
    ("alethias-atmospheric-based-measurement-reporting-and-verification-approach",
     "prakritis-atmospheric-based-measurement-reporting-and-verification-approach"),
    ("Scaling Alethia’s Intelligence with AI", "Scaling Prakriti’s Intelligence with AI"),
    ("Scaling Alethia's Intelligence with AI", "Scaling Prakriti's Intelligence with AI"),
    ("scaling-alethias-intelligence-with-ai", "scaling-prakritis-intelligence-with-ai"),
    ("The Alethia Solution", "The Prakriti Solution"),
    ("Within the first year, Alethia established", "Within the first year, Prakriti established"),
    ("monitored with Alethia’s aMRV platform", "monitored with Prakriti’s aMRV platform"),
    ("monitored with Alethia's aMRV platform", "monitored with Prakriti's aMRV platform"),
    ("At the core of Alethia’s platform", "At the core of Prakriti’s platform"),
    ("At the core of Alethia's platform", "At the core of Prakriti's platform"),
    ("Alethia\xe2\x80\x99s continuous monitoring", "Prakriti\xe2\x80\x99s continuous monitoring"),
    ("Alethia’s continuous monitoring", "Prakriti’s continuous monitoring"),
    ("Alethia's continuous monitoring", "Prakriti's continuous monitoring"),
    ("Alethia turns atmospheric signals into truth", "Prakriti turns atmospheric signals into truth"),
    ("Alethia anchors each result", "Prakriti anchors each result"),
    ("Alethia expands its observational reach", "Prakriti expands its observational reach"),
    ("Alethia’s platform applies", "Prakriti’s platform applies"),
    ("Alethia's platform applies", "Prakriti's platform applies"),
    ("Alethia\xe2\x80\x99s platform applies", "Prakriti\xe2\x80\x99s platform applies"),
    ("Alethia’s integrated platform", "Prakriti’s integrated platform"),
    ("Alethia's integrated platform", "Prakriti's integrated platform"),
    ("Alethia deployed its", "Prakriti deployed its"),
    ("Alethia established a defensible", "Prakriti established a defensible"),
    ("Media & News - Alethia", "Media & News - Prakriti"),
    ("Research & Insights - Alethia", "Research & Insights - Prakriti"),
    ("Case Studies - Alethia", "Case Studies - Prakriti"),
    ("Alethia Team", "Prakriti Team"),

    # Person & Team
    ("Bautista Saubidet Birkner", "Rohan Sharma"),
    ("Bautista Saubidet", "Rohan Sharma"),
    ("Maia Moreno", "Dr. Ananya Roy"),

    # Case study & Partner identities
    ("Case Study: Adecoagro: From Regenerative Agriculture to Verified Climate Performance",
     "Case Study: AgroVeritas: From Regenerative Agriculture to Verified Climate Performance"),
    ("Adecoagro, one of Latin America’s leading food and energy producers",
     "AgroVeritas Ecosystems, one of the leading regional agro-ecological initiatives"),
    ("Adecoagro, one of Latin America's leading food and energy producers",
     "AgroVeritas Ecosystems, one of the leading regional agro-ecological initiatives"),
    ("Adecoagro’s rice and crop systems", "AgroVeritas’s rice and crop systems"),
    ("Adecoagro's rice and crop systems", "AgroVeritas's rice and crop systems"),
    ("Adecoagro needed a way", "AgroVeritas needed a way"),
    ("Adecoagro could see a clear", "AgroVeritas could see a clear"),
    ("Adecoagro’s operations", "AgroVeritas’s operations"),
    ("Adecoagro's operations", "AgroVeritas's operations"),
    ("positioned Adecoagro to expand", "positioned AgroVeritas to expand"),
    ("integrated into Adecoagro’s", "integrated into AgroVeritas’s"),
    ("integrated into Adecoagro's", "integrated into AgroVeritas's"),
    ("Adecoagro is prepared", "AgroVeritas is prepared"),
    ("solidify Adecoagro’s", "solidify AgroVeritas’s"),
    ("solidify Adecoagro's", "solidify AgroVeritas's"),
    ("Adecoagro", "AgroVeritas"),

    # General brand tokens
    ("alethia.earth", "prakriti.earth"),
    ("Alethia", "Prakriti"),
    ("ALETHIA", "PRAKRITI"),
    ("alethia", "prakriti"),
]

def transform_text(text):
    if not isinstance(text, str):
        return text
    for src, dst in REPLACEMENTS:
        text = text.replace(src, dst)
    return text

class FramerCMSParser:
    def __init__(self, data):
        self.data = data
        self.offset = 0

    def read_u8(self):
        v = self.data[self.offset]; self.offset += 1; return v

    def read_u16(self):
        v = struct.unpack_from('>H', self.data, self.offset)[0]; self.offset += 2; return v

    def read_u32(self):
        v = struct.unpack_from('>I', self.data, self.offset)[0]; self.offset += 4; return v

    def read_i64(self):
        v = struct.unpack_from('>q', self.data, self.offset)[0]; self.offset += 8; return v

    def read_f64(self):
        v = struct.unpack_from('>d', self.data, self.offset)[0]; self.offset += 8; return v

    def read_string(self):
        l = self.read_u32()
        s = self.data[self.offset:self.offset+l].decode('utf-8')
        self.offset += l
        return s

    def read_value(self):
        tag = self.read_u8()
        if tag == 0: return ('null', None)
        elif tag == 1:
            count = self.read_u16()
            return ('array', [self.read_value() for _ in range(count)])
        elif tag == 2: return ('bool', self.read_u8() != 0)
        elif tag == 3: return ('color', self.read_string())
        elif tag == 4: return ('date', self.read_i64())
        elif tag == 5: return ('enum', self.read_string())
        elif tag == 6: return ('file', self.read_string())
        elif tag == 7: return ('link', self.read_string())
        elif tag == 8: return ('number', self.read_f64())
        elif tag == 9:
            count = self.read_u16()
            obj = {self.read_string(): self.read_value() for _ in range(count)}
            return ('object', obj)
        elif tag == 10: return ('image', self.read_string())
        elif tag == 11:
            subtag = self.read_u8()
            return ('richtext', (subtag, self.read_string()))
        elif tag == 12: return ('string', self.read_string())
        elif tag == 13: return ('vectorset', self.read_u32())
        else:
            raise ValueError(f'Unknown tag {tag} at offset {self.offset-1}')

class FramerCMSWriter:
    def __init__(self):
        self.buf = bytearray()

    def write_u8(self, v): self.buf.append(v & 0xff)
    def write_u16(self, v): self.buf.extend(struct.pack('>H', v))
    def write_u32(self, v): self.buf.extend(struct.pack('>I', v))
    def write_i64(self, v): self.buf.extend(struct.pack('>q', v))
    def write_f64(self, v): self.buf.extend(struct.pack('>d', v))

    def write_string(self, s):
        b = s.encode('utf-8')
        self.write_u32(len(b))
        self.buf.extend(b)

    def write_value(self, val):
        t, v = val
        if t == 'null':
            self.write_u8(0)
        elif t == 'array':
            self.write_u8(1)
            self.write_u16(len(v))
            for item in v: self.write_value(item)
        elif t == 'bool':
            self.write_u8(2)
            self.write_u8(1 if v else 0)
        elif t == 'color':
            self.write_u8(3)
            self.write_string(v)
        elif t == 'date':
            self.write_u8(4)
            self.write_i64(v)
        elif t == 'enum':
            self.write_u8(5)
            self.write_string(v)
        elif t == 'file':
            self.write_u8(6)
            self.write_string(v)
        elif t == 'link':
            self.write_u8(7)
            self.write_string(v)
        elif t == 'number':
            self.write_u8(8)
            self.write_f64(v)
        elif t == 'object':
            self.write_u8(9)
            self.write_u16(len(v))
            for k, item in v.items():
                self.write_string(k)
                self.write_value(item)
        elif t == 'image':
            self.write_u8(10)
            self.write_string(v)
        elif t == 'richtext':
            self.write_u8(11)
            subtag, s = v
            self.write_u8(subtag)
            self.write_string(s)
        elif t == 'string':
            self.write_u8(12)
            self.write_string(v)
        elif t == 'vectorset':
            self.write_u8(13)
            self.write_u32(v)

def transform_value(val):
    t, v = val
    if t == 'string':
        return (t, transform_text(v))
    elif t == 'richtext':
        subtag, s = v
        return (t, (subtag, transform_text(s)))
    elif t == 'image':
        return (t, transform_text(v))
    elif t == 'link':
        return (t, transform_text(v))
    elif t == 'array':
        return (t, [transform_value(x) for x in v])
    elif t == 'object':
        return (t, {k: transform_value(x) for k, x in v.items()})
    else:
        return val

def process_chunk(path):
    print(f'Processing {path}...')
    with open(path, 'rb') as f:
        data = f.read()

    p = FramerCMSParser(data)
    num_records = p.read_u32()
    new_records = []

    for r in range(num_records):
        num_fields = p.read_u16()
        fields = []
        for _ in range(num_fields):
            name = p.read_string()
            val = p.read_value()
            new_val = transform_value(val)
            fields.append((name, new_val))
        new_records.append(fields)

    w = FramerCMSWriter()
    w.write_u32(len(new_records))
    item_offsets = [] # (offset, length)
    for fields in new_records:
        rec_start = len(w.buf)
        w.write_u16(len(fields))
        for k, v in fields:
            w.write_string(k)
            w.write_value(v)
        rec_len = len(w.buf) - rec_start
        item_offsets.append((rec_start, rec_len))

    new_data = bytes(w.buf)
    with open(path, 'wb') as f:
        f.write(new_data)
    print(f'  Updated {path}: {len(data)} -> {len(new_data)} bytes. Items: {item_offsets}')
    return item_offsets

def process_indexes(path, item_offsets):
    print(f'Processing index {path}...')
    with open(path, 'rb') as f:
        data = f.read()

    new_data = bytearray(data)
    for src, dst in [
        (b"Alethia's", b"Prakriti's"),
        (b"Alethia\xe2\x80\x99s", b"Prakriti\xe2\x80\x99s"),
        (b"Alethia", b"Prakriti"),
        (b"alethias-", b"prakritis-"),
        (b"Adecoagro", b"AgroVeritas")
    ]:
        idx = 0
        while True:
            pos = new_data.find(src, idx)
            if pos == -1: break
            if pos >= 4:
                old_l = struct.unpack_from('>I', new_data, pos-4)[0]
                if old_l >= len(src):
                    diff = len(dst) - len(src)
                    new_l = old_l + diff
                    struct.pack_into('>I', new_data, pos-4, new_l)
            new_data[pos:pos+len(src)] = dst
            idx = pos + len(dst)

    with open(path, 'wb') as f:
        f.write(new_data)
    print(f'  Updated index {path}: {len(data)} -> {len(new_data)} bytes.')

def main():
    import urllib.request
    chunks = [
        ('framerusercontent.com/cms/3mNtgy8pfkniYPTyBHeX/LNzwe2L4ZhztYODkLuo2/mcdL8OCmS-chunk-default-0.framercms',
         'framerusercontent.com/cms/3mNtgy8pfkniYPTyBHeX/LNzwe2L4ZhztYODkLuo2/mcdL8OCmS-indexes-default-0.framercms',
         'https://framerusercontent.com/cms/3mNtgy8pfkniYPTyBHeX/LNzwe2L4ZhztYODkLuo2/mcdL8OCmS-chunk-default-0.framercms',
         'https://framerusercontent.com/cms/3mNtgy8pfkniYPTyBHeX/LNzwe2L4ZhztYODkLuo2/mcdL8OCmS-indexes-default-0.framercms'),
        ('framerusercontent.com/cms/76RnKRWm3DMl5fWUimzL/DpENvMTsqtR0MKO4L6hs/HPP6OkUXl-chunk-default-0.framercms',
         'framerusercontent.com/cms/76RnKRWm3DMl5fWUimzL/DpENvMTsqtR0MKO4L6hs/HPP6OkUXl-indexes-default-0.framercms',
         'https://framerusercontent.com/cms/76RnKRWm3DMl5fWUimzL/DpENvMTsqtR0MKO4L6hs/HPP6OkUXl-chunk-default-0.framercms',
         'https://framerusercontent.com/cms/76RnKRWm3DMl5fWUimzL/DpENvMTsqtR0MKO4L6hs/HPP6OkUXl-indexes-default-0.framercms'),
        ('framerusercontent.com/cms/s1WjcTp5of1oFg6IotGU/owr39drwpBsU6BPW8ucU/B33wnMHvT-chunk-default-0.framercms',
         'framerusercontent.com/cms/s1WjcTp5of1oFg6IotGU/owr39drwpBsU6BPW8ucU/B33wnMHvT-indexes-default-0.framercms',
         'https://framerusercontent.com/cms/s1WjcTp5of1oFg6IotGU/owr39drwpBsU6BPW8ucU/B33wnMHvT-chunk-default-0.framercms',
         'https://framerusercontent.com/cms/s1WjcTp5of1oFg6IotGU/owr39drwpBsU6BPW8ucU/B33wnMHvT-indexes-default-0.framercms'),
    ]

    for chunk_p, idx_p, cdn_chunk, cdn_idx in chunks:
        # Fetch clean base first from CDN to ensure zero byte corruption
        req_chunk = urllib.request.Request(cdn_chunk, headers={'User-Agent': 'Mozilla/5.0'})
        with open(chunk_p, 'wb') as f:
            f.write(urllib.request.urlopen(req_chunk, timeout=10).read())
        req_idx = urllib.request.Request(cdn_idx, headers={'User-Agent': 'Mozilla/5.0'})
        with open(idx_p, 'wb') as f:
            f.write(urllib.request.urlopen(req_idx, timeout=10).read())

        offsets = process_chunk(chunk_p)
        process_indexes(idx_p, offsets)

    print('\nAll CMS chunks and indexes processed successfully!')

if __name__ == '__main__':
    main()
