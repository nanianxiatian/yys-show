import React, { useEffect, useState } from 'react'
import {
  Card, DatePicker, Table, Tag, Statistic, Row, Col, message, Button
} from 'antd'
import { TrophyOutlined, FireOutlined, PercentageOutlined } from '@ant-design/icons'
import { shikigamiApi } from '../../services/api'
import dayjs from 'dayjs'

function ShikigamiAnalysis() {
  const [startDate, setStartDate] = useState(dayjs().subtract(30, 'day'))
  const [endDate, setEndDate] = useState(dayjs())
  const [analysis, setAnalysis] = useState([])
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState({
    totalAppearances: 0,
    topShikigami: '-',
    avgWinRate: 0
  })

  useEffect(() => {
    fetchAnalysis()
  }, [startDate, endDate])

  const fetchAnalysis = async () => {
    try {
      setLoading(true)
      const res = await shikigamiApi.getAnalysis({
        start_date: startDate.format('YYYY-MM-DD'),
        end_date: endDate.format('YYYY-MM-DD')
      })

      if (res.success) {
        setAnalysis(res.data)
        calculateStats(res.data)
      }
    } catch (error) {
      message.error('获取分析数据失败')
    } finally {
      setLoading(false)
    }
  }

  const calculateStats = (data) => {
    if (!data || data.length === 0) {
      setStats({
        totalAppearances: 0,
        topShikigami: '-',
        avgWinRate: 0
      })
      return
    }

    const totalAppearances = data.reduce((sum, item) => sum + item.appearances, 0)
    const topShikigami = data[0]?.name || '-'
    const avgWinRate = data.length > 0
      ? (data.reduce((sum, item) => sum + item.win_rate, 0) / data.length).toFixed(2)
      : 0

    setStats({
      totalAppearances,
      topShikigami,
      avgWinRate
    })
  }

  const columns = [
    {
      title: '排名',
      dataIndex: 'rank',
      width: 80,
      render: (_, record, index) => {
        const rank = index + 1
        const colors = ['#ff4d4f', '#ff7a45', '#ffa940']
        return (
          <Tag color={colors[rank - 1] || '#d9d9d9'}>
            {rank}
          </Tag>
        )
      }
    },
    {
      title: '式神',
      dataIndex: 'name',
      width: 120
    },
    {
      title: '出场次数',
      dataIndex: 'appearances',
      width: 100,
      sorter: (a, b) => a.appearances - b.appearances,
      defaultSortOrder: 'descend'
    },
    {
      title: '胜场',
      dataIndex: 'wins',
      width: 80,
      render: (num) => <Tag color="success">{num}</Tag>
    },
    {
      title: '负场',
      dataIndex: 'losses',
      width: 80,
      render: (num) => <Tag color="error">{num}</Tag>
    },
    {
      title: '胜率',
      dataIndex: 'win_rate',
      width: 100,
      sorter: (a, b) => a.win_rate - b.win_rate,
      render: (rate) => (
        <Tag color={rate >= 60 ? 'success' : rate >= 40 ? 'warning' : 'error'}>
          {rate}%
        </Tag>
      )
    }
  ]

  return (
    <div>
      <Card
        title="式神出场分析"
        extra={
          <Row gutter={16} align="middle">
            <Col>
              <DatePicker
                value={startDate}
                onChange={setStartDate}
                allowClear={false}
                placeholder="开始日期"
              />
            </Col>
            <Col>至</Col>
            <Col>
              <DatePicker
                value={endDate}
                onChange={setEndDate}
                allowClear={false}
                placeholder="结束日期"
              />
            </Col>
            <Col>
              <Button type="primary" onClick={fetchAnalysis}>
                刷新
              </Button>
            </Col>
          </Row>
        }
      >
        <Row gutter={16} style={{ marginBottom: 24 }}>
          <Col span={8}>
            <Card>
              <Statistic
                title="总出场次数"
                value={stats.totalAppearances}
                prefix={<FireOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="出场最多式神"
                value={stats.topShikigami}
                prefix={<TrophyOutlined />}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic
                title="平均胜率"
                value={stats.avgWinRate}
                suffix="%"
                prefix={<PercentageOutlined />}
              />
            </Card>
          </Col>
        </Row>

        <Table
          columns={columns}
          dataSource={analysis}
          rowKey="name"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 个式神`,
            pageSizeOptions: ['10', '20', '50']
          }}
        />
      </Card>
    </div>
  )
}

export default ShikigamiAnalysis
