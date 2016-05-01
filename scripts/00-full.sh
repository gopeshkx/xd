#!/bin/sh

# Usage:
#  $0 <base>
#   produces a similarity check for a bunch of raw crosswords, creating several artifacts along the way

set -e

BASE=$1
#scripts/10-download-puzzles.py -o xd-`date +"%Y%m%d"`.zip ${BASE}-latest.zip

mkdir -p ${BASE}
rm -f receipts.tsv
scripts/20-convert2xd.py -o ${BASE}-converted.zip ${BASE}.zip
scripts/25-clean-headers.py -o ${BASE}-cleaned.zip ${BASE}-converted.zip
scripts/30-shelve.py -o ${BASE} ${BASE}-cleaned.zip
scripts/40-catalog-puzzles.py -o ${BASE}/puzzles.tsv ${BASE}
scripts/50-findsimilar.py -o ${BASE}-similar.tsv ${BASE}
scripts/60-mkwww-diffs.py -o www/${BASE} ${BASE}-similar.tsv
#scripts/65-mkwww-publishers -o www/publishers/ ${BASE}-similar.tsv
#scripts/65-mkwww-index.py -o www/${BASE} ${BASE}-similar.tsv

