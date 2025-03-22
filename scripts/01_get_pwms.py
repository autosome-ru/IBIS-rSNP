import os
from io import StringIO
from glob import glob
import pandas as pd
import numpy as np

def convert(freq_str):
    freq = float(freq_str)
    return str(np.log2( (freq + 1e-5)  / 0.25))


file_paths = glob('/home/nikgr/ibis_validation/submissions/*/PWMS.txt')
file_paths.append('/home/ivankozin/ibis_benchmark/mex_top1_pwm/IBIS_top1_motifs.txt')
asb_finals = pd.read_table('finals.tsv')
tfs = set(asb_finals['Transcription factor'])

last = len(file_paths) - 1
for i, path in enumerate(file_paths):
    print(path)
    text = open(path).read()
    pwms = text.split('\n\n')
    team = path.split('/')[-2]
    if i == last:
        team = 'mex1'
    for pwm in pwms:
        header = pwm.split('\n')[0][1:].strip().replace(' ', '@')
        tf = header.split('@')[0]
        if tf not in tfs:
            print(tf)
            continue
        pwm_table = []
        for line in (pwm.strip().split('\n')[1:]):
            new_line = line.strip().split(' ')
            pwm_table.append(' '.join([convert(x) for x in new_line]))
        filename = 'pwms/' + header + '@' + team + '.pwm'
        if i == last:
            filename = 'pwms/' + tf + '@' + team + '@' + team + '.pwm'
        with open(filename, 'w') as pwm_file:
            print(header, file=pwm_file)
            print('\n'.join(pwm_table), file=pwm_file)
