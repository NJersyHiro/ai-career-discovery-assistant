import React from 'react'
import { Form, Input, Button, Card, Typography } from 'antd'
import { UserOutlined, LockOutlined, MailOutlined } from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'

const { Title, Text } = Typography

interface RegisterFormValues {
  email: string
  password: string
  confirmPassword: string
  fullName?: string
}

export const RegisterForm: React.FC = () => {
  const [form] = Form.useForm<RegisterFormValues>()
  const { register } = useAuth()
  const [loading, setLoading] = React.useState(false)

  const onFinish = async (values: RegisterFormValues) => {
    setLoading(true)
    try {
      await register(values.email, values.password, values.fullName)
    } catch (error) {
      // Error is handled in AuthContext
    } finally {
      setLoading(false)
    }
  }

  return (
    <Card className="w-full max-w-md mx-auto">
      <div className="text-center mb-8">
        <Title level={2}>新規登録</Title>
        <Text type="secondary">
          アカウントを作成してAIキャリア分析を始めましょう
        </Text>
      </div>

      <Form
        form={form}
        name="register"
        onFinish={onFinish}
        layout="vertical"
        size="large"
      >
        <Form.Item
          name="fullName"
          label="お名前（任意）"
        >
          <Input
            prefix={<UserOutlined />}
            placeholder="山田 太郎"
            autoComplete="name"
          />
        </Form.Item>

        <Form.Item
          name="email"
          label="メールアドレス"
          rules={[
            { required: true, message: 'メールアドレスを入力してください' },
            { type: 'email', message: '有効なメールアドレスを入力してください' }
          ]}
        >
          <Input
            prefix={<MailOutlined />}
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
            placeholder="パスワード（8文字以上）"
            autoComplete="new-password"
          />
        </Form.Item>

        <Form.Item
          name="confirmPassword"
          label="パスワード（確認）"
          dependencies={['password']}
          rules={[
            { required: true, message: 'パスワードを再度入力してください' },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue('password') === value) {
                  return Promise.resolve()
                }
                return Promise.reject(new Error('パスワードが一致しません'))
              },
            }),
          ]}
        >
          <Input.Password
            prefix={<LockOutlined />}
            placeholder="パスワード（確認）"
            autoComplete="new-password"
          />
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            block
            loading={loading}
          >
            登録する
          </Button>
        </Form.Item>

        <div className="text-center">
          <Text>
            すでにアカウントをお持ちの方は{' '}
            <Link to="/login">ログイン</Link>
          </Text>
        </div>
      </Form>
    </Card>
  )
}