from Greedy_implementation.SM10_Product_Task import Product

product = Product(pv_Id=1, pi_Id=1, task_list=[[1,11], [12 ,11]],
                            inProduction=True, finished=False, last_instance=1, robot=0,
                            wk=0,released=False)


print(product.task_list[0])