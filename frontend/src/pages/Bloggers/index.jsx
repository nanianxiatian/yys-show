import React, { useEffect, useState } from 'react'
import {
  Table, Button, Modal, Form, Input, Switch, Space, Tag, message, Popconfirm, Radio
} from 'antd'
import {
  PlusOutlined, EditOutlined, DeleteOutlined, SyncOutlined, UserOutlined, LinkOutlined
} from '@ant-design/icons'
import { bloggerApi } from '../../services/api'

function Bloggers() {
  const [bloggers, setBloggers] = useState([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingBlogger, setEditingBlogger] = useState(null)
  const [syncLoading, setSyncLoading] = useState({})
  const [form] = Form.useForm()
  const [inputMode, setInputMode] = useState('nickname') // 'nickname' 或 'url'
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0
  })

  useEffect(() => {
    fetchBloggers()
  }, [])

  const fetchBloggers = async (params = {}) => {
    try {
      setLoading(true)
      const queryParams = {
        page: pagination.current,
        per_page: pagination.pageSize,
        ...params
      }
      const res = await bloggerApi.getList(queryParams)
      if (res.success) {
        setBloggers(res.data)
        setPagination({
          ...pagination,
          total: res.pagination?.total || res.data.length,
          current: res.pagination?.page || 1
        })
      }
    } catch (error) {
      message.error('获取博主列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleTableChange = (newPagination) => {
    setPagination(newPagination)
    fetchBloggers({
      page: newPagination.current,
      per_page: newPagination.pageSize
    })
  }

  const handleAdd = () => {
    setEditingBlogger(null)
    setInputMode('nickname')
    form.resetFields()
    setModalVisible(true)
  }

  // 从微博URL提取UID
  const extractUidFromUrl = (url) => {
    // 支持多种URL格式：
    // https://weibo.com/u/1234567890
    // https://weibo.com/1234567890
    // https://weibo.com/n/昵称
    const patterns = [
      /\/u\/(\d+)/,           // /u/1234567890
      /weibo\.com\/(\d{6,})/, // weibo.com/1234567890 (6位以上数字)
    ]
    
    for (const pattern of patterns) {
      const match = url.match(pattern)
      if (match) {
        return match[1]
      }
    }
    return null
  }

  const handleEdit = (record) => {
    setEditingBlogger(record)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = async (id) => {
    try {
      const res = await bloggerApi.delete(id)
      if (res.success) {
        message.success('删除成功')
        fetchBloggers()
      }
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleSync = async (id) => {
    try {
      setSyncLoading({ ...syncLoading, [id]: true })
      const res = await bloggerApi.sync(id)
      if (res.success) {
        message.success(res.message)
        // 同步成功后刷新页面
        fetchBloggers()
      } else {
        message.error(res.message)
      }
    } catch (error) {
      message.error('同步失败')
    } finally {
      setSyncLoading({ ...syncLoading, [id]: false })
    }
  }

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields()
      
      // 处理URL模式
      if (!editingBlogger && inputMode === 'url' && values.weibo_url) {
        const uid = extractUidFromUrl(values.weibo_url)
        if (!uid) {
          message.error('无法从URL中提取UID，请检查URL格式')
          return
        }
        values.weibo_uid = uid
        // 如果没有填写昵称，使用默认值
        if (!values.nickname) {
          values.nickname = '新博主' + uid.slice(-4)
        }
      }
      
      if (editingBlogger) {
        const res = await bloggerApi.update(editingBlogger.id, values)
        if (res.success) {
          message.success('更新成功')
          setModalVisible(false)
          fetchBloggers()
        }
      } else {
        const res = await bloggerApi.create(values)
        if (res.success) {
          message.success('创建成功')
          setModalVisible(false)
          fetchBloggers()
        }
      }
    } catch (error) {
      console.error(error)
    }
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80
    },
    {
      title: '头像',
      dataIndex: 'avatar_url',
      width: 80,
      render: (avatar) => (
        avatar ? (
          <img
            src={avatar}
            alt="头像"
            style={{ width: 50, height: 50, borderRadius: '50%', objectFit: 'cover' }}
          />
        ) : (
          <div style={{ width: 50, height: 50, borderRadius: '50%', background: '#f0f0f0', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <UserOutlined style={{ fontSize: 24, color: '#999' }} />
          </div>
        )
      )
    },
    {
      title: '昵称',
      dataIndex: 'nickname'
    },
    {
      title: '微博UID',
      dataIndex: 'weibo_uid',
      width: 120,
      render: (uid) => uid || '-'
    },
    {
      title: '个人主页',
      dataIndex: 'weibo_uid',
      width: 100,
      render: (uid) => {
        if (!uid) return '-'
        const url = `https://weibo.com/u/${uid}`
        return (
          <a href={url} target="_blank" rel="noopener noreferrer">
            <LinkOutlined /> 查看
          </a>
        )
      }
    },
    {
      title: '描述',
      dataIndex: 'description',
      ellipsis: true,
      render: (desc) => desc || '-'
    },
    {
      title: '状态',
      dataIndex: 'is_active',
      width: 100,
      render: (active) => (
        <Tag color={active ? 'success' : 'default'}>
          {active ? '启用' : '禁用'}
        </Tag>
      )
    },
    {
      title: '操作',
      key: 'action',
      width: 250,
      render: (_, record) => (
        <Space>
          <Button
            type="primary"
            size="small"
            icon={<SyncOutlined />}
            loading={syncLoading[record.id]}
            onClick={() => handleSync(record.id)}
          >
            同步信息
          </Button>
          <Button
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确定删除吗？"
            onConfirm={() => handleDelete(record.id)}
          >
            <Button
              size="small"
              danger
              icon={<DeleteOutlined />}
            >
              删除
            </Button>
          </Popconfirm>
        </Space>
      )
    }
  ]

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
          添加博主
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={bloggers}
        rowKey="id"
        loading={loading}
        pagination={{
          ...pagination,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `共 ${total} 条，当前显示 ${range[0]}-${range[1]} 条`,
          pageSizeOptions: [5, 10, 20, 50]
        }}
        onChange={handleTableChange}
      />

      <Modal
        title={editingBlogger ? '编辑博主' : '添加博主'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={520}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ is_active: true }}
        >
          {!editingBlogger && (
            <Form.Item label="录入方式">
              <Radio.Group 
                value={inputMode} 
                onChange={(e) => {
                  setInputMode(e.target.value)
                  form.resetFields()
                }}
              >
                <Radio.Button value="nickname">
                  <UserOutlined /> 通过昵称
                </Radio.Button>
                <Radio.Button value="url">
                  <LinkOutlined /> 通过主页URL
                </Radio.Button>
              </Radio.Group>
            </Form.Item>
          )}

          {inputMode === 'nickname' || editingBlogger ? (
            <Form.Item
              name="nickname"
              label="博主昵称"
              rules={[{ required: true, message: '请输入博主昵称' }]}
            >
              <Input placeholder="请输入微博昵称" />
            </Form.Item>
          ) : (
            <>
              <Form.Item
                name="weibo_url"
                label="微博主页URL"
                rules={[{ required: true, message: '请输入微博主页URL' }]}
                extra="支持格式：https://weibo.com/u/1234567890 或 https://weibo.com/1234567890"
              >
                <Input.TextArea 
                  rows={2} 
                  placeholder="请输入微博主页URL，例如：https://weibo.com/u/1234567890"
                />
              </Form.Item>
              <Form.Item
                name="nickname"
                label="博主昵称（可选）"
                extra="留空会自动生成"
              >
                <Input placeholder="留空会自动生成" />
              </Form.Item>
            </>
          )}

          <Form.Item
            name="weibo_uid"
            label="微博UID"
            extra="可选，保存后会自动获取"
          >
            <Input placeholder="留空会自动获取" disabled />
          </Form.Item>

          <Form.Item
            name="description"
            label="描述"
          >
            <Input.TextArea rows={3} placeholder="可选" />
          </Form.Item>

          <Form.Item
            name="is_active"
            label="状态"
            valuePropName="checked"
          >
            <Switch checkedChildren="启用" unCheckedChildren="禁用" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default Bloggers
