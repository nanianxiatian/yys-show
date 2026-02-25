import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { Layout, Menu, Typography } from 'antd'
import {
  HomeOutlined,
  TeamOutlined,
  FileTextOutlined,
  BarChartOutlined,
  EditOutlined,
  SettingOutlined,
  FireOutlined,
  CrownOutlined,
  SafetyOutlined
} from '@ant-design/icons'
import Home from './pages/Home'
import Bloggers from './pages/Bloggers'
import WeiboList from './pages/WeiboList'
import GuessAnalysis from './pages/GuessAnalysis'
import OfficialInput from './pages/OfficialInput'
import JobManager from './pages/JobManager'
import ShikigamiAnalysis from './pages/ShikigamiAnalysis'
import ShikigamiManager from './pages/ShikigamiManager'
import CookieManager from './pages/CookieManager'

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
    key: '/shikigami',
    icon: <FireOutlined />,
    label: '式神分析',
  },
  {
    key: '/shikigami-manager',
    icon: <CrownOutlined />,
    label: '式神管理',
  },
  {
    key: '/jobs',
    icon: <SettingOutlined />,
    label: '定时任务管理',
  },
  {
    key: '/cookie',
    icon: <SafetyOutlined />,
    label: 'Cookie管理',
  },
]

// 内部组件，可以使用 useLocation
function AppContent({ collapsed, setCollapsed }) {
  const location = useLocation()
  
  // 获取当前路径作为选中项
  const selectedKey = location.pathname

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
        padding: '0 24px',
        borderBottom: '2px solid #ffd700'
      }}>
        <img
          src="/frog.png"
          alt="青蛙瓷器"
          style={{
            width: '44px',
            height: '44px',
            marginRight: '12px',
            borderRadius: '50%',
            border: '2px solid #ffffff',
            boxShadow: '0 0 10px rgba(255, 255, 255, 0.5)',
            objectFit: 'cover'
          }}
        />
        <Title level={3} style={{
          color: '#fff',
          margin: 0,
          textShadow: '0 0 10px rgba(255, 215, 0, 0.5)'
        }}>
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
            selectedKeys={[selectedKey]}
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
            <Route path="/shikigami" element={<ShikigamiAnalysis />} />
            <Route path="/shikigami-manager" element={<ShikigamiManager />} />
            <Route path="/official" element={<OfficialInput />} />
            <Route path="/jobs" element={<JobManager />} />
            <Route path="/cookie" element={<CookieManager />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  )
}

function App() {
  const [collapsed, setCollapsed] = React.useState(false)

  return (
    <Router>
      <AppContent collapsed={collapsed} setCollapsed={setCollapsed} />
    </Router>
  )
}

export default App
