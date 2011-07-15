cat $1 | 
awk 'BEGIN{i=0;IGNORECASE=1}{if($0~/^[^A-Z]*SEQUENCE LISTING[^A-Z]*$/){i=1}if(i==1){print $0}}' | 
sed '/[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn]/s/ //g' | 
grep -i '\(SEQ[^A-Z]*ID[^A-Z]*NO[^A-Z0-9][0-9][0-9]*\|[ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN]\)' | 
grep -B1 -i '[ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN][ATGCN]' | 
sed '/SEQ[^A-Z]*ID[^A-Z]*NO[^A-Z0-9][0-9][0-9]*/s/.*\(SEQ[^A-Z]*ID[^A-Z]*NO[^A-Z0-9][0-9][0-9]*\).*/\1/' | 
sed '/^SEQ/s/SEQ.[^0-9]*\([0-9][0-9]*\)/>SEQ ID NO \1/' | 
sed 's/Ala//g; s/Cys//g; s/Asp//g; s/Glu//g; s/Phe//g; s/Gly//g; s/His//g; s/Ile//g; s/Lys//g; s/Leu//g; s/Met//g; s/Asn//g; s/Pro//g; s/Gln//g; s/Arg//g; s/Ser//g; s/Thr//g; s/Val//g; s/Trp//g; s/Tyr//g;'  | 
sed '/[ATGCNatgcn][ATGCNatgcn][ATGCNatgcn][ATGCNatgcn]/s/[^A-Z]//g' | 
grep -i '\(^>\|^[ATGCN][ATGCN][ATGCN][ATGCN][ATGCN]\)' | 
tr 'a-z' 'A-Z' | 
awk '{if($1~/^>/){if(i!=0){print output;output=""};print $0;i++}else{output=output$0}}END{print output}'
exit 0
