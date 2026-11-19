# resolution-gap-every-focus

**Wherever the observer focuses: the lower side of the logarithmic law of the resolution gap at every focus and every resolution**

Code, stored results, interval-arithmetic proofs and a verification script for the paper by Taishi Namba (2026).

**Paper:** T. Namba, *Wherever the observer focuses: the lower side of the logarithmic law of the resolution gap at every focus and every resolution*, preprint, Zenodo (2026), [doi:10.5281/zenodo.24371172](https://doi.org/10.5281/zenodo.24371172) (all versions; v1.0 is [10.5281/zenodo.24371173](https://doi.org/10.5281/zenodo.24371173)).

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24370921.svg)](https://doi.org/10.5281/zenodo.24370921)
[![verify](https://github.com/neginyan/resolution-gap-every-focus/actions/workflows/verify.yml/badge.svg)](https://github.com/neginyan/resolution-gap-every-focus/actions/workflows/verify.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## The result in brief

This is the follow-up to [paper H](https://doi.org/10.5281/zenodo.23932698) (code: [resolution-gap-weak-ripple](https://github.com/neginyan/resolution-gap-weak-ripple)), which proved the lower side of the logarithmic law of the resolution gap for windows with a weak ripple when the observer's focus spans at least about 0.7 ripple periods and ℓ = ln(1/σ) ≤ 960.8. Here the focus and the resolution are free.

- **Theorem 1 (every focus, every resolution).** For every window with a weak ripple (η ≤ 1/ℓ) and every ℓ ≥ 55.26 (σ ≤ e^{−55.26} ≈ 1.002 × 10⁻²⁴, with no lower limit on σ), every state satisfies g√ℓ ≥ 1 − ε̄. For ℓ ≥ 960.8 every state satisfies the stronger bound g√ℓ ≥ (1 − ε̄)√(1 + 10/ℓ).
- **Five statements, one for each kind of focus.** Narrow focus (Theorem 2, computer-assisted), focus at the resolution (Theorem 3, proof), wide focus (Theorem 4, computer-assisted), very wide focus (Theorem 5, proof), and Theorem H1 of paper H for the moderate range. A check of the map shows that every state lies in the range of one of them.
- **Computer assistance by decimal interval arithmetic.** The computer-assisted parts of this paper are decimal interval arithmetic with outward rounding, run with `decimal.Inexact` trapped, so that no inexact operation can escape the rounding. They do not use the assumption on floating-point elementary functions that the certificates of paper H use.
- **Tried to break first.** Every lemma and every line was attacked with adversarial searches before it was proved, and every search reports the deliberately wrong versions it can break (§VIII of the paper).

Every statement in the paper carries its status: proof, computer-assisted proof, derivation, numerical, or conjecture.

## Verify

```bash
pip install -r requirements.txt
python verification/quick.py                                       # a few minutes; no other repository needed
python verification/run_all.py --h-repo ../resolution-gap-weak-ripple   # about ten minutes
```

`quick.py` reruns the interval arithmetic of Lemmas 15, 20, 21 and 27, of Propositions 6 and 13 and of Lemma 7, the self-test of the interval arithmetic and the map of Theorem 1, and generates the tables of App. C again from the records. It is the check of the GitHub Actions workflow.

`run_all.py` runs `quick.py` and then Propositions 12 and 14 on all 9,809 and 6,952 pieces (with the corrected constant 9.549), the absorptions (R1) and (R3), the four figures, and the comparison with the true quantities; with the repository of paper H it also checks that the statements of paper H used here are in its text. Some modules of this paper import modules of paper H's repository (v1.3), which are not copied here: pass its location with `--h-repo` or the environment variable `H_REPO`.

Every rerun is made in a temporary copy and compared with the stored record entry by entry (flags, counts and interval bounds exactly; double-precision floats up to a relative 10⁻⁹, since their last digits may differ between machines); the stored records are never overwritten. Theorem H1 is certified by the repository of paper H (its `verification/run_all.py`), not here.

## What is where

| result | status | script → results |
|---|---|---|
| Theorem 1 (assembly; the map of the five ranges) | proof | `verification/map_check.py` |
| Theorem 2 / Proposition 12 (narrow focus, 48 numbers and 18 conditions) | computer-assisted | `src/dl_consts.py` (with 9.549 by `src/du_fix.py`) → `results/du_fix.json`; tables of App. C: `src/du_tables.py` |
| absorptions (R1), (R3) | computer-assisted | `src/dp_r1.py` → `results/dp_r1.json` |
| Theorem 3 / Proposition 13 (focus at the resolution) | proof | `src/dp_room2.py` → `results/dp_room2.json`; Lemma 21 (by hand): `src/dv_m3.py` → `results/dv_m3.json` |
| Theorem 4 / Proposition 14 (wide focus) | computer-assisted | `src/dp_room1.py`, `src/dq_room1_low.py` (with 9.549 by `src/du_fix.py`) → `results/du_fix.json` |
| Lemma 15 (M₄), Lemma 20 (M₁, M₂), Lemma 27 (E_J) | computer-assisted | `src/dq_m4.py`, `src/du_cl.py`, `src/dq_ej.py` |
| Theorem 5 / Proposition 6, Lemma 7 | proof (constants in interval arithmetic) | `src/dr_be.py`, `src/ds_check.py` |
| interval arithmetic and its self-test | — | `src/dl_interval.py`, `src/dn_ivtest.py`, `src/do_check.py` |
| the lines and their audit (App. B), the searches (§VIII) | derivation / numerical | `src/dj_lines.py`, `src/dj_proof.py`, `src/dk_*.py`, `src/dm_groups.py`, `src/dp_search.py`, `src/dp_truth.py`, `src/dr_truth.py` |
| figures | — | `src/ds_figure.py`, `src/dt_figures.py` |

| folder | content |
|---|---|
| `src/` | the code of the paper (Python 3, NumPy, SciPy, Matplotlib) |
| `results/` | the stored records |
| `verification/` | `quick.py`, `run_all.py`, `map_check.py`, `common.py` |
| `paper/` | LaTeX source of the paper (REVTeX 4.2) its figures and the PDF of v1.0 |

The working record of the proofs (the stage reports of the lab sessions) is kept by the author.

## Known issues

None at present.

## Related work by the author

- T. Namba, *Beyond few harmonics: the lower side of the logarithmic law of the resolution gap for windows with a weak ripple*, Zenodo (2026), [doi:10.5281/zenodo.23932698](https://doi.org/10.5281/zenodo.23932698) (paper H; code [resolution-gap-weak-ripple](https://github.com/neginyan/resolution-gap-weak-ripple)).
- T. Namba, *How fine can a hidden ripple be? A two-sided logarithmic law for the resolution gap of the arrow of time*, Zenodo (2026), [doi:10.5281/zenodo.23856796](https://doi.org/10.5281/zenodo.23856796) (paper F; code [resolution-gap-two-sided](https://github.com/neginyan/resolution-gap-two-sided)).

Paper F and its repository are not changed by this work. This work uses version 1.3 of paper H ([doi:10.5281/zenodo.24369012](https://doi.org/10.5281/zenodo.24369012)), prepared together with it.

## Use of AI assistants

The study was carried out with AI assistants: Anthropic Claude (planning, proofs, computations, code, verification and drafting), Google Gemini and OpenAI ChatGPT (review of the manuscript). Their roles are described in the acknowledgments of the paper. The author directed the research and takes full responsibility for it.

## Citation

Please cite the paper ([doi:10.5281/zenodo.24371172](https://doi.org/10.5281/zenodo.24371172)) and this repository; see `CITATION.cff`. The code is archived at Zenodo: [doi:10.5281/zenodo.24370921](https://doi.org/10.5281/zenodo.24370921) (all versions; v1.0.0 is [10.5281/zenodo.24370922](https://doi.org/10.5281/zenodo.24370922)).

## License

MIT © 2026 Taishi Namba
