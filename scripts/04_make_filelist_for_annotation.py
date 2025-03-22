from glob import glob
from collections import defaultdict
from os.path import basename, abspath
from itertools import product


def get_pairs(asbs_by_tfs, pwms_by_tfs):
    all_tfs = set(pwms_by_tfs.keys()).union(set(asbs_by_tfs.keys()))
    for tf in all_tfs:
        pwms = pwms_by_tfs[tf]
        asbs = asbs_by_tfs[tf]
        for p, a in product(pwms, asbs):
            yield p, a

pwms = glob('pwms/*.pwm')
asbs = glob('asb/*.tsv')
pwms_by_tfs = defaultdict(list)
for pwm in pwms:
    tf = basename(pwm).split('@')[0]
    pwms_by_tfs[tf].append(pwm)
asbs_by_tfs = defaultdict(list)
for asb in asbs:
    tf = basename(asb).split('@')[1][:-4]
    asbs_by_tfs[tf].append(asb)

arglist = open('arglist.txt', 'w')
for pwm, asb in get_pairs(asbs_by_tfs, pwms_by_tfs):
    base_pwm = pwm[5:-4]
    base_asb = asb[4:-4]
    base_out = f'{base_asb.split("@")[0]}@{base_pwm}'
    thr = f'thrs/{base_pwm}.thr'
    snp_out = f'snp_out/{base_out}.txt'
    out = f'motif_tables/{base_out}.tsv'
    row = [asb, pwm, thr, snp_out, out]
    row = [abspath(s) for s in row]
    row_str = ' '.join(row)
    print(row_str, file=arglist)
arglist.close()
