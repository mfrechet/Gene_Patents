cat $1 | 
awk 'BEGIN{i=0;IGNORECASE=1}{if($0~/[^A-Z]*SEQUENCE LISTING[^A-Z]*/){i=1}if(i==1){print $0}}'|
sed '/[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn].*[ATGCNatgcn]/s/ //g'
 
exit 0
