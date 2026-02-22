import React, { useEffect, useState } from 'react'
import {
  Card, DatePicker, Radio, Button, Table, Tag, message, Space, Modal, Form, Input
} from 'antd'
import { SaveOutlined, PlusOutlined } from '@ant-design/icons'
import { officialApi } from '../../services/api'
import dayjs from 'dayjs'

const { TextArea } = Input

function OfficialInput() {
  const [selectedDate, setSelectedDate] = useState(dayjs())
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [editingRound, setEditingRound] = useState(null)
  const [form] = Form.useForm()

  // 7轮竞猜
  const rounds = [1, 2, 3, 4, 5, 6, 7]

  useEffect(() => {
    fetchResults()
  }, [selectedDate])

  const fetchResults = async () => {
    try {
      setLoading(true)
      const dateStr = selectedDate.format('YYYY-MM-DD')
      const res = await officialApi.getList({ date: dateStr })
      
      if (res.success) {
        // 构建完整的结果列表
        const resultMap = {}
        res.data.forEach(item => {
          resultMap[item.guess_round] = item
        })
        
        const fullResults = rounds.map(round => ({
          guess_round: round,
          ...resultMap[round]
        }))
        
        setResults(fullResults)
      }
    } catch (error) {
      message.error('获取数据失败')
    } finally {
      setLoading(false)
    }
  }

  const handleAddResult = (round) => {
    setEditingRound(round)
    form.resetFields()
    form.setFieldsValue({
      guess_date: selectedDate.format('YYYY-MM-DD'),
      guess_round: round
    })
    setModalVisible(true)
  }

  const handleEditResult = (record) => {
    setEditingRound(record.guess_round)
    form.setFieldsValue({
      guess_date: record.guess_date,
      guess_round: record.guess_round,
      result: record.result,
      left_team: record.left_team,
      right_team: record.right_team,
      description: record.description
    })
    setModalVisible(true)
  }

  const handleModalOk = async () => {
    try {
      const values = await form.validateFields()
      setSaving(true)
      
      // 查找是否已存在
      const existing = results.find(r => r.guess_round === values.guess_round && r.id)
      
      let res
      if (existing) {
        res = await officialApi.update(existing.id, values)
      } else {
        res = await officialApi.create(values)
      }
      
      if (res.success) {
        message.success('保存成功')
        setModalVisible(false)
        fetchResults()
      }
    } catch (error) {
      message.error('保存失败')
    } finally {
      setSaving(false)
    }
  }

  const handleBatchSave = async () => {
    try {
      // 检查是否有未录入的轮次
      const pendingRounds = results.filter(r => !r.id)
      if (pendingRounds.length === 0) {
        message.info('所有轮次已录入')
        return
      }
      
      message.info(`还有 ${pendingRounds.length} 轮未录入，请逐轮录入`)
    } catch (error) {
      message.error('操作失败')
    }
  }

  const columns = [
    {
      title: '轮次',
      dataIndex: 'guess_round',
      width: 100,
      render: (round) => `第 ${round} 轮`
    },
    {
      title: '时间',
      width: 150,
      render: (_, record) => {
        const timeMap = {
          1: '10:00-12:00',
          2: '12:00-14:00',
          3: '14:00-16:00',
          4: '16:00-18:00',
          5: '18:00-20:00',
          6: '20:00-22:00',
          7: '22:00-24:00'
        }
        return timeMap[record.guess_round]
      }
    },
    {
      title: '左侧阵营',
      dataIndex: 'left_team',
      render: (team) => team || '-'
    },
    {
      title: '右侧阵营',
      dataIndex: 'right_team',
      render: (team) => team || '-'
    },
    {
      title: '结果',
      dataIndex: 'result',
      width: 120,
      render: (result) => {
        if (!result) return <Tag>未录入</Tag>
        return (
          <Tag color={result === 'left' ? 'red' : 'blue'}>
            {result === 'left' ? '左胜' : '右胜'}
          </Tag>
        )
      }
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Button
          type={record.id ? 'default' : 'primary'}
          icon={<PlusOutlined />}
          onClick={() => record.id ? handleEditResult(record) : handleAddResult(record.guess_round)}
        >
          {record.id ? '编辑' : '录入'}
        </Button>
      )
    }
  ]

  return (
    <div>
      <Card
        title="官方竞猜结果录入"
        extra={
          <Space>
            <DatePicker
              value={selectedDate}
              onChange={setSelectedDate}
              allowClear={false}
            />
            <Button
              type="primary"
              icon={<SaveOutlined />}
              onClick={handleBatchSave}
            >
              批量检查
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={results}
          rowKey="guess_round"
          loading={loading}
          pagination={false}
        />
      </Card>

      <Modal
        title={`录入第 ${editingRound} 轮结果`}
        open={modalVisible}
        onOk={handleModalOk}
        onCancel={() => setModalVisible(false)}
        confirmLoading={saving}
      >
        <Form
          form={form}
          layout="vertical"
        >
          <Form.Item
            name="guess_date"
            label="日期"
            hidden
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="guess_round"
            label="轮次"
            hidden
          >
            <Input />
          </Form.Item>

          <Form.Item
            name="left_team"
            label="左侧阵营"
          >
            <Input placeholder="可选，如：鬼切队" />
          </Form.Item>

          <Form.Item
            name="right_team"
            label="右侧阵营"
          >
            <Input placeholder="可选，如：酒吞队" />
          </Form.Item>

          <Form.Item
            name="result"
            label="获胜方"
            rules={[{ required: true, message: '请选择获胜方' }]}
          >
            <Radio.Group>
              <Radio.Button value="left">左侧获胜</Radio.Button>
              <Radio.Button value="right">右侧获胜</Radio.Button>
            </Radio.Group>
          </Form.Item>

          <Form.Item
            name="description"
            label="备注"
          >
            <TextArea rows={3} placeholder="可选" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default OfficialInput
