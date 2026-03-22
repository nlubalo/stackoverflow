SELECT
    --- Are discussions happening before answers or after?
    DATE_TRUNC('month', creation_date) AS month,

    AVG(total_comment_count) AS avg_total_comments,
    AVG(question_comment_count) AS avg_question_comments,
    AVG(answer_comment_count) AS avg_answer_comments,

    SUM(CASE WHEN question_comment_count > 0 AND answer_comment_count = 0 THEN 1 ELSE 0 END)
        * 1.0 / COUNT(*) AS only_question_comments_rate,

    SUM(CASE WHEN answer_comment_count > 0 AND question_comment_count = 0 THEN 1 ELSE 0 END)
        * 1.0 / COUNT(*) as only_answer_comments_rate,

    SUM(CASE WHEN question_comment_count > 0 AND answer_comment_count > 0 THEN 1 ELSE 0 END)
        * 1.0 / COUNT(*) as both_comment_types_rate

FROM {{ref('fct_question_activity')}}
GROUP BY 1
ORDER BY 1
