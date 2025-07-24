import React, { useState } from 'react'
import { Layout, Menu, Button, Dropdown, Avatar, Space, Drawer } from 'antd'
import { Link, useLocation } from 'react-router-dom'
import {
  HomeOutlined,
  UploadOutlined,
  DashboardOutlined,
  UserOutlined,
  LogoutOutlined,
  MenuOutlined,
} from '@ant-design/icons'
import { useAuth } from '@/contexts/AuthContext'

const { Header, Content, Footer } = Layout

interface MainLayoutProps {
  children: React.ReactNode
}

const MainLayout: React.FC<MainLayoutProps> = ({ children }) => {
  const { user, logout, isAuthenticated } = useAuth()
  const location = useLocation()
  const [drawerVisible, setDrawerVisible] = useState(false)

  const menuItems = isAuthenticated
    ? [
        { key: '/', icon: <HomeOutlined />, label: <Link to="/">ホーム</Link> },
        { key: '/upload', icon: <UploadOutlined />, label: <Link to="/upload">書類アップロード</Link> },
        { key: '/dashboard', icon: <DashboardOutlined />, label: <Link to="/dashboard">ダッシュボード</Link> },
      ]
    : [
        { key: '/', icon: <HomeOutlined />, label: <Link to="/">ホーム</Link> },
      ]

  const userMenuItems = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: <Link to="/profile">プロフィール</Link>,
    },
    {
      type: 'divider' as const,
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: 'ログアウト',
      onClick: logout,
    },
  ]

  return (
    <Layout className="min-h-screen">
      <Header className="fixed z-10 w-full bg-white shadow-sm" style={{ padding: 0 }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Link to="/" className="flex items-center mr-8">
                <h1 className="text-xl font-bold text-gray-900">
                  AI Career Discovery
                </h1>
              </Link>
              {/* Desktop Menu - 個別のリンクとして表示 */}
              <nav className="hidden md:flex items-center space-x-6">
                <Link
                  to="/"
                  className={`text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium ${
                    location.pathname === '/' ? 'text-blue-600' : ''
                  }`}
                >
                  <HomeOutlined className="mr-1" />
                  ホーム
                </Link>
                {isAuthenticated && (
                  <>
                    <Link
                      to="/upload"
                      className={`text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium ${
                        location.pathname === '/upload' ? 'text-blue-600' : ''
                      }`}
                    >
                      <UploadOutlined className="mr-1" />
                      書類アップロード
                    </Link>
                    <Link
                      to="/dashboard"
                      className={`text-gray-700 hover:text-gray-900 px-3 py-2 text-sm font-medium ${
                        location.pathname === '/dashboard' ? 'text-blue-600' : ''
                      }`}
                    >
                      <DashboardOutlined className="mr-1" />
                      ダッシュボード
                    </Link>
                  </>
                )}
              </nav>
            </div>

            <div className="flex items-center">
              {/* Mobile Menu Button */}
              <Button
                type="text"
                icon={<MenuOutlined />}
                onClick={() => setDrawerVisible(true)}
                className="md:hidden"
              />
              
              {isAuthenticated ? (
                <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
                  <Button type="text" className="flex items-center">
                    <Space>
                      <Avatar icon={<UserOutlined />} />
                      <span className="hidden sm:inline">{user?.full_name || user?.email}</span>
                    </Space>
                  </Button>
                </Dropdown>
              ) : (
                <Space>
                  <Link to="/login">
                    <Button type="text">ログイン</Button>
                  </Link>
                  <Link to="/register">
                    <Button type="primary">新規登録</Button>
                  </Link>
                </Space>
              )}
            </div>
          </div>
        </div>
      </Header>

      {/* Mobile Menu Drawer */}
      <Drawer
        title="メニュー"
        placement="left"
        onClose={() => setDrawerVisible(false)}
        open={drawerVisible}
        styles={{ body: { padding: 0 } }}
      >
        <Menu
          mode="vertical"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={() => setDrawerVisible(false)}
        />
      </Drawer>

      <Content className="mt-16">
        <div className="min-h-[calc(100vh-64px-70px)]">
          {children}
        </div>
      </Content>

      <Footer className="text-center bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-gray-600">
            AI Career Discovery Assistant ©{new Date().getFullYear()} Created with ❤️ for Japan
          </p>
        </div>
      </Footer>
    </Layout>
  )
}

export default MainLayout