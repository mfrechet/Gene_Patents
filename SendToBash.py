from subprocess import Popen
import shlex, sys, os

#os.setuid(30114)

args = shlex.split('/m/canvas1/mfrechet/ncbi-blast-2.2.25+/bin/makeblastdb -title BlastRefDatabase -in blastDirectory.rna.fna -dbtype "nucl" -out BlastRefDatabase -parse_seqids -hash_index')
Popen(args)

args = shlex.split('/m/canvas1/mfrechet/ncbi-blast-2.2.25+/bin/blast -p blastn -i Sequences/sequence_3719500_through_3720000.txt -d BlastRefDatabase -B 1 -N T -a 6 -L -F T -e 1e-0 >BlastOutput.txt 2>BlastErrorFile.txt')
Popen(args)
