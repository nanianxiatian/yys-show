import React, { useEffect, useState } from 'react'
import {
  Card, DatePicker, Table, Tag, Row, Col, Statistic, Radio, message, Select, Button, Modal, List
} from 'antd'
import {
  CheckCircleOutlined, CloseCircleOutlined, QuestionCircleOutlined, EyeOutlined
} from '@ant-design/icons'
import { guessApi, bloggerApi } from '../../services/api'
import dayjs from 'dayjs'

function GuessAnalysis() {
  const [selectedDate, setSelectedDate] = useState(dayjs())
  const [analysis, setAnalysis] = useState({
    date: '',
    total_rounds: 0,
    blogger_count: 0,
    results: []
  })
  const [leaderboard, setLeaderboard] = useState([])
  const [range, setRange] = useState('7d')
  const [loading, setLoading] = useState(false)
  const [selectedRound, setSelectedRound] = useState(null)
  const [allBloggers, setAllBloggers] = useState([])
  const [missingModalVisible, setMissingModalVisible] = useState(false)
  const [missingBloggers, setMissingBloggers] = useState([])

  useEffect(() => {
    fetchAnalysis()
    fetchAllBloggers()
  }, [selectedDate])

  useEffect(() => {
    fetchLeaderboard()
  }, [range])

  const fetchAllBloggers = async () => {
    try {
      // 获取所有博主，不分页
      const res = await bloggerApi.getList({ is_active: true, per_page: 100 })
      if (res.success) {
        setAllBloggers(res.data)
        console.log('获取到博主数量:', res.data.length)
      }
    } catch (error) {
      console.error('获取博主列表失败', error)
    }
  }

  // 计算指定轮次没有竞猜的博主
  const calculateMissingBloggers = (round) => {
    if (!round || !analysis.results || analysis.results.length === 0) return []
    
    // 获取该轮次有竞猜的博主ID集合
    const bloggersWithGuess = new Set()
    analysis.results.forEach(blogger => {
      const hasRound = blogger.predictions.some(p => p.round === round)
      if (hasRound) {
        bloggersWithGuess.add(blogger.blogger_id)
      }
    })
    
    // 找出没有竞猜的博主
    const missing = allBloggers.filter(blogger => !bloggersWithGuess.has(blogger.id))
    return missing
  }

  // 显示缺失博主弹窗
  const showMissingBloggers = (round) => {
    console.log('选择的轮次:', round)
    console.log('allBloggers数量:', allBloggers.length)
    console.log('allBloggers:', allBloggers.map(b => b.nickname))
    console.log('analysis.results:', analysis.results)
    
    setSelectedRound(round)
    const missing = calculateMissingBloggers(round)
    console.log('缺失博主数量:', missing.length)
    console.log('缺失博主:', missing.map(b => b.nickname))
    setMissingBloggers(missing)
    setMissingModalVisible(true)
  }

  const fetchAnalysis = async () => {
    try {
      setLoading(true)
      const dateStr = selectedDate.format('YYYY-MM-DD')
      const res = await guessApi.getAnalysis({ date: dateStr })
      
      if (res.success) {
        setAnalysis(res.data)
      }
    } catch (error) {
      message.error('获取分析数据失败')
    } finally {
      setLoading(false)
    }
  }

  const fetchLeaderboard = async () => {
    try {
      const res = await guessApi.getLeaderboard({ range })
      if (res.success) {
        setLeaderboard(res.data)
      }
    } catch (error) {
      message.error('获取排行榜失败')
    }
  }

  const expandedRowRender = (record) => {
    const columns = [
      {
        title: '轮次',
        dataIndex: 'round',
        width: 80,
        render: (round) => `第${round}轮`
      },
      {
        title: '预测',
        dataIndex: 'prediction',
        width: 100,
        render: (pred) => {
          const colors = { left: 'red', right: 'blue', unknown: 'default', multiple: 'warning' }
          const texts = { left: '左', right: '右', unknown: '未知', multiple: '多条' }
          return <Tag color={colors[pred]}>{texts[pred]}</Tag>
        }
      },
      {
        title: '官方结果',
        dataIndex: 'official_result',
        width: 100,
        render: (result) => {
          if (!result) return <Tag>未录入</Tag>
          return <Tag color={result === 'left' ? 'red' : 'blue'}>{result === 'left' ? '左' : '右'}</Tag>
        }
      },
      {
        title: '状态',
        dataIndex: 'status',
        width: 100,
        render: (status) => {
          const config = {
            correct: { color: 'success', icon: <CheckCircleOutlined />, text: '正确' },
            wrong: { color: 'error', icon: <CloseCircleOutlined />, text: '错误' },
            unknown: { color: 'default', icon: <QuestionCircleOutlined />, text: '未知' },
            pending: { color: 'warning', icon: null, text: '待录入' }
          }
          const c = config[status]
          return <Tag color={c.color} icon={c.icon}>{c.text}</Tag>
        }
      },
      {
        title: '内容',
        dataIndex: 'content',
        ellipsis: true
      }
    ]

    return (
      <Table
        columns={columns}
        dataSource={record.predictions}
        rowKey="round"
        pagination={false}
        size="small"
      />
    )
  }

  const columns = [
    {
      title: '博主',
      dataIndex: 'blogger_nickname'
    },
    {
      title: '预测次数',
      dataIndex: 'correct',
      width: 100,
      render: (_, record) => record.correct + record.wrong + record.unknown
    },
    {
      title: '正确',
      dataIndex: 'correct',
      width: 80,
      render: (num) => <Tag color="success">{num}</Tag>
    },
    {
      title: '错误',
      dataIndex: 'wrong',
      width: 80,
      render: (num) => <Tag color="error">{num}</Tag>
    },
    {
      title: '未知',
      dataIndex: 'unknown',
      width: 80,
      render: (num) => <Tag>{num}</Tag>
    },
    {
      title: '准确率',
      dataIndex: 'accuracy_rate',
      width: 100,
      render: (rate) => (
        <Tag color={rate >= 70 ? 'success' : rate >= 50 ? 'warning' : 'error'}>
          {rate}%
        </Tag>
      )
    }
  ]

  const leaderboardColumns = [
    {
      title: '排名',
      dataIndex: 'rank',
      width: 70,
      render: (rank) => {
        const colors = ['#ff4d4f', '#ff7a45', '#ffa940']
        return (
          <Tag color={colors[rank - 1] || '#d9d9d9'}>
            {rank}
          </Tag>
        )
      }
    },
    {
      title: '博主',
      dataIndex: 'blogger_nickname',
      width: 120
    },
    {
      title: '总预测',
      dataIndex: 'valid_guesses',
      width: 80
    },
    {
      title: '总正确',
      dataIndex: 'correct_guesses',
      width: 80
    },
    {
      title: '总错误',
      dataIndex: 'wrong_guesses',
      width: 80
    },
    {
      title: '总准确率',
      dataIndex: 'accuracy_rate',
      width: 90,
      render: (rate) => (
        <Tag color={rate >= 70 ? 'success' : rate >= 50 ? 'warning' : 'error'}>
          {rate}%
        </Tag>
      )
    },
    {
      title: '最近一天预测',
      dataIndex: 'last_day_guesses',
      width: 100,
      render: (_, record) => {
        const lastDayCorrect = record.last_day_correct || 0
        const lastDayWrong = record.last_day_wrong || 0
        return lastDayCorrect + lastDayWrong
      }
    },
    {
      title: '最近一天正确',
      dataIndex: 'last_day_correct',
      width: 100,
      render: (num) => <Tag color="success">{num || 0}</Tag>
    },
    {
      title: '最近一天错误',
      dataIndex: 'last_day_wrong',
      width: 100,
      render: (num) => <Tag color="error">{num || 0}</Tag>
    },
    {
      title: '最近一天准确率',
      dataIndex: 'last_day_accuracy',
      width: 110,
      render: (_, record) => {
        const correct = record.last_day_correct || 0
        const wrong = record.last_day_wrong || 0
        const total = correct + wrong
        const rate = total > 0 ? Math.round((correct / total) * 100) : 0
        return (
          <Tag color={rate >= 70 ? 'success' : rate >= 50 ? 'warning' : 'error'}>
            {rate}%
          </Tag>
        )
      }
    }
  ]

  return (
    <div>
      {/* 准确率排行榜 - 占据整行（上方） */}
      <Card title="准确率排行榜" style={{ marginBottom: 16 }}>
        <Table
          columns={leaderboardColumns}
          dataSource={leaderboard}
          rowKey="blogger_id"
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
            pageSizeOptions: ['10', '20', '50']
          }}
          size="small"
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 每日竞猜分析 - 占据整行（下方） */}
      <Card
        title="每日竞猜分析"
        extra={
          <DatePicker
            value={selectedDate}
            onChange={setSelectedDate}
            allowClear={false}
          />
        }
      >
        <Row gutter={16} style={{ marginBottom: 16 }}>
          <Col span={6}>
            <Statistic
              title="参与博主"
              value={analysis.blogger_count}
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="官方结果"
              value={analysis.total_rounds}
              suffix="/ 7轮"
            />
          </Col>
          <Col span={6}>
            <Statistic
              title="日期"
              value={analysis.date}
            />
          </Col>
          <Col span={6}>
            <div style={{ marginBottom: 8 }}>查看无竞猜博主</div>
            <Select
              placeholder="选择轮次"
              style={{ width: 120 }}
              onChange={showMissingBloggers}
              options={[
                { label: '第1轮', value: 1 },
                { label: '第2轮', value: 2 },
                { label: '第3轮', value: 3 },
                { label: '第4轮', value: 4 },
                { label: '第5轮', value: 5 },
                { label: '第6轮', value: 6 },
                { label: '第7轮', value: 7 }
              ]}
            />
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={analysis.results}
          rowKey="blogger_id"
          loading={loading}
          expandable={{ expandedRowRender }}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 条`,
            pageSizeOptions: ['10', '20', '50']
          }}
        />
      </Card>

      {/* 缺失博主弹窗 */}
      <Modal
        title={`第${selectedRound}轮 - 未参与竞猜的博主 (${missingBloggers.length}人)`}
        open={missingModalVisible}
        onCancel={() => setMissingModalVisible(false)}
        footer={[
          <Button key="close" onClick={() => setMissingModalVisible(false)}>
            关闭
          </Button>
        ]}
        width={500}
      >
        {missingBloggers.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '20px 0' }}>
            <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a' }} />
            <p style={{ marginTop: 16 }}>所有博主都参与了第{selectedRound}轮竞猜！</p>
          </div>
        ) : (
          <List
            dataSource={missingBloggers}
            renderItem={(blogger) => (
              <List.Item>
                <List.Item.Meta
                  avatar={
                    blogger.avatar_url ? (
                      <img
                        src={blogger.avatar_url}
                        alt={blogger.nickname}
                        style={{ width: 40, height: 40, borderRadius: '50%' }}
                      />
                    ) : (
                      <div style={{ width: 40, height: 40, borderRadius: '50%', background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        <span>{blogger.nickname?.[0] || '?'}</span>
                      </div>
                    )
                  }
                  title={
                    blogger.profile_url ? (
                      <a
                        href={blogger.profile_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#1890ff', textDecoration: 'none' }}
                      >
                        {blogger.nickname}
                      </a>
                    ) : blogger.weibo_uid ? (
                      <a
                        href={`https://weibo.com/u/${blogger.weibo_uid}`}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: '#1890ff', textDecoration: 'none' }}
                      >
                        {blogger.nickname}
                      </a>
                    ) : (
                      <span style={{ color: '#666' }}>{blogger.nickname}</span>
                    )
                  }
                  description={blogger.description || '暂无描述'}
                />
              </List.Item>
            )}
          />
        )}
      </Modal>
    </div>
  )
}

export default GuessAnalysis
