#!/usr/bin/env python3
"""Generate the three-figure Amendment 004 HMG set from frozen outputs."""
from pathlib import Path
import sys

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures" / "amendment004"
SRC = OUT / "source_data"
SUP = ROOT / "supplement" / "amendment004"
for p in (OUT, SRC, SUP):
    p.mkdir(parents=True, exist_ok=True)

BLUE, TEAL, PURPLE, ORANGE = "#3569A8", "#278C88", "#7353A6", "#D9822B"
INK, MID, LIGHT, PALE = "#20252B", "#59636E", "#D6DCE2", "#F5F7F9"
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 7, "axes.titlesize": 8, "axes.labelsize": 7, "xtick.labelsize": 6,
    "ytick.labelsize": 6, "axes.linewidth": 0.8, "axes.spines.top": False,
    "axes.spines.right": False, "legend.frameon": False, "pdf.fonttype": 42, "svg.fonttype": "none",
})


def save(fig, stem, out=OUT):
    opts = dict(bbox_inches="tight", pad_inches=0.04, facecolor="white")
    fig.savefig(out / f"{stem}.svg", **opts)
    fig.savefig(out / f"{stem}.pdf", **opts)
    fig.savefig(out / f"{stem}.tiff", dpi=600, pil_kwargs={"compression": "tiff_lzw"}, **opts)
    fig.savefig(out / f"{stem}.png", dpi=300, **opts)
    plt.close(fig)


def figure1():
    fig, ax = plt.subplots(figsize=(7.09, 4.15))
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    ax.text(0.18, 0.91, "Retinal phenotypes", ha="center", weight="bold", fontsize=9)
    for x, label in zip([0.07, 0.18, 0.29], ["Neuroretina", "Outer retina", "Microvasculature"]):
        ax.scatter(x, 0.82, s=25, color=BLUE)
        ax.text(x, 0.77, label, ha="center", va="top", fontsize=6.5)
    ax.text(0.82, 0.91, "Eight systemic diseases", ha="center", weight="bold", fontsize=9)
    for x, label in zip([0.69, 0.78, 0.87, 0.96], ["Cardio-\nmetabolic", "Renal", "Neuro-\ndegeneration", "Immune /\ninflammation"]):
        ax.scatter(x, 0.82, s=25, color=TEAL)
        ax.text(x, 0.77, label, ha="center", va="top", fontsize=5.8)
    ax.plot([0.30, 0.70], [0.82, 0.82], color=LIGHT)
    ax.add_patch(FancyBboxPatch((0.405, 0.745), 0.19, 0.10, boxstyle="round,pad=.01", facecolor=PALE, edgecolor="#AAB3BC"))
    ax.text(0.50, 0.795, "Genetic\nrelationships", ha="center", va="center", weight="bold", fontsize=7.2)

    layers = [
        ("A", "Genome-wide sharing", "14 retinal traits x 8 diseases\n112 LDSC pairs", BLUE),
        ("B", "Regional sharing", "Locked 47-pair subset\nHDL-L plus LAVA sensitivity", TEAL),
        ("C", "Directional evidence", "7 qualified OCT traits x 8 diseases x 2\n112 MR directions", ORANGE),
    ]
    for (letter, title, detail, color), x in zip(layers, [0.055, 0.365, 0.675]):
        ax.add_patch(Rectangle((x, 0.30), 0.27, 0.29, facecolor="white", edgecolor=LIGHT))
        ax.add_patch(Rectangle((x, 0.555), 0.27, 0.035, facecolor=color, edgecolor=color))
        ax.text(x+0.015, 0.52, letter, color=color, weight="bold", fontsize=9)
        ax.text(x+0.05, 0.52, title, weight="bold", fontsize=7.5)
        ax.text(x+0.135, 0.41, detail, ha="center", va="center", fontsize=6.6, color=MID)
    ax.text(0.81, 0.25, "Vascular traits retained in\nglobal and local analyses;\nnot evaluated by MR", ha="center", va="top", fontsize=6.6, color=MID)
    ax.text(0.50, 0.11, "MR restricted prospectively to data-integrity-qualified OCT traits", ha="center", weight="bold", fontsize=8)
    pd.DataFrame([{"layer":x[1], "universe":x[2]} for x in layers]).to_csv(SRC/"Figure1_source_data.tsv",sep="\t",index=False)
    save(fig, "Figure1_complementary_framework")


def figure2():
    tracks = [
        ("A", "Genome-wide sharing", "112 pairs", "0 FDR-significant", "No corrected broad sharing", BLUE),
        ("B", "Primary local sharing", "116,472 block tests", "0 global-local FDR", "No corrected primary local sharing", TEAL),
        ("C", "Native LAVA sensitivity", "26,639 rows", "9 FDR; 8/9 boundary-sensitive", "Procedure-sensitive local evidence", PURPLE),
        ("D", "OCT-only directional MR", "112 directions", "110 null; 2 suggestive; 0 FDR", "No robust OCT directional signal", ORANGE),
    ]
    fig, ax = plt.subplots(figsize=(7.09, 4.8))
    ax.set_xlim(0,1); ax.set_ylim(-.85,3.9); ax.axis("off")
    xs=[.31,.57,.84]
    for x,h in zip(xs,["Testing universe","Corrected result","Interpretation"]): ax.text(x,3.72,h,ha="center",weight="bold",color=MID)
    for i,(letter,label,universe,result,meaning,color) in enumerate(tracks):
        y=3.1-i
        ax.text(.02,y+.17,letter,weight="bold",color=color,fontsize=9)
        ax.text(.06,y+.17,label,weight="bold",fontsize=7.7)
        ax.plot([.25,.93],[y,y],color=LIGHT)
        for x in xs: ax.scatter(x,y,s=34,facecolor="white",edgecolor=color,linewidth=1.4)
        ax.text(xs[0],y-.18,universe,ha="center",va="top",fontsize=7)
        ax.text(xs[1],y-.18,result,ha="center",va="top",fontsize=6.8,weight="bold")
        ax.text(xs[2],y-.18,meaning,ha="center",va="top",fontsize=6.6,color=MID)
    ax.text(.02,-.66,"Seven vascular traits were not analysed by MR because release-specific frequency semantics remained unresolved.",fontsize=6.5,color=MID)
    pd.DataFrame(tracks,columns=["panel","layer","universe","corrected_result","interpretation","color"]).drop(columns="color").to_csv(SRC/"Figure2_source_data.tsv",sep="\t",index=False)
    save(fig,"Figure2_integrated_evidence")


def figure3():
    sys.path.insert(0, str(ROOT / "scripts"))
    import plot_hmg_visual_final as original
    original.OUT = OUT; original.SRC = SRC
    def clean_panel_label(ax, label, title):
        ax.text(-0.13, 1.03, label, transform=ax.transAxes, fontsize=9,
                fontweight="bold", va="bottom", ha="left", color=INK)
        ax.text(0.03, 1.03, title, transform=ax.transAxes, fontsize=7.3,
                fontweight="bold", va="bottom", ha="left", color=INK, linespacing=1.05)
    original.panel_label = clean_panel_label
    original.figure3()


def supplementary_matrix():
    master = pd.read_csv(ROOT/"results/amendment004/MR_DIRECTIONAL_MASTER_OCT_ONLY.tsv",sep="\t",keep_default_na=False)
    panel = pd.read_csv(ROOT/"config/amendment004_oct_trait_panel.tsv",sep="\t")
    exclusions = pd.read_csv(ROOT/"config/amendment004_vascular_mr_exclusions.tsv",sep="\t")
    diseases = ["CAD","Stroke","T2D","CKD","AD","PD","SLE","IBD"]
    sysids = ["sys_cad_nikpay2015","sys_stroke_megastroke2018","sys_t2d_scott2017","sys_ckd_wuttke2019","sys_ad_kunkle2019","sys_pd_nalls2019_clinical","sys_sle_bentham2015","sys_ibd_delange2017"]
    traits = panel.trait_id.tolist()+exclusions.trait_id.tolist()
    labels = [x.replace("ret_","").replace("_"," ") for x in traits]
    code=np.zeros((14,8),int)
    # 0 null, 1 suggestive, 2 supported/unresolved, 3 not analysed
    for i,t in enumerate(traits):
        for j,s in enumerate(sysids):
            if i>=7: code[i,j]=3; continue
            g=master[(master.retinal_trait==t)&(master.disease==s)]
            statuses=set(g.evidence_status)
            code[i,j]=2 if ("DIRECTIONAL_MR_SUPPORTED" in statuses or "UNRESOLVED" in statuses) else (1 if "SUGGESTIVE" in statuses else 0)
    from matplotlib.colors import ListedColormap
    fig,ax=plt.subplots(figsize=(7.09,5.5))
    ax.imshow(code,cmap=ListedColormap(["#E5E8EB","#EFCB75","#A95454","#F7F7F7"]),vmin=-.5,vmax=3.5,aspect="auto")
    for i in range(14):
        for j in range(8):
            ax.text(j,i,"NA" if code[i,j]==3 else ("S" if code[i,j]==1 else ("?" if code[i,j]==2 else "N")),ha="center",va="center",fontsize=6.5,color=MID if code[i,j] in {0,3} else INK)
    ax.axhline(6.5,color=INK,lw=.8)
    ax.set_xticks(range(8),diseases,rotation=40,ha="right",rotation_mode="anchor")
    ax.set_yticks(range(14),labels)
    ax.set_title("Final directional-evidence matrix")
    ax.text(7.45,10,"Vascular traits:\nnot analysed",ha="left",va="center",fontsize=6.5,color=MID)
    fig.tight_layout()
    save(fig,"Supplementary_Figure_S2_directional_matrix",SUP)


if __name__ == "__main__":
    figure1(); figure2(); figure3(); supplementary_matrix()
