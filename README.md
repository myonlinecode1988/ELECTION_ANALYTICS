# Arnab Sarkar's implementation of [Insight 2018 challenge](https://github.com/InsightDataScience/donation-analytics)

## Contents

1. [Introduction](README.md#introduction)
2. [Run instructions](README.md#run-instructions)
3. [Testing](README.md#testing)
4. [Algorithm and Data Structure](README.md#algorithm-and-data-structure)
5. [Code Dependencies and Comments](README.md#code-dependencies-and-comments)


### Introduction
The aim of the project is to process a stream data of campaign contributions,
identify repeat donors & report total dollars received, the total number of
contributions received & donation amount in a given percentile.

Big data processing requires close attention to runtime & how data is stored
& processed. Although a naive implementation of
[percentile](https://en.wikipedia.org/wiki/Percentile) is fairly easy to
implement; **a special algorithm for percentile (using two Heap Queues)** was
developed for calculating fast percentiles & is the main highlight of my
implementation.

The program can process a 1.2G `itcont.txt` file in about 2.5 min on an
Intel(R) Core(TM)2 Duo CPU E8135 (year:2009) processor. It uses about 450 MB of
main memory.

### Run instructions
Download the application from github. Follow these steps to run the application:
```
$ git clone https://github.com/myonlinecode1988/ELECTION_ANALYTICS
$ cd ELECTION_ANALYTICS
$ chmod +x run.sh
$ ./run.sh
```
If you want to run your own input data set; you can do so by editing `run.sh` as
show below:
```
#!/bin/bash
#
python ./src/donation-analytics.py ./<YOUR-PATH>/itcont.txt ./<YOUR-PATH>/percentile.txt ./output/repeat_donors.txt
```
### Testing
We have included a 4 new tests highlighting accuracy & speed of our code & algorithm.
To run the tests follow these steps:
```
    $ cd insight_testsuite/
    insight_testsuite~$ chmod +x run_tests.sh
    insight_testsuite~$ ./run_tests.sh
```
The output should look similar to this:

```
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
```
#### Description of tests:
- **test_1**: This is the default test provided to us.
- **test_2**: This test has been provided to evaluate correct results for CMTE_ID=C00640623 & ZIP_CODE=35043.
- **test_3**: This test has been provided to take care of out-of-order streams as explained in the FAQ section.
- **test_4**: This test has been provided to highlight how the code checks & skips malformed data.
- **UNIT TEST#1**: This a test that highlights the accuracy/performance of **Dual Heap Percentile Implementation** vs. **Naive Percentile Implementation**.


### Algorithm and Data Structure

#### Algorithm
```
                         Read rows, check input data sanity
                                        |
                    Use  (NAME, ZIP_CODE) as a key in Dictionary#1
                        and store donor info (YEAR, COUNT)
                                        |
                    Reset repeat donor info to current donor entry
                        if out-of-order calendar year appears
                                        |
                    Is (NAME,ZIP_CODE) key present in Dictionary#1 ?
                                        |
            |----------------------------------------------------------------|
	 (if no)							 (if yes)
    Create a new entry in Dictionary#1                            Update count in Dictionary#1
     (NAME,ZIP_CODE):[YEAR,count=1]                          	(NAME,ZIP_CODE):[YEAR,count+=1]
                                                                    This is a repeat donor
                                                                            |
                                                      Is  (CMTE_ID,ZIP_CODE) key present in RepeatDonorDictionary ?
                         |----------------------------------------------------------------| 
	              (if no)							       (if yes)
          Create entry in RepeatDonorDictionary with                           Update entry in RepeatDonorDictionary with
    	(CMTE_ID,ZIP_CODE):[update Percentile object,       	              (CMTE_ID,ZIP_CODE):[update Percentile object,
find new percentile and update running donation total and counts]    find new percentile and update running donation total and counts]
```
#### Data Structure
We use two dictionaries & a Percentile object which comprises of two 
[heap data strucures](https://en.wikipedia.org/wiki/Heap_(data_structure)).

##### Dictionaries
The first dictionary (referred to as `Dictionary#1` above &
`NAME_ZIP_to_YEAR_COUNT` in code) uses `(NAME,ZIP_CODE)` as key & stores
`[YEAR,count]` as its values.
 
The second dictionary (referred to as `RepeatDonorDictionary` above &
`REPEAT_DONOR_DICT` in code ) uses `(CMTE_ID,ZIP_CODE)` as key & stores
`[CMTE_ID,ZIP_CODE,TRANSACTION_DT,Percentile-Object,Percentile,Running
Count,Running Total Amount]` as its values.  Dictionary is a good data structure
to use because key search is of O(1) complexity.

#####  Percentile Object
We create two heaps `MinHeap` & `MaxHeap`. Let's say we are evaluating for 30
percentile.  `MaxHeap` would contain elements smaller than or equal to 30
percentile value.  `MinHeap` would contain all the elements greater than 30
percentile value.  Now we insert values according to the size of the heap for
that iteration.

It takes good advantage of ordered data required for percentile calculation and 
the fact that heap has O(1) complexity to `find-min-value` operation & O(log
n) complexity for `insert` operation. `Heapq` module in python is an
implementation of `MinHeap`. To implement `MaxHeap` I made the value of keys
negative.

## Code Dependencies and Comments
- The code was tested in `Python 2.7.10`. Although I haven't tested it, I
  expect that the code should work with `Python 2.7.x`.  The code has not been
tested for `Python 3`. The code should work with baseline python installation.
- The code uses the following modules: `sys`, `os.path`, `heapq` & `math`
- I have used calendar years instead of dates in the entire program.  All
  output donation values have been rounded to `int`.
- The nearest-rank-method is NOT defined for Percentile=0. Please use
  Percentile between (0,100] 
- Although the fast-percentile-algorithm was exhaustively tested with 1000s of
  random data & has been shown as part of my tests; I should have used
`unittest` module for more formal testing.
