# SQL Query Examples for MIND Dashboard

## Overview
This file contains example SQL queries used in the MIND Dashboard for reference and testing purposes.

---

## Student Dashboard Queries

### Student Performance Overview
```sql
-- Get student's total attempts
SELECT COUNT(*) as total_attempts
FROM `gen-lang-client-0625543859.mind_analytics.conversation`
WHERE user_id = 'USER_ID_HERE'

-- Get student's average score
SELECT AVG(final_score) as avg_score
FROM `gen-lang-client-0625543859.mind_analytics.grades`
WHERE user_id = 'USER_ID_HERE'

-- Get completed case studies
SELECT COUNT(DISTINCT case_study_id) as completed_cases
FROM `gen-lang-client-0625543859.mind_analytics.grades`
WHERE user_id = 'USER_ID_HERE'
```

### Performance by Case Study
```sql
SELECT 
    c.title as case_title,
    COUNT(g.grade_id) as attempts,
    AVG(g.final_score) as avg_score,
    MAX(g.final_score) as best_score,
    AVG(g.communication) as avg_communication,
    AVG(g.comprehension) as avg_comprehension,
    AVG(g.critical_thinking) as avg_critical_thinking
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.casestudy` c 
    ON g.case_study_id = c.case_study_id
WHERE g.user_id = 'USER_ID_HERE'
GROUP BY c.title
ORDER BY avg_score DESC
```

### Skill Development Timeline
```sql
SELECT 
    DATE(g.timestamp) as date,
    AVG(g.communication) as communication,
    AVG(g.comprehension) as comprehension,
    AVG(g.critical_thinking) as critical_thinking,
    AVG(g.final_score) as overall
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
WHERE g.user_id = 'USER_ID_HERE'
GROUP BY DATE(g.timestamp)
ORDER BY date
```

---

## Faculty Dashboard Queries

### Cohort Performance Overview
```sql
-- Total students in cohort
SELECT COUNT(DISTINCT u.user_id) as total_students
FROM `gen-lang-client-0625543859.mind_analytics.user` u
WHERE u.cohort = 'COHORT_NAME'

-- Average cohort score
SELECT AVG(g.final_score) as avg_score
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.user` u 
    ON g.user_id = u.user_id
WHERE u.cohort = 'COHORT_NAME'
```

### Student Performance Distribution
```sql
SELECT 
    u.name,
    AVG(g.final_score) as avg_score,
    COUNT(g.grade_id) as num_attempts
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.user` u 
    ON g.user_id = u.user_id
WHERE u.cohort = 'COHORT_NAME'
GROUP BY u.name
ORDER BY avg_score DESC
LIMIT 20
```

### At-Risk Students Detection
```sql
WITH student_stats AS (
    SELECT 
        u.user_id,
        u.name,
        u.student_email,
        COUNT(DISTINCT g.grade_id) as num_attempts,
        AVG(g.final_score) as avg_score,
        MAX(c.timestamp) as last_activity
    FROM `gen-lang-client-0625543859.mind_analytics.user` u
    LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
        ON u.user_id = g.user_id
    LEFT JOIN `gen-lang-client-0625543859.mind_analytics.conversation` c 
        ON u.user_id = c.user_id
    WHERE u.cohort = 'COHORT_NAME'
    GROUP BY u.user_id, u.name, u.student_email
)
SELECT 
    name,
    student_email,
    num_attempts,
    ROUND(avg_score, 1) as avg_score,
    last_activity,
    TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_activity, DAY) as days_since_activity
FROM student_stats
WHERE 
    (avg_score < 70 AND num_attempts > 0)
    OR (num_attempts < 3 AND TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_activity, DAY) > 14)
    OR (TIMESTAMP_DIFF(CURRENT_TIMESTAMP(), last_activity, DAY) > 30)
ORDER BY avg_score ASC, days_since_activity DESC
```

### Rubric Performance Heatmap
```sql
SELECT 
    c.title as case_study,
    AVG(g.communication) as communication,
    AVG(g.comprehension) as comprehension,
    AVG(g.critical_thinking) as critical_thinking
FROM `gen-lang-client-0625543859.mind_analytics.grades` g
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.user` u 
    ON g.user_id = u.user_id
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.casestudy` c 
    ON g.case_study_id = c.case_study_id
WHERE u.cohort = 'COHORT_NAME'
GROUP BY c.title
ORDER BY c.title
```

---

## Developer Dashboard Queries

### Data Freshness Check
```sql
-- Check last update time and row count for a table
SELECT 
    COUNT(*) as row_count,
    MAX(GREATEST(
        COALESCE(date_updated, TIMESTAMP('1970-01-01')),
        COALESCE(date_added, TIMESTAMP('1970-01-01')),
        COALESCE(timestamp, TIMESTAMP('1970-01-01')),
        COALESCE(created_at, TIMESTAMP('1970-01-01'))
    )) as last_update
FROM `gen-lang-client-0625543859.mind_analytics.TABLE_NAME`
```

### Backend Error Rate
```sql
SELECT 
    derived_endpoint_group as endpoint,
    COUNT(*) as total_requests,
    SUM(CASE WHEN derived_is_error THEN 1 ELSE 0 END) as errors,
    ROUND(100.0 * SUM(CASE WHEN derived_is_error THEN 1 ELSE 0 END) / COUNT(*), 2) as error_rate
FROM `gen-lang-client-0625543859.mind_analytics.backend_telemetry`
WHERE created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY derived_endpoint_group
ORDER BY error_rate DESC
```

### Response Time Analysis
```sql
SELECT 
    derived_endpoint_group as endpoint,
    AVG(derived_response_time_ms) as avg_response_time,
    MAX(derived_response_time_ms) as max_response_time,
    MIN(derived_response_time_ms) as min_response_time,
    STDDEV(derived_response_time_ms) as stddev_response_time
FROM `gen-lang-client-0625543859.mind_analytics.backend_telemetry`
WHERE derived_response_time_ms IS NOT NULL
AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
GROUP BY derived_endpoint_group
ORDER BY avg_response_time DESC
```

### AI Usage Metrics
```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as ai_requests,
    SUM(derived_ai_total_tokens) as total_tokens,
    AVG(derived_ai_total_tokens) as avg_tokens_per_request,
    SUM(derived_ai_input_tokens) as total_input_tokens,
    SUM(derived_ai_output_tokens) as total_output_tokens
FROM `gen-lang-client-0625543859.mind_analytics.backend_telemetry`
WHERE derived_ai_total_tokens IS NOT NULL
AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC
```

### Data Quality Checks
```sql
-- Check for orphaned conversations (without grades)
SELECT 
    'Conversations without Grades' as check_name,
    COUNT(*) as count
FROM `gen-lang-client-0625543859.mind_analytics.conversation` c
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
    ON c.conversation_id = g.conversation_id
WHERE g.grade_id IS NULL

-- Check for users without email
UNION ALL

SELECT 
    'Users without Email' as check_name,
    COUNT(*) as count
FROM `gen-lang-client-0625543859.mind_analytics.user`
WHERE student_email IS NULL
```

---

## Admin Dashboard Queries

### Platform-wide KPIs
```sql
-- Get all main counts
SELECT 
    (SELECT COUNT(*) FROM `gen-lang-client-0625543859.mind_analytics.user`) as total_users,
    (SELECT COUNT(*) FROM `gen-lang-client-0625543859.mind_analytics.sessions`) as total_sessions,
    (SELECT COUNT(*) FROM `gen-lang-client-0625543859.mind_analytics.conversation`) as total_conversations,
    (SELECT COUNT(*) FROM `gen-lang-client-0625543859.mind_analytics.grades`) as total_grades
```

### Daily Active Users
```sql
SELECT 
    DATE(timestamp) as date,
    COUNT(DISTINCT user_id) as daily_active_users
FROM `gen-lang-client-0625543859.mind_analytics.conversation`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY DATE(timestamp)
ORDER BY date
```

### Case Study Usage Analytics
```sql
SELECT 
    c.title,
    COUNT(DISTINCT s.user_id) as unique_users,
    COUNT(s.session_pk) as total_sessions,
    COUNT(g.grade_id) as graded_attempts,
    AVG(g.final_score) as avg_score
FROM `gen-lang-client-0625543859.mind_analytics.casestudy` c
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.sessions` s 
    ON c.case_study_id = s.case_study_id
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
    ON c.case_study_id = g.case_study_id
GROUP BY c.title
ORDER BY unique_users DESC
```

### Completion Funnel
```sql
WITH funnel AS (
    SELECT 
        (SELECT COUNT(DISTINCT user_id) 
         FROM `gen-lang-client-0625543859.mind_analytics.user`) as registered_users,
        (SELECT COUNT(DISTINCT user_id) 
         FROM `gen-lang-client-0625543859.mind_analytics.sessions`) as users_with_sessions,
        (SELECT COUNT(DISTINCT user_id) 
         FROM `gen-lang-client-0625543859.mind_analytics.conversation`) as users_with_conversations,
        (SELECT COUNT(DISTINCT user_id) 
         FROM `gen-lang-client-0625543859.mind_analytics.grades`) as users_with_grades
)
SELECT * FROM funnel
```

### Department Performance
```sql
SELECT 
    COALESCE(u.department, 'No Department') as department,
    COUNT(DISTINCT u.user_id) as students,
    COUNT(g.grade_id) as attempts,
    AVG(g.final_score) as avg_score,
    MIN(g.final_score) as min_score,
    MAX(g.final_score) as max_score
FROM `gen-lang-client-0625543859.mind_analytics.user` u
LEFT JOIN `gen-lang-client-0625543859.mind_analytics.grades` g 
    ON u.user_id = g.user_id
GROUP BY department
HAVING students > 0
ORDER BY avg_score DESC
```

---

## Useful Utility Queries

### List All Tables
```sql
SELECT table_name, row_count, size_bytes / 1024 / 1024 as size_mb
FROM `gen-lang-client-0625543859.mind_analytics.__TABLES__`
ORDER BY table_name
```

### Get Table Schema
```sql
SELECT column_name, data_type, is_nullable
FROM `gen-lang-client-0625543859.mind_analytics.INFORMATION_SCHEMA.COLUMNS`
WHERE table_name = 'TABLE_NAME'
ORDER BY ordinal_position
```

### Check for Duplicates
```sql
-- Check for duplicate users
SELECT student_email, COUNT(*) as count
FROM `gen-lang-client-0625543859.mind_analytics.user`
GROUP BY student_email
HAVING COUNT(*) > 1
```

### Recent Activity Summary
```sql
SELECT 
    'Sessions (24h)' as metric,
    COUNT(*) as value
FROM `gen-lang-client-0625543859.mind_analytics.sessions`
WHERE last_activity >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)

UNION ALL

SELECT 
    'New Users (7d)' as metric,
    COUNT(*) as value
FROM `gen-lang-client-0625543859.mind_analytics.user`
WHERE date_added >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)

UNION ALL

SELECT 
    'Grades (24h)' as metric,
    COUNT(*) as value
FROM `gen-lang-client-0625543859.mind_analytics.grades`
WHERE timestamp >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 24 HOUR)
```

---

## Notes

- Replace `USER_ID_HERE`, `COHORT_NAME`, `TABLE_NAME` with actual values
- All timestamps use TIMESTAMPTZ format
- Queries use LEFT JOIN to handle missing relationships gracefully
- COALESCE is used to handle NULL values in aggregations
- Date ranges can be adjusted using TIMESTAMP_SUB with INTERVAL
