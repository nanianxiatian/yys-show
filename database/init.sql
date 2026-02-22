-- 阴阳师对弈竞猜系统数据库初始化脚本
-- 数据库: yys_guess

CREATE DATABASE IF NOT EXISTS yys_guess DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE yys_guess;

-- 博主表
CREATE TABLE IF NOT EXISTS bloggers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nickname VARCHAR(100) NOT NULL COMMENT '博主昵称',
    weibo_uid VARCHAR(50) COMMENT '微博用户ID',
    profile_url VARCHAR(500) COMMENT '主页链接',
    avatar_url VARCHAR(500) COMMENT '头像URL',
    description TEXT COMMENT '博主描述',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否启用',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_nickname (nickname)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='博主信息表';

-- 微博帖子表
CREATE TABLE IF NOT EXISTS weibo_posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    blogger_id INT NOT NULL COMMENT '博主ID',
    weibo_id VARCHAR(50) NOT NULL COMMENT '微博ID',
    content TEXT NOT NULL COMMENT '微博内容',
    guess_prediction ENUM('left', 'right', 'unknown') DEFAULT 'unknown' COMMENT '预测结果:左/右/未知',
    guess_round INT COMMENT '竞猜轮次(1-7)',
    guess_date DATE COMMENT '竞猜日期',
    publish_time TIMESTAMP COMMENT '发布时间',
    reposts_count INT DEFAULT 0 COMMENT '转发数',
    comments_count INT DEFAULT 0 COMMENT '评论数',
    attitudes_count INT DEFAULT 0 COMMENT '点赞数',
    is_guess_related BOOLEAN DEFAULT FALSE COMMENT '是否包含对弈竞猜',
    pic_urls TEXT COMMENT '微博图片URL列表(JSON数组)',
    weibo_url VARCHAR(500) COMMENT '微博原链接',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_weibo_id (weibo_id),
    INDEX idx_blogger_date (blogger_id, guess_date),
    INDEX idx_guess_date_round (guess_date, guess_round),
    FOREIGN KEY (blogger_id) REFERENCES bloggers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='微博帖子表';

-- 官方竞猜结果表
CREATE TABLE IF NOT EXISTS official_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    guess_date DATE NOT NULL COMMENT '竞猜日期',
    guess_round INT NOT NULL COMMENT '竞猜轮次(1-7)',
    result ENUM('left', 'right') NOT NULL COMMENT '官方结果:左/右',
    left_team VARCHAR(200) COMMENT '左侧阵营描述',
    right_team VARCHAR(200) COMMENT '右侧阵营描述',
    description TEXT COMMENT '备注',
    created_by VARCHAR(100) COMMENT '录入人',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_date_round (guess_date, guess_round),
    INDEX idx_guess_date (guess_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='官方竞猜结果表';

-- 博主竞猜统计表(每日更新)
CREATE TABLE IF NOT EXISTS blogger_stats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    blogger_id INT NOT NULL COMMENT '博主ID',
    stat_date DATE NOT NULL COMMENT '统计日期',
    total_guesses INT DEFAULT 0 COMMENT '总预测次数',
    correct_guesses INT DEFAULT 0 COMMENT '正确次数',
    wrong_guesses INT DEFAULT 0 COMMENT '错误次数',
    unknown_guesses INT DEFAULT 0 COMMENT '未知/未预测次数',
    accuracy_rate DECIMAL(5,2) DEFAULT 0.00 COMMENT '准确率(%)',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_blogger_date (blogger_id, stat_date),
    FOREIGN KEY (blogger_id) REFERENCES bloggers(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='博主竞猜统计表';

-- 系统配置表
CREATE TABLE IF NOT EXISTS system_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    config_key VARCHAR(100) NOT NULL COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(500) COMMENT '配置说明',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';

-- 爬虫日志表
CREATE TABLE IF NOT EXISTS spider_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    spider_type VARCHAR(50) NOT NULL COMMENT '爬虫类型:auto/manual',
    blogger_id INT COMMENT '博主ID(手动同步时有)',
    status ENUM('running', 'success', 'failed') NOT NULL COMMENT '状态',
    start_time TIMESTAMP COMMENT '开始时间',
    end_time TIMESTAMP COMMENT '结束时间',
    posts_count INT DEFAULT 0 COMMENT '抓取帖子数',
    error_message TEXT COMMENT '错误信息',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    FOREIGN KEY (blogger_id) REFERENCES bloggers(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='爬虫日志表';

-- 插入默认配置
INSERT INTO system_config (config_key, config_value, description) VALUES
('spider_keywords', '对弈竞猜', '爬虫关键词，多个用逗号分隔'),
('spider_auto_enabled', 'true', '是否启用自动爬虫'),
('spider_cron_schedule', '0 30 11,13,15,17,19,21,23 * * *', '自动爬虫定时规则(每2小时)'),
('weibo_cookie', '', '微博登录Cookie'),
('cookie_expire_time', '', 'Cookie过期时间')
ON DUPLICATE KEY UPDATE config_value = VALUES(config_value);
