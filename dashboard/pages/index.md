# Stack Overflow Behavioral Shift Analysis

This project analyzes how user bahaviour on Stack Oveflow has evolved over time,
with a focus on the impact of Large Language Models (LLMs).

---

## Objectives
To determine whether developers are shifting from:
- Community-driven problem solving
-> to
- Self-solving behavior aided by LLMs

```sql kpi_metrics
select * from fct_funnel
```

<BigValue
    data={kpi_metrics}
    value=total_questions
    label="Total Questions Asked"
    />
<BigValue data={kpi_metrics} value=answered_questions title="Answered Questions" />
<BigValue data={kpi_metrics} value=accepted_answer_questions title="Accepted Answers" />
<BigValue data={kpi_metrics} value=answer_conversion_rate title="Answer Conversion Rate" />


```sql funnel_pivot
  select 'Total questions' AS stage, total_questions AS value from fct_funnel
    union all
   select 'Answered questions' AS stage, answered_questions AS value from fct_funnel
    union all
   select 'Accepted answer questions' AS stage, accepted_answer_questions AS value from fct_funnel
```

<FunnelChart
    data={funnel_pivot}
    nameCol=stage
    valueCol=value
    title="Stack Overflow Funnel"
/>


```sql funnel_time
select * from fct_funnel_time
```

<LineChart
    data={funnel_time}
    x=month
    y=answer_conversion_rate
    y2=accepted_answer_conversion_rate
    yAxisTitle="Answer Conversion Rate"
/>