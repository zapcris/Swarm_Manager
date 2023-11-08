
from pymongo import MongoClient, errors
import tkinter as tk
from tkinter import StringVar, messagebox


# def database():
#     try:
#         # replace username and password into your details
#         cluster = "mongodb+srv://akshayavhad89:akshay@cluster0.w9kab.mongodb.net/swarm_production?retryWrites=true&w=majority"
#         client = MongoClient(cluster)
#         db = client.swarm_production
#         # db = client.your_database_name  #other way to create database
#         collection = db.orderlist  # create a collection from the database
#         return collection  # return database so that functions from button can perform CRUD operation
#     except errors.ConfigurationError:
#         # database can be accessed only if you have active internet connection, this will prompt user the error,
#         # if user is not connected to internet
#         messagebox.showerror("Network Error", "No internet connection")