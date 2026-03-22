SELECT
    DATE_TRUNC('month', creation_date) AS month,
    COUNT(*) as total_questions,

    SUM(has_view) AS viewed_questions,
    SUM(has_question_comment) AS questions_with_q_comments,
    SUM(has_answer_comment) AS questions_with_a_comments,
    SUM(has_answer) AS answered_questions,
    SUM(has_accepted_answer) AS resolved_questions,

    -- Conversion rates
    SUM(has_view) * 1.0 / COUNT(*) AS view_rate,
    SUM(has_question_comment) * 1.0 / COUNT(*) AS question_comment_rate,
    SUM(has_answer_comment) * 1.0 / COUNT(*) AS answer_comment_rate,
    SUM(has_answer) * 1.0 / COUNT(*) AS answer_rate,
    SUM(has_accepted_answer) * 1.0 / COUNT(*) AS resolution_rate

FROM {{ref('fct_question_activity')}}
GROUP BY 1
ORDER BY 1