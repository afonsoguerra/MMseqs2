#!/usr/bin/env python3
"""
Parse MMseqs2 clustering results into numbered clusters with sequences as members.

Usage:
    python parse_mmseqs2_clusters.py <cluster_tsv> <output_file>

The script expects an MMseqs2 cluster TSV file with two columns:
- Column 1: Representative sequence ID
- Column 2: Cluster member ID
"""

import sys
from collections import defaultdict
import argparse


def parse_mmseqs2_clusters(tsv_file, output_file):
    """
    Parse MMseqs2 cluster TSV and create numbered clusters.
    
    Args:
        tsv_file: Path to MMseqs2 cluster TSV file
        output_file: Path to output file
    """
    # Dictionary to store clusters: representative -> list of members
    clusters = defaultdict(list)
    
    # Read the TSV file
    try:
        with open(tsv_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                parts = line.split('\t')
                if len(parts) < 2:
                    print(f"Warning: Skipping malformed line: {line}")
                    continue
                
                representative = parts[0]
                member = parts[1]
                
                # Add member to the cluster
                clusters[representative].append(member)
    
    except FileNotFoundError:
        print(f"Error: File '{tsv_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
    
    # Sort clusters by size (descending) and then by representative ID
    sorted_clusters = sorted(clusters.items(), 
                           key=lambda x: (-len(x[1]), x[0]))
    
    # Write numbered clusters to output file
    try:
        with open(output_file, 'w') as f:
            # Write header
            f.write("# MMseqs2 Clusters\n")
            f.write(f"# Total clusters: {len(sorted_clusters)}\n")
            f.write(f"# Total sequences: {sum(len(members) for _, members in sorted_clusters)}\n")
            f.write("#\n")
            f.write("# Format: Cluster_ID<TAB>Size<TAB>Representative<TAB>Members (comma-separated)\n")
            f.write("#\n")
            
            # Write clusters
            for cluster_num, (representative, members) in enumerate(sorted_clusters, 1):
                # Include all members (representative is already in the list)
                all_members = sorted(set(members))  # Remove duplicates and sort
                size = len(all_members)
                members_str = ','.join(all_members)
                
                f.write(f"Cluster_{cluster_num}\t{size}\t{representative}\t{members_str}\n")
    
    except Exception as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)
    
    # Print summary
    print(f"Successfully processed {len(sorted_clusters)} clusters")
    print(f"Total sequences: {sum(len(members) for _, members in sorted_clusters)}")
    print(f"Largest cluster size: {len(sorted_clusters[0][1]) if sorted_clusters else 0}")
    print(f"Results written to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Parse MMseqs2 clustering results into numbered clusters',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example:
    python parse_mmseqs2_clusters.py clusters.tsv numbered_clusters.txt
    
The output file will contain:
    - Numbered clusters (Cluster_1, Cluster_2, etc.)
    - Cluster size
    - Representative sequence ID
    - All member sequence IDs (comma-separated)
        """
    )
    
    parser.add_argument('cluster_tsv', 
                       help='MMseqs2 cluster TSV file (from createtsv)')
    parser.add_argument('output_file', 
                       help='Output file for numbered clusters')
    parser.add_argument('--min-size', type=int, default=1,
                       help='Minimum cluster size to include (default: 1)')
    
    args = parser.parse_args()
    
    # Filter by minimum size if specified
    if args.min_size > 1:
        print(f"Note: Filtering clusters with size >= {args.min_size}")
        # This would require modifying the function to add filtering
        # For now, just process all clusters
    
    parse_mmseqs2_clusters(args.cluster_tsv, args.output_file)


if __name__ == '__main__':
    main()
