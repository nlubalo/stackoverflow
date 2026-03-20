WITH base AS(
    SELECT
        *,
        CASE
          WHEN tags LIKE '%chatgpt%'
          OR tags LIKE '%gpt%'
          OR tags LIKE '%llm%'
          OR tags LIKE '%language model%'
          OR tags LIKE '%ai%'
          OR tags LIKE '%artificial intelligence%'
          THEN 'AI-related'
          ELSE 'Non-AI-related'
        END AS segment
    FROM {{ ref('question_answer_metric') }}
)
SELECT segment,
    COUNT(*) AS total_questions,
    SUM(CASE WHEN view_count >0 THEN 1 ELSE 0 END) AS viewed_questions,
    SUM(CASE WHEN answer_count >0 THEN 1 ELSE 0 END) AS answered_questions,
    SUM(has_accepted_answer) AS accepted_answer_questions,
    AVG(time_to_first_answer_seconds) AS avg_time_to_first_answer_seconds,

    --- Conversion rates
    SUM(CASE WHEN answer_count >0 THEN 1 ELSE 0 END) * 1.0 / NULLIF(COUNT(*), 0) AS answer_conversion_rate,
    SUM(has_accepted_answer) * 1.0 / NULLIF(SUM(CASE WHEN answer_count >0 THEN 1 ELSE 0 END), 0) AS accepted_answer_conversion_rate
FROM base
GROUP BY segment
ORDER BY segment
