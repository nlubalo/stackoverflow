WITH comments_data AS(
    SELECT
        * from {{ source('stackover_flow_raw', 'comments') }}
),
questions AS(
    SELECT question_id FROM {{source('stackover_flow_raw', 'questions')}}
),
answers AS(
    SELECT answer_id, question_id FROM {{ source('stackover_flow_raw', 'answers')}}
)
SELECT
    c.comment_id,
    c.post_id,
    c.creation_date,
    c.owner_user_id,

    --- Identify where the comment is from
    CASE
        WHEN q.question_id IS NOT NULL THEN 'question'
        WHEN a.answer_id IS NOT NULL THEN 'answer'
        ELSE 'unknown'
    END AS comment_type,

    --- Normalize everything to question level
    COALESCE(q.question_id, a.question_id) AS question_id

FROM comments_data c
LEFT JOIN questions q
    ON c.post_id = q.question_id
LEFT JOIN answers a
    ON c.post_id = a.answer_id

