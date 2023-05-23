#!/bin/sh
#SBATCH --ntasks 1
#SBATCH --cpus-per-task 2
#SBATCH --mem 4G
#SBATCH --time 48:00:00
#SBATCH --partition middle_idx
#SBATCH --output NC_045512.2_20230503_viralrecon_2.log
#SBATCH --chdir /scratch/bi/20230420_TFM-PABLO-RELECOV-BATCH2_pmata_T/ANALYSIS/20230503_ANALYSIS01_AMPLICONS_HUMAN

export NXF_OPTS="-Xms500M -Xmx4G"

nextflow run /data/bi/pipelines/TEST/nf-core-viralrecon-2.6.0/workflow/main.nf \
          -c ../../DOC/viralrecon_sars.config \
          -params-file ../../DOC/viralrecon_sars_params.yml \
          --input samplesheet_NC_045512.2.csv \
          --outdir NC_045512.2_20230503_viralrecon_mapping \
          --fasta /data/bi/references/virus/2019-nCoV/genome/NC_045512.2.fasta \
          --gff /data/bi/references/virus/2019-nCoV/genes/NC_045512.2.gff \
          -resume
