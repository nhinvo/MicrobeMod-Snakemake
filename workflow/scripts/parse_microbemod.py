import pandas as pd 
from pathlib import Path 

# import paths from snakemake rule 
motif_paths = snakemake.input[0]  # list of path to motifs.tsv files
samples_fpath = snakemake.config['input']['sample table']
output = snakemake.output[0]  # path to output final .tsv file 

def main():
    # import sample table and metadata 
    samples_df = pd.read_table(samples_fpath)

    dfs = []  # list to store motifs.tsv from all samples 
    for fpath in motif_paths:
        fpath = Path(fpath)
        df = pd.read_table(fpath)
        fname = fpath.stem.replace('_motifs', '')
        df['sample'] = fname
        dfs.append(df)

    df = pd.concat(dfs)
    df = pd.merge(samples_df, df, on='sample', how='inner')


main()