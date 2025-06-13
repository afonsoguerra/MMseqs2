# 1. Create database
mmseqs createdb dataset_peptide_annotation_table.fasta DB

# 2. Cluster
mmseqs cluster DB clusterDB tmp --min-aln-len 30 --cluster-mode 1 --cov-mode 5 --min-seq-id 0.8 -v 3

# 3. Create TSV
mmseqs createtsv DB DB clusterDB clusters.tsv

# 4. Parse with script
python parse_mmseqs2_clusters.py clusters.tsv numbered_clusters.txt
