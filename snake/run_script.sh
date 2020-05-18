echo "Training: N-3 mem-1"
python3 train.py 3 1 250000 
echo "Training: N-3 mem-2"
python3 train.py 3 2 250000 
echo "Training: N-3 mem-3"
python3 train.py 3 3 250000 

echo "Training: N-5 mem-1"
python3 train.py 5 1 250000
echo "Training: N-5 mem-2"
python3 train.py 5 2 250000
echo "Training: N-5 mem-3"
python3 train.py 5 3 250000

echo "Training: N-7 mem-1"
python3 train.py 7 1 500000
echo "Training: N-7 mem-2"
python3 train.py 7 2 500000
echo "Training: N-7 mem-3"
python3 train.py 7 3 500000

