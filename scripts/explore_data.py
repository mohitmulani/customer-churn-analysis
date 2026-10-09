import pandas as pd

df=pd.read_csv("data/raw/Churn_Modelling.csv")
df.info()
df.describe()

print(df.head())
print(df.shape)
print(df.columns)
print(df["Exited"].value_counts())

churn_rate = df["Exited"].mean()*100
print(churn_rate)

print(df["Geography"].value_counts())

print(df["Gender"].value_counts())

print(df["NumOfProducts"].value_counts().sort_index())

print(df.groupby("Geography")["Exited"].mean()*100)

print(df.groupby("Gender")["Exited"].mean()*100)

print(df.groupby("NumOfProducts")["Exited"].mean()*100)

product_analysis = df.groupby("NumOfProducts").agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)

product_analysis["churn_rate"] = product_analysis["churn_rate"]*100
print(product_analysis)

four_products = df[df["NumOfProducts"]==4]
print(four_products.head())
print(four_products.shape)
print(four_products["Exited"].value_counts())

print(four_products[[
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "EstimatedSalary",
    "IsActiveMember",
    "HasCrCard"
]].describe())

print(four_products["Geography"].value_counts())
print(four_products["IsActiveMember"].value_counts())

product_activity = df.groupby([
    "NumOfProducts","IsActiveMember"
]).agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)

product_activity["churn_rate"]=product_activity["churn_rate"]*100
print(product_activity)

print("Duplicate rows:", df.duplicated().sum())

print("Duplicate Customer IDs:", df["CustomerId"].duplicated().sum())

print("Geography:", df["Geography"].unique())

print("Gender:", df["Gender"].unique())

print("HasCrCard:", df["HasCrCard"].unique())

print("IsActiveMember:", df["IsActiveMember"].unique())

print("Exited:", df["Exited"].unique())

print("NumOfProducts:", df["NumOfProducts"].unique())

print("Age range:", df["Age"].min(), df["Age"].max())

print("Credit Score range:", df["CreditScore"].min(), df["CreditScore"].max())

older_customers = df[df["Age"]>50]
print(older_customers.head())
print(older_customers.shape)

german_customers = df[df["Geography"]=="Germany"]
print(german_customers.head())
print(german_customers.shape)

german_churned = df[(df["Geography"]=="Germany") & (df["Exited"]==1)]
print(german_churned.head())
print(german_churned.shape)

old_and_inactive = df[(df["Age"]>50) & (df["IsActiveMember"]==0)]
print(old_and_inactive.head())
print(old_and_inactive.shape)

overall_churn = df["Exited"].mean()*100
old_inactive_churn = old_and_inactive["Exited"].mean()*100
print("Overall churn rate:", overall_churn)
print("Older inactive churn rate:", old_inactive_churn)

print("Older inactive customers: ",old_and_inactive["CustomerId"].count())
print("Older inactive customers: ",old_and_inactive["Exited"].sum())

old_inactive_geo = old_and_inactive.groupby("Geography")["Exited"].agg(
    customer_count = "count",
    churned_customers = "sum",
    churn_rate= "mean"
)

old_inactive_geo["churn_rate"]*=100
print(old_inactive_geo)

old_inactive_credit = old_and_inactive.copy()

old_inactive_credit["CreditScoreBand"] = pd.cut(
    old_inactive_credit["CreditScore"],
    bins=[0, 499, 599, 699, 850],
    labels=["Poor", "Fair", "Good", "Very Good"]
)

credit_analysis = old_inactive_credit.groupby("CreditScoreBand",observed=True).agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)

credit_analysis["churn_rate"]*=100
print(credit_analysis)

product_analysis_old = old_inactive_credit.groupby("NumOfProducts").agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)

product_analysis_old["churn_rate"]*=100
print(product_analysis_old)

old_inactive_tenure = old_and_inactive.copy()

old_inactive_tenure["TenureBand"] = pd.cut(
    old_inactive_tenure["Tenure"],
    bins=[-1,2,5,7,10],
    labels=["0-2 years","3-5 years", "6-7 years", "8-10 years"]
)
tenure_analysis = old_inactive_tenure.groupby("TenureBand",observed=True).agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)
tenure_analysis['churn_rate']*=100
print(tenure_analysis)

age_activity_analysis = df.groupby(
    [
        pd.cut(
            df['Age'],
            bins=[0,50,100],
            labels=["50 or younger", "Over 50"]
        ),
        "IsActiveMember"
    ]
).agg(
    customer_count = ("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)
age_activity_analysis['churn_rate']*=100
print(age_activity_analysis)

old_inactive_balance=old_and_inactive.copy()

old_inactive_balance["BalanceBand"] = pd.cut(
    old_inactive_balance["Balance"],
    bins=[-1,50000,100000,150000,float("inf")],
    labels=["0-50k","50k-100k","100k-150k","150k+"]
)

balance_analysis = old_inactive_balance.groupby("BalanceBand",observed=True).agg(
    customer_count=("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)
balance_analysis["churn_rate"] *= 100
print(balance_analysis)

gender_analysis = old_and_inactive.groupby("Gender").agg(
    customer_count=("CustomerId","count"),
    churned_customers = ("Exited","sum"),
    churn_rate = ("Exited","mean")
)
gender_analysis["churn_rate"] *=100
print(gender_analysis)

print(df.isnull().sum())

print(df.describe().T)

zero_balance = df[df["Balance"]==0]

print("Zero balance customers: ",len(zero_balance))

zero_balance_churn = zero_balance["Exited"].mean() * 100

print("Zero balance churn rate:", zero_balance_churn)

print("Overall churn rate:", df["Exited"].mean() * 100)
print("Zero balance churn rate:", zero_balance_churn)

nonzero_balance = df[df["Balance"] > 0]

print("Non-zero balance customers:", len(nonzero_balance))

nonzero_balance_churn = nonzero_balance["Exited"].mean() * 100

print("Non-zero balance churn rate:", nonzero_balance_churn)
print("Overall churn rate:", df["Exited"].mean() * 100)
print("Zero balance churn rate:", zero_balance_churn)
print("Non-zero balance churn rate:", nonzero_balance_churn)

print(df["Geography"].value_counts())
print()
print(df["Gender"].value_counts())
print()
print(df["NumOfProducts"].value_counts().sort_index())