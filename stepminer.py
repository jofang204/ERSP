import sys

def mean(arr):
	mean = 0.0
	sum = 0.0
	for s in arr:
		sum += s
	return sum/len(arr)

def variance(arr):
	sq = 0.0
	m = mean(arr)
	for s in arr:
		sq += (s-m) * (s-m)
	return sq/len(arr)

def stdev(arr):
	return variance(arr) ** 0.5

def mse(arr):
	var = variance(arr)
	return var * len(arr)

def main():
	inputarr = [float(s) for s in open(sys.argv[1]).readline().split(",")]
	print "input is: " + ', '.join([str(s) for s in inputarr])
	print "mean is: " + str(mean(inputarr))
	print "variance is "+ str(variance(inputarr))
	print "mse is "+ str(mse(inputarr))
	print "standard deviation is " + str(stdev(inputarr))

if __name__ == "__main__":
	main()

