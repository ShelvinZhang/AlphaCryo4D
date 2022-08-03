#!/bin/bash
th=9
dir=./clustered_stars
starfile=`ls -d $dir/u*b*c*star | head -n 1`
imgName=`grep '^_rlnImageName' $starfile | awk '{print substr($2,2)}'`

awk 'BEGIN {i=0} {if ($1!~"data_particles" && i==0) {print $0} else if ($1~"data_particles") {print $0; i=1; } else { if (NF<3) {print $0; if ($1~"_rln") i++; } else {exit} } }' $starfile > $dir/pre_vote.star
cp $dir/pre_vote.star $dir/post_vote.star

grep -h mrcs $dir/u*b*c*star | awk '{print $'$imgName'}' | sort | uniq -c > $dir/pre_vote.log
grep -h mrcs $dir/u*b*c*star | sort -u -k $imgName,$imgName >> $dir/pre_vote.star
awk '{if ($1>='$th') {print $2}}' $dir/pre_vote.log > $dir/post_vote.log
grep -Ff $dir/post_vote.log $dir/pre_vote.star >> $dir/post_vote.star

echo "Particle number before voting:" `grep mrcs $dir/pre_vote.star|wc -l`
echo "Particle number after voting:" `grep mrcs $dir/post_vote.star|wc -l`
