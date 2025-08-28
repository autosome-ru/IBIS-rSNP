import pandas as pd
import os

def filter_asb(asb, tag):
    tfs = set(asb["TF"])
    columns = [
        '#chr', 'start', 'end', 'mean_bad', 'id', 'max_cover', 'ref', 'alt',
        'n_reps', 'bads', 'scorefiles', 'ref_counts', 'alt_counts', 'ref_es',
        'alt_es', 'ref_pval', 'alt_pval', 'ref_comb_es', 'alt_comb_es',
        'ref_comb_pval', 'alt_comb_pval', 'ref_fdr_comb_pval',
        'alt_fdr_comb_pval', 'pref_allele', 'comb_es', 'comb_pval',
        'fdr_comb_pval'
    ]
    for tf in tfs:
        path = f'asb/{tag}@{tf}.tsv'
        mask = asb[['ref_motif_pval', 'alt_motif_pval']].min(axis=1) < 2.0
        mask = mask * (asb['TF'] == tf)
        table = asb[mask][columns].copy()
        if len(table) > 0:
            table.to_csv(path, index=False, sep='\t')


chipseq = pd.read_table('/home/vladimirnoz/Projects/Codebook_Perspectives/AS_CHS_GHTS/build/chipseq.tsv')
filter_asb(chipseq, 'chipseq')

selex = pd.read_table('/home/vladimirnoz/Projects/Codebook_Perspectives/AS_CHS_GHTS/build/selex.tsv')
filter_asb(selex, 'selex')
