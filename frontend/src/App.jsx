import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Layout, Menu, Typography } from 'antd'
import {
  HomeOutlined,
  TeamOutlined,
  FileTextOutlined,
  BarChartOutlined,
  EditOutlined,
  SettingOutlined
} from '@ant-design/icons'
import Home from './pages/Home'
import Bloggers from './pages/Bloggers'
import WeiboList from './pages/WeiboList'
import GuessAnalysis from './pages/GuessAnalysis'
import OfficialInput from './pages/OfficialInput'
import JobManager from './pages/JobManager'

const { Header, Sider, Content } = Layout
const { Title } = Typography

const menuItems = [
  {
    key: '/',
    icon: <HomeOutlined />,
    label: '首页',
  },
  {
    key: '/bloggers',
    icon: <TeamOutlined />,
    label: '博主管理',
  },
  {
    key: '/weibo',
    icon: <FileTextOutlined />,
    label: '微博列表',
  },
  {
    key: '/analysis',
    icon: <BarChartOutlined />,
    label: '竞猜分析',
  },
  {
    key: '/official',
    icon: <EditOutlined />,
    label: '官方结果录入',
  },
  {
    key: '/jobs',
    icon: <SettingOutlined />,
    label: '定时任务管理',
  },
]

function App() {
  const [collapsed, setCollapsed] = React.useState(false)

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center',
          background: '#001529',
          padding: '0 24px'
        }}>
          <Title level={3} style={{ color: '#fff', margin: 0 }}>
            阴阳师对弈竞猜分析系统
          </Title>
        </Header>
        <Layout>
          <Sider 
            collapsible 
            collapsed={collapsed} 
            onCollapse={(value) => setCollapsed(value)}
            theme="light"
          >
            <Menu
              mode="inline"
              defaultSelectedKeys={['/']}
              items={menuItems}
              onClick={({ key }) => {
                window.location.href = key
              }}
            />
          </Sider>
          <Content style={{ margin: '24px 16px', padding: 24, background: '#fff' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/bloggers" element={<Bloggers />} />
              <Route path="/weibo" element={<WeiboList />} />
              <Route path="/analysis" element={<GuessAnalysis />} />
              <Route path="/official" element={<OfficialInput />} />
              <Route path="/jobs" element={<JobManager />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  )
}

export default App
