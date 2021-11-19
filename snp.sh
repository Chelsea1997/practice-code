#!/bin/bash
a=""
b=""
r=""
o=""
f=""
e=0
z=0
i=0
h=""
while getopts "a:b:r:f:eo:zvih" opt
do
	case $opt in
	        a)reads1=$OPTARG;;
                b)reads2=$OPTARG;;
                r)ref=$OPTARG;;
                e)realign=1;;
                o)output=$OPTARG;;
                f)millsFile=$OPTARG;;
                z)gunzip=1;;
                i)index=1;;
                v)v=1;;
                h)echo "edit";;
        esac
done
### check  required files,whether they are on your system
if [[ "$v" == 1 ]];
then
	echo "********Files are present in system**********"
fi
	if [[ ! -f "$reads1" ]];
	then
		echo "Reads1 does not exist"
	fi
if [[ ! -f "$reads2" ]];
then
	echo "Reads2 does not exist"
fi
if [[ ! -f "$ref" ]];
then
	echo "Reference file does not exist"
fi
if [[ ! -f "$millsFile" ]];
then
	echo "Millsfile does not exist"
fi
# check output file"
if [[ -f "$output" ]];
then
	echo " The output file aready exists. Do you want to rewrite"
	read -r answer
	if [[ $answer == 'y' ]];
	then
		exit 1
	fi
fi
## map the files
if [[ "$v" == 1 ]]
then
	echo "****The two files are being mapped to reference file****"
fi
#index refernece file
bwa index "$ref"
# File mapping is done by the following command   
bwa mem -R '@RG\tID:foo\tSM:bar\tLB:library1\tPL:ILLUMINA' "$ref" "$reads1" "$reads2" > lane.sam
#lane.sam is the output same file
# conversion of sam file to bam file
samtools fixmate -O bam lane.sam lane_fixmate.bam
# sort bam file	
samtools sort -O bam -o lane_sorted.bam lane_fixmate.bam
#creation of dictionary file of reference genome
samtools faidx "$ref"
samtools dict "$ref" -o chr17.dict	
samtools index lane_sorted.bam
##Improvement of lane_sorted.bam file
if [[ "$v" == '1' ]]
then
	echo "****Mapped file improvement in progress****"
fi
## These steps to reduce number of miscalls of INDELS
java -Xmx2g -jar GenomeAnalysisTK.jar -T RealignerTargetCreator -R "$ref" -I lane_sorted.bam -o lane.intervals --known "$millsFile"
java -Xmx4g -jar GenomeAnalysisTK.jar -T IndelRealigner -R "$ref" -I lane_sorted.bam -targetIntervals lane.intervals -known "$millsFile" -o lane_realigned.bam
#index lane_realigned.bam
samtools index lane_realigned.bam
## call of variant function
if [[ "$v" == '1' ]]
then
	echo "** we are on final step of variant function**"
fi
bcftools mpileup -Ou -f "$ref" lane_sorted.bam | bcftools call -vmO z -o "$output".vcf.gz
## gunzip the vcf file obtained
gunzip "$output".vcf.gz 
## conversion of file format
if [[ "$v" == '1' ]]
then
	echo "Conversion of vcf to bed format"
fi
# Removal of ## lines at beginning of file
cat output.vcf | grep -P "INDEL" > noi.vcf
#conversion to bed file
vcf2bed < noi.vcf > noi.bed
## getting the desired columns snip.txt file
cat noi.bed | awk '{print $1,$2,$3, length($7)-length($6) }' > snip1.txt
# creation of indel.txt
cat noi.bed | awk '{print $1,$2,$3, length($6)-length($7) }' > indel1.txt
# deletion of chr word
cat snip1.txt | sed 's/chr//' > snip.txt
cat indel1.txt | sed 's/chr//' > indel.txt
sed 's/^/chr,start,stop,length/' snip.txt > snip.txt
sed 's/^/chr,start,stop,length/' indel.txt > indel.txt

