echo "Training: N-3 mem-0"
python3 train.py 3 0 25000 
echo "Training: N-3 mem-1"
python3 train.py 3 1 25000 
echo "Training: N-3 mem-2"
python3 train.py 3 2 25000 
echo "Training: N-3 mem-3"
python3 train.py 3 3 25000 

echo "Training: N-5 mem-0"
python3 train.py 5 0 25000
echo "Training: N-5 mem-1"
python3 train.py 5 1 25000
echo "Training: N-5 mem-2"
python3 train.py 5 2 25000
echo "Training: N-5 mem-3"
python3 train.py 5 3 25000

echo "Training: N-7 mem-0"
python3 train.py 7 0 50000
echo "Training: N-7 mem-1"
python3 train.py 7 1 50000
echo "Training: N-7 mem-2"
python3 train.py 7 2 50000
echo "Training: N-7 mem-3"
python3 train.py 7 3 50000

