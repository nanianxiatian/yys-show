import React, { useEffect, useState } from 'react'
import {
  Card, Table, Button, Input, Modal, Form, message, Space, Popconfirm, Tag, Select
} from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined, SearchOutlined } from '@ant-design/icons'
import { shikigamiManagerApi } from '../../services/api'

const { Option } = Select

// 稀有度选项
const RARITY_OPTIONS = [
  { value: 'N', label: 'N', color: 'default' },
  { value: 'R', label: 'R', color: 'success' },
  { value: 'SR', label: 'SR', color: 'blue' },
  { value: 'SSR', label: 'SSR', color: 'purple' },
  { value: 'SP', label: 'SP', color: 'orange' },
  { value: 'UR', label: 'UR', color: 'red' },
  { value: '素材', label: '素材', color: 'cyan' }
]

function ShikigamiManager() {
  const [shikigamis, setShikigamis] = useState([])
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingShikigami, setEditingShikigami] = useState(null)
  const [searchKeyword, setSearchKeyword] = useState('')
  const [selectedRarity, setSelectedRarity] = useState(undefined)
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 20,
    total: 0
  })
  const [form] = Form.useForm()

  useEffect(() => {
    fetchShikigamis()
  }, [pagination.current, pagination.pageSize, searchKeyword, selectedRarity])

  const fetchShikigamis = async () => {
    try {
      setLoading(true)
      const params = {
        page: pagination.current,
        per_page: pagination.pageSize,
        keyword: searchKeyword
      }
      if (selectedRarity) {
        params.rarity = selectedRarity
      }
      const res = await shikigamiManagerApi.getList(params)

      if (res.success) {
        setShikigamis(res.data)
        setPagination({
          ...pagination,
          total: res.total
        })
      }
    } catch (error) {
      message.error('获取式神列表失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAdd = () => {
    setEditingShikigami(null)
    form.resetFields()
    setModalVisible(true)
  }

  const handleEdit = (record) => {
    setEditingShikigami(record)
    form.setFieldsValue(record)
    setModalVisible(true)
  }

  const handleDelete = async (id) => {
    try {
      const res = await shikigamiManagerApi.delete(id)
      if (res.success) {
        message.success('删除成功')
        fetchShikigamis()
      } else {
        message.error(res.message)
      }
    } catch (error) {
      message.error('删除失败')
    }
  }

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields()

      let res
      if (editingShikigami) {
        res = await shikigamiManagerApi.update(editingShikigami.id, values)
      } else {
        res = await shikigamiManagerApi.create(values)
      }

      if (res.success) {
        message.success(editingShikigami ? '更新成功' : '创建成功')
        setModalVisible(false)
        fetchShikigamis()
      } else {
        message.error(res.message)
      }
    } catch (error) {
      message.error('操作失败')
    }
  }

  const handleSearch = (value) => {
    setSearchKeyword(value)
    setPagination({ ...pagination, current: 1 })
  }

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      width: 80
    },
    {
      title: '式神名称',
      dataIndex: 'name',
      width: 150,
      render: (name) => <Tag color="blue">{name}</Tag>
    },
    {
      title: '英文简称',
      dataIndex: 'english_name',
      width: 120
    },
    {
      title: '稀有度',
      dataIndex: 'rarity',
      width: 100,
      render: (rarity) => {
        const option = RARITY_OPTIONS.find(r => r.value === rarity)
        return <Tag color={option?.color || 'default'}>{rarity || 'SR'}</Tag>
      }
    },
    {
      title: '一技能',
      dataIndex: 'skill_1',
      ellipsis: true
    },
    {
      title: '二技能',
      dataIndex: 'skill_2',
      ellipsis: true
    },
    {
      title: '三技能',
      dataIndex: 'skill_3',
      ellipsis: true
    },
    {
      title: '备注',
      dataIndex: 'description',
      ellipsis: true
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button
            type="primary"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
          <Popconfirm
            title="确认删除"
            description={`确定要删除式神 "${record.name}" 吗？`}
            onConfirm={() => handleDelete(record.id)}
            okText="删除"
            cancelText="取消"
            okButtonProps={{ danger: true }}
          >
            <Button
              type="primary"
              danger
              size="small"
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
      <Card
        title="式神管理"
        extra={
          <Space>
            <Select
              placeholder="筛选稀有度"
              allowClear
              style={{ width: 120 }}
              value={selectedRarity}
              onChange={(value) => {
                setSelectedRarity(value)
                setPagination({ ...pagination, current: 1 })
              }}
            >
              {RARITY_OPTIONS.map(option => (
                <Option key={option.value} value={option.value}>
                  <Tag color={option.color}>{option.label}</Tag>
                </Option>
              ))}
            </Select>
            <Input.Search
              placeholder="搜索式神名称"
              allowClear
              onSearch={handleSearch}
              style={{ width: 200 }}
              prefix={<SearchOutlined />}
            />
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleAdd}
            >
              添加式神
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={shikigamis}
          rowKey="id"
          loading={loading}
          pagination={{
            ...pagination,
            showSizeChanger: true,
            showTotal: (total) => `共 ${total} 个式神`,
            pageSizeOptions: ['10', '20', '50', '100']
          }}
          onChange={(p) => setPagination({
            ...pagination,
            current: p.current,
            pageSize: p.pageSize
          })}
        />
      </Card>

      <Modal
        title={editingShikigami ? '编辑式神' : '添加式神'}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Form.Item
            name="name"
            label="式神名称"
            rules={[{ required: true, message: '请输入式神名称' }]}
          >
            <Input placeholder="如：鬼切" />
          </Form.Item>

          <Form.Item
            name="english_name"
            label="英文简称"
          >
            <Input placeholder="如：Onikiri" />
          </Form.Item>

          <Form.Item
            name="rarity"
            label="稀有度"
            rules={[{ required: true, message: '请选择稀有度' }]}
          >
            <Select placeholder="选择稀有度">
              {RARITY_OPTIONS.map(option => (
                <Option key={option.value} value={option.value}>
                  <Tag color={option.color}>{option.label}</Tag>
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="skill_1"
            label="一技能"
          >
            <Input placeholder="描述一技能效果" />
          </Form.Item>

          <Form.Item
            name="skill_2"
            label="二技能"
          >
            <Input placeholder="描述二技能效果" />
          </Form.Item>

          <Form.Item
            name="skill_3"
            label="三技能"
          >
            <Input placeholder="描述三技能效果" />
          </Form.Item>

          <Form.Item
            name="description"
            label="备注"
          >
            <Input.TextArea rows={3} placeholder="其他备注信息" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default ShikigamiManager
