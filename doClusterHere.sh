
#peptides seem to be 62AA?
# --cluster-reassign
/usr/bin/time mmseqs easy-cluster --cluster-mode 1 --cov-mode 0 -c 0.9 --min-seq-id 0.9 -v 1 --alignment-output-mode 0 --alignment-mode 0 --cluster-reassign 1  dataset_peptide_annotation_table.fasta resultsClust tmp

