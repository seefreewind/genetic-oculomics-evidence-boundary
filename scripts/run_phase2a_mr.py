#!/usr/bin/env python3
"""Phase 2A bidirectional two-sample MR for all 14 x 8 locked pairs.

The script uses the already-clumped Phase 0 instruments, streams each public
summary-statistics file once for requested SNPs, performs explicit allele
harmonisation, and writes an auditable directional master table. It does not
run colocalisation or any downstream causal-taxonomy method.
"""
from __future__ import annotations

import csv
import gzip
import io
import math
import re
import subprocess
import zipfile
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy.stats import norm, chi2

ROOT = Path(__file__).resolve().parents[1]
PHASE2 = ROOT / "results/phase2"
RAW_MANIFEST = ROOT / "data/raw/FULL_DOWNLOAD_MANIFEST.tsv"
REGISTRY = ROOT / "config/phenotype_registry.tsv"
CLUMP_DIR = ROOT / "results/phase0/clumping"
CAND_DIR = ROOT / "results/phase0/instrument_candidates"
EUR_BIM = ROOT / "data/reference/1kg_v3/EUR.bim"
EUR_BFILE = ROOT / "data/reference/1kg_v3/EUR"

RETINAL = [
    "ret_rnfl_left", "ret_gcipl_left", "ret_inl_left", "ret_inl_elm_left",
    "ret_elm_isos_left", "ret_isos_rpe_left", "ret_macular_total_left",
    "ret_art_tort", "ret_ven_tort", "ret_crae", "ret_crve", "ret_avr",
    "ret_art_density", "ret_ven_density",
]
SYSTEMIC = [
    "sys_cad_nikpay2015", "sys_stroke_megastroke2018", "sys_t2d_scott2017",
    "sys_ckd_wuttke2019", "sys_ad_kunkle2019", "sys_pd_nalls2019_clinical",
    "sys_sle_bentham2015", "sys_ibd_delange2017",
]

ALIASES = {
    "chr": ["chromosome", "chr", "chrom", "chr_id", "chromosome_id"],
    "pos": ["base_pair_location", "position", "pos", "bp", "bp37", "pos_b37", "bp_hg19"],
    "rsid": ["rsid", "snp", "markername", "marker_name", "marker_id", "variant_id", "id"],
    "ea": ["effect_allele", "effectallele", "a1", "allele1", "coded_all", "coded_allele"],
    "oa": ["other_allele", "noneffect_allele", "non_effect_allele", "a2", "allele2", "noncoded_all", "noncoded_allele"],
    "beta": ["beta", "b", "effect", "estimate", "log_odds", "logor"],
    "or": ["or", "odds_ratio", "oddsratio"],
    "se": ["standard_error", "se", "stderr", "sebeta", "se_beta", "se_dgc", "std_err"],
    "p": ["p_value", "p", "pvalue", "p.value", "pval", "p_value_gc", "p_dgc"],
    "eaf": ["effect_allele_frequency", "eaf", "freq1", "a1freq", "frq", "effect_allele_freq", "effect_allele_frequency"],
    "n": ["n", "sample_size", "samplesize", "neff", "n_total", "n_total_sum", "totalsamplesize", "total_n"],
}

def norm_col(x: str) -> str:
    return re.sub(r"[^a-z0-9_.]+", "_", str(x).strip().strip('"').strip("'").lower()).strip("_")

def parse_num(x: object) -> Optional[float]:
    try:
        y = float(str(x).strip().strip('"'))
        return y if math.isfinite(y) else None
    except (TypeError, ValueError):
        return None

def split_line(line: str, delimiter: Optional[str]) -> List[str]:
    if delimiter == "\t": return next(csv.reader([line], delimiter="\t"))
    if delimiter == ",": return next(csv.reader([line], delimiter=","))
    return re.split(r"\s+", line.strip())

def resolve(header: Sequence[str]) -> Dict[str, Optional[int]]:
    normal = [norm_col(h) for h in header]
    result = {role: next((normal.index(a) for a in aliases if a in normal), None)
              for role, aliases in ALIASES.items()}
    composite = next((i for i, n in enumerate(normal) if n in {"chr_position", "chromosome_position", "chr_pos"}), None)
    if composite is not None:
        if result["chr"] is None: result["chr"] = composite
        if result["pos"] is None: result["pos"] = composite
    return result

def open_text(path: Path):
    if zipfile.is_zipfile(path):
        archive = zipfile.ZipFile(path)
        members = [m for m in archive.infolist() if not m.is_dir() and not m.filename.startswith("__MACOSX/")]
        if not members:
            archive.close(); raise ValueError("ZIP contains no data file")
        member = max(members, key=lambda m: m.file_size)
        raw = archive.open(member)
        if member.filename.endswith(".gz"): raw = gzip.GzipFile(fileobj=raw)
        return _ChainedContext(io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""), archive)
    if path.name.endswith((".gz", ".gz.complete", ".bgz", ".bgz.complete")):
        return gzip.open(path, "rt", encoding="utf-8", errors="replace", newline="")
    return path.open("r", encoding="utf-8", errors="replace", newline="")

class _ChainedContext:
    def __init__(self, text, archive): self.text, self.archive = text, archive
    def __enter__(self): return self.text
    def __exit__(self, *args): self.text.close(); self.archive.close()

def value(parts: Sequence[str], index: Optional[int]) -> str:
    return parts[index].strip().strip('"') if index is not None and index < len(parts) else ""

def coord_from(text: str) -> Optional[Tuple[str, int]]:
    m = re.match(r"^(?:chr)?([0-9]{1,2}|X|Y|MT)[:_]([0-9]+)", text.strip().strip('"'), re.I)
    return (m.group(1).upper(), int(m.group(2))) if m else None

def norm_chr(x: str) -> str:
    return x.strip().strip('"').removeprefix("chr").upper()

def load_registry() -> Dict[str, Dict[str, str]]:
    with REGISTRY.open(encoding="utf-8", newline="") as h:
        return {r["trait_id"]: r for r in csv.DictReader(h, delimiter="\t")}

def registry_n(meta: Dict[str, str]) -> Optional[float]:
    m = re.search(r"[0-9]+(?:\.[0-9]+)?", meta.get("sample_size", ""))
    return float(m.group(0)) if m else None

def registry_cases_controls(meta: Dict[str, str]) -> Tuple[Optional[float], Optional[float]]:
    def first(x: str) -> Optional[float]:
        m = re.search(r"[0-9]+(?:\.[0-9]+)?", x or "")
        return float(m.group(0)) if m else None
    return first(meta.get("n_cases", "")), first(meta.get("n_controls", ""))

def load_manifest() -> Dict[str, Path]:
    out = {}
    manifest_paths = [RAW_MANIFEST, ROOT / "data/raw/FULL_DOWNLOAD_MANIFEST_ZENODO.tsv"]
    for manifest_path in manifest_paths:
        if not manifest_path.exists(): continue
        with manifest_path.open(encoding="utf-8", newline="") as h:
            for r in csv.DictReader(h, delimiter="\t"):
                if r.get("status") in {"COMPLETE", "REUSED", "OK"} and r.get("path") not in {None, "NA"}:
                    p = ROOT / r["path"]
                    if p.exists(): out[r["trait_id"]] = p
    return out

def load_bim() -> Tuple[Dict[str, Tuple[str, int, str, str]], Dict[Tuple[str, int], str]]:
    by_id: Dict[str, Tuple[str, int, str, str]] = {}; by_coord: Dict[Tuple[str, int], str] = {}
    with EUR_BIM.open(encoding="utf-8", errors="replace") as h:
        for line in h:
            f = line.split()
            if len(f) < 6: continue
            c, rid, pos, a1, a2 = norm_chr(f[0]), f[1], int(f[3]), f[4].upper(), f[5].upper()
            by_id[rid] = (c, pos, a1, a2); by_coord[(c, pos)] = rid
    return by_id, by_coord

def load_leads(traits: Sequence[str]) -> Dict[str, List[Dict[str, object]]]:
    out: Dict[str, List[Dict[str, object]]] = {}
    for trait in traits:
        clump = CLUMP_DIR / f"{trait}.clumps"
        candidates = {}; candidates_coord = {}
        with (CAND_DIR / f"{trait}.tsv").open(encoding="utf-8", errors="replace", newline="") as h:
            for r in csv.DictReader(h, delimiter="\t"):
                rid = (r.get("rsid") or "").strip()
                if rid: candidates[rid] = r
                c = norm_chr(r.get("chromosome", "")); p = parse_num(r.get("position"))
                if c and p is not None: candidates_coord[(c, int(p))] = r
        rows = []
        with clump.open(encoding="utf-8", errors="replace", newline="") as h:
            for r in csv.DictReader(h, delimiter="\t"):
                rid = r["ID"]; c = norm_chr(r["#CHROM"]); pos = int(r["POS"])
                src = candidates.get(rid) or candidates_coord.get((c, pos), {})
                beta = parse_num(src.get("beta")); se = parse_num(src.get("standard_error"))
                if beta is None or se is None or se <= 0:
                    continue
                rows.append({"rsid": rid, "chrom": c, "pos": pos, "p": parse_num(r["P"]),
                             "ea": (src.get("effect_allele") or "").upper(), "oa": (src.get("other_allele") or "").upper(),
                             "eaf": parse_num(src.get("effect_allele_frequency")), "beta": beta, "se": se,
                             "n": parse_num(src.get("sample_size")), "f": parse_num(src.get("f_statistic"))})
        out[trait] = rows
    return out

def build_reference_frequency(leads: Dict[str, List[Dict[str, object]]], bim: Dict[str, Tuple[str, int, str, str]]) -> Dict[str, float]:
    PHASE2.mkdir(parents=True, exist_ok=True)
    ids = sorted({str(x["rsid"]) for rows in leads.values() for x in rows if x["rsid"] in bim})
    idfile = PHASE2 / "1kg_eur_iv_ids.txt"; idfile.write_text("\n".join(ids) + "\n", encoding="utf-8")
    outprefix = PHASE2 / "1kg_eur_iv_freq"
    afreq = outprefix.with_suffix(".afreq")
    if not afreq.exists() or afreq.stat().st_size == 0:
        cmd = ["plink2", "--bfile", str(EUR_BFILE), "--extract", str(idfile), "--freq", "--threads", "1", "--out", str(outprefix)]
        proc = subprocess.run(cmd, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (PHASE2 / "1kg_eur_iv_freq.log").write_text(proc.stdout, encoding="utf-8")
        if proc.returncode != 0: raise RuntimeError("plink2 reference frequency failed")
    freq: Dict[str, Tuple[str, float]] = {}
    with afreq.open(encoding="utf-8") as h:
        for r in csv.DictReader(h, delimiter="\t"):
            f = parse_num(r.get("ALT1_FREQ") or r.get("ALT_FREQS")); alt = (r.get("ALT1") or r.get("ALT") or "").upper()
            if f is not None: freq[r["ID"]] = (alt, f)
    out: Dict[str, float] = {}
    for rid, (c, pos, a1, a2) in bim.items():
        if rid not in freq: continue
        alt, f = freq[rid]
        if alt == a1: out[rid] = f
        elif alt == a2: out[rid] = 1.0 - f
    return out

def load_outcome_trait(trait: str, path: Path, requests: set, coord_requests: set, fallback_n: Optional[float]) -> Dict[str, Dict[str, object]]:
    found: Dict[str, Dict[str, object]] = {}
    with open_text(path) as h:
        first = ""
        while not first:
            first = h.readline()
            if not first: raise ValueError("empty outcome file")
            first = first.strip("\ufeff\r\n")
        delim = "\t" if first.count("\t") >= 2 else ("," if first.count(",") >= 2 else None)
        header = split_line(first, delim); cmap = resolve(header)
        for line in h:
            if not line.strip(): continue
            parts = split_line(line.rstrip("\r\n"), delim)
            if len(parts) < len(header): continue
            rid = value(parts, cmap["rsid"])
            rid = rid if rid and rid not in {".", "NA", "N/A"} else ""
            chrom_raw = value(parts, cmap["chr"])
            pos_raw = value(parts, cmap["pos"])
            if cmap["chr"] == cmap["pos"] and ":" in chrom_raw:
                chrom_raw, pos_raw = chrom_raw.split(":", 1)
            chrom = norm_chr(chrom_raw)
            pos = int(float(pos_raw)) if pos_raw and re.match(r"^[0-9]+(?:\.0+)?$", pos_raw) else None
            c_from = coord_from(rid)
            if (not chrom or pos is None) and c_from: chrom, pos = c_from
            key_coord = (chrom, pos) if chrom and pos is not None else None
            if rid not in requests and key_coord not in coord_requests: continue
            ea, oa = value(parts, cmap["ea"]).upper(), value(parts, cmap["oa"]).upper()
            beta = parse_num(value(parts, cmap["beta"])) if cmap["beta"] is not None else None
            if beta is None and cmap["or"] is not None:
                odds = parse_num(value(parts, cmap["or"])); beta = math.log(odds) if odds and odds > 0 else None
            se = parse_num(value(parts, cmap["se"]))
            p = parse_num(value(parts, cmap["p"]))
            if p is None and beta is not None and se and se > 0: p = 2 * norm.sf(abs(beta / se))
            if not ea or not oa or beta is None or se is None or not math.isfinite(se) or se <= 0: continue
            eaf = parse_num(value(parts, cmap["eaf"])) if cmap["eaf"] is not None else None
            n = parse_num(value(parts, cmap["n"])) if cmap["n"] is not None else fallback_n
            row = {"rsid": rid, "chrom": chrom, "pos": pos, "ea": ea, "oa": oa, "beta": beta,
                   "se": se, "p": p, "eaf": eaf, "n": n}
            keys = [rid] if rid else []
            if key_coord: keys.append("coord:" + key_coord[0] + ":" + str(key_coord[1]))
            for key in keys:
                previous = found.get(key)
                if previous is None or ((p is not None) and (previous.get("p") is None or p < previous["p"])):
                    found[key] = row
    return found

def lookup_outcome(found: Dict[str, Dict[str, object]], inst: Dict[str, object], bim: Dict[str, Tuple[str, int, str, str]]) -> Optional[Dict[str, object]]:
    row = found.get(str(inst["rsid"]))
    if row is None:
        row = found.get("coord:" + str(inst["chrom"]) + ":" + str(inst["pos"]))
    return dict(row) if row is not None else None

def is_pal(a: str, b: str) -> bool:
    return {a, b} in ({"A", "T"}, {"C", "G"})

def allele_eaf(rid: str, allele: str, source: Optional[float], ref_eaf: Dict[str, float], bim: Dict[str, Tuple[str, int, str, str]]) -> Optional[float]:
    if source is not None: return float(source)
    base = ref_eaf.get(rid); info = bim.get(rid)
    if base is None or info is None: return None
    if allele == info[2]: return base
    if allele == info[3]: return 1.0 - base
    return None

def harmonize(exposure: List[Dict[str, object]], outcome: Dict[str, Dict[str, object]], ref_eaf: Dict[str, float], bim: Dict[str, Tuple[str, int, str, str]]) -> Tuple[List[Dict[str, object]], Dict[str, int]]:
    counts = defaultdict(int); kept = []
    for x in exposure:
        counts["initial_iv"] += 1
        y = lookup_outcome(outcome, x, bim)
        if y is None: counts["missing_outcome"] += 1; continue
        counts["matched_iv"] += 1
        ea, oa, ya, yo = str(x["ea"]), str(x["oa"]), str(y["ea"]), str(y["oa"])
        if not ea or not oa or not ya or not yo: counts["missing_alleles"] += 1; continue
        eaf_x = allele_eaf(str(x["rsid"]), ea, x.get("eaf"), ref_eaf, bim)
        eaf_y = allele_eaf(str(x["rsid"]), ya, y.get("eaf"), ref_eaf, bim)
        pal = is_pal(ea, oa)
        flip = False
        if pal:
            if eaf_x is None or eaf_y is None or 0.42 <= float(eaf_x) <= 0.58 or 0.42 <= float(eaf_y) <= 0.58:
                counts["palindromic_ambiguous"] += 1; continue
            same = abs(float(eaf_x) - float(eaf_y)); rev = abs(float(eaf_x) - (1.0 - float(eaf_y)))
            if same <= rev and same <= 0.20: flip = False
            elif rev < same and rev <= 0.20: flip = True
            else: counts["palindromic_frequency_mismatch"] += 1; continue
        elif ea == ya and oa == yo:
            flip = False
        elif ea == yo and oa == ya:
            flip = True
        else:
            counts["incompatible_alleles"] += 1; continue
        beta_y = -float(y["beta"]) if flip else float(y["beta"])
        eaf_y_aligned = (1.0 - float(eaf_y)) if (flip and eaf_y is not None) else eaf_y
        if eaf_x is not None and eaf_y_aligned is not None and abs(float(eaf_x) - float(eaf_y_aligned)) > 0.20:
            counts["eaf_mismatch"] += 1; continue
        counts["final_iv"] += 1
        kept.append({"rsid": x["rsid"], "beta_exp": float(x["beta"]), "se_exp": float(x["se"]),
                     "beta_out": beta_y, "se_out": float(y["se"]), "eaf": eaf_x,
                     "n_exp": x.get("n"), "n_out": y.get("n"), "f": x.get("f"),
                     "p_exp": x.get("p"), "p_out": y.get("p"), "binary_exp": False,
                     "binary_out": False})
    return kept, dict(counts)

def weighted_median(values: np.ndarray, weights: np.ndarray) -> float:
    order = np.argsort(values); v, w = values[order], weights[order]
    return float(v[np.searchsorted(np.cumsum(w) / w.sum(), 0.5)])

def weighted_mode(values: np.ndarray, weights: np.ndarray) -> float:
    if len(values) < 3: return float("nan")
    sd = np.std(values, ddof=1) if len(values) > 1 else 0.0
    bw = max(1.06 * sd * len(values) ** (-1 / 5), 1e-6)
    grid = np.linspace(float(values.min()) - 3 * bw, float(values.max()) + 3 * bw, 2000)
    dens = np.exp(-0.5 * ((grid[:, None] - values[None, :]) / bw) ** 2) @ weights
    return float(grid[int(np.argmax(dens))])

def egger(values: np.ndarray, beta_exp: np.ndarray, se_out: np.ndarray) -> Tuple[float, float, float, float]:
    w = 1 / np.maximum(se_out, 1e-300) ** 2
    X = np.column_stack([np.ones(len(values)), beta_exp])
    XtW = X.T * w
    cov = np.linalg.pinv(XtW @ X)
    coef = cov @ (XtW @ (values * se_out * 0 + (values * beta_exp * 0))) if False else None
    # Outcome beta is reconstructed by ratio * exposure beta.
    y = values * beta_exp
    coef = cov @ (XtW @ y)
    resid = y - X @ coef
    df = max(len(values) - 2, 1); sigma2 = float((w * resid ** 2).sum() / df)
    se = np.sqrt(np.diag(cov) * sigma2)
    return float(coef[1]), float(se[1]), float(coef[0]), float(se[0])

def ivw_random(beta_exp: np.ndarray, se_exp: np.ndarray, beta_out: np.ndarray, se_out: np.ndarray) -> Dict[str, float]:
    ratio = beta_out / beta_exp
    var = (se_out ** 2 / beta_exp ** 2) + (beta_out ** 2 * se_exp ** 2 / beta_exp ** 4)
    var = np.maximum(var, 1e-300); w = 1 / var
    fixed = float((w * ratio).sum() / w.sum()); Q = float((w * (ratio - fixed) ** 2).sum())
    sw2 = float((w ** 2).sum()); tau = max(0.0, (Q - (len(ratio) - 1)) / max(w.sum() - sw2 / w.sum(), 1e-300))
    wr = 1 / (var + tau); beta = float((wr * ratio).sum() / wr.sum()); se = float(math.sqrt(1 / wr.sum()))
    return {"beta": beta, "se": se, "Q": Q, "Q_p": float(1 - chi2.cdf(Q, max(len(ratio) - 1, 1))),
            "tau2": tau, "p": float(2 * norm.sf(abs(beta / se))), "ratio": ratio, "ratio_var": var}

def steiger(rows: List[Dict[str, object]], binary_exp: bool, binary_out: bool, exp_meta: Dict[str, str], out_meta: Dict[str, str]) -> Tuple[object, object, object, object]:
    r_exp = []; r_out = []; n_exp = []; n_out = []
    for r in rows:
        p = parse_num(r.get("eaf"));
        if p is None or not (0 < p < 1): return ("NA", "NA", "NA", "NA")
        r_exp.append(math.sqrt(max(0.0, 2 * p * (1 - p) * float(r["beta_exp"]) ** 2)))
        r_out.append(math.sqrt(max(0.0, 2 * p * (1 - p) * float(r["beta_out"]) ** 2)))
        n_exp.append(float(r["n_exp"]) if r.get("n_exp") else np.nan); n_out.append(float(r["n_out"]) if r.get("n_out") else np.nan)
    n1 = float(np.nanmean(n_exp)) if np.isfinite(np.nanmean(n_exp)) else float("nan")
    n2 = float(np.nanmean(n_out)) if np.isfinite(np.nanmean(n_out)) else float("nan")
    if binary_exp:
        ca, co = registry_cases_controls(exp_meta); n1 = 4 / (1 / ca + 1 / co) if ca and co else n1
    if binary_out:
        ca, co = registry_cases_controls(out_meta); n2 = 4 / (1 / ca + 1 / co) if ca and co else n2
    re_ = min(math.sqrt(sum(x*x for x in r_exp)), 0.999999); ro_ = min(math.sqrt(sum(x*x for x in r_out)), 0.999999)
    if not (n1 > 3 and n2 > 3): return (re_ ** 2, ro_ ** 2, re_ > ro_, "NA")
    z = (math.atanh(re_) - math.atanh(ro_)) / math.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    return (re_ ** 2, ro_ ** 2, re_ > ro_, float(2 * norm.sf(abs(z))))

def run_direction(exposure: str, outcome: str, exp_rows: List[Dict[str, object]], outcome_rows: Dict[str, Dict[str, object]], ref_eaf: Dict[str, float], registry: Dict[str, Dict[str, str]], bim: Dict[str, Tuple[str, int, str, str]]) -> Tuple[Dict[str, object], List[Dict[str, object]]]:
    exp_meta, out_meta = registry[exposure], registry[outcome]
    # Fill binary/continuous labels and fallback N on exposure instruments.
    exp_binary = exposure.startswith("sys_"); out_binary = outcome.startswith("sys_")
    enriched = []
    for x in exp_rows:
        z = dict(x); z["binary_exp"] = exp_binary; z["n"] = z.get("n") or registry_n(exp_meta); enriched.append(z)
    harmonized, counts = harmonize(enriched, outcome_rows, ref_eaf, bim)
    for r in harmonized:
        r["binary_exp"] = exp_binary; r["binary_out"] = out_binary
        r["n_exp"] = r.get("n_exp") or registry_n(exp_meta)
        r["n_out"] = r.get("n_out") or registry_n(out_meta)
    k = len(harmonized); qc = []
    if k < 3: qc.append("LOW_INSTRUMENT_COUNT")
    if counts.get("missing_outcome", 0): qc.append("MISSING_OUTCOME_VARIANTS")
    if any(counts.get(x, 0) for x in ["palindromic_ambiguous", "palindromic_frequency_mismatch"]): qc.append("PALINDROMIC_REMOVALS")
    if counts.get("incompatible_alleles", 0): qc.append("INCOMPATIBLE_ALLELES_REMOVED")
    if counts.get("eaf_mismatch", 0): qc.append("EAF_MISMATCH_REMOVALS")
    base = {"retinal_trait": exposure if exposure.startswith("ret_") else outcome,
            "retinal_domain": registry[exposure if exposure.startswith("ret_") else outcome].get("subdomain", "NA"),
            "systemic_disease": outcome if outcome.startswith("sys_") else exposure,
            "direction": f"{exposure}_to_{outcome}", "exposure": exposure, "outcome": outcome,
            "n_iv_initial": len(exp_rows), "n_iv_matched": counts.get("matched_iv", 0), "n_iv_final": k,
            "mean_F": float(np.nanmean([float(x["f"]) for x in exp_rows if x.get("f") is not None])) if any(x.get("f") is not None for x in exp_rows) else np.nan,
            "min_F": float(np.nanmin([float(x["f"]) for x in exp_rows if x.get("f") is not None])) if any(x.get("f") is not None for x in exp_rows) else np.nan,
            "method": "NO_VALID_IV", "beta": np.nan, "se": np.nan, "ci_low": np.nan, "ci_high": np.nan,
            "OR": np.nan, "p": np.nan, "q_global_directional": np.nan, "q_direction_specific": np.nan,
            "heterogeneity_Q": np.nan, "heterogeneity_p": np.nan, "egger_intercept": np.nan, "egger_p": np.nan,
            "steiger_direction": "NA", "steiger_p": np.nan, "variance_explained_exposure": np.nan,
            "variance_explained_outcome": np.nan, "presso_status": "NOT_RUN", "loo_status": "NOT_RUN",
            "weighted_median": np.nan, "weighted_mode": np.nan, "egger_beta": np.nan,
            "weighted_median_p": np.nan, "weighted_mode_p": np.nan, "harmonisation_initial_iv": counts.get("initial_iv", 0),
            "harmonisation_matched_iv": counts.get("matched_iv", 0), "harmonisation_final_iv": k,
            "qc_flag": ";".join(qc) if qc else "PASS", "evidence_status": "UNRESOLVED" if k == 0 else "NULL",
            "binary_exposure": exp_binary, "binary_outcome": out_binary,
            "steiger_assumption": "binary traits use effective N=4/(1/cases+1/controls); r2 uses 2*p*(1-p)*beta^2; reference EAF fallback when source EAF missing"}
    if k == 0: return base, []
    bx = np.array([r["beta_exp"] for r in harmonized], dtype=float); sx = np.array([r["se_exp"] for r in harmonized], dtype=float)
    by = np.array([r["beta_out"] for r in harmonized], dtype=float); sy = np.array([r["se_out"] for r in harmonized], dtype=float)
    if k == 1:
        beta = by[0] / bx[0]; se = math.sqrt(sy[0] ** 2 / bx[0] ** 2 + by[0] ** 2 * sx[0] ** 2 / bx[0] ** 4)
        mr = {"beta": beta, "se": se, "p": 2 * norm.sf(abs(beta / se)), "Q": np.nan, "Q_p": np.nan, "ratio": np.array([beta]), "ratio_var": np.array([se*se])}
        base["method"] = "Wald_ratio"
    else:
        mr = ivw_random(bx, sx, by, sy); beta, se = mr["beta"], mr["se"]; base["method"] = "IVW_random_effects"
    base.update({"beta": beta, "se": se, "ci_low": beta - 1.95996398454 * se, "ci_high": beta + 1.95996398454 * se,
                 "OR": math.exp(beta) if out_binary and abs(beta) < 700 else np.nan, "p": mr["p"],
                 "heterogeneity_Q": mr.get("Q", np.nan), "heterogeneity_p": mr.get("Q_p", np.nan)})
    if k >= 3:
        ratios = by / bx; weights = 1 / np.maximum(mr["ratio_var"], 1e-300)
        base["weighted_median"] = weighted_median(ratios, weights)
        base["weighted_median_p"] = 2 * norm.sf(abs(base["weighted_median"] / math.sqrt(1 / weights.sum())))
        base["weighted_mode"] = weighted_mode(ratios, weights)
        base["weighted_mode_p"] = 2 * norm.sf(abs(base["weighted_mode"] / math.sqrt(1 / weights.sum())))
        eb, ese, ei, eise = egger(ratios, bx, sy)
        base["egger_beta"] = eb; base["egger_intercept"] = ei; base["egger_p"] = 2 * norm.sf(abs(ei / eise)) if eise > 0 else np.nan
        loo = []
        for i in range(k):
            if k - 1 < 2: continue
            m = ivw_random(np.delete(bx, i), np.delete(sx, i), np.delete(by, i), np.delete(sy, i)); loo.append(m["beta"])
        base["loo_status"] = "COMPUTED" if loo else "NOT_RUN"; base["loo_beta_min"] = min(loo) if loo else np.nan; base["loo_beta_max"] = max(loo) if loo else np.nan
    elif k == 2:
        base["loo_status"] = "NOT_RUN_TWO_IV"
    ve, vo, correct, sp = steiger(harmonized, exp_binary, out_binary, exp_meta, out_meta)
    base["variance_explained_exposure"] = ve; base["variance_explained_outcome"] = vo; base["steiger_direction"] = bool(correct) if isinstance(correct, (bool, np.bool_)) else "NA"; base["steiger_p"] = sp if isinstance(sp, (float, int)) else np.nan
    if k >= 4: base["presso_status"] = "PENDING_MRPRESSO"
    else: base["presso_status"] = "NOT_ELIGIBLE_LT4_IV"
    return base, harmonized

def main() -> None:
    PHASE2.mkdir(parents=True, exist_ok=True)
    registry = load_registry(); bim, by_coord = load_bim()
    traits = RETINAL + SYSTEMIC
    manifest = load_manifest()
    missing = [t for t in traits if t not in manifest]
    if missing: raise RuntimeError("Missing raw files for locked traits: " + ",".join(missing))
    leads = load_leads(traits)
    if any(len(leads[t]) == 0 for t in traits): raise RuntimeError("No clumped instruments for " + ",".join(t for t in traits if not leads[t]))
    ref_eaf = build_reference_frequency(leads, bim)
    requests = {}
    for outcome in traits:
        rsids = {str(x["rsid"]) for exp in traits if exp != outcome for x in leads[exp]}
        coords = {(str(x["chrom"]), int(x["pos"])) for exp in traits if exp != outcome for x in leads[exp]}
        requests[outcome] = (rsids, coords)
    outcome_data = {}
    for idx, outcome in enumerate(traits, 1):
        fallback = registry_n(registry[outcome])
        print(f"loading outcome {idx}/{len(traits)} {outcome}", flush=True)
        outcome_data[outcome] = load_outcome_trait(outcome, manifest[outcome], *requests[outcome], fallback)
        print(f"loaded keys={len(outcome_data[outcome])}", flush=True)
    records = []; harmonized_all = []
    for retinal in RETINAL:
        for systemic in SYSTEMIC:
            for exposure, outcome in [(retinal, systemic), (systemic, retinal)]:
                row, harm = run_direction(exposure, outcome, leads[exposure], outcome_data[outcome], ref_eaf, registry, bim)
                pair_key = retinal + "__" + systemic; row["pair_key"] = pair_key
                records.append(row)
                for h in harm:
                    h.update({"pair_key": pair_key, "direction": row["direction"], "exposure": exposure, "outcome": outcome})
                    harmonized_all.append(h)
    df = pd.DataFrame(records)
    # Primary and direction-specific BH are calculated only after all 224 rows exist.
    df["q_global_directional"] = bh(df["p"])
    df["q_direction_specific"] = np.nan
    for direction, idx in df.groupby("direction").groups.items(): df.loc[idx, "q_direction_specific"] = bh(df.loc[idx, "p"])
    # MRPRESSO consumes the harmonised instrument-level table in one R process.
    harm_path = PHASE2 / "MR_HARMONIZED_INSTRUMENTS.tsv"
    pd.DataFrame(harmonized_all).to_csv(harm_path, sep="\t", index=False, na_rep="NA")
    subprocess.run(["Rscript", str(ROOT / "scripts/run_phase2a_mrpresso.R"), str(harm_path), str(PHASE2 / "MR_PRESSO_RESULTS.tsv")], cwd=ROOT, check=False)
    presso = pd.read_csv(PHASE2 / "MR_PRESSO_RESULTS.tsv", sep="\t") if (PHASE2 / "MR_PRESSO_RESULTS.tsv").exists() else pd.DataFrame()
    if len(presso):
        lookup = {(r.pair_key, r.direction): r.status for r in presso.itertuples(index=False)}
        df["presso_status"] = [lookup.get((r.pair_key, r.direction), r.presso_status) for r in df.itertuples(index=False)]
    # Evidence classes: primary global FDR + direction + Steiger + broad sensitivity.
    for i, r in df.iterrows():
        if r["n_iv_final"] == 0 or r["evidence_status"] == "UNRESOLVED": df.at[i, "evidence_status"] = "UNRESOLVED"; continue
        if pd.notna(r["q_global_directional"]) and r["q_global_directional"] < 0.05:
            steiger_ok = (r["steiger_direction"] is True) or (str(r["steiger_direction"]).lower() == "true")
            pleio = pd.notna(r["egger_p"]) and r["egger_p"] < 0.05
            sens = True if r["n_iv_final"] < 3 else (pd.isna(r["weighted_median"]) or np.sign(r["weighted_median"]) == np.sign(r["beta"]))
            df.at[i, "evidence_status"] = "DIRECTIONAL_MR_SUPPORTED" if steiger_ok and not pleio and sens else "UNRESOLVED"
        elif pd.notna(r["p"]) and r["p"] < 0.05: df.at[i, "evidence_status"] = "SUGGESTIVE"
        else: df.at[i, "evidence_status"] = "NULL"
    out_master = PHASE2 / "MR_DIRECTIONAL_MASTER.tsv"
    df.to_csv(out_master, sep="\t", index=False, na_rep="NA")
    pair_rows = []
    for (retinal, systemic), g in df.groupby(["retinal_trait", "systemic_disease"]):
        a = g[g["direction"] == f"{retinal}_to_{systemic}"].iloc[0]; b = g[g["direction"] == f"{systemic}_to_{retinal}"].iloc[0]
        sa, sb = a["evidence_status"], b["evidence_status"]
        if sa == "UNRESOLVED" or sb == "UNRESOLVED": pattern = "E_UNRESOLVED"
        elif sa == "DIRECTIONAL_MR_SUPPORTED" and sb == "DIRECTIONAL_MR_SUPPORTED": pattern = "C_BOTH_SUPPORTED"
        elif sa == "DIRECTIONAL_MR_SUPPORTED": pattern = "A_RETINA_TO_DISEASE_ONLY"
        elif sb == "DIRECTIONAL_MR_SUPPORTED": pattern = "B_DISEASE_TO_RETINA_ONLY"
        elif sa == "NULL" and sb == "NULL": pattern = "D_NEITHER_SUPPORTED"
        else: pattern = "E_UNRESOLVED"
        pair_rows.append({"retinal_trait": retinal, "retinal_domain": registry[retinal].get("subdomain", "NA"), "systemic_disease": systemic,
                          "retina_to_disease_status": sa, "disease_to_retina_status": sb, "pattern": pattern,
                          "retina_to_disease_beta": a["beta"], "retina_to_disease_p": a["p"], "retina_to_disease_q": a["q_global_directional"],
                          "disease_to_retina_beta": b["beta"], "disease_to_retina_p": b["p"], "disease_to_retina_q": b["q_global_directional"]})
    pair_df = pd.DataFrame(pair_rows); pair_df.to_csv(PHASE2 / "MR_PAIR_SUMMARY.tsv", sep="\t", index=False, na_rep="NA")
    make_atlas(pair_df)
    report = make_report(df, pair_df, registry)
    (ROOT / "reports/PHASE2A_BIDIRECTIONAL_MR.md").write_text(report, encoding="utf-8")
    print(f"directions={len(df)} pairs={len(pair_df)} output={out_master}")

def bh(s: pd.Series) -> pd.Series:
    p = pd.to_numeric(s, errors="coerce").to_numpy(dtype=float); q = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    if not ok.any(): return pd.Series(q, index=s.index)
    idx = np.where(ok)[0]; order = idx[np.argsort(p[ok])]; v = p[order] * len(order) / np.arange(1, len(order)+1); v = np.minimum.accumulate(v[::-1])[::-1]; q[order] = np.minimum(v,1); return pd.Series(q,index=s.index)

def make_atlas(pair_df: pd.DataFrame) -> None:
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.colors import ListedColormap
    colors = {"A_RETINA_TO_DISEASE_ONLY":"#0F4D92", "B_DISEASE_TO_RETINA_ONLY":"#42949E", "C_BOTH_SUPPORTED":"#9A4D8E", "D_NEITHER_SUPPORTED":"#CFCECE", "E_UNRESOLVED":"#B64342"}
    symbols = {"A_RETINA_TO_DISEASE_ONLY":"→", "B_DISEASE_TO_RETINA_ONLY":"←", "C_BOTH_SUPPORTED":"↔", "D_NEITHER_SUPPORTED":"○", "E_UNRESOLVED":"?"}
    mat = np.zeros((len(RETINAL), len(SYSTEMIC)), dtype=int); codes = list(colors)
    for i, r in enumerate(RETINAL):
        for j, s in enumerate(SYSTEMIC): mat[i,j] = codes.index(pair_df.loc[(pair_df.retinal_trait==r)&(pair_df.systemic_disease==s), "pattern"].iloc[0])
    fig, ax = plt.subplots(figsize=(13, 8)); ax.imshow(mat, cmap=ListedColormap([colors[c] for c in codes]), vmin=-.5, vmax=len(codes)-.5, aspect="auto")
    for i in range(len(RETINAL)):
        for j in range(len(SYSTEMIC)):
            ax.text(j, i, symbols[codes[mat[i,j]]], ha="center", va="center", fontsize=18, color="black")
    ax.set_xticks(range(len(SYSTEMIC))); ax.set_xticklabels([x.replace("sys_","").replace("_"," ") for x in SYSTEMIC], rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(RETINAL))); ax.set_yticklabels([x.replace("ret_","").replace("_"," ") for x in RETINAL], fontsize=9)
    ax.set_xlabel("Systemic disease"); ax.set_ylabel("Retinal phenotype"); ax.set_title("MR directionality atlas (224 prespecified tests)")
    handles = [plt.Line2D([0],[0], marker="s", color="w", markerfacecolor=colors[c], markersize=10, label=f"{symbols[c]} {c.split('_',1)[1].replace('_',' ')}") for c in codes]
    ax.legend(handles=handles, frameon=False, bbox_to_anchor=(1.02,1), loc="upper left", fontsize=9)
    fig.tight_layout(pad=2); out = ROOT / "figures/phase2"; out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "Figure_2A_MR_directionality_atlas.png", dpi=300, bbox_inches="tight"); fig.savefig(out / "Figure_2A_MR_directionality_atlas.svg", bbox_inches="tight"); plt.close(fig)

def make_report(df: pd.DataFrame, pairs: pd.DataFrame, registry: Dict[str, Dict[str, str]]) -> str:
    def count(mask): return int(mask.sum())
    retina_sig = df[(df.direction.str.startswith("ret_")) & (df.q_global_directional < .05)]
    disease_sig = df[(df.direction.str.startswith("sys_")) & (df.q_global_directional < .05)]
    status = df.evidence_status.value_counts().to_dict()
    pattern = pairs.pattern.value_counts().to_dict()
    return f"""# Phase 2A bidirectional Mendelian randomization

Date: 2026-09-18 (Asia/Shanghai)

## Completion

- Planned pairs: 112 retinal × systemic pairs
- Planned directions: 224
- Completed directional rows: {len(df)}
- Directional rows with no valid IV: {count(df.n_iv_final == 0)}
- Directional rows labelled unresolved: {count(df.evidence_status == 'UNRESOLVED')}
- Primary estimator: IVW random-effects when ≥2 valid IVs; Wald ratio for one valid IV
- Global primary multiplicity: BH-FDR across all 224 directional primary tests

## Primary results

- Global-FDR significant retina→disease directions: {len(retina_sig)}
- Global-FDR significant disease→retina directions: {len(disease_sig)}
- Evidence-status counts: {status}
- Pair-pattern counts: {pattern}

No result is labelled DRIVER, TARGET, BYSTANDER or BIDIRECTIONAL. Pair patterns are descriptive MR directionality patterns only.

## Harmonisation and robustness

Harmonisation counts, F-statistics, palindromic handling, allele-frequency checks, Steiger directionality, heterogeneity, Egger intercept, weighted estimators, leave-one-out and MR-PRESSO statuses are in `results/phase2/MR_DIRECTIONAL_MASTER.tsv`. Binary traits use effective sample size `4/(1/cases + 1/controls)` for Steiger comparisons; the approximate observed-scale `2*p*(1-p)*beta^2` variance contribution and reference-EAF fallback are recorded in each row. No automatic proxy SNPs were used.

## Relation to Phase 1

The Phase 1B local-rg null and LAVA discrepancy were not used as MR admission criteria. The cross-direction summary can be joined to `results/phase1b/LOCAL_RG_METHOD_CONCORDANCE.tsv` and `reports/PHASE1B1_FINAL_LOCAL_RG_VERDICT.md`; MR-positive/local-rg-null and MR-null/local-rg-evidence patterns are descriptive only.

## Boundary

Phase 1C colocalisation remains `NO_GO_UNDER_CURRENT_LOCK`. CAUSE, LCV, GSMR, MVMR, mediation and final causal-taxonomy labels were not run. This report is the Phase 2A stopping point.
"""

if __name__ == "__main__": main()
