import Greedy_implementation.SM04_Task_Planner
import Greedy_implementation.SM05_Scheduler
import Greedy_implementation.SM07_Robot_agent

### Initialize Reactive Scheduler
GreedyScheduler = Greedy_implementation.SM05_Scheduler.Scheduling_agent(
    order=Greedy_implementation.SM04_Task_Planner.order,
    product_task=Greedy_implementation.SM04_Task_Planner.Product_task,
    data_opcua=Greedy_implementation.SM07_Robot_agent.data_opcua,
    T_robot=Greedy_implementation.SM07_Robot_agent.T_robot
)
