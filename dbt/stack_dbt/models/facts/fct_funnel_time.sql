SELECT
    DATE_TRUNC('month', question_creation_date) AS month,
    COUNT(*) AS total_questions,
    SUM(CASE WHEN view_count >0 THEN 1 ELSE 0 END) AS viewed_questions,
    SUM(CASE WHEN answer_count >0 THEN 1 ELSE 0 END) AS answered_questions,
    SUM(has_accepted_answer) AS accepted_answer_questions,
    SUM(has_self_instant_answer) AS self_instant_answer_questions,
    AVG(time_to_first_answer_seconds) AS avg_time_to_first_answer_seconds,

    --- Conversion rates
    SUM(CASE WHEN answer_count > 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS answer_conversion_rate,
    SUM(has_accepted_answer) * 1.0 / NULLIF(SUM(CASE WHEN answer_count > 0 THEN 1 ELSE 0 END), 0) AS accepted_answer_conversion_rate,
    SUM(has_self_instant_answer) * 1.0 / NULLIF(COUNT(*), 0) AS self_instant_answer_conversion_rate
FROM {{ ref('question_answer_metric') }}
GROUP BY 1
ORDER BY 1