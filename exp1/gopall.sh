#!/bin/bash

for i in *.hevc
do
	./gop.sh $i
done
 wc -L *.txt
