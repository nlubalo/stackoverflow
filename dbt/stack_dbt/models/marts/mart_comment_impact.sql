--- Do comments actually drive outcomes?
SELECT
    CASE
        WHEN has_question_comment = 0 AND has_answer_comment = 0 THEN 'no_comment'
        WHEN has_question_comment = 1 AND has_answer_comment = 0 THEN 'question_comment_only'
        WHEN has_question_comment = 0 AND has_answer_comment = 1 THEN 'answer_comment_only'
        WHEN has_question_comment = 1 AND has_answer_comment = 1 THEN 'both'
    END AS comment_segment,

    COUNT(*) AS total_questions,

    SUM(has_answer) AS answered_questions,
    SUM(has_accepted_answer) AS resolved_questions,

    SUM(has_answer) * 1.0 / COUNT(*) AS answer_rate,
    SUM(has_accepted_answer) * 1.0 / COUNT(*) AS resolution_rate

FROM {{ref('fct_question_activity')}}
GROUP BY 1
order by total_questions DESC