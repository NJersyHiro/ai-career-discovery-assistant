import React from 'react'
import { Button, Typography, Row, Col, Card } from 'antd'
import { Link } from 'react-router-dom'
import { 
  FileTextOutlined, 
  RocketOutlined, 
  TeamOutlined,
  BulbOutlined 
} from '@ant-design/icons'
import { useAuth } from '@/contexts/AuthContext'

const { Title, Paragraph } = Typography

const HomePage: React.FC = () => {
  const { isAuthenticated } = useAuth()

  const features = [
    {
      icon: <FileTextOutlined className="text-4xl text-blue-500" />,
      title: '簡単アップロード',
      description: '履歴書や職務経歴書をドラッグ&ドロップで簡単にアップロード',
    },
    {
      icon: <BulbOutlined className="text-4xl text-green-500" />,
      title: 'AI分析',
      description: '最新のAI技術であなたのスキルと経験を詳細に分析',
    },
    {
      icon: <RocketOutlined className="text-4xl text-purple-500" />,
      title: 'キャリアパス提案',
      description: '企業転職、フリーランス、起業の3つの観点から最適なパスを提案',
    },
    {
      icon: <TeamOutlined className="text-4xl text-orange-500" />,
      title: '成長サポート',
      description: 'スキルギャップ分析と具体的な学習リソースの提供',
    },
  ]

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-50 to-indigo-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <Title level={1} className="text-5xl font-bold text-gray-900 mb-6">
              AIがあなたの隠れた才能を発見
            </Title>
            <Paragraph className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
              履歴書や職務経歴書をアップロードするだけで、AIが分析し、
              あなたに最適なキャリアパスを提案します。
              企業転職、フリーランス、起業まで、新しい可能性を見つけましょう。
            </Paragraph>
            <div className="space-x-4">
              {isAuthenticated ? (
                <Link to="/upload">
                  <Button type="primary" size="large" className="h-12 px-8">
                    分析を始める
                  </Button>
                </Link>
              ) : (
                <>
                  <Link to="/register">
                    <Button type="primary" size="large" className="h-12 px-8">
                      無料で始める
                    </Button>
                  </Link>
                  <Link to="/login">
                    <Button size="large" className="h-12 px-8">
                      ログイン
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Title level={2} className="text-3xl font-bold text-gray-900 mb-4">
              AI Career Discoveryの特徴
            </Title>
            <Paragraph className="text-lg text-gray-600">
              最先端のAI技術で、あなたのキャリアを多角的に分析
            </Paragraph>
          </div>

          <Row gutter={[24, 24]}>
            {features.map((feature, index) => (
              <Col xs={24} sm={12} lg={6} key={index}>
                <Card className="h-full text-center hover:shadow-lg transition-shadow">
                  <div className="mb-4">{feature.icon}</div>
                  <Title level={4}>{feature.title}</Title>
                  <Paragraph className="text-gray-600">
                    {feature.description}
                  </Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Title level={2} className="text-3xl font-bold text-gray-900 mb-4">
              使い方は簡単3ステップ
            </Title>
          </div>

          <Row gutter={[48, 48]}>
            <Col xs={24} md={8}>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  1
                </div>
                <Title level={4}>書類をアップロード</Title>
                <Paragraph className="text-gray-600">
                  履歴書や職務経歴書をPDFまたはWord形式でアップロード
                </Paragraph>
              </div>
            </Col>
            <Col xs={24} md={8}>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  2
                </div>
                <Title level={4}>AIが分析</Title>
                <Paragraph className="text-gray-600">
                  最新のAI技術でスキルや経験を詳細に分析
                </Paragraph>
              </div>
            </Col>
            <Col xs={24} md={8}>
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-500 text-white rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                  3
                </div>
                <Title level={4}>結果を確認</Title>
                <Paragraph className="text-gray-600">
                  3つの観点からキャリアパスと具体的なアクションプランを提案
                </Paragraph>
              </div>
            </Col>
          </Row>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-blue-600">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <Title level={2} className="text-3xl font-bold text-white mb-4">
            今すぐあなたの可能性を発見しよう
          </Title>
          <Paragraph className="text-xl text-blue-100 mb-8">
            完全無料で始められます。クレジットカード不要。
          </Paragraph>
          {!isAuthenticated && (
            <Link to="/register">
              <Button type="primary" size="large" className="h-12 px-8 bg-white text-blue-600 hover:bg-gray-100 border-0">
                無料で始める
              </Button>
            </Link>
          )}
        </div>
      </section>
    </div>
  )
}

export default HomePage