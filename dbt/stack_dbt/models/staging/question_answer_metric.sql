WITH answers_enrinched AS(
    SELECT
        a.*,
        a.owner_user_id,
        CASE
            WHEN a.owner_user_id = q.owner_user_id
            AND a.creation_date >= q.creation_date THEN 1
            ELSE 0
        END AS is_self_instant_answer
    FROM {{ source('stackoverflow_raw', 'answers') }} a
    JOIN {{ source('stackoverflow_raw', 'questions') }} q
    ON a.question_id = q.question_id
),

-- exclude for core metrics
filtered_answers AS (
    SELECT *
    FROM answers_enrinched
    WHERE is_self_instant_answer = 0
),

answer_count AS(
    SELECT
        question_id,
        COUNT(*) AS answer_count
    FROM filtered_answers
    GROUP BY question_id
),
accepted AS (
    SELECT
    question_id,
    MAX(CASE WHEN is_accepted THEN 1 ELSE 0 END) AS has_accepted_answer
    FROM filtered_answers
    GROUP BY question_id
),
first_answer AS(
    SELECT
        question_id,
        MIN(creation_date) AS first_answer_time
    FROM filtered_answers
    GROUP BY question_id
),
-- self-instant tracking
self_instant_answers AS (
    SELECT
        question_id,
        MAX(is_self_instant_answer) AS has_self_instant_answer
    FROM answers_enrinched
    GROUP BY question_id
)
SELECT
    q.question_id as question_id,
    q.creation_date as question_creation_date,
    q.tags,
    q.score as question_score,
    q.view_count,
    COALESCE(ac.answer_count, 0) as answer_count,
    COALESCE(a.has_accepted_answer, 0) as has_accepted_answer,
    COALESCE(self_instant_answers.has_self_instant_answer, 0) as has_self_instant_answer,
    fa.first_answer_time,
    datediff('second', q.creation_date, fa.first_answer_time) as time_to_first_answer_seconds
FROM {{ source('stackoverflow_raw', 'questions') }} q
LEFT JOIN answer_count ac ON q.question_id = ac.question_id
LEFT JOIN accepted a ON q.question_id = a.question_id
LEFT JOIN first_answer fa ON q.question_id = fa.question_id
LEFT JOIN self_instant_answers ON q.question_id = self_instant_answers.question_id