WITH user_activity AS (
    SELECT
        owner_user_id,

        COUNT(*) AS questions_asked,
        SUM(has_question_comment) AS questions_with_q_comments,
        SUM(has_answer) AS questions_answered,
        SUM(has_accepted_answer) AS resolved_questions

    FROM {{ref('fct_question_activity')}}
    GROUP BY owner_user_id

)
SELECT
    CASE
        WHEN questions_asked >= 10 THEN 'power_asker'
        WHEN questions_asked >=3 THEN 'active_asker'
        WHEN questions_asked >= 1 THEN 'casual_asker'
        ELSE 'inactive'
    END AS user_segment,

    COUNT(*) AS users,
    AVG(questions_asked) AS avg_questions,
    AVG(resolved_questions * 1.0 / NULLIF(questions_asked, 0)) AS avg_resolution_rate
FROM user_activity
GROUP BY 1
ORDER BY users DESC
