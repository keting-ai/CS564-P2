DATA="./ebay_data"
rm categories.dat
rm items.dat
rm bids.dat
rm users.dat
for i in $(ls $DATA); do
  python3 skeleton_parser.py $DATA/$i
done
sort -u categories.dat -o categories.dat
sort -u items.dat -o items.dat
sort -u bids.dat -o bids.dat
sort -u users.dat -o users.dat
