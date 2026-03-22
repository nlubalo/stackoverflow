SELECT
    q.question_id,
    q.owner_user_id,
    q.creation_date,
    q.view_count,

    COALESCE(a.answer_count, 0) AS answer_count,
    COALESCE(c.total_comment_count, 0) AS total_comment_count,
    COALESCE(c.question_comment_count, 0) AS question_comment_count,
    COALESCE(c.answer_comment_count, 0) AS answer_comment_count,

    -- FLAGS
    CASE WHEN q.view_count > 0 THEN 1 ELSE 0 END AS has_view,
    CASE WHEN a.answer_count > 0 THEN 1 ELSE 0 END AS has_answer,
    CASE WHEN c.total_comment_count > 0 THEN 1 ELSE 0 END AS has_comment,
    CASE WHEN c.question_comment_count > 0 THEN 1 ELSE 0 END AS has_question_comment,
    CASE WHEN c.answer_comment_count > 0 THEN 1 ELSE 0 END AS has_answer_comment,

    COALESCE(a.has_accepted_answer, 0) AS has_accepted_answer,

    -- TIMINGS
    datediff('second', c.first_comment_time, q.creation_date) AS time_to_first_comment_seconds,
    datediff('second', c.first_question_comment_time, q.creation_date) AS time_to_first_question_comment_seconds,
    datediff('second', a.first_answer_time, q.creation_date) AS time_to_first_answer_seconds

FROM {{source('stackoverflow_raw', 'questions')}} q
LEFT JOIN {{ref('int_answers_agg')}} a
    ON q.question_id = a.question_id
LEFT JOIN {{ref('int_comments_agg')}} c
    ON q.question_id = c.question_id