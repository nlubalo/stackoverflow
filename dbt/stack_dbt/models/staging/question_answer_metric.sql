WITH answer_count AS(
    SELECT
        question_id,
        COUNT(*) AS answer_count
    FROM {{ source('stackoverflow_raw', 'answers') }}
    GROUP BY question_id
),
accepted AS (
    SELECT
    question_id,
    MAX(CASE WHEN is_accepted THEN 1 ELSE 0 END) AS has_accepted_answer
    FROM {{ source('stackoverflow_raw', 'answers') }}
    GROUP BY question_id
),
first_answer AS(
    SELECT
        question_id,
        MIN(creation_date) AS first_answer_time
    FROM {{ source('stackoverflow_raw', 'answers') }}
    GROUP BY question_id
)
SELECT
    q.question_id as question_id,
    q.creation_date as question_creation_date,
    q.tags,
    q.score as question_score,
    COALESCE(ac.answer_count, 0) as answer_count,
    COALESCE(a.has_accepted_answer, 0) as has_accepted_answer,
    fa.first_answer_time,
    datediff('second', q.creation_date, fa.first_answer_time) as time_to_first_answer_seconds
FROM {{ source('stackoverflow_raw', 'questions') }} q
LEFT JOIN answer_count ac ON q.question_id = ac.question_id
LEFT JOIN accepted a ON q.question_id = a.question_id
LEFT JOIN first_answer fa ON q.question_id = fa.question_id