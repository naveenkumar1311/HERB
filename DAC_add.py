#DAC algorithm Round1 implementation using python
#Date : 6-6-2017
#last updated : 4-4-2020 
#Name : K Naveen Kumar


#*****************taking input from the file separate by comma and storing into a dictionary called inputdata
#import packages
from __future__ import division 
import sys
import math
#*********************
inputdata={} #dictionary containing the input file data where key will be the first value of the row
filename = sys.argv[1]
#filename = raw_input("Give the name of the input file : ") 
#filename = 'testcase4_tasks1000.txt'

with open(filename,'r') as input_file:
        for line in input_file:
                if not line.startswith('#'):
                        splitline=line.split(",")
                        inputdata[str(splitline[0])]=",".join(splitline[1:]) #taking ',' separated input and taking key as the first value of the row

        for key in inputdata:
                inputdata[key]=inputdata[key].rstrip()         # removing the extra '\n' in the value list
                inputdata[key]=list(inputdata[key].split(",")) # taking the input as comma separated


keyArray1=[k  for k,v in inputdata.items() if (len(v)==8 or len(v) == 9)]

total_task_buffer = keyArray1



#Additive increase sliding window
global_buffer_size = int(sys.argv[2])
initial_window_length = int(sys.argv[3])
val1 = int(sys.argv[4])
val2 = int(sys.argv[5])
val3 = int(sys.argv[6])
global_task_buffer = []
window_length = initial_window_length
time = 0
avg_turnaround_time = []
avg_waiting_time = []
percent_execution = []
completedtasks = []
totaltasks = []
gtb_global = []
wlength = []
threshold_packet_drop = window_length - 2
counttemp = 0


import random
import numpy as np

def insertionsort(list1,list2):
     for index in range(1,len(list1)):
             value1=list1[index]
             value2=list2[index]
             i = index-1
             while i >= 0:
                     if value1 < list1[i]:
                             list1[i+1] = list1[i]
                             list2[i+1] = list2[i]
                             list1[i] = value1
                             list2[i] = value2
                             i = i-1
                     elif (value1 == list1[i]): #the condition where deadlines are equal go for the priority it is used in dead line sorting
                             temp1 = int(inputdata[value2][7]) #priority value
                             temp2 = int(inputdata[value2][4]) #arrival time
                             if int(inputdata[list2[i]][7]) > temp1:
                                list1[i+1] = list1[i]
                                list2[i+1] = list2[i]
                                list1[i] = value1
                                list2[i] = value2
                                i = i-1
                             elif (int(inputdata[list2[i]][7]) == temp1): #the condition where priorities are equal go for the arrivaltime i.e., the one with less arrival time
                                        if int(inputdata[list2[i]][4]) > temp2:
                                                list1[i+1] = list1[i]
                                                list2[i+1] = list2[i]
                                                list1[i] = value1
                                                list2[i] = value2
                                                i = i-1 
                                        else:
                                                break                                     
                             else:
                                break
                     else:
                             break


global_task_buffer = total_task_buffer[:1]
total_task_buffer = total_task_buffer[1:]

while len(total_task_buffer)>0 or len(global_task_buffer) > 0:
        threshold_packet_drop = window_length - 1
        if (len(global_task_buffer)<global_buffer_size):
                dropped_tasks = []
                ###print   total_task_buffer
                #taking tasks from old buffer to global buffer of size 50
                toappend = global_buffer_size - len(global_task_buffer)
                if (toappend > len(total_task_buffer)):
                        toappend = len(total_task_buffer)
                for i in range(toappend):
                        global_task_buffer.append(total_task_buffer[i])
                total_task_buffer = total_task_buffer[toappend:] #deleting the tasks from the old buffer

                if (len(dropped_tasks)>=threshold_packet_drop):
                        window_length = initial_window_length
                if (len(global_task_buffer) < window_length):
                        window_length = len(global_task_buffer)
                
                #sorting the global task buffers based on priority before applying sliding window protocol to put the tasks into local buffer
                #print(filename)
                l1=[int(inputdata[global_task_buffer[i]][7]) for i in range(window_length)] #contains priority list of Tasks(because len of the task specifications are 8 or 9 (if '\n' counts))
                
                insertionsort(l1,global_task_buffer) 
                wlength.append(window_length)
                if len(global_task_buffer)>=window_length:
                        ###print   "At time = ",time
                        ###print   "Window length = ", window_length
                        time += 1
                        completed_tasks = []
                        
                        local_task_buffer = [global_task_buffer[i] for i in range(window_length)]
                        ###print   "ltb"
                        ###print   local_task_buffer

                        ###print   "\n********************ROUND 1 : DIVISION OF Tasks INTO HQ,MQ,LQ************************\n" 
                        ###print   "The local_task_buffer containing sorted Tasks based on priorities: " ,local_task_buffer

     
                        ##print "I m here", window_length, par
                        #******************calculating N1,N2,N3     
                        LAMBDA1 = val1
                        LAMBDA2 = val2
                        LAMBDA3 = val3

                        n=len(local_task_buffer)     #n : number of Tasks
                        # N1= (n//3) + LAMBDA1   #it automatically takes floor value unless we import division package
                        # N2= (n-N1)//2 + LAMBDA2
                        # N3= (n-(N1+N2)) + LAMBDA3

                        div = val1+ val2+val3
                        N1= int(math.floor((val1/div) * n))  #it automatically takes floor value unless we import division package
                        N2= int(math.floor((val2/div) * n))
                        N3= int(math.floor((val3/div) * n))

                        N1 = N1+ (n - (N1+N2+N3))

                        # print(n,val1,div, val1/div,int(math.floor(val1/div)),N1,N2,N3)

                        ##print N1, len(local_task_buffer)
                        ###print   "\nThe number of Tasks in \nHQ  : %d\nMQ  : %d\nLQ  : %d" %(N1,N2,N3)
                        #*****************division of elements into HQ,MQ,LQ 
                        HQ=[local_task_buffer[i] for i in range(N1)]
                        MQ=[local_task_buffer[i] for i in range(N1,N1+N2)]
                        LQ=[local_task_buffer[i] for i in range(N1+N2,n)]

                        ###print   "\nTasks in HQ:",HQ,"\n","Tasks in MQ:",MQ,"\n","Tasks in LQ:",LQ,"\n"

                        #******************internally sorting based on deadlines
                        l1=[int(inputdata[HQ[i]][6]) for i in range(N1)]
                        l2=[HQ[i] for i in range(N1)]
                        insertionsort(l1,l2) #calling insertion sort for sorting HQ Tasks based on deadlines
                        #putting in Finalised HQ, the one sorted based on deadlines lies in l2 so just for convention giving it a name as HQ list
                        HQ=[str(i) for i in l2]


                        l1=[int(inputdata[MQ[i]][6]) for i in range(N2)]
                        l2=[MQ[i] for i in range(N2)]
                        insertionsort(l1,l2) #calling insertion sort for sorting MQ Tasks based on deadlines
                        #putting in Finalized MQ
                        MQ=[str(i) for i in l2]


                        l1=[int(inputdata[LQ[i]][6]) for i in range(N3)]
                        l2=[LQ[i] for i in range(N3)]
                        insertionsort(l1,l2) #calling insertion sort for sorting LQ Tasks based on deadlines
                        #putting in Finalized LQ
                        LQ=[str(i) for i in l2]

                        ###print   "The Finalized internally sorted HQ based on deadlines:",HQ,'\n',"The Finalized internally sorted MQ based on deadlines:",MQ,'\n',"The Finalized internally sorted LQ based on deadlines:",LQ

                        #********************Calculation of time quantum to implement roundrobin for HQ  , MQ
                        #alpha1,alpha2 regulates the time quanta
                        ALPHA1=1
                        ALPHA2=0

                        l1=[int(inputdata[HQ[i]][6]) for i in range(len(HQ))]   
                        l2=[int(inputdata[MQ[i]][6]) for i in range(len(MQ))]
                        if (len(l1)!=0):        
                                TQ1=max(l1)//pow(2,ALPHA1)   
                        else:
                                TQ1 = 2
                        if (len(l2)!=0):
                                TQ2=max(l2)//pow(2,ALPHA2) 
                        else:
                                TQ2 = 4 
         
                        #if TQ1<TQ2 which violates our condition then increasing alpha value will validate the condition
                        while(1):  
                                if TQ1>TQ2 and TQ1>0:      
                                        ALPHA1=ALPHA1+1
                                        TQ1=max(l1)//pow(2,ALPHA1)   
                                else:
                                        break

                        
                        
                        ###print   "\nThe Calculated time quantum as follows:\nTQ1   :   %d\nTQ2   :   %d\n\n" %(TQ1,TQ2) 
                        ###print   "********************END OF ROUND1************************\n\n" 
                        ###print   "\n********************ROUND 2 - CREATION OF VIRTUAL MACHINES************************\n"    

                        #*************************************************************************************
                        #DAC algorithm Round2 implementation using python
                        #Date : 7-6-2017
                        #Name : K Naveen Kumar

                        #hosts specifications
                        Hosts=[k  for k,v in inputdata.items() if len(v)==4]         #contains corresponding Hosts
                        HId=[int(v[0]) for k,v in inputdata.items() if len(v)==4 ]   #contains id's of hosts
                        insertionsort(HId,Hosts)  #sorting based on ids , just for ###print  ing and better output
                        Hram=[int(inputdata[Hosts[i]][1]) for i in range(len(HId))]   #contains ram list of Hosts
                        Hsize=[int(inputdata[Hosts[i]][2]) for i in range(len(HId))]  #contains size list of Hosts
                        Hmips=[int(inputdata[Hosts[i]][3]) for i in range(len(HId))]  #contains Mips list of Hosts

                        ###print   "We have following resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #Average stratergy
                        Instructions=[int(inputdata[HQ[i]][1]) for i in range(len(HQ))]
                        RAM=[int(inputdata[HQ[i]][2]) for i in range(len(HQ))]
                        SIZE=[int(inputdata[HQ[i]][3]) for i in range(len(HQ))]

                        #taking minimum of specifications of HQ
                        if (len(Instructions)!=0):
                                AN= sum(Instructions)//len(Instructions) #Average strategy
                                AR= sum(RAM)//len(RAM)
                                AS= sum(SIZE)//len(SIZE) 

                                #taking minimum of specifications of HQ
                                MN= min(Instructions)  #minimum strategy
                                MR= min(RAM)
                                MS= min(SIZE)
                        else:
                                Instructions=[int(inputdata[MQ[i]][1]) for i in range(len(MQ))]
                                RAM=[int(inputdata[MQ[i]][2]) for i in range(len(MQ))]
                                SIZE=[int(inputdata[MQ[i]][3]) for i in range(len(MQ))]

                                if (len(Instructions)!=0):
                                
                                        AN= sum(Instructions)//len(Instructions) #Average strategy
                                        AR= sum(RAM)//len(RAM)
                                        AS= sum(SIZE)//len(SIZE) 

                                        #taking minimum of specifications of HQ
                                        MN= min(Instructions)  #minimum strategy
                                        MR= min(RAM)
                                        MS= min(SIZE)  
                                
                                else: 
                                        Instructions=[int(inputdata[LQ[i]][1]) for i in range(len(LQ))]
                                        RAM=[int(inputdata[LQ[i]][2]) for i in range(len(LQ))]
                                        SIZE=[int(inputdata[LQ[i]][3]) for i in range(len(LQ))]

                       
                        Vms=[]   #list of Vms
                        m=len(Hosts) #m : number of hosts, calculated since intially the number Vms created are equal to number of hosts
                        vmdict={}
                        #constraint check
                        for i in range(m):
                                if i > 0:
                                        AN=int(vmdict[1][0])+(Hmips[i]//2)
                                        AR=int(vmdict[1][1])+(Hram[i]//2)
                                        AS=int(vmdict[1][2])+(Hsize[i]//2)  
                                ####print   AN, AR, AS
                                #******************Average Strategy**********************

                                if AN <= Hmips[i] and AR <= Hram[i] and AS <= Hsize[i]:
                                        V=[AN,AR,AS]
                                        Vms.append(i+1)
                                        vmdict[(Vms[len(Vms)-1])]=V 
                                        ###print   "\nVM%d is successfully created for Host%d with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2])
                                else:
                                        ###print   "Average stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,+1)             
                        #************************************average strategy failed so going to Minimum strategy**************************                   
                                        if i>0 and (i+1)<=m:
                                                MN1=MN+(Hmips[i]//2)
                                                MR1=MR+(Hram[i]//2)
                                                MS1=MS+(Hsize[i]//2)  
                                                if MN1 <= Hmips[i] and MR1 <= Hram[i] and MS1 <= Hsize[i]:
                                                        V=[MN1,MR1,MS1]
                                                        Vms.append(i+1)
                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                        ###print   "\nVM%d is successfully created for Host%d using Minimum strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                else:
                                                        ###print   "\nMinimum stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,i+1)    

                        #****************************minimum strategy failed so going forDefault strategy*****************************************************
                                                        if i>0 and (i+1)<=m-1:
                                                                DN=(Hmips[0]//2)+(Hmips[i]//2)
                                                                DR=(Hram[0]//2)+(Hram[i]//2)
                                                                DS=(Hsize[0]//2)+(Hsize[i]//2)  
                                        
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                                else:
                                                                        DN=(Hmips[i]//2)
                                                                        DR=(Hram[i]//2)
                                                                        DS=(Hsize[i]//2) 
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                        else:
                                                                DN=(Hmips[i]//2)
                                                                DR=(Hram[i]//2)
                                                                DS=(Hsize[i]//2) 
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                                        ###print   "\nVM%d is successfully created for Host%d using Default strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                        #if average strategy fails for VM1 itself then going for Minimum strategy                                                                        
                                        else:
                                                if MN <= Hmips[i] and MR <= Hram[i] and MS <= Hsize[i]:
                                                        V=[MN,MR,MS]
                                                        Vms.append(i+1)
                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                        ###print   "\nVM%d is successfully created for Host%d using Minimum strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                else:
                                                        ###print   "\nMinimum stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,i+1)   
                        #*************************************Default strategy*****************************************************
                                                        if i>0 and (i+1)<=m:
                                                                ###print   "******************************"
                                                                DN=(Hmips[0]//2)+(Hmips[i]//2)
                                                                DR=(Hram[0]//2)+(Hram[i]//2)
                                                                DS=(Hsize[0]//2)+(Hsize[i]//2)  
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                                else:
                                                                        ###print   "*************************"
                                                                        DN=(Hmips[i]//2)
                                                                        DR=(Hram[i]//2)
                                                                        DS=(Hsize[i]//2) 
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                                                        else:
                                                                DN=(Hmips[i]//2)
                                                                DR=(Hram[i]//2)
                                                                DS=(Hsize[i]//2) 
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                                        ###print   "\nVM%d is successfully created for Host%d using Default strategy with specification\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                        ###print   "********************END OF ROUND2************************\n\n" 
                        #**************ROUND 3 : Execution of Tasks using  virtual machines***********************                                
                        #DAC algorithm Round3 implementation using python
                        #Date : 9-6-2017
                        #Name : K Naveen Kumar

                        ###print   "\n************ROUND 3 : EXECUTION OF Tasks USING VIRTUAL MACHINES*****************\n"    
                        #Vms specifications


                        Vms=[k  for k,v in vmdict.items()]         #contains corresponding Vms
                        Vram=[int(vmdict[Vms[i]][1]) for i in range(len(Vms))]   #contains ram list of Vms
                        Vsize=[int(vmdict[Vms[i]][2]) for i in range(len(Vms))]  #contains size list of Vms
                        Vmips=[int(vmdict[Vms[i]][0]) for i in range(len(Vms))]  #contains Mips list of Vms
                        #VMflags : 1 indicate the Vms are busy and 0 indicate they are free to use
                        #initially taken them as 0 : means not assigned
                        Vflags=[0 for i in range(len(Vms))]
                        ###print   "We have following resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        ###print   "We have following Vms:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n"

                        #Resource utilization
                        Leftoverram={} 
                        Leftoversize={}

                        #***********decrement of resources
                        for i in range(len(Hosts)):
                                Hram[i]=Hram[i]-Vram[i]
                                Hsize[i]=Hsize[i]-Vsize[i]
                                Leftoverram[i+1]=Hram[i]
                                Leftoversize[i+1]=Hsize[i]
        
                        ###print   "We have following remaining resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #*******************************STARTING EXECUTION OF TASKS IN HQ****************************************************
                        ###print   "Execution of Tasks in HQ......\n"                
                        #Tasks specifications
                        Tasks = HQ
                        n=len(Tasks)
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution
                        TCT={} #contains completion time of Tasks
                        TAT={} #contains arrival times into virtual machines
                        TTAT={} #contains turnaround time of Tasks
                        TWT={} #contains waiting times of Tasks
                        TExec={} #contains execution times of Tasks
                                        
                        ###print   "We have following Tasks to be executed in HQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"
         
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)

                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]
                        Vtimer=[0 for i in range(m)] #contains timer of vm

                        #****************now round3 starts

                        count=0 #temparary variable
                        Halloc={} #dictionary containing allocated virtual machines to hosts information
                        while(count<100 and len(Tasks)>0):     
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                
                                while(i<n):                       
                                        for j in range(m): #allocating virtual machines to tasks
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                                
                                        if Tasks[i] not in Talloc.values(): #if tasks doesnot find virtual machine then create new vm
                                                ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                mips=(Tno_of_Instr[i])
                                                ram=(Tram[i])
                                                size=(Tsize[i])
                                                done=0 #creating only once , done=1 indicates created and getting out of the loop
                                                for k in range(l): 
                                                        if done ==0:
                                                                extra=[] #temp list
                                                                if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                        V=[mips,ram,size]
                                                                        Vms.append(len(Vms)+1)
                                                                                ####print   "\n\nVms..",i,Vms 
                                                                        vmdict[(Vms[len(Vms)-1])]=V        
                                                                        Vram.append(ram)
                                                                        Vsize.append(size)
                                                                        Vmips.append(mips)
                                                                        Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                        Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]                                                
                                                                        Talloc[Vms[len(Vms)-1]]=Tasks[i]                                          
                                                                        extra.append(Vms[len(Vms)-1])
                                                                        Halloc[k+1]=extra #allocated newly created vm to host and storing that info in halloc
                                                                                ####print   "\n\n",Halloc,Hosts,Hram,Hsize,'\n\n'
                                                                        Vflags.append(1)
                                                                        Vtimer.append(0) #setting newly created vm's vtimer as 0
                                                                        done=1 
                                                                        del(extra)

                                                        else:
                                                                break
                                                if Tasks[i] not in Talloc.values():
                                                                ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                                dropped_tasks.append(Tasks[i])
                                                                index=Tasks.index(Tasks[i])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                i=i-1
                                                                n=n-1
                                                        
                                        i=i+1
                                       
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  
                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Talloc.keys())
                                valloc=[]
                                i=0
                                #if len of allocted tasks exceeds len of given tasks bring it to len of tasks 'n'
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          

                                ####print   "\n\n",valloc,"\n\n"

                                counter=0 #temp variable
                        #executing in roundrobin fashion with timequantum as TQ1
                                while(h<m):
                                        alreadydone=0
                                        if (TDL[h] > TQ1 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ1+Vtimer[valloc[counter]-1]
                                                
                                                #different cases of calculation of execution times
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TQ1:
                                                        Executiontime = TQ1
                                                if TQ1>TBurst[h] and Executiontime >= TQ1:
                                                        Executiontime = TBurst[h]            
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime #incrementing the vtimer

                                                # ###print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]): #if burstime becomes 0 then remove task from the queue and count the completion time of the task
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1

                                                if (len(Tasks)>0):     #if there are remaining tasks execute round robin again                           
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        TCT[Tasks[h]]=TExec[Tasks[h]]
                                                        ####print   "Execution times",TExec,"\n\n"
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1
                                                
                                        elif (TDL[h] <= TQ1 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0): 
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ1+Vtimer[valloc[counter]-1]
                                                
                                                #different cases of calculation of execution time
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TDL[h]:
                                                        Executiontime = TDL[h]
                                                if TDL[h]>TBurst[h] and Executiontime >= TDL[h]:
                                                        Executiontime = TBurst[h]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                TBurst[h]=TBurst[h]-Executiontime   
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime

                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                Vflags[valloc[counter]-1]=0
                                                counter=counter+1
                                                h=h-1
                                                m=m-1
                                        h=h+1
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        index=Tasks.index(Tasks[h])
                                        b=Tasks.pop(index)
                                        b=Tram.pop(index)
                                        b=Tsize.pop(index)
                                        b=Tno_of_Instr.pop(index)
                                        b=TBurst.pop(index)
        
                                del(Talloc)
                                Talloc={}    
                                count=count+1
      
                     
                        #****************************   COMPLETION OF EXECUTION OF TASKS IN HQ   *********************************                     
                        ####print   Vms,Vram,Vsize
                        ####print   Hosts,Hram,Hsize

                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto
                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'
                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"          
                                for i in range(len(Hosts)):
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]
                                
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize
                                        
                                ###print   "We have following remaining resources after killing extra virtual machines in HQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #*******************************STARTING EXECUTION OF TASKS IN MQ****************************************************
                        ###print   "Execution of Tasks in MQ......\n\n"

                        #Tasks specifications
                        Tasks = MQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution
                        ###print   "We have following Tasks to be executed in MQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"
                                
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)
                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]

                        #****************now round3 starts
                        count=0
                        Halloc={}
                        while(count<50 and len(Tasks)>0): 
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                while(i<n):
                                        ####print   "\n\n",i,n,"\n\n"        
                                        for j in range(m):
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                                
                                        if Tasks[i] not in Talloc.values():
                                                ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                mips=(Tno_of_Instr[i])
                                                ram=(Tram[i])
                                                size=(Tsize[i])
                                                done=0
                                                for k in range(l):
                                                        if done==0: 
                                                                extra=[]
                                                                if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                        V=[mips,ram,size]
                                                                        Vms.append(len(Vms)+1)
                                                                        ####print   "\n\nVms...",Vms
                                                                        vmdict[(Vms[len(Vms)-1])]=V        
                                                                        Vram.append(ram)
                                                                        Vsize.append(size)
                                                                        Vmips.append(mips)
                                                                        Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                        Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]
                                                                        ####print   "Length\n\n",len(Vms)
                                                                        extra.append(Vms[len(Vms)-1])
                                                                        Halloc[k+1]=extra
                                                                        Talloc[Vms[len(Vms)-1]]=Tasks[i]
                                                                        ####print   "\n\n",Talloc,"\n\n"
                                                                        Vflags.append(1)
                                                                        Vtimer.append(0)
                                                                        done=1
                                                                        del(extra)     
                                                        else:
                                                                break

                                                if Tasks[i] not in Talloc.values():
                                                        ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                        dropped_tasks.append(Tasks[i])
                                                        index=Tasks.index(Tasks[i])
                                                        b=Tasks.pop(index)
                                                        Tasks.append(b)
                                                        b=Tram.pop(index)
                                                        Tram.append(b)
                                                        b=Tsize.pop(index)
                                                        Tsize.append(b)
                                                        b=Tno_of_Instr.pop(index)
                                                        Tno_of_Instr.append(b)
                                                        b=TBurst.pop(index)
                                                        TBurst.append(b)
                                                        b=TDL.pop(index)
                                                        TDL.append(b)
                                                        i=i-1
                                                        n=n-1               
                                                        ####print   "I am here\n\n",Tasks,"\n\n"
                                        i=i+1
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  

                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Tasks)
                                valloc=[]
                                i=0
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          
                                ####print   "\n\n",Tasks,valloc,"\n\n"

                                counter=0
                                while(h<m):
                                        alreadydone=0
                                        ####print   "\n\n",valloc,counter,Vtimer,valloc[counter],"\n\n"
                                        ####print   "\n\nVtimer",Tasks[h],Vtimer[valloc[counter]-1],"\n\n" 
                                        if (TDL[h] > TQ2 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ2+Vtimer[valloc[counter]-1]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        ####print   "You are right i am here\n\n"
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,TDL[h],"\n\n"  
                                                if Executiontime > TQ2:
                                                        Executiontime = TQ2
                        #                                ###print   "here here bursttime,executiontime",TBurst[h],Executiontime,"\n\n"                              
                                                if Executiontime>TBurst[h]:
                                                        Executiontime = TBurst[h]
                                                ####print   "The Execution here is :  %d" %Executiontime
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        ####print   "\n\ni m here here here",Tasks[h],TCT[Tasks[h]]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1
                                                if (len(Tasks)>0):
                                                        ####print   "\n\n......",Tasks[h]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        TCT[Tasks[h]]=TExec[Tasks[h]]
                                                        ####print   "Execution times",TExec,"\n\n"
                                                        ####print   "\n\ni m here here",Tasks[h],TCT[Tasks[h]]
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1
                                                
                                        elif (TDL[h] <= TQ2 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0): 
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ2+Vtimer[valloc[counter]-1]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        ####print   "You are right i am here\n\n"
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TDL[h]:
                                                        Executiontime = TDL[h]
                                                if TDL[h]>TBurst[h] and Executiontime >= TDL[h]:
                                                        Executiontime = TBurst[h]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,TDL[h],"\n\n"    
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                TBurst[h]=TBurst[h]-Executiontime   
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:                                
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                
                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                Vflags[valloc[counter]-1]=0
                                                counter=counter+1
                                                h=h-1
                                                m=m-1
                                        h=h+1
                                
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        index=Tasks.index(Tasks[h])
                                        b=Tasks.pop(index)
                                        b=Tram.pop(index)
                                        b=Tsize.pop(index)
                                        b=Tno_of_Instr.pop(index)
                                        b=TBurst.pop(index)

                                del(Talloc)
                                count=count+1        
                                Talloc={}                
                        ###print   '\n\n',Vtimer,Tasks,TCT,TBurst,TDL,Vflags,TExec,'\n\n'     
                                        
                        ####print   "\n\n",TCT,TExec                    
                        #****************************END OF MQ EXECUTION**************************
                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto

                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'

                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"          
                                for i in range(len(Hosts)):
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]        
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]
                                
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize         
                                ###print   "We have following remaining resources after killing extra virtual machines in MQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        
                        #****************************START OF LQ EXECUTION IN FCFS FASHION                     
                        ###print   "Execution of Tasks in LQ......\n\n"
                        #Tasks specifications


                        Tasks = LQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution 
                        ###print   "We have following Tasks to be executed in LQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"    

                        ####print   TBurst     
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)
                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]
                        count=0
                        Halloc={}
                        while(count<50 and len(Tasks)>0):     
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                while(i<n):
                                        ####print   "\n\n",i,n,"\n\n"        
                                        for j in range(m):
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                        if Tasks[i] not in Talloc.values():
                                                ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                mips=(Tno_of_Instr[i])
                                                ram=(Tram[i])
                                                size=(Tsize[i])
                                                done=0
                                                for k in range(l): 
                                                        if done==0:
                                                                extra=[]
                                                                if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                        V=[mips,ram,size]
                                                                        Vms.append(len(Vms)+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V        
                                                                        Vram.append(ram)
                                                                        Vsize.append(size)
                                                                        Vmips.append(mips)
                                                                        Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                        Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]
                                                                        extra.append(Vms[len(Vms)-1])
                                                                        Halloc[k+1]=extra
                                                                        Talloc[Vms[len(Vms)-1]]=Tasks[i]
                                                                        Vflags.append(1)
                                                                        Vtimer.append(0)
                                                                        done=1
                                                                        del(extra)
                                                        else:
                                                                break;
                                                if Tasks[i] not in Talloc.values():
                                                        ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                        dropped_tasks.append(Tasks[i])
                                                        index=Tasks.index(Tasks[i])
                                                        b=Tasks.pop(index)
                                                        Tasks.append(b)
                                                        b=Tram.pop(index)
                                                        Tram.append(b)
                                                        b=Tsize.pop(index)
                                                        Tsize.append(b)
                                                        b=Tno_of_Instr.pop(index)
                                                        Tno_of_Instr.append(b)
                                                        b=TBurst.pop(index)
                                                        TBurst.append(b)
                                                        b=TDL.pop(index)
                                                        TDL.append(b)
                                                        i=i-1
                                                        n=n-1
                                        i=i+1
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  
                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Talloc.keys())
                                valloc=[]
                                i=0
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          
                                ####print   "\n\n",valloc,"\n\n"
                                counter=0
                                while(h<m):
                                        alreadydone=0
                                        ####print   "\n\nDeadlines",Tasks,Tasks[h],Vtimer[valloc[counter]-1],TDL[h],"\n\n" 
                                        if (TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=Vtimer[valloc[counter]-1]+TBurst[h]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,"\n\n"
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        ####print   TCT[Tasks[h]]                                
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1
                                                if (len(Tasks)>0):
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1


                                        else:
                                                ###print   "Task %s cannot be executed...because of low deadline,please extend deadline or increase the priority for the task to execute..\n\n" %Tasks[h]
                                                dropped_tasks.append(Tasks[h])
                                                TCT[Tasks[h]]=0
                                                TExec[Tasks[h]]=0
                                                Vflags[valloc[counter]-1]=0
                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                h=h-1
                                                counter=counter+1
                                                m=m-1
                                        h=h+1
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        break     
                                del(Talloc)
                                count=count+1        
                                Talloc={}

                        ####print   TAT
                        #if the task has 0 execution then turn around time and waiting time is equal to deadline
                        for k,v in TCT.items():
                                if TExec[k]==0:
                                        TAT[k] = int(inputdata[k][5])
                                        TTAT[k]= int(inputdata[k][6])
                                        TWT[k] = int(inputdata[k][6])   
                                else:             
                                        TTAT[k] = TCT[k] - TAT[k]               
                                        TWT[k] = TTAT[k] - TExec[k]
                                
                        #calculation of execution times
                        for k in TExec.keys():
                                T=int(TExec[k])/int(inputdata[k][5])
                                T=T*int(inputdata[k][1])
                                TExec[k]=T
                                

                        Tasks=[k for k,v in TCT.items()]
                        l2=[int(inputdata[Tasks[i]][0]) for i in range(len(Tasks))]
                        insertionsort(l2,Tasks) #sorting based on id for proper outputs

                        #*******************displaying output of execution of HQ and MQ and LQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        TCTime=[int(TCT[Tasks[i]]) for i in range(len(Tasks))] #contains completion time of Tasks
                        TTATime=[int(TTAT[Tasks[i]]) for i in range(len(Tasks))] #contains turnaround time of Tasks
                        TWTime=[int(TWT[Tasks[i]]) for i in range(len(Tasks))] #contains waiting times of Tasks
                        TExecTime=[int(TExec[Tasks[i]]) for i in range(len(Tasks))] #contains execution times of Tasks               
                        ###print   "We have following output after executing Tasks in HQ,MQ and LQ:\nTasks                       :     ",Tasks,"\nRAMs                        :     ",Tram,"\nSizes                       :     ",Tsize,"\nNo of Instructions          :     ",Tno_of_Instr,"\nArrivalTime                 :     ",TArrival,"\nBurstTime                   :     ",TBurst,"\nDeadLine                    :     ",TDL,"\nTasks completionTime        :     ",TCTime,"\nTasks TurnAroundtime        :     ",TTATime,"\nTasks WaitingTime           :     ",TWTime,"\nNo.of Instructions Executed :     ",TExecTime,"\n\n"                      

                        #******************************************
                        #case when extra virtual machines created,hence killing them after the completion of execution of LQ
                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto
                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'
                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"               
                                for i in range(len(Hosts)): #caluculation of resources used
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]      
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize
                                ###print   "We have following remaining resources after killing extra virtual machines in LQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        
                                
                        #************COMPLETION OF ALGORITHM********** 
                        #killing the intially created virtual machines and updating the host machine specifications
                        for i in range(len(Hosts)):
                                
                                ###print   "Virtual machine %d has been destroyed...\n\n" % (i+1)
                                addram=Vram[i]
                                addsize=Vsize[i]
                                ####print   addram,addsize
                                Hram[i]=Hram[i]+addram
                                Hsize[i]=Hsize[i]+addsize
                                ####print   Hram,Hsize        
                                ###print   "We have following resources after destroying of the Virtual machine:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                                
                        #*****************************************************************                           
                        ###print   "END OF THE ALGORITHM...for time = ", time

                        #****************calculation of percentage of utilization of resources*****************************
                        Usedram={}
                        Usedsize={}

                        for i in range(len(Hosts)):
                                Usedram[i+1]=Hram[i]-Leftoverram[i+1]
                                Usedsize[i+1]=Hsize[i]-Leftoversize[i+1]


                        percentUsedram = (sum(Usedram.values())/sum(Hram))*100 
                        percentUsedsize = (sum(Usedsize.values())/sum(Hsize))*100 

                        ####print   percentUsedram,percentUsedsize 
                        total=percentUsedram+percentUsedsize
                        #********************************************

                        ####print  ing the results
                        ###print   "ResultAnalysis\n\n"
                        ###print   "Average Turnaround Time                 :          %f" %(sum(TTATime)/len(TTATime))
                        ###print   "Average Waiting Time                    :          %f" %(sum(TWTime)/len(TWTime))
                        ###print   "Total Number Of Instructions Executed   :          %d" % (sum(TExecTime))
                        ###print   "Given Total Number Of Instructions      :          %d" % (sum(Tno_of_Instr))
                        ###print   "percentage of utilization of resources  :          %f\n\n" % ((total)/2)

                        #******************************************
                        #writing the outputs to output file
                        # filename='outputDAC'+filename
                        # with open(filename,'w') as output_file:
                        #         for i in range(len(TTATime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TTATime[i])  #writing into the file using , separated
                        #                 else :
                        #                         output_file.write("%d," %TTATime[i])
                        #         for i in range(len(TWTime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TWTime[i])  
                        #                 else :
                        #                         output_file.write("%d," %TWTime[i])
                        #         for i in range(len(TExecTime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TExecTime[i])  
                        #                 else :            
                        #                         output_file.write("%d," %TExecTime[i])

                        ###print   "After time = ",time
                        ###print   "dropped tasks  = ",dropped_tasks
                        completed_tasks = np.setdiff1d(np.asarray(local_task_buffer),np.asarray(dropped_tasks))
                        global_task_buffer = global_task_buffer[window_length:]
                        global_task_buffer = dropped_tasks + global_task_buffer
                        ###print   "gtb"
                        ###print   global_task_buffer
                        window_length +=1
                        ###print   "*************\n"
                        avg_turnaround_time.append(sum(TTATime)/len(TTATime))
                        avg_waiting_time.append(sum(TWTime)/len(TWTime))
                        percent_execution.append((sum(TExecTime)/sum(Tno_of_Instr)) * 100)
                        completedtasks.append(len(completed_tasks))
                        totaltasks.append(len(local_task_buffer))

                else:
                        ###print   "At time = ",time
                        ###print   "Window length = ", len(global_task_buffer)
                        time += 1
                        completed_tasks = []
                        dropped_tasks = []
                        local_task_buffer = global_task_buffer
                        ###print   "ltb"
                        ###print   local_task_buffer


                        ###print   "\n********************ROUND 1 : DIVISION OF Tasks INTO HQ,MQ,LQ************************\n" 
                        ###print   "The local_task_buffer containing sorted Tasks based on priorities: " ,local_task_buffer

     

                        #******************calculating N1,N2,N3     
                        LAMBDA = val         #LAMBDA which regulates the number of Tasks in HQ,MQ,LQ respectively
                        n=len(local_task_buffer)     #n : number of Tasks
                        N1= (n//3) + LAMBDA  #it automatically takes floor value unless we import division package
                        N2= (n-N1)//2
                        N3= (n-(N1+N2))

                        ###print   "\nThe number of Tasks in \nHQ  : %d\nMQ  : %d\nLQ  : %d" %(N1,N2,N3)
                        #*****************division of elements into HQ,MQ,LQ 
                        HQ=[local_task_buffer[i] for i in range(N1)]
                        MQ=[local_task_buffer[i] for i in range(N1,N1+N2)]
                        LQ=[local_task_buffer[i] for i in range(N1+N2,n)]

                        ###print   "\nTasks in HQ:",HQ,"\n","Tasks in MQ:",MQ,"\n","Tasks in LQ:",LQ,"\n"

                        #******************internally sorting based on deadlines
                        l1=[int(inputdata[HQ[i]][6]) for i in range(N1)]
                        l2=[HQ[i] for i in range(N1)]
                        insertionsort(l1,l2) #calling insertion sort for sorting HQ Tasks based on deadlines
                        #putting in Finalised HQ, the one sorted based on deadlines lies in l2 so just for convention giving it a name as HQ list
                        HQ=[str(i) for i in l2]


                        l1=[int(inputdata[MQ[i]][6]) for i in range(N2)]
                        l2=[MQ[i] for i in range(N2)]
                        insertionsort(l1,l2) #calling insertion sort for sorting MQ Tasks based on deadlines
                        #putting in Finalized MQ
                        MQ=[str(i) for i in l2]


                        l1=[int(inputdata[LQ[i]][6]) for i in range(N3)]
                        l2=[LQ[i] for i in range(N3)]
                        insertionsort(l1,l2) #calling insertion sort for sorting LQ Tasks based on deadlines
                        #putting in Finalized LQ

                        LQ=[str(i) for i in l2]

                        ###print   "The Finalized internally sorted HQ based on deadlines:",HQ,'\n',"The Finalized internally sorted MQ based on deadlines:",MQ,'\n',"The Finalized internally sorted LQ based on deadlines:",LQ

                        #********************Calculation of time quantum to implement roundrobin for HQ  , MQ
                        #alpha1,alpha2 regulates the time quanta
                        ALPHA1=1
                        ALPHA2=0

                        l1=[int(inputdata[HQ[i]][6]) for i in range(len(HQ))]   
                        l2=[int(inputdata[MQ[i]][6]) for i in range(len(MQ))]

                        TQ1=max(l1)//pow(2,ALPHA1)   
                        TQ2=max(l2)//pow(2,ALPHA2) 
                        #if TQ1<TQ2 which violates our condition then increasing alpha value will validate the condition
                        while(1):  
                                if TQ1>TQ2 and TQ1>0:      
                                        ALPHA1=ALPHA1+1
                                        TQ1=max(l1)//pow(2,ALPHA1)   
                                else:
                                        break
                        
                        ###print   "\nThe Calculated time quantum as follows:\nTQ1   :   %d\nTQ2   :   %d\n\n" %(TQ1,TQ2) 
                        ###print   "********************END OF ROUND1************************\n\n" 
                        ###print   "\n********************ROUND 2 - CREATION OF VIRTUAL MACHINES************************\n"    

                        #*************************************************************************************
                        #DAC algorithm Round2 implementation using python
                        #Date : 7-6-2017
                        #Name : K Naveen Kumar

                        #hosts specifications
                        Hosts=[k  for k,v in inputdata.items() if len(v)==4]         #contains corresponding Hosts
                        HId=[int(v[0]) for k,v in inputdata.items() if len(v)==4 ]   #contains id's of hosts
                        insertionsort(HId,Hosts)  #sorting based on ids , just for ###print  ing and better output
                        Hram=[int(inputdata[Hosts[i]][1]) for i in range(len(HId))]   #contains ram list of Hosts
                        Hsize=[int(inputdata[Hosts[i]][2]) for i in range(len(HId))]  #contains size list of Hosts
                        Hmips=[int(inputdata[Hosts[i]][3]) for i in range(len(HId))]  #contains Mips list of Hosts

                        ###print   "We have following resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #Average stratergy
                        Instructions=[int(inputdata[HQ[i]][1]) for i in range(len(HQ))]
                        RAM=[int(inputdata[HQ[i]][2]) for i in range(len(HQ))]
                        SIZE=[int(inputdata[HQ[i]][3]) for i in range(len(HQ))]

                        #taking minimum of specifications of HQ
                        AN= sum(Instructions)//len(Instructions) #Average strategy
                        AR= sum(RAM)//len(RAM)
                        AS= sum(SIZE)//len(SIZE) 

                        #taking minimum of specifications of HQ
                        MN= min(Instructions)  #minimum strategy
                        MR= min(RAM)
                        MS= min(SIZE)

                        Vms=[]   #list of Vms
                        m=len(Hosts) #m : number of hosts, calculated since intially the number Vms created are equal to number of hosts
                        vmdict={}

                        #constraint check
                        for i in range(m):
                                if i > 0:
                                        AN=int(vmdict[1][0])+(Hmips[i]//2)
                                        AR=int(vmdict[1][1])+(Hram[i]//2)
                                        AS=int(vmdict[1][2])+(Hsize[i]//2)  

                                #******************Average Strategy**********************

                                if AN <= Hmips[i] and AR <= Hram[i] and AS <= Hsize[i]:
                                        V=[AN,AR,AS]
                                        Vms.append(i+1)
                                        vmdict[(Vms[len(Vms)-1])]=V 
                                        ###print   "\nVM%d is successfully created for Host%d with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2])
                                else:
                                        ###print   "Average stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,+1)             
                        #************************************average strategy failed so going to Minimum strategy**************************                   
                                        if i>0 and (i+1)<=m:
                                                MN1=MN+(Hmips[i]//2)
                                                MR1=MR+(Hram[i]//2)
                                                MS1=MS+(Hsize[i]//2)  
                                                if MN1 <= Hmips[i] and MR1 <= Hram[i] and MS1 <= Hsize[i]:
                                                        V=[MN1,MR1,MS1]
                                                        Vms.append(i+1)
                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                        ###print   "\nVM%d is successfully created for Host%d using Minimum strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                else:
                                                        ###print   "\nMinimum stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,i+1)    

                        #****************************minimum strategy failed so going forDefault strategy*****************************************************
                                                        if i>0 and (i+1)<=m-1:
                                                                DN=(Hmips[0]//2)+(Hmips[i]//2)
                                                                DR=(Hram[0]//2)+(Hram[i]//2)
                                                                DS=(Hsize[0]//2)+(Hsize[i]//2)  
                                        
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                                else:
                                                                        DN=(Hmips[i]//2)
                                                                        DR=(Hram[i]//2)
                                                                        DS=(Hsize[i]//2) 
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                        else:
                                                                DN=(Hmips[i]//2)
                                                                DR=(Hram[i]//2)
                                                                DS=(Hsize[i]//2) 
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                                        ###print   "\nVM%d is successfully created for Host%d using Default strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                        #if average strategy fails for VM1 itself then going for Minimum strategy                                                                        
                                        else:
                                                if MN <= Hmips[i] and MR <= Hram[i] and MS <= Hsize[i]:
                                                        V=[MN,MR,MS]
                                                        Vms.append(i+1)
                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                        ###print   "\nVM%d is successfully created for Host%d using Minimum strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                else:
                                                        ###print   "\nMinimum stratergy failed for VM%d creation for Host%d\nTrying another stratery for creation of VM%d...." %(i+1,i+1,i+1)   
                        #*************************************Default strategy*****************************************************
                                                        if i>0 and (i+1)<=m:
                                                                ###print   "******************************"
                                                                DN=(Hmips[0]//2)+(Hmips[i]//2)
                                                                DR=(Hram[0]//2)+(Hram[i]//2)
                                                                DS=(Hsize[0]//2)+(Hsize[i]//2)  
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 
                                                                else:
                                                                        ###print   "*************************"
                                                                        DN=(Hmips[i]//2)
                                                                        DR=(Hram[i]//2)
                                                                        DS=(Hsize[i]//2) 
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V
                                                                        ###print   "\nVM%d is successfully created for Host%d using Defualt strategy with specifications\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                                                        else:
                                                                DN=(Hmips[i]//2)
                                                                DR=(Hram[i]//2)
                                                                DS=(Hsize[i]//2) 
                                                                if DN <= Hmips[i] and DR <= Hram[i] and DS <= Hsize[i]:
                                                                        V=[DN,DR,DS]
                                                                        Vms.append(i+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V 
                                                                        ###print   "\nVM%d is successfully created for Host%d using Default strategy with specification\nMIPS      :     %d\nRAM       :     %d\nSIZE      :     %d\n" %(i+1,i+1,V[0],V[1],V[2]) 

                        ###print   "********************END OF ROUND2************************\n\n" 
                        #**************ROUND 3 : Execution of Tasks using  virtual machines***********************                                
                        #DAC algorithm Round3 implementation using python
                        #Date : 9-6-2017
                        #Name : K Naveen Kumar

                        ###print   "\n************ROUND 3 : EXECUTION OF Tasks USING VIRTUAL MACHINES*****************\n"    
                        #Vms specifications

                        Vms=[k  for k,v in vmdict.items()]         #contains corresponding Vms
                        Vram=[int(vmdict[Vms[i]][1]) for i in range(len(Vms))]   #contains ram list of Vms
                        Vsize=[int(vmdict[Vms[i]][2]) for i in range(len(Vms))]  #contains size list of Vms
                        Vmips=[int(vmdict[Vms[i]][0]) for i in range(len(Vms))]  #contains Mips list of Vms
                        #VMflags : 1 indicate the Vms are busy and 0 indicate they are free to use
                        #initially taken them as 0 : means not assigned
                        Vflags=[0 for i in range(len(Vms))]
                        ###print   "We have following resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        ###print   "We have following Vms:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n"

                        #Resource utilization
                        Leftoverram={} 
                        Leftoversize={}

                        #***********decrement of resources
                        for i in range(len(Hosts)):
                                Hram[i]=Hram[i]-Vram[i]
                                Hsize[i]=Hsize[i]-Vsize[i]
                                Leftoverram[i+1]=Hram[i]
                                Leftoversize[i+1]=Hsize[i]
        
                        ###print   "We have following remaining resources:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #*******************************STARTING EXECUTION OF TASKS IN HQ****************************************************
                        ###print   "Execution of Tasks in HQ......\n"                
                        #Tasks specifications
                        Tasks = HQ
                        n=len(Tasks)
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution
                        TCT={} #contains completion time of Tasks
                        TAT={} #contains arrival times into virtual machines
                        TTAT={} #contains turnaround time of Tasks
                        TWT={} #contains waiting times of Tasks
                        TExec={} #contains execution times of Tasks
                                        
                        ###print   "We have following Tasks to be executed in HQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"
         
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)

                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]
                        Vtimer=[0 for i in range(m)] #contains timer of vm

                        #****************now round3 starts

                        count=0 #temparary variable
                        Halloc={} #dictionary containing allocated virtual machines to hosts information

                        while(count<50 and len(Tasks)>0):     
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                
                                while(i<n):                       
                                        for j in range(m): #allocating virtual machines to tasks
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                        
                                        if Tasks[i] not in Talloc.values(): #if tasks doesnot find virtual machine then create new vm
                                                ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                mips=(Tno_of_Instr[i])
                                                ram=(Tram[i])
                                                size=(Tsize[i])
                                                done=0 #creating only once , done=1 indicates created and getting out of the loop
                                                for k in range(l): 
                                                        if done ==0:
                                                                extra=[] #temp list
                                                                if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                        V=[mips,ram,size]
                                                                        Vms.append(len(Vms)+1)
                                                                        ####print   "\n\nVms..",i,Vms 
                                                                        vmdict[(Vms[len(Vms)-1])]=V        
                                                                        Vram.append(ram)
                                                                        Vsize.append(size)
                                                                        Vmips.append(mips)
                                                                        Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                        Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]                                                
                                                                        Talloc[Vms[len(Vms)-1]]=Tasks[i]                                          
                                                                        extra.append(Vms[len(Vms)-1])
                                                                        Halloc[k+1]=extra #allocated newly created vm to host and storing that info in halloc
                                                                        ####print   "\n\n",Halloc,Hosts,Hram,Hsize,'\n\n'
                                                                        Vflags.append(1)
                                                                        Vtimer.append(0) #setting newly created vm's vtimer as 0
                                                                        done=1 
                                                                        del(extra)

                                                        else:
                                                                break;
                                                if Tasks[i] not in Talloc.values():
                                                        ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                        dropped_tasks.append(Tasks[i])
                                                        index=Tasks.index(Tasks[i])
                                                        b=Tasks.pop(index)
                                                        Tasks.append(b)
                                                        b=Tram.pop(index)
                                                        Tram.append(b)
                                                        b=Tsize.pop(index)
                                                        Tsize.append(b)
                                                        b=Tno_of_Instr.pop(index)
                                                        Tno_of_Instr.append(b)
                                                        b=TBurst.pop(index)
                                                        TBurst.append(b)
                                                        b=TDL.pop(index)
                                                        TDL.append(b)
                                                        i=i-1
                                                        n=n-1
                                        i=i+1
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  
                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Talloc.keys())
                                valloc=[]
                                i=0
                                #if len of allocted tasks exceeds len of given tasks bring it to len of tasks 'n'
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          

                                ####print   "\n\n",valloc,"\n\n"

                                counter=0 #temp variable
                        #executing in roundrobin fashion with timequantum as TQ1
                                while(h<m):
                                        alreadydone=0
                                        if (TDL[h] > TQ1 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ1+Vtimer[valloc[counter]-1]
                                                
                                                #different cases of calculation of execution times
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TQ1:
                                                        Executiontime = TQ1
                                                if TQ1>TBurst[h] and Executiontime >= TQ1:
                                                        Executiontime = TBurst[h]            
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime #incrementing the vtimer

                                                # ###print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]): #if burstime becomes 0 then remove task from the queue and count the completion time of the task
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1

                                                if (len(Tasks)>0):     #if there are remaining tasks execute round robin again                           
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        TCT[Tasks[h]]=TExec[Tasks[h]]
                                                        ####print   "Execution times",TExec,"\n\n"
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1
                                                
                                        elif (TDL[h] <= TQ1 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0): 
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ1+Vtimer[valloc[counter]-1]
                                                
                                                #different cases of calculation of execution time
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TDL[h]:
                                                        Executiontime = TDL[h]
                                                if TDL[h]>TBurst[h] and Executiontime >= TDL[h]:
                                                        Executiontime = TBurst[h]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                TBurst[h]=TBurst[h]-Executiontime   
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime

                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                Vflags[valloc[counter]-1]=0
                                                counter=counter+1
                                                h=h-1
                                                m=m-1
                                        h=h+1
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        index=Tasks.index(Tasks[h])
                                        b=Tasks.pop(index)
                                        b=Tram.pop(index)
                                        b=Tsize.pop(index)
                                        b=Tno_of_Instr.pop(index)
                                        b=TBurst.pop(index)
        
                                del(Talloc)
                                Talloc={}    
                                count=count+1
      
                     
                        #****************************   COMPLETION OF EXECUTION OF TASKS IN HQ   *********************************                     
                        ####print   Vms,Vram,Vsize
                        ####print   Hosts,Hram,Hsize

                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto
                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'
                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"          
                                for i in range(len(Hosts)):
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]
                                
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize
                                        
                                ###print   "We have following remaining resources after killing extra virtual machines in HQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"

                        #*******************************STARTING EXECUTION OF TASKS IN MQ****************************************************
                        ###print   "Execution of Tasks in MQ......\n\n"

                        #Tasks specifications
                        Tasks = MQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution
                        ###print   "We have following Tasks to be executed in MQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"
                                
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)
                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]

                        #****************now round3 starts
                        count=0
                        Halloc={}
                        while(count<50 and len(Tasks)>0): 
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                while(i<n):
                                        ####print   "\n\n",i,n,"\n\n"        
                                        for j in range(m):
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                                        
                                                if Tasks[i] not in Talloc.values():
                                                        ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                        mips=(Tno_of_Instr[i])
                                                        ram=(Tram[i])
                                                        size=(Tsize[i])
                                                        done=0
                                                        for k in range(l):
                                                                if done==0: 
                                                                        extra=[]
                                                                        if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                                V=[mips,ram,size]
                                                                                Vms.append(len(Vms)+1)
                                                                                ####print   "\n\nVms...",Vms
                                                                                vmdict[(Vms[len(Vms)-1])]=V        
                                                                                Vram.append(ram)
                                                                                Vsize.append(size)
                                                                                Vmips.append(mips)
                                                                                Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                                Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]
                                                                                ####print   "Length\n\n",len(Vms)
                                                                                extra.append(Vms[len(Vms)-1])
                                                                                Halloc[k+1]=extra
                                                                                Talloc[Vms[len(Vms)-1]]=Tasks[i]
                                                                                ####print   "\n\n",Talloc,"\n\n"
                                                                                Vflags.append(1)
                                                                                Vtimer.append(0)
                                                                                done=1
                                                                                del(extra)     
                                                                else:
                                                                        break

                                                        if Tasks[i] not in Talloc.values():
                                                                ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                                dropped_tasks.append(Tasks[i])
                                                                index=Tasks.index(Tasks[i])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                i=i-1
                                                                n=n-1               
                                                                ####print   "I am here\n\n",Tasks,"\n\n"
                                        i=i+1
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  

                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Tasks)
                                valloc=[]
                                i=0
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          
                                ####print   "\n\n",Tasks,valloc,"\n\n"

                                counter=0
                                while(h<m):
                                        alreadydone=0
                                        ####print   "\n\n",valloc,counter,Vtimer,valloc[counter],"\n\n"
                                        ####print   "\n\nVtimer",Tasks[h],Vtimer[valloc[counter]-1],"\n\n" 
                                        if (TDL[h] > TQ2 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ2+Vtimer[valloc[counter]-1]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        ####print   "You are right i am here\n\n"
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,TDL[h],"\n\n"  
                                                if Executiontime > TQ2:
                                                        Executiontime = TQ2
                        #                                ###print   "here here bursttime,executiontime",TBurst[h],Executiontime,"\n\n"                              
                                                if Executiontime>TBurst[h]:
                                                        Executiontime = TBurst[h]
                                                ####print   "The Execution here is :  %d" %Executiontime
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        ####print   "\n\ni m here here here",Tasks[h],TCT[Tasks[h]]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1
                                                if (len(Tasks)>0):
                                                        ####print   "\n\n......",Tasks[h]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        TCT[Tasks[h]]=TExec[Tasks[h]]
                                                        ####print   "Execution times",TExec,"\n\n"
                                                        ####print   "\n\ni m here here",Tasks[h],TCT[Tasks[h]]
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1
                                                
                                        elif (TDL[h] <= TQ2 and TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0): 
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=TQ2+Vtimer[valloc[counter]-1]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        ####print   "You are right i am here\n\n"
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime > TDL[h]:
                                                        Executiontime = TDL[h]
                                                if TDL[h]>TBurst[h] and Executiontime >= TDL[h]:
                                                        Executiontime = TBurst[h]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,TDL[h],"\n\n"    
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                TBurst[h]=TBurst[h]-Executiontime   
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        if Tasks[h] in TCT.keys():
                                                                TCT[Tasks[h]]=TCT[Tasks[h]]+Vtimer[valloc[counter]-1]
                                                        else:                                
                                                                TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                
                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                Vflags[valloc[counter]-1]=0
                                                counter=counter+1
                                                h=h-1
                                                m=m-1
                                        h=h+1
                                
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        index=Tasks.index(Tasks[h])
                                        b=Tasks.pop(index)
                                        b=Tram.pop(index)
                                        b=Tsize.pop(index)
                                        b=Tno_of_Instr.pop(index)
                                        b=TBurst.pop(index)

                                del(Talloc)
                                count=count+1        
                                Talloc={}                
                        ###print   '\n\n',Vtimer,Tasks,TCT,TBurst,TDL,Vflags,TExec,'\n\n'     
                                        
                        ####print   "\n\n",TCT,TExec                    
                        #****************************END OF MQ EXECUTION**************************
                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto

                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'

                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"          
                                for i in range(len(Hosts)):
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]        
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]
                                
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize         
                                ###print   "We have following remaining resources after killing extra virtual machines in MQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        
                        #****************************START OF LQ EXECUTION IN FCFS FASHION                     
                        ###print   "Execution of Tasks in LQ......\n\n"
                        #Tasks specifications
                        Tasks = LQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Talloc={} #contains allocation details of Tasks to Vms during execution 
                        ###print   "We have following Tasks to be executed in LQ with specifications:\nTasks                   :     ",Tasks,"\nRAMs                    :     ",Tram,"\nSizes                   :     ",Tsize,"\nNo of Instructions      :     ",Tno_of_Instr,"\nArrivalTime             :     ",TArrival,"\nBurstTime               :     ",TBurst,"\nDeadLine                :     ",TDL,"\n"    

                        ####print   TBurst     
                        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                        n=len(Tasks)
                        m=len(Vms)
                        l=len(Hosts)
                        Talloc={} #contains allocated tasks
                        Vflags=[0 for i in range(m)]
                        count=0
                        Halloc={}
                        while(count<50 and len(Tasks)>0):     
                                i=0 
                                n=len(Tasks)
                                m=len(Vms)
                                ####print   "\n\n\nEnter for  count = %d\n\n\n" %count
                                ####print   Vflags,Tasks,TBurst,TDL,Tram,Tsize,Tno_of_Instr,Vms,Vram,Vsize,Vmips,"\n\n",Vtimer,"\n\n"
                                while(i<n):
                                        ####print   "\n\n",i,n,"\n\n"        
                                        for j in range(m):
                                                if(Tram[i]<=Vram[j] and Tsize[i]<=Vsize[j] and Tno_of_Instr[i]<=Vmips[j] and Vflags[j]==0):
                                                        Talloc[Vms[j]]=Tasks[i]
                                                        ####print   "\n\n",Talloc,"\n\n"
                                                        Vflags[j]=1
                                                        break
                                        if Tasks[i] not in Talloc.values():
                                                ###print   "Trying to create a new virtual machine for Tasks %s\n" %Tasks[i]
                                                mips=(Tno_of_Instr[i])
                                                ram=(Tram[i])
                                                size=(Tsize[i])
                                                done=0
                                                for k in range(l): 
                                                        if done==0:
                                                                extra=[]
                                                                if mips <= Hmips[k] and ram <= Hram[k] and size <= Hsize[k]:
                                                                        V=[mips,ram,size]
                                                                        Vms.append(len(Vms)+1)
                                                                        vmdict[(Vms[len(Vms)-1])]=V        
                                                                        Vram.append(ram)
                                                                        Vsize.append(size)
                                                                        Vmips.append(mips)
                                                                        Hram[k]=Hram[k]-Vram[len(Vms)-1]
                                                                        Hsize[k]=Hsize[k]-Vsize[len(Vms)-1]
                                                                        extra.append(Vms[len(Vms)-1])
                                                                        Halloc[k+1]=extra
                                                                        Talloc[Vms[len(Vms)-1]]=Tasks[i]
                                                                        Vflags.append(1)
                                                                        Vtimer.append(0)
                                                                        done=1
                                                                        del(extra)
                                                        else:
                                                                break;
                                                if Tasks[i] not in Talloc.values():
                                                        ###print   "Unable to create a new virtual machine for Tasks %s,due to lack of resources,hence waiting for existing Vms to get free\n" %Tasks[i]
                                                        dropped_tasks.append(Tasks[i])
                                                        index=Tasks.index(Tasks[i])
                                                        b=Tasks.pop(index)
                                                        Tasks.append(b)
                                                        b=Tram.pop(index)
                                                        Tram.append(b)
                                                        b=Tsize.pop(index)
                                                        Tsize.append(b)
                                                        b=Tno_of_Instr.pop(index)
                                                        Tno_of_Instr.append(b)
                                                        b=TBurst.pop(index)
                                                        TBurst.append(b)
                                                        b=TDL.pop(index)
                                                        TDL.append(b)
                                                        i=i-1
                                                        n=n-1
                                        i=i+1
                                ###print   "Allocated virtual machines for Tasks for execution are as follows\n",Talloc.keys(),Talloc.values(),"\n\n"                                  
                                ####print   "\n\n\n",Tasks,TDL,TBurst,"\n\n\n"
                                h=0 
                                m=len(Talloc.keys())
                                valloc=[]
                                i=0
                                if m > n:
                                        m=n
                                for i in range(m):              
                                        for k,v in Talloc.items():
                                                if Tasks[i]==v:
                                                        valloc.append(k)          
                                ####print   "\n\n",valloc,"\n\n"
                                counter=0
                                while(h<m):
                                        alreadydone=0
                                        ####print   "\n\nDeadlines",Tasks,Tasks[h],Vtimer[valloc[counter]-1],TDL[h],"\n\n" 
                                        if (TDL[h] > Vtimer[valloc[counter]-1] and TBurst[h]>0):
                                                ####print   "The Tasks entered here is :  %s" %Tasks[h]
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TAT[Tasks[h]] = Vtimer[valloc[counter]-1] 
                                                Executiontime=Vtimer[valloc[counter]-1]+TBurst[h]
                                                if Executiontime>TDL[h] and TDL[h]>Vtimer[valloc[counter]-1]:
                                                        Executiontime = TDL[h] - Vtimer[valloc[counter]-1]
                                                if Executiontime>TBurst[h]:
                                                        Executiontime=TBurst[h]  
                                                Vtimer[valloc[counter]-1]=Vtimer[valloc[counter]-1]+Executiontime
                                                ####print   "The Vtimer here is :  %d" %Vtimer[valloc[counter]-1]
                                                TBurst[h]=TBurst[h]-Executiontime                       
                                                ####print   "here here bursttime,executiontime",TBurst[h],Executiontime,"\n\n"
                                                if (TBurst[h]==0 or TDL[h]<=Vtimer[valloc[counter]-1]):
                                                        TCT[Tasks[h]]=Vtimer[valloc[counter]-1]
                                                        ####print   TCT[Tasks[h]]                                
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        index=Tasks.index(Tasks[h])
                                                        b=Tasks.pop(index)
                                                        b=Tram.pop(index)
                                                        b=Tsize.pop(index)
                                                        b=Tno_of_Instr.pop(index)
                                                        b=TBurst.pop(index)
                                                        b=TDL.pop(index)
                                                        Executiontime=0
                                                        Vflags[valloc[counter]-1]=0
                                                        counter=counter+1
                                                        h=h-1
                                                        m=m-1
                                                        alreadydone=1
                                                if (len(Tasks)>0):
                                                        if Tasks[h] in TExec.keys():
                                                                TExec[Tasks[h]]=TExec[Tasks[h]]+Executiontime
                                                        else:
                                                                TExec[Tasks[h]]=Executiontime
                                                        if alreadydone==0:
                                                                index=Tasks.index(Tasks[h])
                                                                b=Tasks.pop(index)
                                                                Tasks.append(b)
                                                                b=Tram.pop(index)
                                                                Tram.append(b)
                                                                b=Tsize.pop(index)
                                                                Tsize.append(b)
                                                                b=Tno_of_Instr.pop(index)
                                                                Tno_of_Instr.append(b)
                                                                b=TBurst.pop(index)
                                                                TBurst.append(b)
                                                                b=TDL.pop(index)
                                                                TDL.append(b)
                                                                Vflags[valloc[counter]-1]=0
                                                                counter=counter+1
                                                                h=h-1
                                                                m=m-1


                                        else:
                                                ###print   "Task %s cannot be executed...because of low deadline,please extend deadline or increase the priority for the task to execute..\n\n" %Tasks[h]
                                                dropped_tasks.append(Tasks[h])
                                                TCT[Tasks[h]]=0
                                                TExec[Tasks[h]]=0
                                                Vflags[valloc[counter]-1]=0
                                                index=Tasks.index(Tasks[h])
                                                b=Tasks.pop(index)
                                                b=Tram.pop(index)
                                                b=Tsize.pop(index)
                                                b=Tno_of_Instr.pop(index)
                                                b=TBurst.pop(index)
                                                b=TDL.pop(index)
                                                h=h-1
                                                counter=counter+1
                                                m=m-1
                                        h=h+1
                                if len(Talloc.keys())==0:
                                        ###print   "Resources not sufficient to execute Task %s Try giving more resources...\n\n" %Tasks[h]
                                        dropped_tasks.append(Tasks[h])
                                        TCT[Tasks[h]]=0
                                        TExec[Tasks[h]]=0
                                        break     
                                del(Talloc)
                                count=count+1        
                                Talloc={}

                        ####print   TAT
                        #if the task has 0 execution then turn around time and waiting time is equal to deadline
                        for k,v in TCT.items():
                                if TExec[k]==0:
                                        TAT[k] = int(inputdata[k][5])
                                        TTAT[k]= int(inputdata[k][6])
                                        TWT[k] = int(inputdata[k][6])   
                                else:             
                                        TTAT[k] = TCT[k] - TAT[k]               
                                        TWT[k] = TTAT[k] - TExec[k]
                                
                        #calculation of execution times
                        for k in TExec.keys():
                                T=int(TExec[k])/int(inputdata[k][5])
                                T=T*int(inputdata[k][1])
                                TExec[k]=T
                                
                        Tasks=[k for k,v in TCT.items()]
                        l2=[int(inputdata[Tasks[i]][0]) for i in range(len(Tasks))]
                        insertionsort(l2,Tasks) #sorting based on id for proper outputs

                        #*******************displaying output of execution of HQ and MQ and LQ
                        Tram=[int(inputdata[Tasks[i]][2]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        Tsize=[int(inputdata[Tasks[i]][3]) for i in range(len(Tasks))]  #contains size list of Tasks
                        Tno_of_Instr=[int(inputdata[Tasks[i]][1]) for i in range(len(Tasks))]  #contains Number Of Instructions list of Tasks
                        TArrival=[int(inputdata[Tasks[i]][4]) for i in range(len(Tasks))]  #contains Mips list of Tasks
                        TBurst=[int(inputdata[Tasks[i]][5]) for i in range(len(Tasks))]   #contains ram list of Tasks
                        TDL=[int(inputdata[Tasks[i]][6]) for i in range(len(Tasks))]  #contains size list of Tasks
                        TCTime=[int(TCT[Tasks[i]]) for i in range(len(Tasks))] #contains completion time of Tasks
                        TTATime=[int(TTAT[Tasks[i]]) for i in range(len(Tasks))] #contains turnaround time of Tasks
                        TWTime=[int(TWT[Tasks[i]]) for i in range(len(Tasks))] #contains waiting times of Tasks
                        TExecTime=[int(TExec[Tasks[i]]) for i in range(len(Tasks))] #contains execution times of Tasks               
                        ###print   "We have following output after executing Tasks in HQ,MQ and LQ:\nTasks                       :     ",Tasks,"\nRAMs                        :     ",Tram,"\nSizes                       :     ",Tsize,"\nNo of Instructions          :     ",Tno_of_Instr,"\nArrivalTime                 :     ",TArrival,"\nBurstTime                   :     ",TBurst,"\nDeadLine                    :     ",TDL,"\nTasks completionTime        :     ",TCTime,"\nTasks TurnAroundtime        :     ",TTATime,"\nTasks WaitingTime           :     ",TWTime,"\nNo.of Instructions Executed :     ",TExecTime,"\n\n"                      

                        #******************************************
                        #case when extra virtual machines created,hence killing them after the completion of execution of LQ
                        if (len(Halloc.keys())>0):
                                alloctedto = Halloc.keys()
                                NewVms = Halloc.values()
                                ####print   alloctedto
                                ###print   "We have following Vms Now:\nVms       : ",Vms,"\nRAMs      : ",Vram,"\nSizes     : ",Vsize,"\nMIPS      : ",Vmips,"\n",'alloted in the following fashion\nHosts',alloctedto,'<-----Virtual Machines',NewVms,'\n\n'
                                ###print   "Destroying the extra vms created...\nDestroying VM " ,NewVms,"\n\n"               
                                for i in range(len(Hosts)): #caluculation of resources used
                                        if Leftoverram[i+1] > Hram[i]:
                                                Leftoverram[i+1] = Hram[i]
                                        if Leftoversize[i+1] > Hsize[i]:
                                                Leftoversize[i+1] = Hsize[i]      
                                for i in range(len(alloctedto)):
                                        k=alloctedto[i]
                                        index=Halloc[k]
                                        ####print   k,index
                                        addram=Vram[index[0]-1]
                                        addsize=Vsize[index[0]-1]
                                        ####print   addram,addsize
                                        Hram[k-1]=Hram[k-1]+addram
                                        Hsize[k-1]=Hsize[k-1]+addsize
                                        ####print   Hram,Hsize
                                ###print   "We have following remaining resources after killing extra virtual machines in LQ:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                        
                                
                        #************COMPLETION OF ALGORITHM********** 
                        #killing the intially created virtual machines and updating the host machine specifications
                        for i in range(len(Hosts)):
                                
                                ###print   "Virtual machine %d has been destroyed...\n\n" % (i+1)
                                addram=Vram[i]
                                addsize=Vsize[i]
                                ####print   addram,addsize
                                Hram[i]=Hram[i]+addram
                                Hsize[i]=Hsize[i]+addsize
                                ####print   Hram,Hsize        
                                ###print   "We have following resources after destroying of the Virtual machine:\nHosts     : ",Hosts,"\nRAMs      : ",Hram,"\nSizes     : ",Hsize,"\nMIPS      : ",Hmips,"\n"
                                
                        #*****************************************************************                           
                        ###print   "END OF THE ALGORITHM...for time = ", time

                        #****************calculation of percentage of utilization of resources*****************************
                        Usedram={}
                        Usedsize={}

                        for i in range(len(Hosts)):
                                Usedram[i+1]=Hram[i]-Leftoverram[i+1]
                                Usedsize[i+1]=Hsize[i]-Leftoversize[i+1]


                        percentUsedram = (sum(Usedram.values())/sum(Hram))*100 
                        percentUsedsize = (sum(Usedsize.values())/sum(Hsize))*100 

                        ####print   percentUsedram,percentUsedsize 
                        total=percentUsedram+percentUsedsize
                        #********************************************

                        ####print  ing the results
                        ###print   "ResultAnalysis\n\n"
                        ###print   "Average Turnaround Time                 :          %f" %(sum(TTATime)/len(TTATime))
                        ###print   "Average Waiting Time                    :          %f" %(sum(TWTime)/len(TWTime))
                        ###print   "Total Number Of Instructions Executed   :          %d" % (sum(TExecTime))
                        ###print   "Given Total Number Of Instructions      :          %d" % (sum(Tno_of_Instr))
                        ###print   "percentage of utilization of resources  :          %f\n\n" % ((total)/2)

                        #******************************************
                        #writing the outputs to output file
                        # filename='outputDAC'+filename
                        # with open(filename,'w') as output_file:
                        #         for i in range(len(TTATime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TTATime[i])  #writing into the file using , separated
                        #                 else :
                        #                         output_file.write("%d," %TTATime[i])
                        #         for i in range(len(TWTime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TWTime[i])  
                        #                 else :
                        #                         output_file.write("%d," %TWTime[i])
                        #         for i in range(len(TExecTime)):
                        #                 if i==len(TTATime)-1:
                        #                         output_file.write("%d\n" %TExecTime[i])  
                        #                 else :            
                        #                         output_file.write("%d," %TExecTime[i])

                        ###print   "After time = ",time
                        ###print   "dropped tasks  = ",dropped_tasks
                        completed_tasks = np.setdiff1d(np.asarray(local_task_buffer),np.asarray(dropped_tasks))
                        global_task_buffer = global_task_buffer[window_length:]
                        global_task_buffer = dropped_tasks + global_task_buffer
                        ###print   "gtb"
                        ###print   global_task_buffer
                        window_length +=1
                        ###print   "*************\n"


                        # dropped_tasks_id = random.randint(0,window_length-1)
                        # ###print   "dropped task id =",dropped_tasks_id
                        #dropped_tasks.append(global_task_buffer[dropped_tasks_id])
                        avg_turnaround_time.append(sum(TTATime)/len(TTATime))
                        avg_waiting_time.append(sum(TWTime)/len(TWTime))
                        percent_execution.append((sum(TExecTime)/sum(Tno_of_Instr)) * 100)
                        completedtasks.append(len(completed_tasks))
                        totaltasks.append(len(local_task_buffer))
                
        # print("I am here check",counttemp)
        counttemp +=1
        if(counttemp>100):
                # print("Invalid parameter matching!!.. exiting execution..")
                break
        


###print   "ATT....list...", avg_turnaround_time
###print  "Running...Dynamic WFS..."
#pritn "Results of Dynamic WFS..."
###print   "ATT....overall...",sum(avg_turnaround_time)/len(avg_turnaround_time)
###print   "AWT....list...", avg_waiting_time

for i in range(1, len(avg_waiting_time)):
        avg_waiting_time[i] = avg_waiting_time[i] + avg_waiting_time[i-1]
###print   "AWT....list...", avg_waiting_time
###print   "AWT....overall...",sum(avg_waiting_time)/len(avg_waiting_time)
# for i in completedtasks:
#         ###print   "Completed...Tasks...",i

# for i in gtb_global:
#         ###print   "Global...Tasks...",i

###print   "Percetage of Execution...", sum(percent_execution)/len(percent_execution)
              
#*****************Tasks sorting based on priority and storing into a list called local_task_buffer     
#used insertionsort for all kinds of sorting that take place in the algorithm
#function for insertionsort
#print len(completedtasks), len(totaltasks)
#printlen(completedtasks), len(totaltasks)
from tabulate import tabulate
# if filename == "Testcasesall/testcase1_tasks10.txt":
# print"\nWFS Multi results......."
print filename,"... GTB: ",global_buffer_size,"... LTB: ",initial_window_length
# print tabulate([['Dynamic WFS(Multi)',filename,sum(avg_turnaround_time)/len(avg_turnaround_time),sum(avg_waiting_time)/len(avg_waiting_time),time,sum(percent_execution)/len(percent_execution)]],headers=['Alg ', 'Ttcse', 'AvgTAT', 'AvgWT','#Tstmps', '% exec'], tablefmt='orgtbl')
print(wlength)
# # else:
#     #print  tabulate([['Dynamic WFS',filename,sum(avg_turnaround_time)/len(avg_turnaround_time),sum(avg_waiting_time)/len(avg_waiting_time),time,sum(percent_execution)/len(percent_execution)]], tablefmt='orgtbl')
#print "\n"
#for i in range(time):
        #print  tabulate([[i+1,completedtasks[i],totaltasks[i]]],headers=['Time', '# of completed tasks','# of total tasks sent'], tablefmt='orgtbl')

#print "\n"
#print completedtasks
#print totaltasks
#print wlength


# import csv
# with open('allresults.csv', 'a') as csvfile:  
#     # creating a csv writer object  
#     csvwriter = csv.writer(csvfile)   
        
#     # writing the data rows  
#     f = filename
#     f1=f[:-4]
#     f2 = int(f1[-3:])
#     if (f2==0):
#         f2=1000
    
#     queue = 'H'*val1 + 'M'*val2 + 'L'
#     csvwriter.writerow([filename[13:],f2,'Additive',global_buffer_size,initial_window_length,time,sum(avg_turnaround_time)/len(avg_turnaround_time),sum(avg_waiting_time)/len(avg_waiting_time),sum(percent_execution)/len(percent_execution),queue]) 