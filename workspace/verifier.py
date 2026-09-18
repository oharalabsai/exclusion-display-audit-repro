'''exclusion-display-audit verifier (DRAFT, rung 2: exact certificates on frozen displayed relations).

STATUS: NOT EXECUTED BY THE DRAFTING SESSION. The search_architect backend denied every python
invocation (Bash and subagent both DENIED, 2026-09-18). The Director must run
    python verifier.py --fixtures   and   python verifier.py --witnesses
and read the report before this draft is promoted. Every derivation below was checked by hand;
none has been machine-run. Treat any fixture mismatch as a draft defect, never as a finding.

CHANGELOG
- 2026-09-18 round 4 (verifier_editor, machine-run: --fixtures 15/15 ok, --witnesses ok, 0.5 s):
  _lorentzian_at replaced Sturm root counting on the characteristic polynomial with exact Sylvester
  inertia (symmetric congruence diagonalization with zero-diagonal repair). Sturm counts DISTINCT
  real roots, so the witness's repeated transverse eigenvalue (r^2 = 9 twice) read as 1 negative,
  2 positive and every W-7 instance with a repeated eigenvalue failed the signature premise. This
  single defect caused all three round-1..3 failures: the planar witness now confirms (residual 0,
  theta = 2/3, sigma^2 = omega^2 = R_kk = 0), the k-not-null fixture now reaches and fails the
  null-tangent premise, and the coefficient-discrimination control now returns residual -2/9
  (= -(1 - 1/2) theta^2, nonzero as required). ROWS, abstention logic, conventions, FW calibration
  and the candidate schema are byte-identical.

What a candidate is: {"paper": "GO"|"W"|"B"|"FW", "row": "<display id>", "instance": {...},
                      "conventions": {...optional, must equal the pinned printed conventions}}
What verify() does: resolves the printed relation R and its premises P for that row from the frozen
registry ROWS (never from the candidate), establishes P(x) independently, evaluates R(x) exactly at the
printed order, and returns valid=True only for P(x) AND NOT R(x). Definitions, premises and imported
results are refused (they are inputs, not derivations). Derived rows without a mechanical evaluator
abstain with the named missing operation (an abstention is a PARK trigger, never a hit).

Pinned sources (preprint bytes read 2026-09-18; journal reconciliation is a Director acquisition task):
  GO: Graham & Olum, arXiv:0705.3193v2 (27 Aug 2007) = Phys. Rev. D 76, 064001 (2007), pp. 2-4.
  W : Wall, arXiv:0910.5751v2 (16 Feb 2010) = Phys. Rev. D 81, 024038 (2010), pp. 5-16.
  B : Borde, Class. Quantum Grav. 4 (1987) 343-356: ACQUISITION-GATED (only the abstract is public);
      no Borde row exists here; rows enter through `har extend-search` after the inventory freezes.
  FW: Flanagan & Wald, Phys. Rev. D 54, 6233 (1996), Appendix D, Eqs. (D2), (D7), (D13): CALIBRATION
      ONLY. The printed kernel constant 12 pi is PINNED FROM THE PRIMARY BYTES (Director, 2026-09-18):
      sources/flanagan-wald-1996-grqc9602052.pdf, Appendix D, Eq. (D7) 'I(K,x) = 12 pi/x^3 + ...' and
      Eq. (D13) '[12 pi/x^3]'. Sienkiewicz (2026) Remark 8.1's transcription is thereby confirmed.

Printed conventions (frozen; a candidate declaring anything else is refused as a convention mismatch):
  signature (-,+,+,+); R^a_{bcd} = d_c Gamma^a_{db} - ...; R_ab = R^c_{acb} (MTW); Einstein
  8 pi G T_ab = G_ab (Wall Eq. 5, G = 1 from Wall Sec. 4 onward); null tangent k^a affinely
  parametrized; theta = nabla_a k^a; Wall's expansion parameter is hbar with half-integer orders (Eq. 8-9).

Row kinds: definition | premise | imported | derived | prose. Only derived rows can hit.
`consumes` records which steps eat geometric curvature (R_kk) vs matter stress (T_kk) vs neither.

Invariance and fingerprint: candidates are identified by (paper, row, canonicalized instance); no
gauge freedom is quotiented (two coordinate presentations of one geometry count twice, which is the
conservative direction: never merges two genuinely different objects).
'''
from __future__ import annotations
import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

import sympy as sp

VERSION = 'exclusion-display-audit verifier DRAFT 2026-09-18 (rung 2, NOT machine-run by drafter)'
SAFE_TOKEN = re.compile(r'[A-Za-z_]\w*')
ALLOWED_FUNCS = {'exp', 'log', 'sqrt', 'sin', 'cos', 'pi', 'E', 'Rational', 'Abs', 'oo'}
PINNED_CONVENTIONS = {
    'signature': '-+++', 'ricci': 'MTW', 'einstein': '8 pi G T_ab = G_ab', 'G': '1',
    'affine': 'k^b nabla_b k^a = 0', 'theta': 'nabla_a k^a', 'expansion_parameter': 'hbar',
}

# --------------------------------------------------------------------------------------------------
# Frozen display inventory (the per-paper D_p). kind decides eligibility; evaluator names the route.
# --------------------------------------------------------------------------------------------------
ROWS: Dict[str, Dict[str, Any]] = {
    # Graham-Olum, arXiv:0705.3193v2
    'GO-1': dict(paper='GO', page=2, kind='premise', consumes='matter', evaluator=None,
                 text='int_gamma T_ab k^a k^b > 0 (ANEC, the condition under discussion)'),
    'GO-2': dict(paper='GO', page=4, kind='definition', consumes='none', evaluator=None,
                 text='g -> gbar = Omega^2 g (scale transformation; Omega constant, cf. Eq. 5)'),
    'GO-3': dict(paper='GO', page=4, kind='imported', consumes='matter', evaluator=None,
                 text='T^a_b(gbar) = Omega^-4 (T^a_b(g) - 8 a Z^a_b ln Omega) [Visser, ref. 11]'),
    'GO-4': dict(paper='GO', page=4, kind='definition', consumes='geometry', evaluator=None,
                 text='Z^a_b = (nabla_c nabla^d + R_c^d / 2) C^{ca}_{db}'),
    'GO-5': dict(paper='GO', page=4, kind='derived', consumes='matter', evaluator='GO5',
                 text='int_gamma T^a_b(gbar) k^a k_b = Omega^-4 (T_gamma - 8 a ln Omega J_gamma)',
                 premises='GO-3 (imported), Omega constant > 0, T_gamma and J_gamma convergent'),
    'GO-6': dict(paper='GO', page=4, kind='definition', consumes='matter', evaluator=None,
                 text='T_gamma = int_gamma T^a_b(g) k^a k_b'),
    'GO-7': dict(paper='GO', page=4, kind='definition', consumes='geometry', evaluator=None,
                 text='J_gamma = int_gamma Z_ab k^a k^b'),
    'GO-P1': dict(paper='GO', page=4, kind='prose', consumes='none', evaluator=None,
                  text='"Omega of order exp(2880 pi^2)": from GO-5 with T_gamma ~ J_gamma the required '
                       'ln Omega is 1/(8a) = 360 pi^2, not 2880 pi^2 = 1/a; order-of-magnitude prose, '
                       'within one decade, no downstream consequence. Recorded, not a row.'),
    # Wall, arXiv:0910.5751v2
    'W-4': dict(paper='W', page=5, kind='definition', consumes='none', evaluator=None,
                text='S = A/(4 G hbar) + S_out'),
    'W-5': dict(paper='W', page=6, kind='premise', consumes='both', evaluator=None,
                text='8 pi G T_ab = G_ab (classical background)'),
    'W-6': dict(paper='W', page=6, kind='premise', consumes='matter', evaluator=None,
                text='T_ab k^a k^b >= 0 (NEC on the background)'),
    'W-7': dict(paper='W', page=7, kind='derived', consumes='both', evaluator='W7',
                text='-d theta/d lambda = theta^2/2 + sigma_ab sigma^ab + 8 pi G T_ab k^a k^b',
                premises='affinely parametrized null geodesic congruence, twist-free, D = 4 (coefficient '
                         '1/2 is the D = 4 value; dimension is not printed: D != 4 abstains), W-5'),
    'W-8': dict(paper='W', page=8, kind='definition', consumes='none', evaluator=None,
                text='g_ab = g0 + g^{1/2} + g^1 + O(hbar^{3/2})'),
    'W-9': dict(paper='W', page=8, kind='definition', consumes='none', evaluator=None,
                text='T_ab = T0 + T1(rho) + O(hbar^{3/2})'),
    'W-10': dict(paper='W', page=8, kind='derived', consumes='both', evaluator=None,
                 text='8 pi T0 = G0(g0): order-hbar^0 part of W-5 under W-8/W-9; bookkeeping by the '
                      'definition of G^n (exact-order part). Non-evaluable beyond its definition.'),
    'W-11': dict(paper='W', page=8, kind='derived', consumes='geometry', evaluator=None,
                 text='0 = <G^{1/2}(g0, g^{1/2})>: order-hbar^{1/2} part; same bookkeeping.'),
    'W-12': dict(paper='W', page=8, kind='derived', consumes='both', evaluator=None,
                 text='8 pi <T1> = <G1(g0, g^{1/2}, g1)>: order-hbar^1 part; same bookkeeping.'),
    'W-13': dict(paper='W', page=9, kind='premise', consumes='none', evaluator=None,
                 text='theta|_{H+} = 0, theta|_{H-} = 0 through first order (horizon persistence)'),
    'W-14': dict(paper='W', page=10, kind='definition', consumes='none', evaluator=None,
                 text='S0_fut = S0_out(P cap T) + A1/(4 hbar)(H_fut cap T)'),
    'W-15': dict(paper='W', page=11, kind='premise', consumes='none', evaluator=None,
                 text='GSL: Delta[S0_out(P cap T) + A1/(4 hbar)(H_fut cap T)] >= 0'),
    'W-16': dict(paper='W', page=11, kind='premise', consumes='none', evaluator=None,
                 text='anti-GSL: Delta[S0_out(F cap T) + A1/(4 hbar)(H_past cap T)] <= 0'),
    'W-17-18': dict(paper='W', page=11, kind='derived', consumes='none', evaluator='WLIN',
                    text='Delta[S(P) - S(F)] + Delta[A1_fut/4hbar - A1_past/4hbar] >= 0 (15 minus 16)',
                    premises='W-15, W-16'),
    'W-19': dict(paper='W', page=11, kind='premise', consumes='none', evaluator=None,
                 text='weak monotonicity S_{A u C} + S_{B u C} >= S_A + S_B'),
    'W-20': dict(paper='W', page=11, kind='definition', consumes='none', evaluator=None, text='A = T1 cap F'),
    'W-21': dict(paper='W', page=11, kind='definition', consumes='none', evaluator=None, text='B = T2 cap P'),
    'W-22': dict(paper='W', page=11, kind='definition', consumes='none', evaluator=None, text='C = H cap DeltaT'),
    'W-23': dict(paper='W', page=12, kind='derived', consumes='none', evaluator=None,
                 text='S(T2 cap F) + S(T1 cap P) >= S(T1 cap F) + S(T2 cap P): W-19 on W-20..22 plus '
                      'unitarity identifying S_{A u C} with S(T2 cap F) and S_{B u C} with S(T1 cap P). '
                      'Non-evaluable: the identification is a global causal-evolution premise (F4).'),
    'W-24': dict(paper='W', page=12, kind='derived', consumes='none', evaluator='WLIN',
                 text='Delta[S(P) - S(F)] <= 0 (rearrangement of W-23)', premises='W-23'),
    'W-25': dict(paper='W', page=12, kind='derived', consumes='none', evaluator='WLIN',
                 text='Delta[A1(H_fut) - A1(H_past)] >= 0', premises='W-17-18, W-24'),
    'W-26': dict(paper='W', page=12, kind='derived', consumes='none', evaluator=None,
                 text='<theta1_fut - theta1_past> >= 0 everywhere, from W-25 for all intervals. '
                      'Non-evaluable: quantifier over intervals plus an implicit continuity premise (F3/F4).'),
    'W-27': dict(paper='W', page=12, kind='derived', consumes='both', evaluator='WSERIES',
                 text='d<theta1>/d lambda = -8 pi <T1_ab> k^a k^b (linearized W-7, gravitons ignored)',
                 premises='W-7 as a formal series identity through order hbar, theta0 = sigma0 = T0_kk = 0 '
                          'on H (Sec. 3), no hbar^{1/2} terms (Sec. 5), W-13'),
    'W-28': dict(paper='W', page=12, kind='premise', consumes='none', evaluator=None,
                 text='<theta1_fut>(+oo) = 0, <theta1_past>(-oo) = 0 (from W-13)'),
    'W-29': dict(paper='W', page=12, kind='derived', consumes='matter', evaluator='WODE',
                 text='int_X^oo <T1> k k + int_-oo^X <T1> k k >= 0', premises='W-26, W-27, W-28, convergence'),
    'W-30': dict(paper='W', page=15, kind='derived', consumes='geometry', evaluator='WSERIES',
                 text='-d<theta1>/d lambda = <sigma sigma>^1 + <R_ab>^1 k^a k^b (theta^2 omitted)',
                 premises='W-7 geometric part as a series identity, theta0 = sigma0 = 0, W-13, half-order '
                          'no-separation conjecture (Sec. 7) taken as premise'),
    'W-31': dict(paper='W', page=15, kind='derived', consumes='both', evaluator='WSERIES',
                 text='-d<theta1>/d lambda = <sigma sigma>^1 + 8 pi <T1> k k', premises='W-30, W-5/W-12'),
    'W-32': dict(paper='W', page=15, kind='derived', consumes='none', evaluator=None,
                 text='<theta1_fut - theta1_past> >= 0 (W-26 restated under Sec. 7 premises); same obstruction as W-26'),
    'W-33': dict(paper='W', page=15, kind='derived', consumes='both', evaluator='WODE',
                 text='int (<T1> k k + <sigma sigma>^1 / 8 pi) d lambda >= 0', premises='W-31, W-32, W-28, convergence'),
    'W-34': dict(paper='W', page=16, kind='derived', consumes='both', evaluator=None,
                 text='N_s copies: int (N_s <T1> k k + <sigma sigma>^1/8 pi) >= 0, then N_s = hbar^p, -1/2 < p < 0. '
                      'Non-evaluable: uncontrolled remainder ("not so many that gravitational interactions between '
                      'sectors become large" is unquantified) (F3/F4).'),
    # Flanagan-Wald calibration rows (checker behaviour only; not a target paper)
    'FW-D7': dict(paper='FW', page=None, kind='derived', consumes='none', evaluator='FW',
                  text='position-space kernel of k^2 ln k^2 has constant 12 pi (printed, secondary transcription)',
                  printed_constant='12*pi'),
    'FW-D7-corrected': dict(paper='FW', page=None, kind='derived', consumes='none', evaluator='FW',
                            text='corrected control: kernel constant 16 pi', printed_constant='16*pi'),
}

# --------------------------------------------------------------------------------------------------
# Parsing helpers (exact; no floats; token whitelist so sympify never sees attribute access)
# --------------------------------------------------------------------------------------------------

def _parse(s: Any, names: Dict[str, sp.Symbol]) -> sp.Expr:
    if isinstance(s, bool):
        raise ValueError('boolean where an expression was expected')
    if isinstance(s, (int,)):
        return sp.Integer(s)
    if isinstance(s, float):
        raise ValueError('float literal refused: supply exact rationals as strings')
    if not isinstance(s, str):
        raise ValueError('expression must be a string')
    if '.' in s and not re.fullmatch(r'[\d\s()+\-*/^.]*', s):
        raise ValueError('attribute access or decimal in a symbolic expression is refused')
    for tok in SAFE_TOKEN.findall(s):
        if tok not in names and tok not in ALLOWED_FUNCS:
            raise ValueError(f'unknown token {tok!r}')
    return sp.sympify(s.replace('^', '**'), locals=dict(names), rational=True)


def _finite(x: sp.Expr) -> bool:
    if x is None or x.has(sp.Integral) or x.has(sp.nan) or x.has(sp.zoo) or x.has(sp.oo) or x.has(-sp.oo):
        return False
    return x.is_finite is True


def _sign(x: sp.Expr) -> Optional[int]:
    '''Exact sign of a closed-form constant; None when undecidable.'''
    x = sp.nsimplify(sp.simplify(x))
    if x.is_zero:
        return 0
    if x.is_positive:
        return 1
    if x.is_negative:
        return -1
    return None


def _res(valid: bool, reason: str, **details: Any) -> Dict[str, Any]:
    d = {k: (str(v) if isinstance(v, sp.Basic) else v) for k, v in details.items()}
    return {'valid': bool(valid), 'reason': reason, 'details': d}


# --------------------------------------------------------------------------------------------------
# GO-5: integrate Eq. (3) along gamma with constant Omega
# --------------------------------------------------------------------------------------------------

def _ev_GO5(inst: Dict[str, Any]) -> Dict[str, Any]:
    lam = sp.Symbol('lam', real=True)
    consts = {}
    Omega = _parse(inst.get('Omega'), consts)
    a = _parse(inst.get('a'), consts)
    if not (Omega.is_number and Omega.is_positive):
        return _res(False, 'premise fails: Omega must be a positive constant (GO-2 is a scale transformation)')
    if not a.is_number:
        return _res(False, 'premise fails: anomaly coefficient a must be a constant')
    T = _parse(inst.get('T_kk'), {'lam': lam})
    Z = _parse(inst.get('Z_kk'), {'lam': lam})
    Tg = sp.integrate(T, (lam, -sp.oo, sp.oo))
    Jg = sp.integrate(Z, (lam, -sp.oo, sp.oo))
    if not _finite(Tg) or not _finite(Jg):
        return _res(False, 'abstain: T_gamma or J_gamma (GO-6, GO-7) does not converge; ANEC integral undefined (F3)',
                    T_gamma=Tg, J_gamma=Jg)
    lhs = sp.integrate(Omega ** -4 * (T - 8 * a * Z * sp.log(Omega)), (lam, -sp.oo, sp.oo))
    if not _finite(lhs):
        return _res(False, 'abstain: left side of GO-5 does not converge', lhs=lhs)
    rhs = Omega ** -4 * (Tg - 8 * a * sp.log(Omega) * Jg)
    diff = sp.simplify(lhs - rhs)
    holds = diff.is_zero is True
    if holds:
        return _res(False, 'relation GO-5 exactly confirmed on instance (linear in T, Z; Omega constant)',
                    lhs=lhs, rhs=rhs, T_gamma=Tg, J_gamma=Jg)
    if diff.is_zero is None:
        return _res(False, 'abstain: lhs - rhs not decidable symbolically', residual=diff)
    return _res(True, 'GO-5 violated on a premise-satisfying instance', lhs=lhs, rhs=rhs, residual=diff)


# --------------------------------------------------------------------------------------------------
# W-7: exact pointwise Raychaudhuri check from the metric alone
# --------------------------------------------------------------------------------------------------

def _christoffel(g: sp.Matrix, ginv: sp.Matrix, X: List[sp.Symbol]) -> List[List[List[sp.Expr]]]:
    n = len(X)
    dg = [[[sp.diff(g[a, b], X[c]) for c in range(n)] for b in range(n)] for a in range(n)]
    Gam = [[[sp.Integer(0)] * n for _ in range(n)] for _ in range(n)]
    for c in range(n):
        for a in range(n):
            for b in range(a, n):
                s = sp.Integer(0)
                for d in range(n):
                    if ginv[c, d] != 0:
                        s += ginv[c, d] * (dg[d][b][a] + dg[d][a][b] - dg[a][b][d])
                s = sp.cancel(s / 2)
                Gam[c][a][b] = s
                Gam[c][b][a] = s
    return Gam


def _ricci(Gam: List[List[List[sp.Expr]]], X: List[sp.Symbol]) -> sp.Matrix:
    n = len(X)
    R = sp.zeros(n, n)
    for a in range(n):
        for b in range(a, n):
            s = sp.Integer(0)
            for c in range(n):
                s += sp.diff(Gam[c][a][b], X[c]) - sp.diff(Gam[c][a][c], X[b])
                for d in range(n):
                    s += Gam[c][c][d] * Gam[d][a][b] - Gam[c][b][d] * Gam[d][a][c]
            s = sp.cancel(s)
            R[a, b] = s
            R[b, a] = s
    return R


def _lorentzian_at(gp: sp.Matrix) -> Tuple[bool, str]:
    n = gp.shape[0]
    det = sp.cancel(gp.det())
    if det == 0:
        return False, 'metric degenerate at point'
    # Sylvester inertia by exact symmetric congruence (Lagrange diagonalization). Root counting on the
    # characteristic polynomial was WRONG here: Sturm counts DISTINCT roots, so a repeated eigenvalue
    # (e.g. the transverse block r^2, r^2) was counted once (round-1 defect). Inertia is a congruence
    # invariant (Sylvester's law), so this counts every eigenvalue sign with multiplicity, exactly.
    A = sp.Matrix(gp).applyfunc(sp.nsimplify).applyfunc(sp.cancel)
    neg = pos = 0
    while A.shape[0] > 0:
        m = A.shape[0]
        piv = next((i for i in range(m) if A[i, i] != 0), None)
        if piv is None:
            # all diagonal entries zero; det != 0 guarantees an off-diagonal A[0, j] != 0:
            # congruence with e_0 -> e_0 + e_j makes A[0, 0] = 2 A[0, j] != 0
            j = next(j for j in range(1, m) if A[0, j] != 0)
            E = sp.eye(m)
            E[j, 0] = 1
            A = (E.T * A * E).applyfunc(sp.cancel)
            piv = 0
        p = A[piv, piv]
        if p.is_positive:
            pos += 1
        elif p.is_negative:
            neg += 1
        else:
            return False, f'signature undecidable at point (pivot sign of {p} unknown)'
        idx = [i for i in range(m) if i != piv]
        v = sp.Matrix([A[i, piv] for i in idx])
        A = (A.extract(idx, idx) - v * v.T / p).applyfunc(sp.cancel)
    if neg != 1 or pos != n - 1:
        return False, f'signature at point is ({neg} negative, {pos} positive), not Lorentzian (-,+,...,+)'
    return True, 'ok'


def _w7_core(inst: Dict[str, Any], coef: sp.Rational) -> Dict[str, Any]:
    D = int(inst.get('dimension', 4))
    if D != 4:
        return _res(False, f'abstain: dimension {D} is not printed in Wall; the coefficient 1/2 in W-7 is the '
                           'D = 4 value (D - 2 = 2). Applicability question (F4), not a counterexample.')
    names = inst.get('coords')
    if not (isinstance(names, list) and len(names) == D and all(isinstance(s, str) for s in names)):
        return _res(False, 'malformed: coords must be 4 coordinate names')
    X = [sp.Symbol(s, real=True) for s in names]
    ns = {s: x for s, x in zip(names, X)}
    M = inst.get('metric')
    if not (isinstance(M, list) and len(M) == D and all(isinstance(r, list) and len(r) == D for r in M)):
        return _res(False, 'malformed: metric must be a 4x4 nested list of expressions')
    g = sp.Matrix(D, D, lambda i, j: _parse(M[i][j], ns))
    if sp.simplify(g - g.T) != sp.zeros(D, D):
        return _res(False, 'premise fails: metric not symmetric')
    kv = inst.get('k')
    if not (isinstance(kv, list) and len(kv) == D):
        return _res(False, 'malformed: k must be a list of 4 components')
    k = [_parse(s, ns) for s in kv]
    for e in list(g) + k:
        if not e.is_rational_function(*X):
            return _res(False, 'refused: W-7 family is rational-function metrics and tangents (exactness); '
                               'extend the registry for other function classes')
    pt = inst.get('point')
    if not (isinstance(pt, dict) and set(pt) == set(names)):
        return _res(False, 'malformed: point must give every coordinate')
    P = {ns[s]: _parse(pt[s], {}) for s in names}
    gp = g.subs(P)
    if any(not _finite(e) for e in gp):
        return _res(False, 'premise fails: metric singular at the point')
    ok, why = _lorentzian_at(gp)
    if not ok:
        return _res(False, 'premise fails: ' + why)
    ginv = g.inv().applyfunc(sp.cancel)
    # null, identically (k is a field; theta is differentiated along it)
    kk = sp.cancel(sum(g[a, b] * k[a] * k[b] for a in range(D) for b in range(D)))
    if kk != 0:
        return _res(False, 'premise fails: k is not null (g_ab k^a k^b != 0 identically)', g_kk=kk)
    Gam = _christoffel(g, ginv, X)
    # affine geodesic, identically
    for a in range(D):
        acc = sum(k[b] * sp.diff(k[a], X[b]) for b in range(D))
        acc += sum(Gam[a][b][c] * k[b] * k[c] for b in range(D) for c in range(D))
        if sp.cancel(acc) != 0:
            return _res(False, 'premise fails: k^b nabla_b k^a != 0 (not an affinely parametrized geodesic field)',
                        component=a)
    klow = [sp.cancel(sum(g[a, b] * k[b] for b in range(D))) for a in range(D)]
    B = [[sp.cancel(sp.diff(klow[a], X[b]) - sum(Gam[c][a][b] * klow[c] for c in range(D)))
          for b in range(D)] for a in range(D)]
    Bup = [[sp.cancel(sum(ginv[a, c] * ginv[b, d] * B[c][d] for c in range(D) for d in range(D)))
            for b in range(D)] for a in range(D)]
    theta = sp.cancel(sum(ginv[a, b] * B[a][b] for a in range(D) for b in range(D)))
    BB = sp.cancel(sum(B[a][b] * Bup[a][b] for a in range(D) for b in range(D)))
    BBt = sp.cancel(sum(B[a][b] * Bup[b][a] for a in range(D) for b in range(D)))
    sig2 = sp.cancel((BB + BBt) / 2 - theta ** 2 / 2)
    om2 = sp.cancel((BB - BBt) / 2)
    dtheta = sp.cancel(sum(k[a] * sp.diff(theta, X[a]) for a in range(D)))
    Ric = _ricci(Gam, X)
    Rkk = sp.cancel(sum(Ric[a, b] * k[a] * k[b] for a in range(D) for b in range(D)))
    Rs = sp.cancel(sum(ginv[a, b] * Ric[a, b] for a in range(D) for b in range(D)))
    Gkk = sp.cancel(Rkk - Rs * kk / 2)  # kk == 0, so G_kk == R_kk: the Einstein-substitution step
    vals = {}
    for nm, e in [('theta', theta), ('sigma2', sig2), ('omega2', om2), ('dtheta', dtheta), ('R_kk', Rkk), ('G_kk', Gkk)]:
        v = sp.cancel(e.subs(P))
        if not _finite(v):
            return _res(False, f'premise fails: {nm} singular at the point')
        vals[nm] = v
    if vals['omega2'] != 0:
        return _res(False, 'premise fails: congruence has twist at the point (omega_ab omega^ab != 0); W-7 is '
                           'stated for the twist-free horizon congruence', **vals)
    lhs = -vals['dtheta']
    rhs = coef * vals['theta'] ** 2 + vals['sigma2'] + vals['G_kk']  # 8 pi G T_kk := G_kk by W-5
    resid = sp.cancel(lhs - rhs)
    vals['residual'] = resid
    vals['einstein_step_G_kk_minus_R_kk'] = sp.cancel(vals['G_kk'] - vals['R_kk'])
    if resid == 0:
        return _res(False, 'relation W-7 exactly confirmed on instance (geometric Raychaudhuri identity plus '
                           'G_kk = R_kk for null k; 8 pi T_kk consumed as G_kk by W-5)', **vals)
    return _res(True, 'W-7 violated on a premise-satisfying instance', **vals)


def _ev_W7(inst: Dict[str, Any]) -> Dict[str, Any]:
    return _w7_core(inst, sp.Rational(1, 2))


# --------------------------------------------------------------------------------------------------
# W-17-18, W-24, W-25: exact rational bookkeeping of the entropy inequalities (hbar = 1 units)
# --------------------------------------------------------------------------------------------------

def _ev_WLIN(inst: Dict[str, Any], row: str) -> Dict[str, Any]:
    q = lambda key: _parse(inst.get(key), {})
    try:
        if row == 'W-17-18':
            dSP, dSF, dAf, dAp = q('dS_P'), q('dS_F'), q('dA_fut'), q('dA_past')
            p15 = dSP + dAf / 4
            p16 = dSF + dAp / 4
            if _sign(p15) is None or _sign(p16) is None:
                return _res(False, 'abstain: premise sign undecidable')
            if _sign(p15) < 0:
                return _res(False, 'premise fails: W-15 (GSL) not satisfied by instance', W15=p15)
            if _sign(p16) > 0:
                return _res(False, 'premise fails: W-16 (anti-GSL) not satisfied by instance', W16=p16)
            rel = (dSP - dSF) + (dAf - dAp) / 4
            holds = _sign(rel) >= 0
            return _res(not holds, 'relation W-17-18 exactly confirmed on instance (15 minus 16)' if holds
                        else 'W-17-18 violated', value=rel)
        if row == 'W-24':
            S2F, S1F, S1P, S2P = q('S_T2F'), q('S_T1F'), q('S_T1P'), q('S_T2P')
            p23 = (S2F + S1P) - (S1F + S2P)
            s = _sign(p23)
            if s is None:
                return _res(False, 'abstain: premise sign undecidable')
            if s < 0:
                return _res(False, 'premise fails: W-23 not satisfied by instance', W23=p23)
            rel = (S2P - S1P) - (S2F - S1F)
            holds = _sign(rel) <= 0
            return _res(not holds, 'relation W-24 exactly confirmed on instance (rearrangement of W-23)' if holds
                        else 'W-24 violated', value=rel)
        if row == 'W-25':
            dSP, dSF, dAf, dAp = q('dS_P'), q('dS_F'), q('dA_fut'), q('dA_past')
            p18 = (dSP - dSF) + (dAf - dAp) / 4
            p24 = dSP - dSF
            if _sign(p18) is None or _sign(p24) is None:
                return _res(False, 'abstain: premise sign undecidable')
            if _sign(p18) < 0:
                return _res(False, 'premise fails: W-17-18 not satisfied by instance', W18=p18)
            if _sign(p24) > 0:
                return _res(False, 'premise fails: W-24 not satisfied by instance', W24=p24)
            rel = dAf - dAp
            holds = _sign(rel) >= 0
            return _res(not holds, 'relation W-25 exactly confirmed on instance' + (
                ' (non-strict inequality satisfied, strictly)' if _sign(rel) > 0 else ' (saturated)') if holds
                        else 'W-25 violated', value=rel)
    except ValueError as ex:
        return _res(False, f'malformed instance: {ex}')
    return _res(False, 'no evaluator')


# --------------------------------------------------------------------------------------------------
# W-27 / W-30 / W-31: order-by-order extraction from W-7 as a formal series in eps = hbar^(1/2)
# --------------------------------------------------------------------------------------------------

def _ev_WSERIES(inst: Dict[str, Any], row: str) -> Dict[str, Any]:
    lam = sp.Symbol('lam', real=True)
    eps = sp.Symbol('eps')
    ns = {'lam': lam}
    get = lambda key, default='0': _parse(inst.get(key, default), ns)
    th0, thh, th1 = get('theta0'), get('theta_half'), get('theta1')
    s0, sh, s1 = get('sigsq0'), get('sigsq_half'), get('sigsq1')
    T0, T1 = get('T0_kk'), get('T1_kk')
    R1 = get('R1_kk', '8*pi*(' + str(inst.get('T1_kk', '0')).replace('^', '**') + ')')
    # horizon premises (Sec. 3): theta0 = sigma0 = T0_kk = 0 on H
    for nm, e in [('theta0', th0), ('sigsq0', s0), ('T0_kk', T0)]:
        if sp.simplify(e) != 0:
            return _res(False, f'premise fails: {nm} must vanish on the background horizon H (Sec. 3)')
    # W-13 at half order: theta_half -> 0 at both ends; with the half-order Raychaudhuri equation
    # (-d theta_half = theta0 theta_half + (sigma sigma)_half + 8 pi T_half, all zero) theta_half is
    # constant along the generator, hence zero.
    if sp.simplify(sh) != 0:
        return _res(False, 'premise fails: (sigma sigma) has no hbar^(1/2) part when sigma0 = 0')
    if sp.simplify(thh) != 0:
        lim_p, lim_m = sp.limit(thh, lam, sp.oo), sp.limit(thh, lam, -sp.oo)
        if sp.simplify(sp.diff(thh, lam)) != 0 or lim_p != 0 or lim_m != 0:
            return _res(False, 'premise fails: theta_half violates W-13 (must be constant by the half-order '
                               'Raychaudhuri equation and vanish at H+-)', theta_half=thh)
    if row == 'W-27' and sp.simplify(s1) != 0:
        return _res(False, 'premise fails: Sec. 5 ignores graviton fluctuations, so (sigma sigma)^1 = 0 for W-27')
    # premise: W-7 holds as a formal identity through order hbar (eps^2)
    theta = th0 + eps * thh + eps ** 2 * th1
    sigsq = s0 + eps * sh + eps ** 2 * s1
    Tkk = T0 + eps ** 2 * T1
    full = sp.expand(-sp.diff(theta, lam) - (theta ** 2 / 2 + sigsq + 8 * sp.pi * Tkk))
    for order in (0, 1, 2):
        c = sp.simplify(full.coeff(eps, order))
        if c != 0:
            return _res(False, f'premise fails: instance does not satisfy W-7 at order hbar^{order}/2 '
                               f'(residual {c}); an instance of the linearized law must instantiate the law')
    if row == 'W-30':
        lhs, rhs = -sp.diff(th1, lam), s1 + R1
    elif row == 'W-31':
        if sp.simplify(R1 - 8 * sp.pi * T1) != 0:
            return _res(False, 'premise fails: W-5/W-12 (R1_kk = 8 pi T1_kk) not satisfied by instance')
        lhs, rhs = -sp.diff(th1, lam), s1 + 8 * sp.pi * T1
    else:
        lhs, rhs = sp.diff(th1, lam), -8 * sp.pi * T1
    resid = sp.simplify(lhs - rhs)
    if resid == 0:
        return _res(False, f'relation {row} exactly confirmed on instance at the printed order (hbar^1); '
                           'terms of order hbar^(3/2) and higher are outside the assertion', residual=resid)
    return _res(True, f'{row} violated at the printed order on a premise-satisfying instance', residual=resid)


# --------------------------------------------------------------------------------------------------
# W-29 / W-33: ODE + boundary conditions -> integrated inequality
# --------------------------------------------------------------------------------------------------

def _ev_WODE(inst: Dict[str, Any], row: str) -> Dict[str, Any]:
    lam = sp.Symbol('lam', real=True)
    Xs = sp.Symbol('X', real=True)
    ns = {'lam': lam}
    T1 = _parse(inst.get('T1_kk', '0'), ns)
    s1 = _parse(inst.get('sigsq1', '0'), ns) if row == 'W-33' else sp.Integer(0)
    f = 8 * sp.pi * T1 + s1  # -d theta1/d lambda
    I = sp.integrate(f, (lam, -sp.oo, sp.oo))
    if not _finite(I):
        return _res(False, 'abstain: the line integral does not converge (F3); W-28 cannot be imposed', integral=I)
    Ffut = sp.integrate(f, (lam, Xs, sp.oo))      # theta1_fut(X), from W-27/31 and W-28 at +oo
    Fpast = -sp.integrate(f, (lam, -sp.oo, Xs))   # theta1_past(X), from W-28 at -oo
    if not _finite(Ffut.subs(Xs, 0)) or not _finite(Fpast.subs(Xs, 0)):
        return _res(False, 'abstain: half-line integrals undefined', F=Ffut, P=Fpast)
    ode_ok = sp.simplify(sp.diff(Ffut, Xs) + f.subs(lam, Xs)) == 0 and sp.simplify(sp.diff(Fpast, Xs) + f.subs(lam, Xs)) == 0
    bc_ok = sp.limit(Ffut, Xs, sp.oo) == 0 and sp.limit(Fpast, Xs, -sp.oo) == 0
    if not (ode_ok and bc_ok):
        return _res(False, 'abstain: the solved theta1 does not satisfy the ODE/boundary premises symbolically')
    diffX = sp.simplify(Ffut - Fpast - I)
    if diffX != 0:
        return _res(True, f'{row} violated: theta1_fut - theta1_past differs from the full-line integral', residual=diffX)
    s = _sign(I)
    if s is None:
        return _res(False, 'abstain: sign of the line integral undecidable symbolically', integral=I)
    if s < 0:
        return _res(False, 'premise fails: W-26/W-32 (<theta1_fut - theta1_past> >= 0) not satisfied by instance; '
                           'the instance is an ANEC violator, not a counterexample to the derivation', integral=I)
    return _res(False, f'relation {row} exactly confirmed on instance (integral = {I} >= 0 follows from W-26 '
                       'by the ODE solution)', integral=I, theta1_fut=Ffut, theta1_past=Fpast)


# --------------------------------------------------------------------------------------------------
# FW calibration: independent exact evaluation of the k^2 ln k^2 kernel constant
# --------------------------------------------------------------------------------------------------

def _fw_kernel_constant() -> sp.Expr:
    '''2 c'(2) with c(nu) = 2^(nu+2) pi Gamma(1+nu/2)/Gamma(-nu/2) (FW Eq. D2 normalization),
    rewritten by the reflection formula as -2^(nu+2) Gamma(1+nu/2)^2 sin(pi nu/2), which is regular at nu = 2.'''
    nu = sp.Symbol('nu')
    c = -2 ** (nu + 2) * sp.gamma(1 + nu / 2) ** 2 * sp.sin(sp.pi * nu / 2)
    return sp.simplify(2 * sp.diff(c, nu).subs(nu, 2))


def _fw_numeric_control() -> Dict[str, Any]:
    '''h(r) = r^4 exp(-r^2): momentum-side integral of htilde(k) k^2 ln k^2 over the plane versus
    (kernel constant) x int d^2x h(x)/x^4 = (kernel constant) x pi. Floating control only (mpmath 30 dps).'''
    try:
        import mpmath as mp
        k = sp.Symbol('k', positive=True)
        f = sp.exp(-k ** 2 / 4)
        lap = lambda u: sp.diff(u, k, 2) + sp.diff(u, k) / k
        ht = sp.simplify(sp.pi * lap(lap(f)))  # FT of r^4 e^{-r^2}: r^2 <-> -Laplacian_k, FT[e^{-r^2}] = pi e^{-k^2/4}
        fn = sp.lambdify(k, 2 * sp.pi * k * ht * k ** 2 * sp.log(k ** 2), 'mpmath')
        mp.mp.dps = 30
        I = mp.quad(fn, [0, 1, 4, mp.inf])
        ratio = I / mp.pi  # should equal the kernel constant
        return {'momentum_integral_over_pi': mp.nstr(ratio, 25), 'expected_16pi': mp.nstr(16 * mp.pi, 25),
                'expected_12pi': mp.nstr(12 * mp.pi, 25), 'abs_dev_from_16pi': mp.nstr(abs(ratio - 16 * mp.pi), 5)}
    except Exception as ex:  # control only; never decides
        return {'numeric_control_error': repr(ex)}


def _ev_FW(inst: Dict[str, Any], row: str) -> Dict[str, Any]:
    printed = sp.sympify(ROWS[row]['printed_constant'])
    K = _fw_kernel_constant()
    resid = sp.simplify(K - printed)
    ctrl = _fw_numeric_control() if inst.get('numeric_control', True) else {}
    if resid == 0:
        return _res(False, f'relation {row} exactly confirmed: independent kernel constant 2 c\'(2) = {K}',
                    kernel_constant=K, printed=printed, **ctrl)
    return _res(True, f'{row} violated: independent kernel constant 2 c\'(2) = {K}, printed {printed}',
                kernel_constant=K, printed=printed, residual=resid, **ctrl)


# --------------------------------------------------------------------------------------------------
# verify / fingerprint
# --------------------------------------------------------------------------------------------------

EVALUATORS = {'GO5': lambda inst, row: _ev_GO5(inst), 'W7': lambda inst, row: _ev_W7(inst),
              'WLIN': _ev_WLIN, 'WSERIES': _ev_WSERIES, 'WODE': _ev_WODE, 'FW': _ev_FW}


def _row_id(candidate: Dict[str, Any]) -> Optional[str]:
    if isinstance(candidate.get('row_id'), str):
        return candidate['row_id']
    p, r = candidate.get('paper'), candidate.get('row')
    if isinstance(p, str) and (isinstance(r, str) or isinstance(r, int)):
        return f'{p}-{r}'
    return None


def verify(candidate: Any) -> Dict[str, Any]:
    if not isinstance(candidate, dict):
        return _res(False, 'malformed: candidate must be a JSON object')
    rid = _row_id(candidate)
    if rid is None:
        return _res(False, 'malformed: candidate needs paper and row (or row_id)')
    if rid.startswith('B-'):
        return _res(False, 'abstain: Borde (CQG 4, 343) is ACQUISITION-GATED; no frozen inventory row exists. '
                           'Rows enter only through har extend-search after the Director freezes the inventory.')
    if rid not in ROWS:
        return _res(False, f'refused: {rid} is not in the frozen display inventory')
    row = ROWS[rid]
    conv = candidate.get('conventions')
    if conv is not None:
        if not isinstance(conv, dict):
            return _res(False, 'malformed: conventions must be an object')
        for key, val in conv.items():
            if key not in PINNED_CONVENTIONS or str(val) != PINNED_CONVENTIONS[key]:
                return _res(False, f'refused: convention mismatch on {key!r} ({val!r}); the relation is evaluated '
                                   f'only in the printed convention {PINNED_CONVENTIONS.get(key)!r} (F1)')
    kind = row['kind']
    if kind in ('definition', 'premise', 'imported', 'prose'):
        return _res(False, f'refused: {rid} is a {kind}, not a derived assertion; it is an input to the audit '
                           f'and cannot be a counterexample target ({row["text"]})', kind=kind, consumes=row['consumes'])
    ev = row.get('evaluator')
    if ev is None:
        return _res(False, f'abstain: {rid} is derived but has no source-faithful mechanical evaluator: {row["text"]}',
                    kind=kind, consumes=row['consumes'], park_trigger=True)
    inst = candidate.get('instance')
    if not isinstance(inst, dict):
        return _res(False, 'malformed: instance must be an object')
    try:
        out = EVALUATORS[ev](inst, rid)
    except ValueError as ex:
        return _res(False, f'malformed instance: {ex}')
    except Exception as ex:  # any evaluator crash is an abstention, never a hit
        return _res(False, f'abstain: evaluator error {type(ex).__name__}: {ex}')
    out['details'].update({'row': rid, 'kind': kind, 'consumes': row['consumes'], 'premises': row.get('premises', ''),
                           'text': row['text'], 'verifier': VERSION})
    return out


def _canon(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {k: _canon(obj[k]) for k in sorted(obj)}
    if isinstance(obj, list):
        return [_canon(v) for v in obj]
    if isinstance(obj, str):
        try:
            e = sp.sympify(obj.replace('^', '**'), rational=True)
            return sp.srepr(sp.cancel(e)) if isinstance(e, sp.Basic) else obj
        except Exception:
            return obj
    return obj


def fingerprint(candidate: Any) -> str:
    '''Invariance: only syntactic canonicalization of exact expressions (paper, row, instance). No
    coordinate or gauge quotient is applied, so distinct presentations count separately (conservative).'''
    rid = _row_id(candidate) if isinstance(candidate, dict) else None
    return json.dumps([rid, _canon(candidate.get('instance', {}) if isinstance(candidate, dict) else candidate)],
                      sort_keys=True)


# --------------------------------------------------------------------------------------------------
# Fixtures and witnesses (run by the Director: --fixtures / --witnesses)
# --------------------------------------------------------------------------------------------------

_W7_WITNESS = {
    'paper': 'W', 'row': '7',
    'instance': {'dimension': 4, 'coords': ['t', 'r', 'x', 'y'],
                 'metric': [['-(1-2/r)', '0', '0', '0'], ['0', '1/(1-2/r)', '0', '0'],
                            ['0', '0', 'r^2', '0'], ['0', '0', '0', 'r^2']],
                 'k': ['1/(1-2/r)', '1', '0', '0'], 'point': {'t': '0', 'r': '3', 'x': '0', 'y': '0'}}}

FIXTURES: List[Tuple[str, Dict[str, Any], bool, str]] = [
    ('FW positive control (printed 12 pi; must HIT)', {'paper': 'FW', 'row': 'D7', 'instance': {}}, True, 'violated'),
    ('FW corrected control (16 pi; must confirm)', {'paper': 'FW', 'row': 'D7-corrected', 'instance': {}}, False, 'confirmed'),
    ('W-7 witness (planar f = 1 - 2/r, radial null congruence; must confirm)', _W7_WITNESS, False, 'confirmed'),
    ('W-7 missing premise (k not null)', {**_W7_WITNESS, 'instance': {**_W7_WITNESS['instance'], 'k': ['1', '1', '0', '0']}},
     False, 'not null'),
    ('W-7 dimension not printed (D = 5 abstains)', {**_W7_WITNESS, 'instance': {**_W7_WITNESS['instance'], 'dimension': 5}},
     False, 'dimension'),
    ('definition mismatch (GO-4 targeted)', {'paper': 'GO', 'row': '4', 'instance': {}}, False, 'definition'),
    ('convention mismatch', {**_W7_WITNESS, 'conventions': {'signature': '+---'}}, False, 'convention mismatch'),
    ('satisfied strict inequality (W-25 strictly positive)',
     {'paper': 'W', 'row': '25', 'instance': {'dS_P': '-1', 'dS_F': '0', 'dA_fut': '8', 'dA_past': '0'}}, False, 'confirmed'),
    ('beyond printed order (W-27 with hbar^(3/2) data ignored)',
     {'paper': 'W', 'row': '27', 'instance': {'theta1': '-8*pi*lam', 'T1_kk': '1', 'theta_3half': 'lam^5'}}, False, 'confirmed'),
    ('GO-5 linear identity on a convergent instance',
     {'paper': 'GO', 'row': '5', 'instance': {'Omega': '2', 'a': '1/(2880*pi^2)', 'T_kk': 'exp(-lam^2)', 'Z_kk': 'lam^2*exp(-lam^2)'}},
     False, 'confirmed'),
    ('GO-5 divergent J_gamma abstains', {'paper': 'GO', 'row': '5', 'instance': {'Omega': '2', 'a': '1', 'T_kk': 'exp(-lam^2)', 'Z_kk': '1'}},
     False, 'converge'),
    ('W-29 ANEC violator is a premise failure, not a hit',
     {'paper': 'W', 'row': '29', 'instance': {'T1_kk': '-exp(-lam^2)'}}, False, 'premise fails'),
    ('W-23 abstains (unitarity identification)', {'paper': 'W', 'row': '23', 'instance': {}}, False, 'abstain'),
    ('Borde gated', {'paper': 'B', 'row': '1', 'instance': {}}, False, 'ACQUISITION-GATED'),
]


def _run_fixtures() -> int:
    bad = 0
    for name, cand, want_valid, want_sub in FIXTURES:
        out = verify(cand)
        ok = out['valid'] == want_valid and want_sub.lower() in out['reason'].lower()
        bad += 0 if ok else 1
        print(json.dumps({'fixture': name, 'ok': ok, 'valid': out['valid'], 'reason': out['reason']}))
    # discrimination control: the W-7 evaluator with the D = 6 coefficient (1) must FAIL on the witness
    # (theta = 2/r != 0 there), proving the check is sensitive to the printed coefficient.
    disc = _w7_core(_W7_WITNESS['instance'], sp.Integer(1))
    ok = disc['valid'] is True
    bad += 0 if ok else 1
    print(json.dumps({'fixture': 'W-7 coefficient discrimination (1 instead of 1/2 must be detected)', 'ok': ok,
                      'residual': disc['details'].get('residual')}))
    print(json.dumps({'fixtures_failed': bad}))
    return bad


def _run_witnesses() -> int:
    out = verify(_W7_WITNESS)
    print(json.dumps({'witness': 'W-7 planar', 'valid': out['valid'], 'details': out['details']}, default=str))
    fw = verify({'paper': 'FW', 'row': 'D7', 'instance': {}})
    print(json.dumps({'witness': 'FW kernel', 'valid': fw['valid'], 'details': fw['details']}, default=str))
    return 0 if (not out['valid'] and fw['valid']) else 1


if __name__ == '__main__':
    args = sys.argv[1:]
    rc = 0
    if '--fixtures' in args or '--selftest' in args:
        rc |= _run_fixtures()
    if '--witnesses' in args or '--selftest' in args:
        rc |= _run_witnesses()
    if not args:
        print(json.dumps(verify(json.load(sys.stdin)), default=str))
    sys.exit(1 if rc else 0)
