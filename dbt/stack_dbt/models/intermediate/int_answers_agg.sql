SELECT
    question_id,
    count(*) AS answer_count,
    MIN(creation_date) AS first_answer_time,
    MAX(is_accepted) AS has_accepted_answer
FROM {{ source('stackover_flow_raw', 'answers') }}
GROUP BY question_id