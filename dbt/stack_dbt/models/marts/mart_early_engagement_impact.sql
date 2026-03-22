SELECT
    CASE
        WHEN time_to_first_question_comment_seconds <= 600 THEN 'early_q_comment'
        WHEN time_to_first_question_comment_seconds IS NOT NULL THEN 'late_q_comment'
        ELSE 'no_q_comment'
    END AS segment,

    COUNT(*) AS total_questions,

    SUM(has_answer) * 1.0 / COUNT(*) AS answer_rate,
    SUM(has_accepted_answer) * 1.0 / COUNT(*) AS resolution_rate

FROM {{ref('fct_question_activity')}}
GROUP BY 1