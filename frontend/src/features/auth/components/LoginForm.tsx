import React from 'react'
import { Form, Input, Button, Card, Typography } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

const { Title, Text } = Typography

interface LoginFormValues {
  email: string
  password: string
}

export const LoginForm: React.FC = () => {
  const [form] = Form.useForm<LoginFormValues>()
  const { login } = useAuth()
  const [loading, setLoading] = React.useState(false)

  const onFinish = async (values: LoginFormValues) => {
    setLoading(true)
    try {
      await login(values.email, values.password)
    } catch (error) {
      // Error is handled in AuthContext
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <Title level={2}>ログイン</Title>
        <Text type="secondary">
          アカウントにログインしてキャリア分析を始めましょう
        </Text>
      </div>

      <Form
        form={form}
        name="login"
        onFinish={onFinish}
        layout="vertical"
        size="large"
      >
        <Form.Item
          name="email"
          label="メールアドレス"
          rules={[
            { required: true, message: 'メールアドレスを入力してください' },
            { type: 'email', message: '有効なメールアドレスを入力してください' }
          ]}
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="your@email.com"
            autoComplete="email"
          />
        </Form.Item>

        <Form.Item
          name="password"
          label="パスワード"
          rules={[
            { required: true, message: 'パスワードを入力してください' },
            { min: 8, message: 'パスワードは8文字以上で入力してください' }
          ]}
        >
          <Input.Password
            prefix={<LockOutlined />}
            placeholder="パスワード"
            autoComplete="current-password"
          />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            block
            loading={loading}
          >
            ログイン
          </Button>
        </Form.Item>

        <div className="text-center">
          <Text>
            アカウントをお持ちでない方は{' '}
            <Link to="/register">新規登録</Link>
          </Text>
        </div>
      </Form>
    </Card>
  )
}