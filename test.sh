#\!/bin/sh
while read line
do
	echo "GOATS: "
	$line
done < inputs.txt > goals.txt
echo "GOATS: " >> goals.txt
python3 main.py < inputs.txt > outputs.txt
python3 test_extras.py