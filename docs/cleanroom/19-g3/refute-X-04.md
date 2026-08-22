# The finding

**The widened SHOULD is conditioned on a fact the compactor is forbidden to observe — the repair's own example says so**

Location: §20.5, spec/tarn.md lines 3178-3185 (the widened trigger), against [R-WRT-09]'s stated depth at line 3153 and §20.4's no-drop rule for user-metadata records

## Detail

The old trigger, 'Where any such bit is set', was a trailer inspection: cheap, local, and always available to the actor the rule binds. The new trigger is a predicate over the whole output, and the repair's own illustration puts one of its two instances beyond the actor's reach: 'an unrecognized `tarn.` key in a record it never decoded'.

The compactor cannot decode it. §20.5, twelve lines above the repair: 'its verification depth is [R-WRT-09]'s and reaches no decoded content.' And it cannot drop the record either — §20.4: 'No commit therefore removes a layer record, or a user-metadata record at either scope.' So the record is always carried, always undecoded, and whether it holds an unrecognized `tarn.` key is always unknown to the actor whose SHOULD turns on it.

Two readings, both competent:
(a) CONSERVATIVE. The compactor cannot rule out an unimplemented feature in any input carrying a user-metadata record, so it always takes the input's minor as its floor. This collapses the 'Otherwise' branch to the empty case for every file with metadata.
(b) LITERAL. The SHOULD bites on features the compactor knows it does not implement; one it never looked for is not one it 'carries' in any sense it can act on, so it takes [R-CNT-26]'s plain floor.

Compact the same conforming minor-3 input, carrying an undecoded top-level user-metadata record, under both: (a) emits version_minor = 3, (b) emits version_minor = 0. Both outputs are conforming. Nothing in the document resolves which the SHOULD asks for, because the document simultaneously conditions the obligation on the content and forbids the actor to read the content.

The old wording had no such gap. This is a new ambiguity the repair introduced while fixing a real one.

## Text complained about

"Where the output carries any feature the compactor does not implement — by any of the four vehicles §10.1 enumerates (`[R-EXT-01]`), a carried ignore-lane bit and an unrecognized `tarn.` key in a record it never decoded being the two it is likeliest to meet — the output's version_minor SHOULD be at least the input's"

## Contradicting text

§20.5, spec/tarn.md line 3153: "a violation latent in a structure it carries forward verbatim travels into its output (`[R-WRT-01]`) — its verification depth is `[R-WRT-09]`'s and reaches no decoded content."

## Auditor's byte-level rationale

Byte-level. Two competent compactors: implementation A (conservative) writes version_minor = 3, implementation B (literal) writes version_minor = 0, at trailer offset F−56 (the field Appendix A shows at [74,76) of its worked file), compacting the same conforming input. Both outputs are conforming files — §21.6, 'version_minor is higher than this text defines | Accepted; minors never gate' — so this is not a case where a register row bars one side under both readings. Only one reading has each actor in line with the SHOULD, and the two bytes on disk differ. The accept/reject verdict does not move; the emitted bytes do, and a conformance vector for a compacted trailer cannot be written until this is settled.

---

# The downgrade you must attack

Graded **REFUTED**, not byte-level. Its reasoning:

The finding rests on three claims, and each is refuted by text the auditor did not reach.

1. "Forbidden to observe" is not what the cited sentence says. Line 3153-3158 states a verification DEPTH — a MUST-verify floor — in a sentence whose subject is latent violations travelling forward. It is not a prohibition, and the document says so directly two subsections earlier: [R-WRT-01] (line 2869-2872) makes an appender and a compactor "readers of every structure they process (`[R-CNF-11]`)", and §19.2 line 2727 gives every reader "A reader MAY detect any violation earlier (`[R-CNF-12]`)". Nothing bars a compactor from decoding a user-metadata document it carries; [R-WRT-08] (§20.4) bars an updater from RE-ENCODING or modifying an unimplemented record, not from reading one. Supporting, though not by itself decisive: "decoded content" is this document's phrase for decoded tile samples (lines 1793, 1846, 2280, 3932), whereas §18.2 calls a metadata payload "the decoded document" — so line 3158 most plausibly does not even range over metadata documents. The auditor's "contradicting text" therefore does not contradict; it states an obligation floor the SHOULD sits above.

2. Reading (b) is not a reading the text admits, so there are not two competent readings. The trigger — "Where the output carries any feature the compactor does not implement" — has no knowledge quantifier. "Carries" is used in this document as an actor-independent property of bytes: §18.3 line 2572, "A file carrying an unrecognized `tarn.` key is **conforming**". The auditor's (b) rewrites "carries" as "carries so far as the actor looked", which the sentence does not say and the document's own usage of the verb forbids. What the compactor cannot always DO is evaluate the predicate; that is ignorance, not indeterminacy of the rule.

3. The claim that the repair introduced the gap is false on the document's own face. The pre-repair text routed the residual case to [R-CNT-26], and [R-CNT-26] (line 820) is itself "the lowest version_minor that defines every feature present in the file" — an equally actor-independent predicate over features the compactor may not recognize. So under the OLD wording, the auditor's very scenario (minor-3 input, undecoded metadata record carrying a minor-3 key, no ignore-lane bit) already had the compactor obliged to a floor of 3 it could not compute, while a literal implementation wrote 0. Identical divergence, pre-existing, in the rule the old text deferred to. The repair narrows it: it converts precisely the unknowable-floor case into a computable instruction, "at least the input's". The illustration "a record it never decoded" is candid about which instance the compactor will most often meet — it tells the implementer where conservatism is warranted — rather than conditioning the rule on knowledge.

4. The consequential claim also fails. The auditor says "a conformance vector for a compacted trailer cannot be written until this is settled." No vector was ever owed: [R-CNF-12] (line 260) — "Deviation from a SHOULD is not a violation for this purpose: §21's register enumerates MUST-level conditions only, and a verifier reports a SHOULD deviation as an advisory that does not bar certification. A verifier owes no search for one" — and §21.8's coverage duty runs to §21.2-§21.5 rows, all MUST-level. §21.7 already books this exact obligation as unwitnessed ("the floor its version_minor SHOULD take — are unwitnessed"), and the repair's own closing clause cites it.

I searched hard for the opposite outcome. I looked for any sentence capping a compactor's inspection (grep on "verification depth", "MAY verify", [R-WRT-03], [R-WRT-09]); for any rule making metadata decoding unavailable to a writer (§18.2 [R-MTA-09]/[R-MTA-10], §21.5's R1-R10, §19.2's extent-use tier); and for any second, conflicting statement of the compactor's minor (§20.3 step 6 line 3026 is the appender's and says "version_minor per [R-CNT-26]"; Appendix G item 8 line 4247-4252 is non-normative and already states the widened form, "where it carries any feature it does not implement takes §20.5's floor rather than `[R-CNT-26]`'s"). Nothing supports the finding; several passages foreclose it. I also checked the repair for the collateral damage this audit exists to catch — the "four vehicles" count matches §10.1's list exactly, [R-EXT-01] is that list's identifier, "[R-CNT-26]'s floor" names a phrase [R-CNT-26] actually uses ("the maximum of that floor"), the two branches remain exhaustive and exclusive, and §21.7's "two obligations" still matches "Neither obligation". The one thing the repair dropped, the "as it does for an appender (§20.3 step 6)" cross-reference, is an improvement, since [R-CNT-26]'s appender clause is a maximum against a prior trailer that a new-file compaction has none of.

At most this is a clarity nit: the illustration names the harder-to-detect instance without spelling out that a compactor which does not decode cannot evaluate the trigger and is then simply outside a SHOULD nobody can witness. That is not a defect, and it is not the defect reported.

Byte-level, independently: NO. The document determines the correct value objectively — where the output carries an unimplemented feature, at least the input's minor; otherwise [R-CNT-26]'s floor. In the auditor's scenario implementation B is deviating from a SHOULD, not exercising a licensed choice, so the two byte strings are not both what the document asks for. And whatever residual epistemic freedom exists is inherited unchanged from [R-CNT-26] and predates the repair, so no byte the repair touches moved.
