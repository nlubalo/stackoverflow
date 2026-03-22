SELECT
    owner_user_id,
    COUNT(*) AS questions_asked,
    SUM(has_answer) AS question_answered,
    SUM(has_comment) AS questions_with_comments
FROM {{ref('fct_question_activity')}}
GROUP BY owner_user_id