rule microbemod:
    input: 
        sorted_bam = scratch_dict["read_mapping"] / "{sample}_sorted.bam",
        reference = lambda wildcards: SAMPLE_TABLE.loc[wildcards.sample, 'reference_path'], 
    output: 
        scratch_dict['microbemod_call_methylation'] / "{sample}_motifs.tsv", 
    conda: config["MicrobeMod"]["conda env name"]  
    params: 
        microbemod_path = config["MicrobeMod"]["installation path"], 
        methylation_confidence = config["MicrobeMod"]["methylation_confidence_threshold"], 
    shell:
        """
        {params.microbemod_path}/bin/MicrobeMod call_methylation \
            --methylation_confidence_threshold {params.methylation_confidence} \
            --bam_file {input.sorted_bam} \
            --reference_fasta {input.reference} \
            --threads {resources.cpus_per_task} \
            --output_prefix {wildcards.sample} \
            --output_directory $(dirname {output})
        """