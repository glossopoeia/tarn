# Byte-shuffle measurements on interleaved data (Q-E2)

The measurement that settled Q-E2 (shuffle scope on interleaved
layers), per its "what settles it" clause. Fully synthetic and
reproducible; no external datasets.

## Method

Each dataset is generated with a fixed PRNG seed (42), byte-shuffled
with the stated stride (view the buffer as n = length/stride groups
of stride bytes; output byte i·n + j = input byte j·stride + i), and
compressed with zlib (deflate) level 6, unshuffled vs shuffled.
"Gain" is 1 − shuffled/unshuffled compressed size. deflate stands
proxy for the codec menu; shuffle's mechanism (grouping
same-significance bytes) is codec-agnostic.

Datasets, chosen for the workloads interleaved layout exists for:

1. **rgb8** — 256×256 interleaved RGB uint8, per-channel smooth
   gradients (x-, y-, and xy-ramps over 0–255) plus uniform noise
   ±6; stride 3.
2. **points** — 50,000 records of float32 x, y, z + uint8 class
   (x: 0.01-step ramp with σ=0.02 gaussian noise; y: 100·sin(i/1000)
   with σ=0.05; z: 500 with σ=2; class uniform 0–4), packed
   `<fffB`; stride 13.
3. **u16x4** — 128×128 four-channel uint16, smooth
   sin·cos fields around 2048 (amplitude 1000, per-channel phase
   offset 17·ch, σ=8 noise, clamped 0–4095), little-endian;
   stride 8.
4. **f32-planar control** — 65,536 float32
   (20 + 5·sin(i/1000) + σ=0.1 noise), stride 4 — the known planar
   baseline the interleaved results are compared against.

## Results

| dataset | raw bytes | zlib | zlib after shuffle | gain |
|---|---|---|---|---|
| rgb8 interleaved (stride 3) | 196,608 | 181,091 | 167,015 | 7.8% |
| points interleaved (stride 13) | 650,000 | 534,236 | 357,058 | 33.2% |
| u16x4 interleaved (stride 8) | 131,072 | 99,603 | 71,882 | 27.8% |
| f32 planar control (stride 4) | 262,144 | 216,608 | 163,425 | 24.6% |

## Reading

Stride-Q shuffle on interleaved tiles delivers gains comparable to
the planar element-size case on float- and wide-integer-heavy data
(33.2% and 27.8% vs the 24.6% control) and a modest gain on 8-bit
imagery (7.8%, where bytes are already whole values). That is the
"benefit materializes" outcome Q-E2's settling clause asked for:
interleaved layers are in scope with stride = sample stride Q
(ADR-0039).
