import React, { useEffect, useState } from 'react'
import { Card, Button, Input, Form, message, Descriptions, Tag, Space, Modal } from 'antd'
import { CheckCircleOutlined, ExclamationCircleOutlined, CopyOutlined, EditOutlined } from '@ant-design/icons'
import { systemApi } from '../../services/api'

function CookieManager() {
  const [cookieStatus, setCookieStatus] = useState(null)
  const [loading, setLoading] = useState(false)
  const [modalVisible, setModalVisible] = useState(false)
  const [cookieInput, setCookieInput] = useState('')
  const [form] = Form.useForm()

  useEffect(() => {
    checkCookieStatus()
  }, [])

  const checkCookieStatus = async () => {
    try {
      setLoading(true)
      const res = await systemApi.checkCookie()
      if (res.success) {
        setCookieStatus(res.data)
      }
    } catch (error) {
      message.error('检查Cookie状态失败')
    } finally {
      setLoading(false)
    }
  }

  const handleUpdateCookie = async () => {
    if (!cookieInput.trim()) {
      message.error('Cookie不能为空')
      return
    }

    try {
      setLoading(true)
      const res = await systemApi.updateCookie(cookieInput.trim())
      if (res.success) {
        message.success('Cookie更新成功')
        setModalVisible(false)
        setCookieInput('')
        checkCookieStatus()
      } else {
        message.error(res.message || 'Cookie更新失败')
      }
    } catch (error) {
      message.error('更新Cookie失败: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      message.success('已复制到剪贴板')
    }).catch(() => {
      message.error('复制失败')
    })
  }

  return (
    <div>
      <Card
        title="Cookie 管理"
        extra={
          <Button
            type="primary"
            icon={<EditOutlined />}
            onClick={() => setModalVisible(true)}
          >
            更新 Cookie
          </Button>
        }
      >
        <Descriptions bordered column={1} loading={loading}>
          <Descriptions.Item label="Cookie 状态">
            {cookieStatus ? (
              cookieStatus.is_valid ? (
                <Tag icon={<CheckCircleOutlined />} color="success">
                  有效
                </Tag>
              ) : (
                <Tag icon={<ExclamationCircleOutlined />} color="error">
                  无效或已过期
                </Tag>
              )
            ) : (
              <Tag>未知</Tag>
            )}
          </Descriptions.Item>
          <Descriptions.Item label="Cookie 过期时间">
            {cookieStatus?.cookie_expire_date ? (
              <span>
                {cookieStatus.cookie_expire_date}
                {cookieStatus.days_left !== null && (
                  <Tag 
                    color={cookieStatus.days_left < 7 ? 'red' : cookieStatus.days_left < 30 ? 'orange' : 'green'}
                    style={{ marginLeft: 8 }}
                  >
                    还剩 {cookieStatus.days_left} 天
                  </Tag>
                )}
              </span>
            ) : '无法解析'}
          </Descriptions.Item>
          <Descriptions.Item label="更新时间">
            {cookieStatus?.expire_time || '无记录'}
          </Descriptions.Item>
        </Descriptions>

        <div style={{ marginTop: 24 }}>
          <h4>使用说明：</h4>
          <ol>
            <li>打开浏览器，登录微博网页版</li>
            <li>按 F12 打开开发者工具，切换到 Network（网络）标签</li>
            <li>刷新页面，找到任意一个请求（如 <code>statuses/mymblog</code>）</li>
            <li>在请求头中找到 <code>Cookie</code> 字段，复制其值</li>
            <li>点击上方"更新 Cookie"按钮，粘贴并保存</li>
          </ol>
        </div>
      </Card>

      <Modal
        title="更新 Cookie"
        open={modalVisible}
        onOk={handleUpdateCookie}
        onCancel={() => {
          setModalVisible(false)
          setCookieInput('')
        }}
        confirmLoading={loading}
        width={600}
      >
        <Form layout="vertical">
          <Form.Item
            label="Cookie 字符串"
            required
            help="请从浏览器开发者工具中复制完整的 Cookie 字符串"
          >
            <Input.TextArea
              rows={6}
              value={cookieInput}
              onChange={(e) => setCookieInput(e.target.value)}
              placeholder="粘贴 Cookie 字符串..."
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default CookieManager
