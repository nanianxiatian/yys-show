import React, { useEffect, useState } from 'react'
import { Row, Col, Card, Statistic, Table, Tag, message } from 'antd'
import {
  TeamOutlined,
  FileTextOutlined,
  CheckCircleOutlined
} from '@ant-design/icons'
import { systemApi, guessApi } from '../../services/api'
import dayjs from 'dayjs'

function Home() {
  const [stats, setStats] = useState({
    blogger_count: 0,
    weibo_count: 0,
    official_count: 0
  })
  const [leaderboard, setLeaderboard] = useState([])
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      
      // 获取系统统计
      const statsRes = await systemApi.getStats()
      if (statsRes.success) {
        setStats(statsRes.data.stats)
        setLogs(statsRes.data.latest_logs)
      }
      
      // 获取排行榜
      const boardRes = await guessApi.getLeaderboard({ range: '7d' })
      if (boardRes.success) {
        setLeaderboard(boardRes.data.slice(0, 5))
      }
    } catch (error) {
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }



  const leaderboardColumns = [
    {
      title: '排名',
      dataIndex: 'rank',
      width: 80,
      render: (rank) => {
        const colors = ['#ff4d4f', '#ff7a45', '#ffa940', '#73d13d', '#40a9ff']
        return (
          <Tag color={colors[rank - 1] || '#d9d9d9'}>
            {rank}
          </Tag>
        )
      }
    },
    {
      title: '博主',
      dataIndex: 'blogger_nickname'
    },
    {
      title: '预测次数',
      dataIndex: 'valid_guesses',
      width: 100
    },
    {
      title: '正确次数',
      dataIndex: 'correct_guesses',
      width: 100
    },
    {
      title: '准确率',
      dataIndex: 'accuracy_rate',
      width: 100,
      render: (rate) => `${rate}%`
    }
  ]

  const logColumns = [
    {
      title: '类型',
      dataIndex: 'spider_type',
      width: 100,
      render: (type) => (
        <Tag color={type === 'auto' ? 'blue' : 'green'}>
          {type === 'auto' ? '自动' : '手动'}
        </Tag>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      width: 100,
      render: (status) => {
        const colors = {
          running: 'processing',
          success: 'success',
          failed: 'error'
        }
        const labels = {
          running: '运行中',
          success: '成功',
          failed: '失败'
        }
        return <Tag color={colors[status]}>{labels[status]}</Tag>
      }
    },
    {
      title: '抓取数量',
      dataIndex: 'posts_count',
      width: 100
    },
    {
      title: '时间',
      dataIndex: 'created_at',
      render: (time) => dayjs(time).format('MM-DD HH:mm')
    }
  ]

  return (
    <div>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={8}>
          <Card>
            <Statistic
              title="监控博主"
              value={stats.blogger_count}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="竞猜微博"
              value={stats.weibo_count}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic
              title="官方结果"
              value={stats.official_count}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="近7天准确率排行榜" loading={loading}>
            <Table
              dataSource={leaderboard}
              columns={leaderboardColumns}
              rowKey="blogger_id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="最近爬虫记录" loading={loading}>
            <Table
              dataSource={logs}
              columns={logColumns}
              rowKey="id"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default Home
