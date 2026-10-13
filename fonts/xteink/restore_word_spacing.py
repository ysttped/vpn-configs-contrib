"""Restore word-space advances in an XTF built with a negative letterSpacing.

Usage: python3 restore_word_spacing.py ORIGINAL.xtf TIGHT.xtf OUT.xtf

ORIGINAL is built with letterSpacing 0 and TIGHT with letterSpacing -1, from the
same font and settings. OUT is TIGHT with whitespace advances copied back from
ORIGINAL: the U+0020 entry of the ASCII table, header asciiWidth (0x0E, the
firmware's fallback for EPUB no-break spaces) and the per-glyph advance byte of
every whitespace code point. Both CRC32 fields are recomputed.
"""
import struct
import sys
import zlib

WHITESPACE = (
    [*range(0x09, 0x0E), 0x20, 0x85, 0xA0, 0x1680, *range(0x2000, 0x200C),
     0x2028, 0x2029, 0x202F, 0x205F, 0x2060, 0x3000, 0xFEFF]
)


def parse(data):
    if data[:4] != b"XTF0":
        raise ValueError("not an XTF0 file")
    ranges, glyphs = struct.unpack_from("<II", data, 0x14)
    data_off, block = struct.unpack_from("<II", data, 0x24)
    table_end = struct.unpack_from("<I", data, 0x38)[0]
    index = {}
    for i in range(ranges):
        start, count, base, _, _ = struct.unpack_from("<IIIHH", data, 0x40 + 16 * i)
        for k in range(count):
            index[start + k] = base + k
    return index, data_off, block, table_end, glyphs


def main(orig_path, tight_path, out_path):
    orig = open(orig_path, "rb").read()
    out = bytearray(open(tight_path, "rb").read())
    o_idx, o_off, o_block, o_table, _ = parse(orig)
    t_idx, t_off, t_block, t_table, t_glyphs = parse(out)
    if o_idx != t_idx or o_block != t_block or orig[0x0A:0x0D] != out[0x0A:0x0D]:
        raise ValueError("files were not built from the same font and size")

    out[t_table] = orig[o_table]  # U+0020 in the ASCII advance table
    out[0x0E] = orig[0x0E]        # header asciiWidth
    for cp in WHITESPACE:
        if cp in t_idx:
            out[t_off + t_block * t_idx[cp]] = orig[o_off + o_block * o_idx[cp]]

    if len(out) != t_off + t_block * t_glyphs:
        raise ValueError("unexpected glyph data length")
    struct.pack_into("<I", out, 0x30, zlib.crc32(out[t_off:]))
    struct.pack_into("<I", out, 0x34, zlib.crc32(out[:0x34]))
    open(out_path, "wb").write(out)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    main(*sys.argv[1:])
