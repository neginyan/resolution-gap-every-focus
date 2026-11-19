"""Paper I -- the full verification (about ten minutes).  Python 3.11 grammar.
    python3 verification/run_all.py --h-repo PATH      (or the environment variable H_REPO)
PATH is the repository of paper H (resolution-gap-weak-ripple, v1.3): some modules of this paper import modules of it, which are not copied here.
It runs verification/quick.py first, then, in a temporary copy, compares every new record with the stored one:
  (ii)  Propositions 12 and 14 on all pieces with the constant 9.549 (du_fix.py: dl_consts.py on 9,809 pieces, dq_room1_low.py on 6,952 pieces, and the tails),
        and (R1), (R3) as one piece (dp_r1.py);
  (v)   the four figures drawn again from the records (ds_figure.py, dt_figures.py);
  (vii) the comparison with the true quantities at the resolution (dp_truth.py);
  (viii) if the repository of paper H is given: the statements of paper H used here are in its text (Lemma CM-1, the range of Lemma BE, Lemma R_theta).
Theorem H1 is certified by the repository of paper H (its verification/run_all.py), not here."""
import json, os, sys, shutil, subprocess, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, RES, check, finish, workdir, run, rerun_and_compare, h_src


def main():
    q = subprocess.run([sys.executable, os.path.join(ROOT, 'verification', 'quick.py')], capture_output=True, text=True)
    print(''.join('    ' + l + '\n' for l in q.stdout.splitlines() if l.strip()), end='')
    check('verification/quick.py', q.returncode == 0)
    hs = h_src()
    check('the repository of paper H is given (--h-repo or H_REPO): %s' % (os.path.dirname(hs) if hs else 'not given'), hs is not None)
    w = workdir()
    try:
        if hs:
            rerun_and_compare(w, 'du_fix.py', 'du_fix.json', '(ii) Propositions 12 and 14 on all pieces, constant 9.549, decimal.Inexact trapped', hsrc=hs)
            rerun_and_compare(w, 'dp_r1.py', 'dp_r1.json', '(ii) (R1) and (R3) on [55.26, inf) as one piece, and the numerical check (II)', hsrc=hs)
        rc1, o1, s1 = run(w, 'ds_figure.py'); rc2, o2, s2 = run(w, 'dt_figures.py')
        figs = ['fig_map', 'fig_cases', 'fig_lemma7', 'fig_true']
        made = all(os.path.getsize(os.path.join(w, 'paperI', 'figures', f + '.pdf')) > 1000 for f in figs if os.path.exists(os.path.join(w, 'paperI', 'figures', f + '.pdf')))
        made = made and all(os.path.exists(os.path.join(w, 'paperI', 'figures', f + '.pdf')) for f in figs)
        try:
            import matplotlib.image as mi, numpy as np
            same = [f for f in figs if np.array_equal(mi.imread(os.path.join(w, 'paperI', 'figures', f + '.png')), mi.imread(os.path.join(ROOT, 'paper', 'figures', f + '.png')))]
        except Exception as e:
            same = []
        check('(v) the four figures drawn again from the records (%d of 4 identical to the stored PNG, pixel by pixel)' % len(same), rc1 == 0 and rc2 == 0 and made and len(same) == 4)
        rerun_and_compare(w, 'dp_truth.py', 'dp_truth.json', '(vii) Theorem 3 against the true quantities')
        if hs:
            H = ''.join(open(f, encoding='utf-8').read() for f in sorted(glob.glob(os.path.join(os.path.dirname(hs), 'paper', 'sections', '*.tex'))))
            want = {'Lemma CM-1': r"xE_1\le\Bigl(1+\frac b2\Bigr)E_0\ln\frac{2B_0}{E_0}+\frac{\sqrt2}{e}\,b\,E_0'", 'the proof of CM-1 uses only f >= 0': r"The proof uses only $f\ge0$",
                    'Lemma BE, range (v1.3)': r"Let $\sigma\in[10^{-3000},e^{-55.26}]$", 'Lemma R_theta': r"\label{lem:Rtheta}", 'Lemma A4*': r"Lemma A4*"}
            miss = [k for k, v in want.items() if v not in H]
            check('(viii) the statements of paper H used here are in its text: %s' % ', '.join(want), not miss, ('missing: ' + ', '.join(miss)) if miss else '')
    finally:
        shutil.rmtree(w, ignore_errors=True)
    finish()


if __name__ == '__main__':
    main()
