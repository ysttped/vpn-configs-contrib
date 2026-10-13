# RIDIBatang XTF fonts for XTEink X3

| File | Size (px) | Cell (W×H) | Glyphs |
| --- | --- | --- | --- |
| `30_RIDIBatang.xtf` | 30 | 31×39 | 31,321 |
| `32_RIDIBatang.xtf` | 32 | 33×43 | 31,321 |

Generated from `RIDIBatang.otf` with the official XT-Cloud XTFont Maker worker
(`xtfont.worker-DNIsIZBe.js`) using its default settings: 2bpp, gamma 1.8,
thresholds `56,120,184`, auto embolden bias 0.1, full glyph scope plus the
default device character set, and system fallback enabled. Characters missing
from RIDIBatang (mostly Hanja) are rendered with Noto Serif CJK.

They cover the same codepoints as the reference `28_RIDIBatang.xtf`.

## Letter spacing

Both files use 1px tighter letter spacing while keeping word spacing unchanged:

1. Build once with `letterSpacing: 0` and once with `letterSpacing: -1`.
   The -1 build changes only advances; glyph bitmaps are identical.
2. Run `restore_word_spacing.py ORIGINAL.xtf TIGHT.xtf OUT.xtf` to copy the
   original whitespace advances back into the tight build. It restores the
   U+0020 entry of the ASCII table, the header ASCII fallback width (used for
   EPUB no-break spaces) and the per-glyph advance of every whitespace code
   point, then recomputes both CRC32 fields.

| Advance | 30 | 32 |
| --- | --- | --- |
| Space (U+0020, U+00A0) | 11 (unchanged) | 12 (unchanged) |
| Hangul / Hanja (header full width) | 31 → 30 | 33 → 32 |
| ASCII letters, digits, punctuation | −1 each | −1 each |

U+3000 (ideographic space) follows the header full width on the device, so it
is 1px narrower too.

Copy the file to the `/fonts` folder on the device's microSD card.
