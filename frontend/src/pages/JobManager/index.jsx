import React, { useEffect, useState } from 'react'
import { Card, Table, Button, Tag, message, Space, Popconfirm, Descriptions } from 'antd'
import { 
  PlayCircleOutlined, 
  PauseCircleOutlined, 
  ReloadOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
  ExclamationCircleOutlined
} from '@ant-design/icons'
import { systemApi } from '../../services/api'
import dayjs from 'dayjs'

function JobManager() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [actionLoading, setActionLoading] = useState({})

  useEffect(() => {
    fetchJobs()
  }, [])

  const fetchJobs = async () => {
    try {
      setLoading(true)
      console.log('正在获取定时任务列表...')
      const res = await systemApi.getJobs()
      console.log('API响应:', res)
      if (res.success) {
        setJobs(res.data || [])
        console.log('设置任务列表:', res.data)
      } else {
        message.error('获取定时任务列表失败: ' + (res.message || '未知错误'))
      }
    } catch (error) {
      console.error('获取定时任务列表出错:', error)
      message.error('获取定时任务列表失败: ' + (error.message || '网络错误'))
    } finally {
      setLoading(false)
    }
  }

  const handlePauseJob = async (jobId) => {
    try {
      setActionLoading({ ...actionLoading, [jobId]: true })
      const res = await systemApi.pauseJob(jobId)
      if (res.success) {
        message.success(res.message)
        fetchJobs()
      } else {
        message.error(res.message || '暂停失败')
      }
    } catch (error) {
      message.error('暂停任务失败')
    } finally {
      setActionLoading({ ...actionLoading, [jobId]: false })
    }
  }

  const handleResumeJob = async (jobId) => {
    try {
      setActionLoading({ ...actionLoading, [jobId]: true })
      const res = await systemApi.resumeJob(jobId)
      if (res.success) {
        message.success(res.message)
        fetchJobs()
      } else {
        message.error(res.message || '启动失败')
      }
    } catch (error) {
      message.error('启动任务失败')
    } finally {
      setActionLoading({ ...actionLoading, [jobId]: false })
    }
  }

  const handleRunNow = async () => {
    try {
      setActionLoading({ ...actionLoading, runNow: true })
      const res = await systemApi.runSpiderNow()
      if (res.success) {
        message.success(res.message)
      } else {
        message.error(res.message || '执行失败')
      }
    } catch (error) {
      message.error('立即执行失败')
    } finally {
      setActionLoading({ ...actionLoading, runNow: false })
    }
  }

  const getStatusTag = (job) => {
    // 根据paused字段判断任务状态
    if (job.paused) {
      return <Tag color="warning" icon={<ExclamationCircleOutlined />}>已暂停</Tag>
    } else {
      return <Tag color="success" icon={<CheckCircleOutlined />}>运行中</Tag>
    }
  }

  const columns = [
    {
      title: '任务ID',
      dataIndex: 'id',
      width: 150,
    },
    {
      title: '任务名称',
      dataIndex: 'name',
      width: 150,
    },
    {
      title: '触发规则',
      dataIndex: 'trigger',
      width: 200,
      render: (trigger) => (
        <Space>
          <ClockCircleOutlined />
          <span>{trigger}</span>
        </Space>
      )
    },
    {
      title: '下次执行时间',
      dataIndex: 'next_run_time',
      width: 180,
      render: (time) => {
        if (!time) {
          return <span style={{ color: '#999' }}>-</span>
        }
        return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
      }
    },
    {
      title: '状态',
      width: 120,
      render: (_, record) => getStatusTag(record)
    },
    {
      title: '操作',
      width: 200,
      render: (_, record) => (
        <Space>
          {record.paused ? (
            <Button
              type="primary"
              size="small"
              icon={<PlayCircleOutlined />}
              onClick={() => handleResumeJob(record.id)}
              loading={actionLoading[record.id]}
            >
              启动
            </Button>
          ) : (
            <Popconfirm
              title="确认暂停"
              description={`确定要暂停任务 "${record.name}" 吗？`}
              onConfirm={() => handlePauseJob(record.id)}
              okText="确认"
              cancelText="取消"
            >
              <Button
                type="primary"
                danger
                size="small"
                icon={<PauseCircleOutlined />}
                loading={actionLoading[record.id]}
              >
                暂停
              </Button>
            </Popconfirm>
          )}
        </Space>
      )
    }
  ]

  return (
    <div>
      <Card
        title="定时任务管理"
        extra={
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={fetchJobs}
              loading={loading}
            >
              刷新
            </Button>
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={handleRunNow}
              loading={actionLoading.runNow}
            >
              立即执行爬虫
            </Button>
          </Space>
        }
      >
        <Descriptions 
          title="任务说明" 
          bordered 
          column={1}
          style={{ marginBottom: 24 }}
        >
          <Descriptions.Item label="自动爬虫">
            定时爬取监控博主的微博数据，默认每天 11:30, 13:30, 15:30, 17:30, 19:30, 21:30, 23:30 执行
          </Descriptions.Item>
          <Descriptions.Item label="每日统计">
            每天凌晨 01:00 执行，统计前一天的竞猜数据
          </Descriptions.Item>
        </Descriptions>

        <Table
          columns={columns}
          dataSource={jobs}
          rowKey="id"
          loading={loading}
          pagination={false}
          bordered
        />

        <div style={{ marginTop: 16, padding: 16, background: '#f5f5f5', borderRadius: 4 }}>
          <h4 style={{ marginTop: 0 }}>使用说明：</h4>
          <ul style={{ margin: 0, paddingLeft: 20 }}>
            <li>点击"暂停"可以暂停定时任务，暂停后任务不会自动执行</li>
            <li>点击"启动"可以恢复暂停的定时任务</li>
            <li>点击"立即执行爬虫"可以手动触发一次爬虫任务</li>
            <li>任务状态显示"运行中"表示任务正常调度，"已暂停"表示任务已停止</li>
          </ul>
        </div>
      </Card>
    </div>
  )
}

export default JobManager
