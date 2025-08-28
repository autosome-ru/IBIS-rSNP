# Allele-specificity benchmaring of IBIS PWM and AAA submissions

Benchmarks **PWM** and **AAA** models on regulatory SNPs from allele-specific binding (ChIP-seq, GHT-SELEX).


## 1) Executables

* **Scripts** (`scripts/`)

  * `01_get_pwms.py` — convert submitted PFMs to PWMs
  * `02_generate_uniform_thrs.sh` — create PERFECTOS-APE thresholds
  * `03_extract_asb.py` — (optional) rebuild ASB SNP tables
  * `04_make_filelist_for_annotation.py` — generate a file with all SNP–PWM–THR combinations used by `05_run_annotation.sh`
  * `05_run_annotation.sh` — run of annotation
  * additional files
      * `ape.jar` — PERFECTOS-APE tool
      * `_run_perfectos.sh` — run multiple annotation processes in parallel
      * `_annotate_with_motifs.py` — annotation of a single SNP-PWM-THR combination


* **Notebooks** (`notebooks/`)

  * `01_pwm_calculate_auc.ipynb` — compute PWM AUCs
  * `02_aaa_calculate_auc_and_join_pwms.ipynb` — compute AAA AUCs and merge with PWM
  * `03_draw_curves_examples.ipynb` — plot concordance curves and selected figures

**Execution order:**

1. run all **scripts** (01 -> 05)
2. run all **notebooks** (01 -> 03) 


## 2) Data

* `pwm_submissions/` — raw PWM submissions
* `aaa_submissions/` — raw AAA predictions
* `mex4/` — top-4 reference PWMs (MEX set)
* `finals.tsv` — IBIS Final TFs
* `asb/` — pre-filtered allele-specific SNPs
* `pwms/` — converted PWMs (log-odds)
* `thrs/` — uniform thresholds (used for motif P-Value calculation)


## 3) Results and figures

* `tables/pwm_auc.tsv` — PWM AUC scores
* `ibis_auc_scores.tsv` — combined PWM + AAA scores
* `figures/` — plots and curve data:

  * `auc_box.png` — AUC boxplot
  * `aaa_auc_weighed_mean_strip.png` — weighted mean AUC strip plot (AAA)
  * `curves_plots/A2G.*`, `curves_plots/G2A.*` — summary concordance curves (PDF/PNG/SVG)
  * `curves_plots/curves/…` — per-TF concordance curve TSVs for TFs: GCM1 (A2G) and MYF6 (G2A), across selected teams/models

