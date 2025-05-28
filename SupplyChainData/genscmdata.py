import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

# Constants
NUM_ROWS = 10000
NUM_PRODUCTS = 100
NUM_CUSTOMERS = 500
NUM_STORES = 10
NUM_SUPPLIERS = 20
NUM_DAYS = 365

# Date Dimension
start_date = datetime.today() - timedelta(days=NUM_DAYS)
dates = [start_date + timedelta(days=i) for i in range(NUM_DAYS)]
dim_date = pd.DataFrame({
    'DateKey': [int(date.strftime('%Y%m%d')) for date in dates],
    'Date': dates,
    'Year': [date.year for date in dates],
    'Month': [date.month for date in dates],
    'Day': [date.day for date in dates],
    'Weekday': [date.strftime('%A') for date in dates]
})

# Product Dimension
dim_product = pd.DataFrame({
    'ProductKey': range(1, NUM_PRODUCTS + 1),
    'ProductName': [fake.word().capitalize() for _ in range(NUM_PRODUCTS)],
    'Category': [random.choice(['Electronics', 'Clothing', 'Groceries']) for _ in range(NUM_PRODUCTS)],
    'SubCategory': [random.choice(['Mobile', 'Shirt', 'Vegetables']) for _ in range(NUM_PRODUCTS)],
    'Brand': [fake.company() for _ in range(NUM_PRODUCTS)],
    'UnitCost': np.random.uniform(5, 500, NUM_PRODUCTS).round(2)
})

# Customer Dimension
dim_customer = pd.DataFrame({
    'CustomerKey': range(1, NUM_CUSTOMERS + 1),
    'FirstName': [fake.first_name() for _ in range(NUM_CUSTOMERS)],
    'LastName': [fake.last_name() for _ in range(NUM_CUSTOMERS)],
    'Gender': [random.choice(['Male', 'Female']) for _ in range(NUM_CUSTOMERS)],
    'City': [fake.city() for _ in range(NUM_CUSTOMERS)],
    'Region': [fake.state() for _ in range(NUM_CUSTOMERS)]
})

# Store Dimension
dim_store = pd.DataFrame({
    'StoreKey': range(1, NUM_STORES + 1),
    'StoreName': [f"{fake.company()} Store" for _ in range(NUM_STORES)],
    'City': [fake.city() for _ in range(NUM_STORES)],
    'Region': [fake.state() for _ in range(NUM_STORES)]
})

# Supplier Dimension
dim_supplier = pd.DataFrame({
    'SupplierKey': range(1, NUM_SUPPLIERS + 1),
    'SupplierName': [fake.company() for _ in range(NUM_SUPPLIERS)],
    'Country': [fake.country() for _ in range(NUM_SUPPLIERS)],
    'ContactName': [fake.name() for _ in range(NUM_SUPPLIERS)]
})

# Fact Table
fact_sales = pd.DataFrame({
    'SalesID': range(1, NUM_ROWS + 1),
    'DateKey': [int(random.choice(dates).strftime('%Y%m%d')) for _ in range(NUM_ROWS)],
    'ProductKey': np.random.randint(1, NUM_PRODUCTS + 1, NUM_ROWS),
    'CustomerKey': np.random.randint(1, NUM_CUSTOMERS + 1, NUM_ROWS),
    'StoreKey': np.random.randint(1, NUM_STORES + 1, NUM_ROWS),
    'SupplierKey': np.random.randint(1, NUM_SUPPLIERS + 1, NUM_ROWS),
    'Quantity': np.random.randint(1, 10, NUM_ROWS)
})

# Join UnitCost from dim_product
fact_sales = fact_sales.merge(dim_product[['ProductKey', 'UnitCost']], on='ProductKey', how='left')
fact_sales['UnitPrice'] = (fact_sales['UnitCost'] * np.random.uniform(1.1, 1.5, NUM_ROWS)).round(2)
fact_sales['Discount'] = np.random.choice([0, 5, 10, 15], size=NUM_ROWS)
fact_sales['TotalAmount'] = (fact_sales['Quantity'] * fact_sales['UnitPrice'] - fact_sales['Discount']).round(2)
fact_sales['CostPrice'] = (fact_sales['Quantity'] * fact_sales['UnitCost']).round(2)

# Export to CSV
dim_date.to_csv("DimDate.csv", index=False)
dim_product.to_csv("DimProduct.csv", index=False)
dim_customer.to_csv("DimCustomer.csv", index=False)
dim_store.to_csv("DimStore.csv", index=False)
dim_supplier.to_csv("DimSupplier.csv", index=False)
fact_sales.to_csv("FactSales.csv", index=False)

