SELECT
    question_id,
    COUNT(*) AS total_comment_count,
    SUM(CASE WHEN comment_type = 'question' THEN 1 ELSE 0 END) AS question_comment_count,
    SUM(CASE WHEN comment_type = 'answer' THEN 1 ELSE 0 END) as answer_comment_count,
    MIN(creation_date) AS first_comment_time,
    MIN(CASE WHEN comment_type = 'question' THEN creation_date END) AS first_question_comment_time,
    MIN(CASE WHEN comment_type ='answer' THEN creation_date END) AS first_answer_comment_time

FROM {{ref('int_enriched_comments')}}
GROUP BY question_id