
from Greedy_implementation.SM10_Product_Task import  Product


production_order = {
    "Name": "Test",
    "PV": [1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    "sequence": [[11, 1, 12], #[11, 1, 7, 5, 6, 8, 9, 12]
                 [11, 2, 4, 6, 8, 12],
                 [11, 3, 5, 6, 8, 9, 7, 12],
                 [11, 5, 7, 8, 9, 12],
                 [11, 1, 4, 5, 7, 8, 9, 12],
                 [11, 2, 5, 6, 8, 3, 12],
                 [11, 3, 6, 8, 2, 4, 3, 12],
                 [11, 4, 5, 6, 8, 7, 12],
                 [11, 3, 4, 6, 1, 8, 9, 12],
                 [11, 2, 4, 6, 8, 5, 7, 9, 12]
                 ],

    "PI": [2, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "Wk_type": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3],
    "Process_times": [[4, 4, 4, 4, 4, 4, 4, 4, 4, 4], #[20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [10, 10, 10, 10, 10, 10, 10, 10, 10, 10], #[20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [10, 10, 10, 10, 10, 10, 10, 10, 10, 10], #[20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60],
                      [20, 30, 40, 50, 20, 40, 80, 70, 30, 60]
                      ]
}

#
# def initialize_production(self_order):
#     self_robots = [100,200,300]
#     remaining_order = []
#     active_products = []
#     for i, pv in enumerate(self_order["PV"]):
#         if pv == 1:
#             remaining_order.append(i+1)
#     print("Remaining order list", remaining_order)
#
#     #### Initialization of Products based on total available robots ######
#     if len(remaining_order) >= len(self_robots):
#         for i, r in enumerate(self_robots):
#             ########### encapsulated task sequence object for every product instance #######
#             variant = remaining_order.pop(0)
#             p = Product(pv_Id=variant, pi_Id=1, task_list=[], inProduction=True, finished=False,
#                         last_instance=1, robot=0, wk=0, released=False)
#             print(f"First instance of product type {variant} and product {p} generated for production")
#             active_products.append(p)
#
#     else:  ###### if total robots greater than product variants############
#         iterate_order = remaining_order
#         for i in range(len(iterate_order)):
#             variant = remaining_order.pop(0)
#             p = Product(pv_Id=variant, pi_Id=1, task_list=[], inProduction=True, finished=False,
#                         last_instance=1, robot=0, wk=0, released=False)
#             print(f"First instance of product type {variant} and product {p} generated for production")
#             active_products.append(p)
#     print("Finally remaining List", remaining_order)


# initialize_production(production_order)

a = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3]

print(a[-1])