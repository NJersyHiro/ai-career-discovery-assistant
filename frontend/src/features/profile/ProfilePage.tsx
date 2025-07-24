import React, { useState, useEffect } from 'react'
import { Form, Input, Button, Card, Typography, message, Row, Col, Divider, Upload, Avatar } from 'antd'
import { UserOutlined, MailOutlined, PhoneOutlined, EnvironmentOutlined, UploadOutlined, SaveOutlined } from '@ant-design/icons'
import { useAuth } from '@/contexts/AuthContext'
import axios from 'axios'

const { Title, Text } = Typography

interface ProfileData {
  full_name: string
  email: string
  phone?: string
  location?: string
  bio?: string
  skills?: string[]
  experience_years?: number
}

const ProfilePage: React.FC = () => {
  const { user, updateUser } = useAuth()
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [profileData, setProfileData] = useState<ProfileData | null>(null)

  useEffect(() => {
    if (user) {
      const data: ProfileData = {
        full_name: user.full_name || '',
        email: user.email,
        phone: '',
        location: '',
        bio: '',
        skills: [],
        experience_years: 0
      }
      setProfileData(data)
      form.setFieldsValue(data)
    }
  }, [user, form])

  const handleSubmit = async (values: ProfileData) => {
    setLoading(true)
    try {
      const response = await axios.put('/api/v1/users/me', values)
      updateUser(response.data)
      message.success('プロフィールを更新しました')
    } catch (error) {
      message.error('プロフィールの更新に失敗しました')
    } finally {
      setLoading(false)
    }
  }

  const handlePasswordChange = async (values: { current_password: string; new_password: string }) => {
    setLoading(true)
    try {
      await axios.post('/api/v1/users/change-password', values)
      message.success('パスワードを変更しました')
      form.resetFields(['current_password', 'new_password', 'confirm_password'])
    } catch (error: any) {
      if (error.response?.status === 400) {
        message.error('現在のパスワードが正しくありません')
      } else {
        message.error('パスワードの変更に失敗しました')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <Title level={2}>プロフィール設定</Title>
      
      <Row gutter={[24, 24]}>
        <Col xs={24} lg={8}>
          <Card>
            <div className="text-center">
              <Avatar size={120} icon={<UserOutlined />} className="mb-4" />
              <Upload showUploadList={false} disabled>
                <Button icon={<UploadOutlined />} disabled>
                  プロフィール画像を変更（準備中）
                </Button>
              </Upload>
              <Divider />
              <div className="text-left">
                <Text strong>登録日</Text>
                <br />
                <Text type="secondary">
                  {user?.created_at ? new Date(user.created_at).toLocaleDateString('ja-JP') : '-'}
                </Text>
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={16}>
          <Card title="基本情報" className="mb-4">
            <Form
              form={form}
              layout="vertical"
              onFinish={handleSubmit}
              initialValues={profileData || {}}
            >
              <Row gutter={16}>
                <Col xs={24} sm={12}>
                  <Form.Item
                    name="full_name"
                    label="氏名"
                    rules={[{ required: true, message: '氏名を入力してください' }]}
                  >
                    <Input prefix={<UserOutlined />} placeholder="山田 太郎" />
                  </Form.Item>
                </Col>
                <Col xs={24} sm={12}>
                  <Form.Item
                    name="email"
                    label="メールアドレス"
                    rules={[
                      { required: true, message: 'メールアドレスを入力してください' },
                      { type: 'email', message: '有効なメールアドレスを入力してください' }
                    ]}
                  >
                    <Input prefix={<MailOutlined />} disabled />
                  </Form.Item>
                </Col>
              </Row>

              <Row gutter={16}>
                <Col xs={24} sm={12}>
                  <Form.Item name="phone" label="電話番号">
                    <Input prefix={<PhoneOutlined />} placeholder="090-1234-5678" />
                  </Form.Item>
                </Col>
                <Col xs={24} sm={12}>
                  <Form.Item name="location" label="居住地">
                    <Input prefix={<EnvironmentOutlined />} placeholder="東京都" />
                  </Form.Item>
                </Col>
              </Row>

              <Form.Item name="bio" label="自己紹介">
                <Input.TextArea 
                  rows={4} 
                  placeholder="あなたの経歴や興味について簡単に説明してください"
                  maxLength={500}
                  showCount
                />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} icon={<SaveOutlined />}>
                  プロフィールを更新
                </Button>
              </Form.Item>
            </Form>
          </Card>

          <Card title="パスワード変更">
            <Form layout="vertical" onFinish={handlePasswordChange}>
              <Form.Item
                name="current_password"
                label="現在のパスワード"
                rules={[{ required: true, message: '現在のパスワードを入力してください' }]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                name="new_password"
                label="新しいパスワード"
                rules={[
                  { required: true, message: '新しいパスワードを入力してください' },
                  { min: 8, message: 'パスワードは8文字以上で入力してください' }
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item
                name="confirm_password"
                label="新しいパスワード（確認）"
                dependencies={['new_password']}
                rules={[
                  { required: true, message: 'パスワードを再入力してください' },
                  ({ getFieldValue }) => ({
                    validator(_, value) {
                      if (!value || getFieldValue('new_password') === value) {
                        return Promise.resolve()
                      }
                      return Promise.reject(new Error('パスワードが一致しません'))
                    },
                  }),
                ]}
              >
                <Input.Password />
              </Form.Item>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading}>
                  パスワードを変更
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default ProfilePage