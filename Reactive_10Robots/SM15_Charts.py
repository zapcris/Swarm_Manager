import pandas as pd
from dataclasses import dataclass
from typing import List

from Reactive_10Robots.SM10_Product_Task import Product


def save_products_to_excel(products: List[Product], excel_file_path: str, product_stats, prod_name, makespan,
                           data_snapshot):
    # Create an Excel writer object
    excel_writer = pd.ExcelWriter(excel_file_path, engine='xlsxwriter')

    # Save each product as a separate sheet
    for product in products:
        data = [[] for i in range(100)]
        data2 = [[] for i in range(100)]
        column = ["Station", "Position", "Start time", "Stop time", "Total in seconds"]
        column2 = ["Product", "Makespan", "Transfer time", "Blockage time", "Process time", "Idle time"]
        column3 = ["Time_stamp", "Active_Products", "Throughput"]

        for i, obj in enumerate(product.tracking):
            if obj.sts == "Source":
                data[i].append(obj.sts)
                data[i].append(None)
                data[i].append(obj.tstamp.strftime("%m/%d/%Y, %H:%M:%S"))
                data[i].append(None)
                data[i].append(None)
            elif obj.sts == "Transfer":
                str = f"{obj.sts}"
                data[i].append(str)
                str2 = f"{obj.sts} to workstation {obj.drop} by Robot {obj.tr_no} "
                data[i].append(str2)
                data[i].append(obj.stime)
                data[i].append(obj.etime)
                data[i].append(int(obj.dtime))
            elif obj.sts == "Wait":
                str = f"{obj.sts}"
                data[i].append(str)
                str2 = f"{obj.sts} at workstation {obj.drop} by Robot {obj.tr_no} "
                data[i].append(str2)
                data[i].append(obj.stime)
                data[i].append(obj.etime)
                data[i].append(int(obj.dtime))
            elif obj.sts == "Process":
                str = f"{obj.sts}"
                data[i].append(str)
                str2 = f"{obj.sts} at workstation {obj.wk_no}  "
                data[i].append(str2)
                data[i].append(obj.stime)
                data[i].append(obj.etime)
                data[i].append(int(obj.dtime))
            elif obj.sts == "Sink":
                data[i].append(obj.sts)
                data[i].append(None)
                data[i].append(None)
                data[i].append(obj.tstamp.strftime("%m/%d/%Y, %H:%M:%S"))

        for i, (name, times, span) in enumerate(zip(prod_name, product_stats, makespan)):
            data2[i].append(name)
            data2[i].append(int(span))
            data2[i].append(int(times[0]))
            data2[i].append(int(times[1]))
            data2[i].append(int(times[2]))
            data2[i].append(int(times[3]))

        prod_summary = [ele for ele in data2 if ele != []]
        print(prod_summary)
        sorted_list = sorted(prod_summary, key=lambda x: x[0])
        print(sorted_list)

        throughput_data = [0 for o in data_snapshot]
        for i, (snap, thr_data) in enumerate(zip(data_snapshot, throughput_data)):
            throughput = 0
            for x in prod_summary:
                p = []
                print("Test this", x)
                for char in x[0]:
                    if char.isdigit():
                        p.append(int(char))
                    if p in snap[1]:
                        throughput += 10 / x[1]
            d = [snap[0], snap[1], throughput]
            print(d)
            throughput_data[i] = d

        # df = pd.DataFrame(data, columns=["Product Tracking"])
        df = pd.DataFrame(data, columns=column)
        df2 = pd.DataFrame(sorted_list, columns=column2)
        df3 = pd.DataFrame(throughput_data, columns=column3)
        # df_transposed = df.transpose()
        str_name = f"{product.pv_Id}_{product.pi_Id}"
        sheet_name = str_name.replace(' ', '_')  # Use a modified name as the sheet name
        df2.to_excel(excel_writer, sheet_name="summary", index=False, header=True)
        df3.to_excel(excel_writer, sheet_name="throughput", index=False, header=True)
        df.to_excel(excel_writer, sheet_name=sheet_name, index=False, header=True)

    # Save the Excel file
    excel_writer._save()
    print(f'Data has been saved to {excel_file_path}')


def create_barchart():
    print("")


if __name__ == "__main__":
    # List of Product objects
    # products = [
    #     Product('Product 1', 10.0, 5),
    #     Product('Product 2', 20.0, 8),
    #     Product('Product 3', 15.0, 12)
    # ]

    p1 = Product(pv_Id=1, pi_Id=1, mission_list=[[11, 1], [2, 5]], inProduction=False, finished=False, last_instance=1,
                 robot=0,
                 wk=0, released=False, tracking=[1, 4, 5, 7], priority=1, current_mission=[], task=[])
    p2 = Product(pv_Id=2, pi_Id=1, mission_list=[[11, 2], [2, 8]], inProduction=False, finished=False, last_instance=1,
                 robot=0,
                 wk=0, released=False, tracking=[1, 4, 6, 6], priority=1, current_mission=[], task=[])
    p3 = Product(pv_Id=3, pi_Id=1, mission_list=[[11, 3], [3, 6]], inProduction=False, finished=False, last_instance=1,
                 robot=0,
                 wk=0, released=False, tracking=[1, 4, 5, 6], priority=1, current_mission=[], task=[])
    products = [p1, p2, p3]
    # Define the Excel file path with the '.xlsx' extension
    excel_file_path = 'products.xlsx'  # Use .xlsx for Excel format

    # Save the products to the Excel file
    save_products_to_excel(products, excel_file_path)
