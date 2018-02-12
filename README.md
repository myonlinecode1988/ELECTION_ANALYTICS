# Arnab Sarkar's implementation of [Insight 2018 challenge](https://github.com/InsightDataScience/donation-analytics)

## Contents

1. [Introduction](README.md#introduction)
2. [Run instructions](README.md#run-instructions)
3. [Testing](README.md#testing)
4. [Algorithm and Data Structure](README.md#algorithm-and-data-structure)
5. [Assumptions and Comments](README.md#assumptions-and-comments)


### Introduction
The aim of the project is to process a stream data of campaign contributions,
identify repeat donors and report total dollars received, the total number of
contributions received and donation amount in a given percentile.

Big data processing requires close attention to runtime and how data is stored
and processed and although a naive implementation of
[**percentile**](https://en.wikipedia.org/wiki/Percentile) is fairly easy to
implement; a special algorithm (which uses two Heap Queues) was developed for
calculating fast percentiles and is the main highlight of my implementation.

The program can process a 1.2G `itcont.txt` file in about 2.5 min on an Intel(R)
Core(TM)2 Duo CPU E8135 (year:2009) processor.

### Run instructions
Download the application from github. You can run the application in the root
folder by:
```
$ chmod +x run.sh
$ ./run.sh
```
If you want to run your own input data set you can do so by editing `run.sh` as
show below:
```
#!/bin/bash
#
python ./src/donation-analytics.py ./<your-path>/itcont.txt ./<your-path>/percentile.txt ./output/repeat_donors.txt
```
### Testing
We have included a 4 new tests highlighting accuracy and speed of our code and algorithm.
```
    $ cd insight_testsuite/
    insight_testsuite~$ chmod +x run_tests.sh
    insight_testsuite~$ ./run_tests.sh
```
The output should look similar to this:
````
[PASS]: test_1 repeat_donors.txt
[PASS]: test_2 repeat_donors.txt
[PASS]: test_3 repeat_donors.txt
[PASS]: test_4 repeat_donors.txt
[Mon Feb 12 11:04:19 EST 2018] 4 of 4 tests passed
[UNIT TEST#1: Comparing Speed & Accuracy: Naive-Nearest-Rank-Percentile-Method vs. Dual-Heap-Nearest-Rank-Percentile-Method Implementations for 10 Random Seeds]
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.47 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.45 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.2 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.13 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.08 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.21 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.1 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.05 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.12 times faster than naive implementation
SUCESS:Percentile Match. Dual-Heap-Percentile implementation is 3.19 times faster than naive implementation
````

### Algorithm and Data Structure

                         Read rows, check input data sanity
                                        |
                    Use  (NAME, ZIP_CODE) as a key in Hashtable
                        to store DONOR info (YEAR, COUNT)
                                        |
                    Reset repeat donor to current donor entry
                        if out-of-order calendar year appears
                                        |
                    if (NAME,ZIP_CODE) is present we identify
                        repeat donors and have a new Hash
                        Table with (CMTE_ID,ZIP_CODE) as
                        key to store relevant information.
                        We also create a Percentile Object
                        that stores the data and returns the
                        percentile value. The Percentile
                        object gets updated everytime the key
                                    is accessed.
                                        |
                    The output is written in repeat_donors.txt

####  Percentile Object
We create two heaps `MinHeap` and `MaxHeap`. Let's say we are evaluating for 30
percentile.  `MaxHeap` would contain elements smaller than or equal to 30
percentile value.  `MinHeap` would contain all the elements greater than 30
percentile value.  Now we insert values according to the size of the heap for
that iteration.

It takes good advantage of ordered data required for percentile calculation and
the fact that heap has O(1) complexity to `find-min` operation and O(log n)
complexity for `insert` operation. `Heapq` module in python is an implementation
of `MinHeap`. To implement `MaxHeap` I made the value of keys negative.

## Assumptions and Comments
The code was tested in `Python 2.7.10`. Although I haven't tested it, I expect
that the code should work with `Python 2.7.x`.  The code has not been tested
for `Python 3`.

I have used calendar years instead of dates in the entire program.
All output donation values have been rounded to `int`.

The nearest-rank-method is NOT defined for P=0. Please use P between (0,100] 


