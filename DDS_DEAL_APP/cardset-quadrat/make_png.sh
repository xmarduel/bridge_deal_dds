for filename in *.svg; do
    rsvg-convert -h $1 $filename > ${filename%.*}.png
done
