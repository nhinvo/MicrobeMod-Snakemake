import pandas as pd 
from pathlib import Path 

def main():
    # convert to list of path if input is string (1 file)
    if isinstance(snakemake.input[0], str):  
        motif_paths = [snakemake.input[0]]  
    else:
        motif_paths = snakemake.input[0]

    # import sample table and metadata 
    samples_df = pd.read_table(snakemake.config['input']['sample table'])

    dfs = []  # list to store motifs.tsv from all samples 
    for fpath in motif_paths:
        fpath = Path(fpath)
        df = pd.read_table(fpath)
        fname = fpath.stem.replace('_motifs', '')
        df['sample'] = fname
        dfs.append(df)

    df = pd.concat(dfs)
    df = pd.merge(samples_df, df, on='sample', how='inner')

    df.to_csv(snakemake.output['tsv'], sep='\t', index=False)
    df.to_excel(snakemake.output['xlsx'], index=False)


main()