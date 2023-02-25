


### Task Allocation to robot bidders


### GREEDY TASK ALLOCATION #####
def broadcast_bid(task_list, T_robot):

    # for i, task in enumerate(task_list):
    #  #print("Task Broadcasted", task)
    #  for j, tr in enumerate(T_robot):
    #     print(i, j)
    #     break
    #     print(T_robot[j].bid("test task"))

    for i, tr in enumerate(T_robot):
        for j, task in enumerate(task_list):
            print(i,j)
            (T_robot[i].bid(task))
            break






### PROACTIVE TASK ALLOCATION#####