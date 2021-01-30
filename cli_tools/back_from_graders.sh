part1="$(dirname "$1")"  
part2="$(basename "$1")"

echo "Flatten"
python do/stage003/flatten.py $1 submissions/0310_flatten/$part2;

echo "Burst"
python do/stage003/burst.py submissions/0310_flatten/$part2 submissions/0320_burst/$part2;

echo "Compress"
python do/stage003/compress.py submissions/0320_burst/$part2 submissions/0330_compress/$part2;

echo "Write marks"
python do/stage003/write_marks.py submissions/0330_compress/$part2 submissions/0340_write_marks/$part2;

echo "Make check files"
python do/stage003/make_check_files.py submissions/0340_write_marks/$part2 submissions/0400_check_files 