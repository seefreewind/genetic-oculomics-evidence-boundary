#!/usr/bin/env python3
"""Build HMG display and supplementary figures from frozen project outputs.

No association is recalculated here. The script only reshapes locked result files
for publication graphics and writes SVG/PDF/PNG/TIFF variants.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "hmg"
OUT.mkdir(parents=True, exist_ok=True)
SUP = ROOT / "supplement" / "hmg"
SUP.mkdir(parents=True, exist_ok=True)

mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 7, "axes.titlesize": 8, "axes.labelsize": 7,
    "xtick.labelsize": 6, "ytick.labelsize": 6, "legend.fontsize": 6,
    "axes.spines.right": False, "axes.spines.top": False, "axes.linewidth": 0.7,
    "svg.fonttype": "none", "pdf.fonttype": 42,
})

BLUE, ORANGE, PURPLE = "#2E5EAA", "#D97832", "#7653A8"
TEAL, RED, GRAY = "#2C8C8C", "#B0444A", "#6E7781"
PALE_BLUE, PALE_ORANGE, PALE_PURPLE = "#DCE8F7", "#F5E3D2", "#E8DFF2"


def save(fig: plt.Figure, stem: str, out: Path = OUT) -> None:
    base = out / stem
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(base.with_suffix(".png"), dpi=600, bbox_inches="tight")
    fig.savefig(base.with_suffix(".tiff"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def panel(ax, label):
    ax.text(-0.09, 1.04, label, transform=ax.transAxes, fontsize=9,
            fontweight="bold", va="bottom")


def fig1_framework():
    fig, ax = plt.subplots(figsize=(7.2, 4.1))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(.02, .97, "Biological framework for retinal–systemic human genetics",
            fontsize=10.5, fontweight="bold", va="top")
    ax.text(.02, .91, "Retinal domains are evaluated against distinct systemic contexts and evidence claims.",
            fontsize=7, color="#4B5563")
    # Domain columns
    retinal = [("Neuroretina", "RNFL, ganglion-cell and\ninner-retinal measures", PALE_BLUE, BLUE),
               ("Outer retina", "photoreceptor and\nouter-layer measures", PALE_ORANGE, ORANGE),
               ("Microvasculature", "arteriolar calibre,\nvenular calibre and tortuosity", PALE_PURPLE, PURPLE)]
    systemic = [("Cardiometabolic / vascular", "CAD, stroke, T2D", "#E8F1EE", TEAL),
                ("Renal", "CKD", "#EEF2F6", BLUE),
                ("Neurodegenerative", "Alzheimer, Parkinson disease", "#F3EEE8", ORANGE),
                ("Immune / inflammatory", "SLE, IBD", "#F2EAF3", PURPLE)]
    ax.text(.17, .84, "Retinal quantitative traits", ha="center", fontsize=8, fontweight="bold")
    ax.text(.68, .84, "Systemic disease contexts", ha="center", fontsize=8, fontweight="bold")
    ys = [.70, .52, .34]
    for (title, detail, fill, edge), y in zip(retinal, ys):
        ax.add_patch(FancyBboxPatch((.03, y-.075), .28, .13, boxstyle="round,pad=.008,rounding_size=.012",
                                    linewidth=1.0, edgecolor=edge, facecolor=fill))
        ax.text(.17, y+.025, title, ha="center", va="center", fontsize=7.2, fontweight="bold")
        ax.text(.17, y-.025, detail, ha="center", va="center", fontsize=5.8, color="#374151")
    for (title, detail, fill, edge), y in zip(systemic, [.74, .58, .42, .26]):
        ax.add_patch(FancyBboxPatch((.53, y-.055), .30, .10, boxstyle="round,pad=.008,rounding_size=.012",
                                    linewidth=1.0, edgecolor=edge, facecolor=fill))
        ax.text(.68, y+.018, title, ha="center", va="center", fontsize=6.8, fontweight="bold")
        ax.text(.68, y-.020, detail, ha="center", va="center", fontsize=5.8, color="#374151")
    for y in [.70, .52, .34]:
        ax.add_patch(FancyArrowPatch((.32, y), (.51, .67), arrowstyle="-|>", mutation_scale=8,
                                     linewidth=.6, color="#9AA1A8", connectionstyle="arc3,rad=-.15"))
    # Evidence ladder
    ax.text(.03, .15, "Evidence ladder", fontsize=8, fontweight="bold")
    ladder = [("Global sharing", "LDSC: 112 pairs", PALE_BLUE, BLUE),
              ("Local architecture", "HDL-L primary; LAVA audit", PALE_ORANGE, ORANGE),
              ("Directionality", "224 bidirectional MR directions", PALE_PURPLE, PURPLE),
              ("Instrument QC", "CRAE–CKD reconstruction", "#F3D9DC", RED)]
    xs = [.16, .39, .62, .85]
    for i, ((title, detail, fill, edge), x) in enumerate(zip(ladder, xs)):
        ax.add_patch(FancyBboxPatch((x-.095, .035), .19, .075, boxstyle="round,pad=.006,rounding_size=.01",
                                    linewidth=1.0, edgecolor=edge, facecolor=fill))
        ax.text(x, .082, title, ha="center", va="center", fontsize=6.4, fontweight="bold")
        ax.text(x, .055, detail, ha="center", va="center", fontsize=5.1, color="#374151")
        if i < len(ladder)-1:
            ax.add_patch(FancyArrowPatch((x+.10, .073), (xs[i+1]-.10, .073), arrowstyle="-|>",
                                         mutation_scale=8, linewidth=.7, color="#9AA1A8"))
    save(fig, "Figure1_biological_framework")


def fig2_integrated():
    fig, ax = plt.subplots(figsize=(7.1, 3.9))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(.02, .96, "Integrated evidence across human-genetic layers", fontsize=10.5,
            fontweight="bold", va="top")
    cols = [(.02, .20, "Evidence layer"), (.22, .41, "Analysed universe"), (.43, .59, "Multiplicity-controlled result"),
            (.61, .98, "Biological interpretation supported")]
    for x0, x1, label in cols:
        ax.add_patch(Rectangle((x0, .80), x1-x0, .075, facecolor="#E9EDF2", edgecolor="white"))
        ax.text((x0+x1)/2, .837, label, ha="center", va="center", fontsize=6.6, fontweight="bold")
    rows = [
        ("Genome-wide LDSC", "112 pairs", "0 global FDR", "No broad common-variant correlation signal", BLUE),
        ("Primary HDL-L", "116,472 blocks / 47 pairs", "0 global-local FDR", "No stable block-level sharing under primary model", TEAL),
        ("Native LAVA audit", "26,639 rows", "9 native FDR;\n8 boundary-sensitive", "Rows require sensitivity interpretation;\nno stable locus claim", PURPLE),
        ("Bidirectional MR", "224 directions", "1 FDR-positive;\norientation unsupported", "No validated direction\nof retinal mediation", RED),
    ]
    ys = [.69, .54, .39, .24]
    for (layer, universe, result, interp, edge), y in zip(rows, ys):
        ax.add_patch(Rectangle((.02, y-.055), .18, .11, facecolor="#F8FAFC", edgecolor=edge, linewidth=1.2))
        ax.text(.11, y, layer, ha="center", va="center", fontsize=6.7, fontweight="bold")
        for x0, x1, val in [(0.22, .41, universe), (.43, .59, result), (.61, .98, interp)]:
            ax.add_patch(Rectangle((x0, y-.055), x1-x0, .11, facecolor="white", edgecolor="#D8DDE3", linewidth=.6))
            ax.text((x0+x1)/2, y, val, ha="center", va="center", fontsize=6.1, color="#374151")
    ax.text(.02, .075, "Primary conclusions are based on complete declared families; nominal and unresolved rows remain in the supplement.",
            fontsize=6.5, color="#4B5563")
    save(fig, "Figure2_integrated_evidence")


def fig3_local():
    boundary = pd.read_csv(ROOT / "results/phase1b_audit/LAVA_BOUNDARY_AUDIT.tsv", sep="\t")
    metrics = {r.metric: int(r.count) for r in boundary.itertuples()}
    fig, axes = plt.subplots(1, 3, figsize=(7.5, 2.8), gridspec_kw={"width_ratios": [1.1, 1.1, 1.25]})
    ax = axes[0]
    labs, vals = ["HDL-L", "Historical\nLAVA", "Native\nLAVA"], [116472, 26639, 26639]
    bars = ax.bar(labs, vals, color=[BLUE, ORANGE, PURPLE], width=.58)
    ax.set_ylabel("Completed tests / rows"); ax.set_title("Analysed scale", loc="left", fontweight="bold"); ax.set_ylim(0, 123000)
    for b, v in zip(bars, vals): ax.text(b.get_x()+b.get_width()/2, v+2600, f"{v:,}", ha="center", fontsize=6.8, fontweight="bold")
    panel(ax, "a")
    ax = axes[1]
    labs, vals = ["HDL-L", "Historical\nLAVA", "Native\nLAVA"], [0, 1877, 9]
    bars = ax.bar(labs, vals, color=[BLUE, ORANGE, PURPLE], width=.58)
    ax.set_ylabel("FDR-positive rows"); ax.set_title("Inference procedure", loc="left", fontweight="bold"); ax.set_ylim(0, 2050)
    for b, v in zip(bars, vals): ax.text(b.get_x()+b.get_width()/2, v+45, str(v), ha="center", fontsize=7, fontweight="bold")
    panel(ax, "b")
    ax = axes[2]
    labs = ["CI touches\n|rho|=1", "Raw\n|rho|>1", "Raw\n|rho|>1.25"]
    vals = [metrics.get("native_ci_touches_boundary", 16938), metrics.get("raw_out_of_bounds_abs_rho_gt_1", 347), metrics.get("raw_out_of_param_lim_abs_rho_gt_1_25", 68)]
    bars = ax.bar(labs, vals, color=[PURPLE, "#9B7DBA", "#C7B4D6"], width=.58)
    ax.set_ylabel("Rows (denominator 26,639)"); ax.set_title("Boundary diagnostics", loc="left", fontweight="bold"); ax.set_ylim(0, 18500)
    for b, v in zip(bars, vals): ax.text(b.get_x()+b.get_width()/2, v+380, f"{v:,}", ha="center", fontsize=6.8, fontweight="bold")
    ax.text(.98, .98, "63.6% of native CIs", transform=ax.transAxes, ha="right", va="top", fontsize=6.2, color="#4B5563")
    panel(ax, "c")
    fig.suptitle("Local retinal–systemic evidence was sensitive to inference procedure", x=.02, ha="left", fontsize=9.5, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, .92)); save(fig, "Figure3_local_method_sensitivity")


def fig4_crae():
    mr = pd.read_csv(ROOT / "results/phase2/MR_DIRECTIONAL_MASTER.tsv", sep="\t")
    counts = mr["evidence_status"].fillna("NULL").value_counts()
    fig, axes = plt.subplots(1, 3, figsize=(8.0, 2.9), gridspec_kw={"width_ratios": [1.15, 1.55, 1.25]})
    ax = axes[0]
    labs, vals = ["NULL", "SUGGESTIVE", "UNRESOLVED"], [int(counts.get(x, 0)) for x in ["NULL", "SUGGESTIVE", "UNRESOLVED"]]
    bars = ax.bar(np.arange(3), vals, color=["#E9EDF2", "#F3C77B", "#C77D9B"], width=.58)
    ax.set_ylabel("Directions"); ax.set_title("224-direction MR status", loc="left", fontweight="bold"); ax.set_ylim(0, 235)
    ax.set_xticks(np.arange(3)); ax.set_xticklabels(labs, rotation=25, ha="right", rotation_mode="anchor")
    for b, v in zip(bars, vals): ax.text(b.get_x()+b.get_width()/2, v+4, str(v), ha="center", fontsize=7.2, fontweight="bold")
    panel(ax, "a")
    ax = axes[1]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title("CRAE–CKD instrument audit", loc="left", fontweight="bold")
    steps = [("427", "GWS\nvariants", PALE_BLUE, BLUE), ("6", "clumped\nleads", PALE_BLUE, BLUE), ("5 removed", "aligned EAF\nmismatch", PALE_ORANGE, ORANGE), ("1", "retained\nrs475377", PALE_PURPLE, PURPLE)]
    xs = [.12, .38, .64, .88]
    for i, ((h, d, fill, edge), x) in enumerate(zip(steps, xs)):
        ax.add_patch(FancyBboxPatch((x-.105, .40), .21, .25, boxstyle="round,pad=.008,rounding_size=.012", linewidth=1.0, edgecolor=edge, facecolor=fill))
        ax.text(x, .56, h, ha="center", va="center", fontsize=8.5, fontweight="bold"); ax.text(x, .47, d, ha="center", va="center", fontsize=5.8, color="#374151")
        if i < 3: ax.add_patch(FancyArrowPatch((x+.115, .525), (xs[i+1]-.115, .525), arrowstyle="-|>", mutation_scale=9, linewidth=.7, color="#9AA1A8"))
    panel(ax, "b")
    ax = axes[2]; ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off"); ax.set_title("Directionality audit", loc="left", fontweight="bold")
    ax.add_patch(FancyBboxPatch((.08, .58), .84, .20, boxstyle="round,pad=.01,rounding_size=.012", edgecolor=BLUE, facecolor=PALE_BLUE)); ax.text(.50, .68, "Wald P = 2.60 × 10−6\nF = 40.83", ha="center", va="center", fontsize=7.5, fontweight="bold")
    ax.add_patch(FancyBboxPatch((.08, .26), .84, .20, boxstyle="round,pad=.01,rounding_size=.012", edgecolor=RED, facecolor="#F3D9DC")); ax.text(.50, .36, "Steiger = FALSE\nP = 6.62 × 10−7; no replication", ha="center", va="center", fontsize=6.6, fontweight="bold")
    ax.text(.50, .10, "Directional support not established", ha="center", fontsize=6.3, color="#4B5563"); panel(ax, "c")
    fig.suptitle("The only corrected MR direction did not pass instrument-level orientation checks", x=.02, ha="left", fontsize=9.5, fontweight="bold")
    fig.tight_layout(rect=(0, 0, 1, .92)); save(fig, "Figure4_CRAE_CKD_directionality_audit")


def supp_s1():
    df = pd.read_csv(ROOT / "results/ldsc/phase1A_rg_heatmap_plotting.tsv", sep="\t")
    retinal, systemic = list(dict.fromkeys(df.retinal_trait)), list(dict.fromkeys(df.systemic_disease))
    mat = df.pivot(index="retinal_trait", columns="systemic_disease", values="rg").reindex(index=retinal, columns=systemic)
    pmat = df.pivot(index="retinal_trait", columns="systemic_disease", values="p").reindex(index=retinal, columns=systemic)
    short_r = {r: r.replace("ret_", "").replace("_left", "").replace("_", " ") for r in retinal}
    short_s = {s: s.replace("sys_", "").replace("_", " ") for s in systemic}
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    sns.heatmap(mat, ax=ax, cmap="vlag", center=0, vmin=-.3, vmax=.3, linewidths=.35, linecolor="white", cbar_kws={"label": "Global genetic correlation (r_g)", "shrink": .75})
    ax.set_xticklabels([short_s[x] for x in systemic], rotation=45, ha="right", rotation_mode="anchor")
    ax.set_yticklabels([short_r[x] for x in retinal], rotation=0, rotation_mode="anchor"); ax.set_xlabel("Systemic disease"); ax.set_ylabel("Retinal trait")
    ax.set_title("Supplementary Figure 1. Global LDSC heatmap", loc="left", fontweight="bold", pad=12)
    ax.text(0, 1.02, "Nominal cells are outlined; none survived the complete 112-pair FDR family.", transform=ax.transAxes, fontsize=7, color="#4B5563")
    for i, r in enumerate(retinal):
        for j, s in enumerate(systemic):
            if float(pmat.loc[r, s]) < .05: ax.add_patch(Rectangle((j, i), 1, 1, fill=False, edgecolor="#333333", linewidth=.7))
    fig.tight_layout(); save(fig, "FigureS1_global_rg", SUP)


def supp_s2():
    mr = pd.read_csv(ROOT / "results/phase2/MR_DIRECTIONAL_MASTER.tsv", sep="\t")
    mr["q"] = pd.to_numeric(mr["q_global_directional"], errors="coerce")
    q = mr.groupby(["retinal_trait", "systemic_disease"], as_index=False)["q"].min()
    q["score"] = -np.log10(q["q"].clip(lower=1e-300))
    r, s = list(dict.fromkeys(q.retinal_trait)), list(dict.fromkeys(q.systemic_disease))
    mat = q.pivot(index="retinal_trait", columns="systemic_disease", values="score").reindex(index=r, columns=s)
    status = mr.assign(status=mr["evidence_status"].fillna("NULL")).groupby(["retinal_trait", "systemic_disease"])["status"].agg(lambda x: ";".join(sorted(set(x))))
    annot = mat.copy().astype(object)
    for rr in r:
        for ss in s: annot.loc[rr, ss] = status.get((rr, ss), "NULL").replace(";", "/")
    short_r = {x: x.replace("ret_", "").replace("_left", "").replace("_", " ") for x in r}
    short_s = {x: x.replace("sys_", "").replace("_", " ") for x in s}
    fig, ax = plt.subplots(figsize=(8.0, 5.1))
    sns.heatmap(mat, ax=ax, cmap="mako", linewidths=.35, linecolor="white", cbar_kws={"label": "−log10(minimum directional q)", "shrink": .75}, annot=annot, fmt="", annot_kws={"fontsize": 5.0})
    ax.set_xticklabels([short_s[x] for x in s], rotation=45, ha="right", rotation_mode="anchor"); ax.set_yticklabels([short_r[x] for x in r], rotation=0, rotation_mode="anchor")
    ax.set_xlabel("Systemic disease"); ax.set_ylabel("Retinal trait"); ax.set_title("Supplementary Figure 2. Bidirectional MR status atlas", loc="left", fontweight="bold", pad=12)
    ax.text(0, 1.02, "Cell labels show the status observed in the two directions; one pair-level family result was FDR-positive.", transform=ax.transAxes, fontsize=6.8, color="#4B5563")
    fig.tight_layout(); save(fig, "FigureS2_MR_atlas", SUP)


def supp_s3():
    b = pd.read_csv(ROOT / "results/phase1b_audit/LAVA_BOUNDARY_AUDIT.tsv", sep="\t")
    metrics = {r.metric: int(r.count) for r in b.itertuples()}
    labels = ["Native CIs touch\n|rho|=1", "Raw |rho|>1", "Raw |rho|>1.25", "Native FDR rows", "Boundary-sensitive\nFDR rows"]
    vals = [metrics["native_ci_touches_boundary"], metrics["raw_out_of_bounds_abs_rho_gt_1"], metrics["raw_out_of_param_lim_abs_rho_gt_1_25"], 9, 8]
    fig, ax = plt.subplots(figsize=(7.2, 3.8)); bars = ax.bar(labels, vals, color=[PURPLE, "#9B7DBA", "#C7B4D6", ORANGE, RED], width=.6)
    ax.set_ylabel("Rows (native LAVA universe = 26,639)"); ax.set_title("Supplementary Figure 3. Native LAVA boundary diagnostics", loc="left", fontweight="bold")
    ax.set_ylim(0, 18500)
    for bar, val in zip(bars, vals): ax.text(bar.get_x()+bar.get_width()/2, val+350, f"{val:,}", ha="center", fontsize=7, fontweight="bold")
    ax.text(.99, .98, "Boundary-touching CIs: 63.6% of rows", transform=ax.transAxes, ha="right", va="top", fontsize=7, color="#4B5563")
    fig.tight_layout(); save(fig, "FigureS3_LAVA_boundary", SUP)


if __name__ == "__main__":
    fig1_framework(); fig2_integrated(); fig3_local(); fig4_crae(); supp_s1(); supp_s2(); supp_s3()
    print("HMG figures written to", OUT)
