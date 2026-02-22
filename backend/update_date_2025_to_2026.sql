-- 更新官方结果表中的日期，将2025年改为2026年
UPDATE official_results 
SET guess_date = DATE_ADD(guess_date, INTERVAL 1 YEAR)
WHERE YEAR(guess_date) = 2025;

-- 更新微博表中的日期，将2025年改为2026年
UPDATE weibo_posts 
SET guess_date = DATE_ADD(guess_date, INTERVAL 1 YEAR)
WHERE YEAR(guess_date) = 2025;

-- 验证更新结果
SELECT 
    'official_results' as table_name,
    COUNT(*) as total_records,
    MIN(guess_date) as min_date,
    MAX(guess_date) as max_date
FROM official_results
UNION ALL
SELECT 
    'weibo_posts' as table_name,
    COUNT(*) as total_records,
    MIN(guess_date) as min_date,
    MAX(guess_date) as max_date
FROM weibo_posts;
