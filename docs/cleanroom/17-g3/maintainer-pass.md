# Maintainer's own pass over round 16's repairs (run while round 17 was in flight)

**M-01 — the growth permission is not aligned with the bar it sits under.
Pre-existing, sharpened by five revisions of the surrounding text.**
The bar enumerates "the set of padding positions (§11.3)" among the things a
commit MUST NOT alter for a tile stored in the superseded generation.
Growing an extent alters exactly that: extents (8,8)/tiles (4,4) with E_x = 7
makes x = 7 padding in the stored edge tile t = (0,1); growing E_x to 8 makes
it real. So the bar's general terms catch growth, while "an extent MAY
**grow**" permits it outright two sentences later.
The effect-test gloss does not cleanly rescue it either. It spares "a change
that leaves every one of those tiles' stored bytes meaning exactly what they
meant" — and after growth the byte at x = 7 means a real sample where it
meant padding, which is the whole point of growing.
Readings: (a) the express MAY is an exception to the general MUST NOT, which
is the ordinary construction and what a careful reader takes; (b) the bar
governs and growth is barred wherever a stored edge tile has padding, which
would make the MAY inoperative in the only case it addresses.
I pick (a). Not obviously byte-level — reading (b) forbids an operation
rather than licensing different bytes, and the file growth produces is
conforming under both — but it is the same rule-versus-exception misalignment
that rounds 14 and 16 both found in this paragraph, and it is the last limb
of it still unaligned.
Fix: say growth is an exception rather than a parallel permission — "the bar
notwithstanding, an extent MAY grow …" — or add "other than by growth" to the
padding-set limb.
