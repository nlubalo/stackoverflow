SELECT
    DATE_TRUNC('month', creation_date) AS month,

    AVG(time_to_first_question_comment_seconds) AS avg_time_to_q_comment,
    AVG(time_to_first_comment_seconds) AS avg_time_to_any_comment,
    AVG(time_to_first_answer_seconds) AS avg_time_to_answer,

    --- Earl engagement impact
    SUM(CASE
        WHEN time_to_first_question_comment_seconds <= 600 THEN 1
        ELSE 0
    END) * 1.0 / COUNT(*) AS early_q_comment_rate

FROM {{ref('fct_question_activity')}}
GROUP BY 1
ORDER BY 1
