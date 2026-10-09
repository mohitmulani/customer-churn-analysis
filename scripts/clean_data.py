import pandas as pd

df = pd.read_csv("data/raw/Churn_Modelling.csv")

df = df.drop(columns=["RowNumber","Surname"])
print(df.columns)
print(df.shape)

print(df.dtypes)

print(df["Geography"].unique())
print(df["Gender"].unique())
print(df["HasCrCard"].unique())
print(df["IsActiveMember"].unique())
print(df["Exited"].unique())

print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Customer IDs:", df["CustomerId"].duplicated().sum())

print("CreditScore range:", df["CreditScore"].min(), "to", df["CreditScore"].max())
print("Age range:", df["Age"].min(), "to", df["Age"].max())
print("Tenure range:", df["Tenure"].min(), "to", df["Tenure"].max())
print("NumOfProducts range:", df["NumOfProducts"].min(), "to", df["NumOfProducts"].max())
print("Balance range:", df["Balance"].min(), "to", df["Balance"].max())
print("EstimatedSalary range:", df["EstimatedSalary"].min(), "to", df["EstimatedSalary"].max())

print("Total missing values:", df.isnull().sum().sum())

df["AgeBand"] = pd.cut(
    df["Age"],
    bins=[0,30,40,50,60,100],
    labels=["18-30","31-40","41-50","51-60","61+"]
)
print(df[["Age", "AgeBand"]].head(10))

print(df["AgeBand"].value_counts().sort_index())

df["ActivityStatus"] = df["IsActiveMember"].map(
    {
        0:"Inactive",
        1:"Active"
    }
)

print(df[["IsActiveMember", "ActivityStatus"]].head(10))
print(df["ActivityStatus"].value_counts())

df["CreditScoreBand"] = pd.cut(
    df["CreditScore"],
    bins=[0,499,599,699,850],
    labels = ["Poor","Fair","Good","Very Good"]
)
print(df[["CreditScore", "CreditScoreBand"]].head(10))
print(df["CreditScoreBand"].value_counts().sort_index())

df["BalanceStatus"] = df["Balance"].apply(
    lambda x: "Zero Balance" if x==0 else "Non-zero Balance"
)
print(df[["Balance", "BalanceStatus"]].head(10))
print(df["BalanceStatus"].value_counts())

print("Final shape:", df.shape)
print("Final columns:")
print(df.columns.tolist())

df.to_csv(
    "data/processed/customer_churn_clean.csv",
    index=False
)

import os

print(os.path.exists("data/processed/customer_churn_clean.csv"))

clean_df = pd.read_csv(
    "data/processed/customer_churn_clean.csv"
)

print(clean_df.shape)
print(clean_df.head())

churn_rate = clean_df["Exited"].mean() * 100

print(f"Overall churn rate: {churn_rate:.2f}%")
print(clean_df["Exited"].value_counts())

geography_analysis = clean_df.groupby("Geography").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

geography_analysis["churn_rate"] *= 100

print(geography_analysis)

gender_analysis = clean_df.groupby("Gender").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

gender_analysis["churn_rate"] *= 100

print(gender_analysis)

age_analysis = clean_df.groupby("AgeBand", observed=True).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

age_analysis["churn_rate"] *= 100

print(age_analysis)

age_activity_analysis = clean_df.groupby(
    ["AgeBand", "ActivityStatus"],
    observed=True
).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

age_activity_analysis["churn_rate"] *= 100

print(age_activity_analysis)

product_analysis = clean_df.groupby("NumOfProducts").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

product_analysis["churn_rate"] *= 100

print(product_analysis)

three_products = clean_df[clean_df["NumOfProducts"] == 3]

print("Shape:", three_products.shape)

print("\nActivity:")
print(three_products["ActivityStatus"].value_counts())

print("\nGeography:")
print(three_products["Geography"].value_counts())

print("\nAge:")
print(three_products["Age"].describe())

print("\nCredit Score:")
print(three_products["CreditScore"].describe())

print("\nBalance:")
print(three_products["Balance"].describe())

three_product_activity = three_products.groupby("ActivityStatus").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

three_product_activity["churn_rate"] *= 100

print(three_product_activity)

three_product_geo = three_products.groupby("Geography").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

three_product_geo["churn_rate"] *= 100

print(three_product_geo)

three_product_gender = three_products.groupby("Gender").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

three_product_gender["churn_rate"] *= 100

print(three_product_gender)

credit_analysis = clean_df.groupby("CreditScoreBand", observed=True).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

credit_analysis["churn_rate"] *= 100

print(credit_analysis)

balance_analysis = clean_df.groupby("BalanceStatus").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

balance_analysis["churn_rate"]*=100
print(balance_analysis)

tenure_analysis = clean_df.groupby("Tenure").agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

tenure_analysis["churn_rate"] *= 100

print(tenure_analysis)

geo_activity_analysis = clean_df.groupby(
    ["Geography", "ActivityStatus"]
).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

geo_activity_analysis["churn_rate"] *= 100

print(geo_activity_analysis)

age_geo_analysis = clean_df.groupby(
    ["AgeBand", "Geography"],
    observed=True
).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

age_geo_analysis["churn_rate"] *= 100

print(age_geo_analysis)

older_customers = clean_df[
    clean_df["AgeBand"].isin(["51-60", "61+"])
]

older_analysis = older_customers.groupby(
    ["AgeBand", "Geography", "ActivityStatus"],
    observed=True
).agg(
    customer_count=("CustomerId", "count"),
    churned_customers=("Exited", "sum"),
    churn_rate=("Exited", "mean")
)

older_analysis["churn_rate"] *= 100

print(older_analysis)

print("=== Geography ===")
print(geography_analysis)

print("\n=== Gender ===")
print(gender_analysis)

print("\n=== Credit Score ===")
print(credit_analysis)

print("\n=== Balance ===")
print(balance_analysis)

print("\n=== Products ===")
print(product_analysis)

print("\n=== Tenure ===")
print(tenure_analysis)