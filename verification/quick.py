"""Paper I -- the short check (a few minutes; it is the check of the GitHub Actions workflow).  Python 3.11 grammar.
Reruns, in a temporary copy, the interval arithmetic that does not need the repository of paper H, and compares each new record with the stored one:
  the self-test of the interval arithmetic (dn_ivtest.py), Lemmas 15, 20, 21, 27 (dq_m4.py, du_cl.py, dv_m3.py, dq_ej.py), Proposition 13 (dp_room2.py),
  Proposition 6 and Lemma 7 at their worst points (dr_be.py, ds_check.py); the map of Theorem 1 (map_check.py); the tables of App. C from the records.
The full verification is verification/run_all.py."""
import json, os, sys, filecmp, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import ROOT, check, finish, workdir, run, rerun_and_compare
import map_check


def main():
    w = workdir()
    try:
        rerun_and_compare(w, 'dn_ivtest.py', 'dn_ivtest.json', '(i) interval arithmetic: true values inside, wrong versions caught')
        rerun_and_compare(w, 'dq_m4.py', 'dq_m4.json', '(iii) Lemma 15, M4(1e-4) <= 2.0475')
        rerun_and_compare(w, 'du_cl.py', 'du_cl.json', '(iii) Lemma 20, M1 and M2 at y = 1e-4, and the identity of c_L')
        rerun_and_compare(w, 'dv_m3.py', 'dv_m3.json', '(iii) Lemma 21 (by hand): the closed forms and the wrong versions V1-V4')
        rerun_and_compare(w, 'dq_ej.py', 'dq_ej.json', '(iii) Lemma 27, E_J')
        rerun_and_compare(w, 'dp_room2.py', 'dp_room2.json', '(iii) Proposition 13, focus at the resolution')
        rerun_and_compare(w, 'dr_be.py', 'dr_be.json', '(iv) Proposition 6 and the constants of Theorem 5')
        rerun_and_compare(w, 'ds_check.py', 'ds_check.json', '(iv) Lemma 7 and the order of the remainders')
        m = map_check.run()
        check('(vi) the map of Theorem 1: %d points (ell from 55.26 to 1e8, every boundary), %d gaps; the inequalities of the proof hold; %d of %d wrong maps show a gap'
              % (m['points'], m['n_gaps'], sum(m['power (a gap must appear)'].values()), len(m['power (a gap must appear)'])), m['ok'])
        rc, out, sec = run(w, 'du_tables.py')
        same = rc == 0 and filecmp.cmp(os.path.join(w, 'paperI', 'sections', 'C_tables.tex'), os.path.join(ROOT, 'paper', 'sections', 'C_tables.tex'), shallow=False)
        check('(v) the tables of App. C, generated again from results/du_fix.json, equal paper/sections/C_tables.tex', same)
    finally:
        shutil.rmtree(w, ignore_errors=True)
    finish()


if __name__ == '__main__':
    main()
