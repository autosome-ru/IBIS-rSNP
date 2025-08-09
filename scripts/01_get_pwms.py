import os
from io import StringIO
from glob import glob
import pandas as pd
import numpy as np

def convert(freq_str):
    freq = float(freq_str)
    return str(np.log2( (freq + 1e-5)  / 0.25))


file_paths = glob('pwm_submissions/*.txt')
file_paths.append('mex4/top4_MEX_motifs_for_IBIS_fixed.txt')
asb_finals = pd.read_table('finals.tsv')
tfs = set(asb_finals['Transcription factor'])

last = len(file_paths) - 1
for i, path in enumerate(file_paths):
    print(path)
    text = open(path).read()
    pwms = text.split('\n\n')
    team = path.split('/')[-1].replace('.txt', '').replace('.', '')
    if i == last:
        team = 'mex4'
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
        with open(filename, 'w') as pwm_file:
            print(header, file=pwm_file)
            print('\n'.join(pwm_table), file=pwm_file)
