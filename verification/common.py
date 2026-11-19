"""Shared helpers of verification/quick.py and verification/run_all.py (paper I).  Python 3.11 grammar.
Every rerun is made in a temporary work folder that holds a copy of src/*.py and of results/; the record it writes there is compared with the stored
record of results/, entry by entry, ignoring only timing and environment entries.  The stored records are never overwritten.
Booleans, integers and strings (among them every interval-arithmetic bound kept as a decimal string, and every 'ok' entry) are compared exactly.
Floats from double-precision numerical steps may differ in the last digits between machines (CPU, libm, BLAS); they are compared with a relative
tolerance FLOAT_RTOL, and two floats that are both at the rounding level (|x| <= FLOAT_ATOL, e.g. a quadrature-against-closed-form difference) are
taken as equal."""
import json, os, shutil, subprocess, sys, tempfile, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORE = ('second', 'python', 'numpy', 'platform', 'elapsed', 'time')
RES = []
FLOAT_RTOL = 1e-9
FLOAT_ATOL = 1e-6


def check(name, ok, info=''):
    RES.append(bool(ok)); print(('[PASS] ' if ok else '[FAIL] ') + name + (('  ' + info) if info else ''), flush=True)


def finish():
    n, p = len(RES), sum(RES)
    print('\n%d/%d checks passed' % (p, n)); sys.exit(0 if p == n else 1)


def workdir():
    w = tempfile.mkdtemp(prefix='paperI_verify_')
    for f in os.listdir(os.path.join(ROOT, 'src')):
        if f.endswith('.py'): shutil.copy(os.path.join(ROOT, 'src', f), w)
    shutil.copytree(os.path.join(ROOT, 'results'), os.path.join(w, 'results'))
    os.makedirs(os.path.join(w, 'paperI', 'figures')); shutil.copytree(os.path.join(ROOT, 'paper', 'sections'), os.path.join(w, 'paperI', 'sections'))
    return w


def h_src():
    """the src/ folder of the repository of paper H (v1.3), from --h-repo PATH or the environment variable H_REPO; None if not given."""
    p = None
    if '--h-repo' in sys.argv: p = sys.argv[sys.argv.index('--h-repo') + 1]
    p = p or os.environ.get('H_REPO')
    if not p: return None
    s = os.path.join(os.path.abspath(p), 'src')
    return s if os.path.isfile(os.path.join(s, 'cl_link.py')) else None


def run(w, script, args=(), hsrc=None, timeout=7200):
    env = dict(os.environ)
    if hsrc: env['PYTHONPATH'] = hsrc + (os.pathsep + env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
    t0 = time.time()
    p = subprocess.run([sys.executable, '-W', 'ignore', script] + list(args), cwd=w, env=env, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout + p.stderr, time.time() - t0


def strip(o):
    if isinstance(o, dict): return {k: strip(v) for k, v in o.items() if not any(s in k.lower() for s in IGNORE)}
    if isinstance(o, list): return [strip(v) for v in o]
    return o


def diff(a, b, path=''):
    """first difference between two records (None if equal)."""
    if isinstance(a, dict) and isinstance(b, dict):
        if set(a) != set(b): return path + ': keys ' + str(sorted(set(a) ^ set(b))[:3])
        for k in a:
            d = diff(a[k], b[k], path + '/' + k)
            if d: return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b): return path + ': lengths %d, %d' % (len(a), len(b))
        for i, (x, y) in enumerate(zip(a, b)):
            d = diff(x, y, '%s[%d]' % (path, i))
            if d: return d
        return None
    if isinstance(a, float) and isinstance(b, float) and not isinstance(a, bool):
        if a == b or (abs(a) <= FLOAT_ATOL and abs(b) <= FLOAT_ATOL) or abs(a - b) <= FLOAT_RTOL * max(abs(a), abs(b)):
            return None
    return None if a == b else '%s: %r vs %r' % (path, a, b)


def same_record(w, name, only=None):
    a = strip(json.load(open(os.path.join(w, 'results', name), encoding='utf-8')))
    b = strip(json.load(open(os.path.join(ROOT, 'results', name), encoding='utf-8')))
    if only: a = {k: v for k, v in a.items() if k in only}; b = {k: v for k, v in b.items() if k in only}
    return diff(a, b)


def rerun_and_compare(w, script, record, label, args=(), hsrc=None, only=None):
    """only: compare these top-level entries of the record (the others must still say ok, if they have an 'ok' entry)."""
    rc, out, sec = run(w, script, args, hsrc)
    d = same_record(w, record, only) if rc == 0 and os.path.exists(os.path.join(w, 'results', record)) else 'no record written'
    if d is None and only:
        new = json.load(open(os.path.join(w, 'results', record), encoding='utf-8'))
        if not new.get('ok', True): d = 'the rerun record says ok = false'
    check('%s (%s, %.0f s): exit %d, the rerun record equals results/%s%s' % (label, script, sec, rc, record, '' if not d else ' -- first difference: ' + d[:200]),
          rc == 0 and d is None, '' if rc == 0 else out[-600:])
