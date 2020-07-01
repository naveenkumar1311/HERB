#!/bin/bash


# testcases=('newtestcases/Testcase1_tasks100.txt' 'newtestcases/Testcase1_tasks500.txt' 'newtestcases/Testcase1_tasks1000.txt')



testcases=('newtestcases/Testcase1_tasks100.txt' 'newtestcases/Testcase1_tasks500.txt' 'newtestcases/Testcase1_tasks1000.txt' 'newtestcases/Testcase2A_tasks100.txt' 'newtestcases/Testcase2A_tasks500.txt' 'newtestcases/Testcase2A_tasks1000.txt' 'newtestcases/Testcase2B_tasks100.txt' 'newtestcases/Testcase2B_tasks500.txt' 'newtestcases/Testcase2B_tasks1000.txt' 'newtestcases/Testcase3A_tasks100.txt' 'newtestcases/Testcase3A_tasks500.txt' 'newtestcases/Testcase3A_tasks1000.txt' 'newtestcases/Testcase3B_tasks100.txt' 'newtestcases/Testcase3B_tasks500.txt' 'newtestcases/Testcase3B_tasks1000.txt' 'newtestcases/Testcase4_tasks100.txt' 'newtestcases/Testcase4_tasks500.txt' 'newtestcases/Testcase4_tasks1000.txt' )


GTBsize=(50 75 100)
# GTBsize=(100)
LTBsize=(2 10 20 30 40 50 60 70)

# LTBsize=(2)



H=(1 2 3)
M=(1 2)
L=(1)

for t in ${testcases[@]}; do
    for gt in ${GTBsize[@]}; do
        for lt in ${LTBsize[@]}; do
            for h in ${H[@]}; do
                for m in ${M[@]}; do
                    for l in ${L[@]}; do
                        # echo $t
                        # echo $gt
                        # echo $lt
                        # echo $h
                        # echo $m
                        # echo $l
                        python DAC_add.py $t $gt $lt $h $m $l 
                        python DAC_stat.py $t $gt $lt $h $m $l  
                        python DAC_multi.py $t $gt $lt $h $m $l  
                    done
                done
            done
        done
    done     
done

## FOR PLOTTING CHANGE IN WINDOW LENGTH


# python DAC_add.py 'newtestcases/Testcase2A_tasks1000.txt' 75 50 3 2 1 
# python DAC_stat.py 'newtestcases/Testcase2A_tasks1000.txt' 75 50 3 2 1   
# python DAC_multi.py 'newtestcases/Testcase2A_tasks1000.txt' 75 50 3 2 1 

# python DAC_add.py 'newtestcases/Testcase3A_tasks1000.txt' 75 50 3 2 1 
# python DAC_stat.py 'newtestcases/Testcase3A_tasks1000.txt' 75 50 3 2 1   
# python DAC_multi.py 'newtestcases/Testcase3A_tasks1000.txt' 75 50 3 2 1 


# python DAC_add.py 'newtestcases/Testcase1_tasks1000.txt' 75 50 3 2 1 
# python DAC_stat.py 'newtestcases/Testcase1_tasks1000.txt' 75 50 3 2 1   
# python DAC_multi.py 'newtestcases/Testcase1_tasks1000.txt' 75 50 3 2 1 

# python DAC_add.py 'newtestcases/Testcase2B_tasks1000.txt' 75 50 3 2 1 
# python DAC_stat.py 'newtestcases/Testcase2B_tasks1000.txt' 75 50 3 2 1   
# python DAC_multi.py 'newtestcases/Testcase2B_tasks1000.txt' 75 50 3 2 1 


