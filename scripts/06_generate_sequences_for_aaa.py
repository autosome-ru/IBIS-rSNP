import shlex
import subprocess
import io
from glob import glob
from sys import argv
import pandas as pd
import numpy as np
from tqdm.auto import tqdm

INPUT_DIR = '/home/vladimirnoz/ibis/asb'
OUTPUT_DIR = '/home/vladimirnoz/ibis/fasta'
GENOME_PATH = '/sandbox/buyanchik/genome/GRCh38.primary_assembly.genome.fa'
FINAL_TFS_LIST = '/home/vladimirnoz/ibis/table.tsv'
SEQ_HALF_SIZE = 151 #output length will be 301

def get_name(row):
    return f"{row['#chr']}@{row['end']}@{row['ref']}@{row['alt']}"

def tf_to_bed(df_init, half_length):
    df = df_init.copy()
    df['start'] = df['end'] - half_length
    df['end'] = df['end'] + half_length - 1
    df['name'] = df_init.apply(get_name, axis=1)
    return df[['#chr', 'start', 'end', 'name']]


def iterate_fasta(string):
    for line in string.split('\n'):
        if line.startswith('>'):
            name = line.strip()[1:]
        else:
            seq = line.strip()
            yield name, seq
   
finals = set(pd.read_table(FINAL_TFS_LIST)['transcription factor'])
print(finals)
asb_files = glob(f'{INPUT_DIR}/*.tsv')
for asb in tqdm(asb_files):
    name = asb.split('/')[-1][:-4].replace('selex', 'ghtselex')
    tf = name.split('@')[-1]
    if tf not in finals:
        continue
    output = f'{OUTPUT_DIR}/{name}.fasta'
    table = pd.read_table(asb)
    table['name'] = table.apply(get_name, axis=1)
    bed = tf_to_bed(table, SEQ_HALF_SIZE)
    bed_file = bed.to_csv(index=False, sep='\t', header=False)
    bedtools_command = shlex.split(f'bedtools getfasta -fi {GENOME_PATH} -bed stdin -name')
    fasta = subprocess.run(bedtools_command, input=bed_file, text=True, capture_output=True).stdout
    result = ''
    with open(output, 'w') as outfile:
        for (name, seq), (index, row) in zip(iterate_fasta(fasta), table.iterrows()):
            pos = SEQ_HALF_SIZE-1
            ref_seq = f">{name}@ref\n{seq[:pos]}{row['ref']}{seq[pos+1:]}"
            alt_seq = f">{name}@alt\n{seq[:pos]}{row['alt']}{seq[pos+1:]}"
            print(ref_seq, file=outfile)
            print(alt_seq, file=outfile)
