import React, { useEffect, useState } from 'react'
import { Table, Tag, DatePicker, Select, Button, message, Card, Image, Space, Modal, Radio, Popover } from 'antd'
import { EditOutlined, LinkOutlined, PictureOutlined, DeleteOutlined, ClockCircleOutlined, DeleteRowOutlined } from '@ant-design/icons'
import { weiboApi, bloggerApi } from '../../services/api'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

function WeiboList() {
  const [weibos, setWeibos] = useState([])
  const [bloggers, setBloggers] = useState([])
  const [loading, setLoading] = useState(false)
  const [editingWeibo, setEditingWeibo] = useState(null)
  const [editModalVisible, setEditModalVisible] = useState(false)
  const [editPrediction, setEditPrediction] = useState('unknown')
  
  // 时间段同步弹窗状态
  const [timeRangeModalVisible, setTimeRangeModalVisible] = useState(false)
  const [timeRangeBloggerId, setTimeRangeBloggerId] = useState(null)
  const [timeRangeDate, setTimeRangeDate] = useState(null)
  const [timeRangeSlot, setTimeRangeSlot] = useState(null)
  const [timeRangeSyncing, setTimeRangeSyncing] = useState(false)
  
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  })
  const [filters, setFilters] = useState({
    blogger_id: undefined,
    date: undefined,
    guess_prediction: undefined,
    guess_round: undefined
  })
  
  // 批量删除相关状态
  const [selectedRowKeys, setSelectedRowKeys] = useState([])
  const [batchDeleting, setBatchDeleting] = useState(false)

  // 使用指定筛选值获取微博列表
  const fetchWeibosWithFilters = async (currentFilters, extraParams = {}) => {
    try {
      setLoading(true)
      // 构建查询参数 - extraParams 放在后面以覆盖默认值
      const queryParams = {
        page: 1,
        per_page: pagination.pageSize,
        ...extraParams
      }
      
      // 添加筛选参数
      if (currentFilters.blogger_id) queryParams.blogger_id = currentFilters.blogger_id
      if (currentFilters.date) queryParams.date = currentFilters.date
      if (currentFilters.guess_prediction) queryParams.guess_prediction = currentFilters.guess_prediction
      if (currentFilters.guess_round) queryParams.round = currentFilters.guess_round
      
      console.log('API请求参数:', queryParams)
      
      const res = await weiboApi.getList(queryParams)
      if (res.success) {
        setWeibos(res.data)
        setPagination({
          ...pagination,
          total: res.pagination.total,
          current: res.pagination.page
        })
      }
    } catch (error) {
      message.error('获取微博列表失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBloggers()
    // 页面加载时使用当前filters获取数据
    fetchWeibosWithFilters({
      blogger_id: undefined,
      date: undefined,
      guess_prediction: undefined,
      guess_round: undefined
    })
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const fetchBloggers = async () => {
    try {
      const res = await bloggerApi.getList({ is_active: true, per_page: 100 })
      if (res.success) {
        setBloggers(res.data)
        console.log('微博列表页获取博主数量:', res.data.length)
      }
    } catch (error) {
      console.error('获取博主列表失败', error)
    }
  }



  // 打开时间段同步弹窗
  const handleOpenTimeRangeSync = () => {
    setTimeRangeBloggerId(null)
    setTimeRangeDate(null)
    setTimeRangeSlot(null)
    setTimeRangeModalVisible(true)
  }

  // 轮询任务状态
  const pollTaskStatus = async (taskId, bloggerName) => {
    const maxAttempts = 60 // 最多轮询60次（约2分钟）
    let attempts = 0
    
    const checkStatus = async () => {
      try {
        const res = await weiboApi.getSyncTaskStatus(taskId)
        
        if (!res.success) {
          message.destroy()
          message.error('获取任务状态失败')
          setTimeRangeSyncing(false)
          return
        }
        
        const { status, result, error } = res.data
        
        if (status === 'completed') {
          message.destroy()
          const totalPosts = result?.total_posts || 0
          message.success(`同步完成，共爬取 ${totalPosts} 条微博`)
          fetchWeibosWithFilters(filters)
          setTimeRangeSyncing(false)
          return
        } else if (status === 'failed') {
          message.destroy()
          message.error(`同步失败: ${error || '未知错误'}`)
          setTimeRangeSyncing(false)
          return
        } else if (status === 'running' || status === 'pending') {
          attempts++
          if (attempts >= maxAttempts) {
            message.destroy()
            message.warning('同步任务仍在进行中，请稍后刷新页面查看结果')
            setTimeRangeSyncing(false)
            return
          }
          // 继续轮询
          setTimeout(checkStatus, 2000)
        }
      } catch (error) {
        console.error('轮询任务状态失败:', error)
        attempts++
        if (attempts >= maxAttempts) {
          message.destroy()
          message.warning('同步任务仍在进行中，请稍后刷新页面查看结果')
          setTimeRangeSyncing(false)
          return
        }
        setTimeout(checkStatus, 2000)
      }
    }
    
    checkStatus()
  }

  // 执行时间段同步
  const handleConfirmTimeRangeSync = async () => {
    if (!timeRangeDate || !timeRangeSlot) {
      message.error('请选择日期和时间段')
      return
    }

    try {
      setTimeRangeSyncing(true)
      setTimeRangeModalVisible(false)
      message.loading('正在创建同步任务...', 0)
      
      const res = await weiboApi.syncByTimeRange({
        blogger_id: timeRangeBloggerId,
        date: timeRangeDate.format('YYYY-MM-DD'),
        time_slot: timeRangeSlot,
        async: true // 启用异步模式
      })
      
      if (res.success && res.data.task_id) {
        message.destroy() // 关闭第一个提示框
        message.loading('同步任务进行中，请稍候...', 0)
        // 开始轮询任务状态
        const bloggerName = timeRangeBloggerId 
          ? bloggers.find(b => b.id === timeRangeBloggerId)?.nickname 
          : '全部博主'
        pollTaskStatus(res.data.task_id, bloggerName)
      } else {
        message.destroy()
        message.error(res.message || '创建同步任务失败')
        setTimeRangeSyncing(false)
      }
    } catch (error) {
      message.destroy()
      message.error('同步失败')
      setTimeRangeSyncing(false)
    }
  }

  const handleEditPrediction = (record) => {
    setEditingWeibo(record)
    setEditPrediction(record.guess_prediction || 'unknown')
    setEditModalVisible(true)
  }

  const handleDelete = async (record) => {
    Modal.confirm({
      title: '确认删除',
      content: `确定要删除这条微博吗？\n\n${record.content?.substring(0, 50)}...`,
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: async () => {
        try {
          const res = await weiboApi.delete(record.id)
          if (res.success) {
            message.success('删除成功')
            fetchWeibosWithFilters(filters)
          } else {
            message.error(res.message || '删除失败')
          }
        } catch (error) {
          message.error('删除失败')
        }
      }
    })
  }

  // 批量删除处理
  const handleBatchDelete = () => {
    if (selectedRowKeys.length === 0) {
      message.warning('请先选择要删除的微博')
      return
    }

    Modal.confirm({
      title: '确认批量删除',
      content: `确定要删除选中的 ${selectedRowKeys.length} 条微博吗？此操作不可恢复！`,
      okText: '删除',
      okType: 'danger',
      cancelText: '取消',
      onOk: async () => {
        try {
          setBatchDeleting(true)
          const res = await weiboApi.batchDelete(selectedRowKeys)
          
          if (res.success) {
            message.success(`成功删除 ${res.data.deleted_count} 条微博`)
            setSelectedRowKeys([]) // 清空选择
            fetchWeibosWithFilters(filters) // 刷新列表
          } else {
            message.error(res.message || '批量删除失败')
          }
        } catch (error) {
          console.error('批量删除错误:', error)
          const errorMsg = error.response?.data?.message || error.message || '批量删除失败'
          message.error(`批量删除失败: ${errorMsg}`)
        } finally {
          setBatchDeleting(false)
        }
      }
    })
  }

  // 表格选择配置
  const rowSelection = {
    selectedRowKeys,
    onChange: (newSelectedRowKeys) => {
      setSelectedRowKeys(newSelectedRowKeys)
    }
  }

  const handleSavePrediction = async () => {
    try {
      const res = await weiboApi.updatePrediction(editingWeibo.id, editPrediction)
      if (res.success) {
        message.success('预测结果更新成功')
        setEditModalVisible(false)
        fetchWeibosWithFilters(filters)
      } else {
        message.error(res.message || '更新失败')
      }
    } catch (error) {
      message.error('更新失败')
    }
  }

  const handleTableChange = (newPagination) => {
    setPagination(newPagination)
    fetchWeibosWithFilters(filters, {
      page: newPagination.current,
      per_page: newPagination.pageSize
    })
  }

  const handleFilterChange = (key, value) => {
    const newFilters = { ...filters, [key]: value }
    setFilters(newFilters)
    setPagination({ ...pagination, current: 1 })
    
    // 立即使用新的筛选值调用API
    fetchWeibosWithFilters(newFilters, { page: 1 })
  }

  // 渲染图片预览
  const renderPics = (picUrls) => {
    if (!picUrls || picUrls.length === 0) {
      return <span style={{ color: '#999' }}>无图片</span>
    }
    
    return (
      <Popover
        content={
          <div style={{ maxWidth: 300 }}>
            <Image.PreviewGroup>
              <Space wrap>
                {picUrls.map((url, index) => (
                  <Image
                    key={index}
                    src={url}
                    width={80}
                    height={80}
                    style={{ objectFit: 'cover', cursor: 'pointer' }}
                    preview={{ src: url }}
                  />
                ))}
              </Space>
            </Image.PreviewGroup>
          </div>
        }
        title="图片预览"
        trigger="click"
      >
        <Button type="link" icon={<PictureOutlined />}>
          查看图片({picUrls.length})
        </Button>
      </Popover>
    )
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 60
    },
    {
      title: '博主',
      dataIndex: 'blogger_nickname',
      width: 100
    },
    {
      title: '内容',
      dataIndex: 'content',
      render: (content, record) => (
        <div>
          <div style={{ 
            maxWidth: 400, 
            maxHeight: 100,
            overflow: 'auto',
            whiteSpace: 'pre-wrap',
            wordBreak: 'break-all',
            marginBottom: 8,
            fontSize: 13,
            lineHeight: 1.5
          }}>{content}</div>
          {record.weibo_url && (
            <a href={record.weibo_url} target="_blank" rel="noopener noreferrer">
              <LinkOutlined /> 查看原微博
            </a>
          )}
        </div>
      )
    },
    {
      title: '图片',
      width: 120,
      render: (_, record) => renderPics(record.pic_urls)
    },
    {
      title: '预测',
      dataIndex: 'guess_prediction_text',
      width: 120,
      render: (text, record) => {
        const colors = {
          '左': 'red',
          '右': 'blue',
          '未知': 'default'
        }
        return (
          <Space>
            <Tag color={colors[text]}>{text}</Tag>
            <Button
              type="link"
              size="small"
              icon={<EditOutlined />}
              onClick={() => handleEditPrediction(record)}
            >
              编辑
            </Button>
          </Space>
        )
      }
    },
    {
      title: '轮次',
      dataIndex: 'guess_round',
      width: 80,
      render: (round) => round ? `第${round}轮` : '-'
    },
    {
      title: '日期',
      dataIndex: 'guess_date',
      width: 110
    },
    {
      title: '发布时间',
      dataIndex: 'publish_time',
      width: 140,
      sorter: (a, b) => new Date(a.publish_time) - new Date(b.publish_time),
      defaultSortOrder: 'descend',
      render: (time) => time ? dayjs(time).format('MM-DD HH:mm') : '-'
    },
    {
      title: '互动',
      width: 140,
      render: (_, record) => (
        <span>
          <Tag color="blue">转{record.reposts_count}</Tag>
          <Tag color="green">评{record.comments_count}</Tag>
          <Tag color="red">赞{record.attitudes_count}</Tag>
        </span>
      )
    },
    {
      title: '操作',
      width: 100,
      fixed: 'right',
      render: (_, record) => (
        <Button
          type="link"
          danger
          size="small"
          icon={<DeleteOutlined />}
          onClick={() => handleDelete(record)}
        >
          删除
        </Button>
      )
    }
  ]

  const bloggerOptions = bloggers.map(b => ({
    label: b.nickname,
    value: b.id
  }))

  return (
    <div>
      <Card
        title="微博列表"
        extra={
          <Space>
            <Button
              type="primary"
              icon={<ClockCircleOutlined />}
              onClick={handleOpenTimeRangeSync}
              loading={timeRangeSyncing}
            >
              同步指定时间段竞猜结果
            </Button>
          </Space>
        }
      >
        <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Space>
            <Select
              placeholder="选择博主"
              style={{ width: 200 }}
              allowClear
              showSearch
              filterOption={(input, option) =>
                option?.label?.toLowerCase().includes(input.toLowerCase())
              }
              options={bloggerOptions}
              value={filters.blogger_id}
              onChange={(value) => handleFilterChange('blogger_id', value)}
            />
          <DatePicker
            placeholder="选择日期"
            style={{ marginRight: 16 }}
            value={filters.date ? dayjs(filters.date) : null}
            onChange={(date) => handleFilterChange('date', date ? date.format('YYYY-MM-DD') : undefined)}
          />
          <Select
            placeholder="预测选项"
            style={{ width: 120, marginRight: 16 }}
            allowClear
            options={[
              { label: '左/红', value: 'left' },
              { label: '右/蓝', value: 'right' },
              { label: '未知', value: 'unknown' },
              { label: '多条', value: 'multiple' }
            ]}
            value={filters.guess_prediction}
            onChange={(value) => handleFilterChange('guess_prediction', value)}
          />
          <Select
            placeholder="选择轮次"
            style={{ width: 120 }}
            allowClear
            options={[
              { label: '第1轮', value: 1 },
              { label: '第2轮', value: 2 },
              { label: '第3轮', value: 3 },
              { label: '第4轮', value: 4 },
              { label: '第5轮', value: 5 },
              { label: '第6轮', value: 6 },
              { label: '第7轮', value: 7 }
            ]}
            value={filters.guess_round}
            onChange={(value) => handleFilterChange('guess_round', value)}
          />
          </Space>
          
          <Button
            type="primary"
            danger
            icon={<DeleteRowOutlined />}
            onClick={handleBatchDelete}
            loading={batchDeleting}
            disabled={selectedRowKeys.length === 0}
          >
            批量删除 ({selectedRowKeys.length})
          </Button>
        </div>

        <Table
          columns={columns}
          dataSource={weibos}
          rowKey="id"
          loading={loading}
          rowSelection={rowSelection}
          pagination={{
            ...pagination,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `共 ${total} 条，当前显示 ${range[0]}-${range[1]} 条`,
            pageSizeOptions: [10, 20, 50, 100]
          }}
          onChange={handleTableChange}
          scroll={{ x: 1200 }}
        />
      </Card>

      {/* 编辑预测结果弹窗 */}
      <Modal
        title="编辑预测结果"
        open={editModalVisible}
        onOk={handleSavePrediction}
        onCancel={() => setEditModalVisible(false)}
      >
        <div style={{ padding: '20px 0' }}>
          <p>微博内容：</p>
          <div style={{ 
            padding: 12, 
            background: '#f5f5f5', 
            borderRadius: 4,
            marginBottom: 16,
            maxHeight: 150,
            overflow: 'auto'
          }}>
            {editingWeibo?.content}
          </div>
          
          {editingWeibo?.pic_urls && editingWeibo.pic_urls.length > 0 && (
            <div style={{ marginBottom: 16 }}>
              <p>图片预览：</p>
              <Image.PreviewGroup>
                <Space wrap>
                  {editingWeibo.pic_urls.map((url, index) => (
                    <Image
                      key={index}
                      src={url}
                      width={100}
                      height={100}
                      style={{ objectFit: 'cover' }}
                    />
                  ))}
                </Space>
              </Image.PreviewGroup>
            </div>
          )}
          
          <p>选择预测结果：</p>
          <Radio.Group 
            value={editPrediction}
            onChange={(e) => setEditPrediction(e.target.value)}
          >
            <Radio.Button value="left">左</Radio.Button>
            <Radio.Button value="right">右</Radio.Button>
            <Radio.Button value="unknown">未知</Radio.Button>
          </Radio.Group>
        </div>
      </Modal>

      {/* 时间段同步弹窗 */}
      <Modal
        title="同步指定时间段竞猜结果"
        open={timeRangeModalVisible}
        onOk={handleConfirmTimeRangeSync}
        onCancel={() => setTimeRangeModalVisible(false)}
        okText="开始同步"
        cancelText="取消"
      >
        <div style={{ padding: '20px 0' }}>
          <p>请选择博主：</p>
          <Select
            placeholder="选择博主（不选则同步全部）"
            style={{ width: '100%', marginBottom: 16 }}
            allowClear
            showSearch
            filterOption={(input, option) =>
              option?.label?.toLowerCase().includes(input.toLowerCase())
            }
            options={bloggerOptions}
            value={timeRangeBloggerId}
            onChange={(value) => setTimeRangeBloggerId(value)}
          />
          
          <p>请选择日期：</p>
          <DatePicker
            placeholder="选择日期"
            style={{ width: '100%', marginBottom: 16 }}
            value={timeRangeDate}
            onChange={(date) => setTimeRangeDate(date)}
            disabledDate={(current) => current && current > dayjs().endOf('day')}
          />
          
          <p>请选择时间段：</p>
          <Select
            placeholder="选择时间段"
            style={{ width: '100%' }}
            value={timeRangeSlot}
            onChange={(value) => setTimeRangeSlot(value)}
            options={[
              { label: '10:00 - 12:00', value: '10:00-12:00' },
              { label: '12:00 - 14:00', value: '12:00-14:00' },
              { label: '14:00 - 16:00', value: '14:00-16:00' },
              { label: '16:00 - 18:00', value: '16:00-18:00' },
              { label: '18:00 - 20:00', value: '18:00-20:00' },
              { label: '20:00 - 22:00', value: '20:00-22:00' },
              { label: '22:00 - 24:00', value: '22:00-24:00' }
            ]}
          />
          
          <p style={{ marginTop: 16, color: '#999', fontSize: 12 }}>
            提示：系统将爬取指定时间段内博主的最新一条竞猜微博。
          </p>
        </div>
      </Modal>
    </div>
  )
}

export default WeiboList
