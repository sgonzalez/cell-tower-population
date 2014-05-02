#!/bin/bash


# prompt for data file name
echo "LOAD TSV CELL TOWER DATA FILES INTO TESSELATION PROGRAM"
echo ""
echo "Name of TSV file with cell tower data: "
read filename

theline=$(sed -n '/\/\/\/\/ END POINT \/\/\/\//=' tesselation2.html)

# load data into array
while IFS=$'\t' read -r -a myArray
do
  echo "        			new jsts.geom.Coordinate(${myArray[1]}, ${myArray[2]}),"
   
 # awk -v insert=giraffe -v before="cat" '
 #   $1 == before && ! inserted {
 #     print insert
 #     inserted++
 #   }
 #   {print}
 # ' BestAnimals.txt > NewBestAnimals.txt
done < ANT_POS.TSV #$(echo $filename)

