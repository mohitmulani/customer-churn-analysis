SELECT
    COUNT(*) AS total_rows,
    COUNT(CustomerId) AS customer_ids,
    COUNT(Geography) AS geography_values,
    COUNT(Exited) AS exited_values
FROM customer_churn_clean;

SELECT
    Geography,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY Geography;

SELECT
    Gender,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY Gender;

SELECT
    AgeBand,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY AgeBand
ORDER BY churn_rate;

SELECT
    AgeBand,
    ActivityStatus,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY AgeBand, ActivityStatus
ORDER BY churn_rate;

SELECT
    NumOfProducts,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY NumOfProducts
HAVING COUNT(*)>100 
AND 
SUM(Exited) * 100.0 / COUNT(*) >20
ORDER BY churn_rate;

WITH CTE AS(
SELECT
    AgeBand,
    ActivityStatus,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY AgeBand, ActivityStatus)
SELECT AgeBand, ActivityStatus, total_customers, churned_customers, churn_rate
FROM CTE
WHERE total_customers>=100
AND
churn_rate>30
ORDER BY churn_rate;

WITH CTE AS(
SELECT
    AgeBand,
    ActivityStatus,
    COUNT(*) AS total_customers,
    SUM(Exited) AS churned_customers,
    CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
FROM customer_churn_clean
GROUP BY AgeBand, ActivityStatus)
SELECT AgeBand, ActivityStatus, total_customers, churned_customers, churn_rate
FROM CTE
WHERE total_customers>=100
AND
churn_rate>30
ORDER BY churned_customers DESC;

SELECT Geography,
count(*) as total_customers,
sum(exited) as churned_customers,
CAST(
    SUM(Exited) * 100.0 / COUNT(*)
    AS DECIMAL(5,2)
) AS churn_rate
from customer_churn_clean
WHERE AgeBand IN ('51-60', '61+')
  AND ActivityStatus = 'Inactive'
group by Geography
having count(*)>=50
order by churn_rate desc;

select AgeBand,
sum(case when ActivityStatus = 'Active' then 1 else 0 end) as Active_Customers,
sum(case when ActivityStatus = 'Inactive' then 1 else 0 end) as Inactive_Customers,
sum(case when ActivityStatus = 'Active' and Exited = 1 then 1 else 0 end) as Active_Churned,
sum(case when ActivityStatus = 'Inactive' and Exited = 1 then 1 else 0 end) as Inactive_Churned
from customer_churn_clean
group by AgeBand;

select AgeBand,
sum(case when ActivityStatus = 'Active' then 1 else 0 end) as Active_Customers,
sum(case when ActivityStatus = 'Inactive' then 1 else 0 end) as Inactive_Customers,
sum(case when ActivityStatus = 'Active' and Exited = 1 then 1 else 0 end) as Active_Churned,
sum(case when ActivityStatus = 'Inactive' and Exited = 1 then 1 else 0 end) as Inactive_Churned,
Cast(
sum(case when ActivityStatus = 'Active' and Exited = 1 then 1 else 0 end)*100.00/
sum(case when ActivityStatus = 'Active' then 1 else 0 end) as decimal(5,2)) as Active_Churn_Rate,
Cast(
sum(case when ActivityStatus = 'Inactive' and Exited = 1 then 1 else 0 end)*100.00/
sum(case when ActivityStatus = 'Inactive' then 1 else 0 end) as decimal(5,2)) as Inactive_Churn_Rate
from customer_churn_clean
group by AgeBand;


WITH segment_analysis AS (
    SELECT
        Geography,
        AgeBand,
        ActivityStatus,
        COUNT(*) AS total_customers,
        SUM(Exited) AS churned_customers,
        CAST(
            SUM(Exited) * 100.0 / COUNT(*)
            AS DECIMAL(5,2)
        ) AS churn_rate
    FROM customer_churn_clean
    GROUP BY
        Geography,
        AgeBand,
        ActivityStatus
)
SELECT
    Geography,
    AgeBand,
    ActivityStatus,
    total_customers,
    churned_customers,
    churn_rate
FROM segment_analysis
WHERE total_customers >= 50
ORDER BY churned_customers DESC;

with cte1 as(
select geography, ageband, activitystatus,
count(*) as total_customers, sum(exited) as churned_customers,
CAST(SUM(Exited) * 100.0 / COUNT(*) AS DECIMAL(5,2)) AS churn_rate
from customer_churn_clean
group by geography, ageband, ActivityStatus)
,cte2 as (
select geography, ageband, activitystatus, churned_customers, churn_rate,
rank() over(partition by geography order by churn_rate desc) as churn_rank
from cte1)
select geography, ageband, activitystatus, churned_customers, churn_rate, churn_rank
from cte2 where churn_rank<=2
order by geography, churn_rank;

WITH segment_analysis AS (
    SELECT
        Geography,
        AgeBand,
        ActivityStatus,
        COUNT(*) AS total_customers,
        SUM(Exited) AS churned_customers,
        CAST(
            SUM(Exited) * 100.0 / COUNT(*)
            AS DECIMAL(5,2)
        ) AS churn_rate
    FROM customer_churn_clean
    GROUP BY Geography, AgeBand, ActivityStatus
),
overall_analysis AS(
    SELECT
        SUM(Exited) * 100.0 / COUNT(*) AS overall_churn_rate
    FROM customer_churn_clean
),
ranked_segments AS (
    SELECT
        Geography,
        AgeBand,
        ActivityStatus,
        total_customers,
        churned_customers,
        churn_rate,
        overall_churn_rate,
        RANK() OVER (
            PARTITION BY Geography
            ORDER BY churn_rate DESC
        ) AS churn_rank,
        
        LAG(churn_rate) OVER(
        PARTITION BY Geography
        ORDER BY churn_rate DESC
        ) AS Previous_churn_rate,
        churn_rate - LAG(churn_rate) OVER(
    PARTITION BY Geography
    ORDER BY churn_rate DESC
) AS churn_rate_difference,
churn_rate - overall_churn_rate as difference_from_overall
    FROM segment_analysis
    CROSS JOIN overall_analysis

)
SELECT *
FROM ranked_segments
ORDER BY Geography, churn_rank;

WITH segment_analysis AS (
    SELECT
        Geography,
        AgeBand,
        ActivityStatus,
        COUNT(*) AS total_customers,
        SUM(Exited) AS churned_customers,
        CAST(
            SUM(Exited) * 100.0 / COUNT(*)
            AS DECIMAL(5,2)
        ) AS churn_rate
    FROM customer_churn_clean
    GROUP BY Geography, AgeBand, ActivityStatus
),
overall_analysis AS(
    SELECT
        SUM(Exited) * 100.0 / COUNT(*) AS overall_churn_rate
    FROM customer_churn_clean
),
ranked_segments AS (
    SELECT
        Geography,
        AgeBand,
        ActivityStatus,
        total_customers,
        churned_customers,
        churn_rate,
        overall_churn_rate,
        RANK() OVER (
            PARTITION BY Geography
            ORDER BY churn_rate DESC
        ) AS churn_rank,
        
        LAG(churn_rate) OVER(
        PARTITION BY Geography
        ORDER BY churn_rate DESC
        ) AS Previous_churn_rate,
        churn_rate - LAG(churn_rate) OVER(
    PARTITION BY Geography
    ORDER BY churn_rate DESC
) AS churn_rate_difference,
churn_rate - overall_churn_rate as difference_from_overall,
CASE
    WHEN churn_rate >= 40 THEN 'High Risk'
    WHEN churn_rate >= 25 THEN 'Moderate Risk'
    ELSE 'Low Risk'
END AS risk_category
    FROM segment_analysis
    CROSS JOIN overall_analysis

)
SELECT
    risk_category,
    COUNT(*) AS segment_count,
    SUM(total_customers) AS total_customers,
    SUM(churned_customers) AS total_churned_customers,
    SUM(churned_customers) * 100.0
/ SUM(total_customers) AS churn_rate
FROM ranked_segments
GROUP BY risk_category
ORDER BY total_churned_customers DESC;