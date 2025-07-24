import React, { useState, useEffect } from 'react'
import { Typography, Card, Button, Empty, Row, Col, Statistic, Progress, Tag, List, Spin } from 'antd'
import { 
  UploadOutlined, 
  FileTextOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  RocketOutlined,
  TeamOutlined,
  BankOutlined,
  TrophyOutlined 
} from '@ant-design/icons'
import { Link } from 'react-router-dom'
import { useAuth } from '@/contexts/AuthContext'
import axios from 'axios'

const { Title, Text, Paragraph } = Typography

interface AnalysisData {
  id: number
  document_id: number
  status: string
  created_at: string
  document: {
    filename: string
    document_type: string
  }
  career_recommendations?: Array<{
    career_type: string
    title: string
    skill_match_percentage: number
    salary_range_min: number
    salary_range_max: number
  }>
}

const DashboardPage: React.FC = () => {
  const { user } = useAuth()
  const [analyses, setAnalyses] = useState<AnalysisData[]>([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    totalDocuments: 0,
    completedAnalyses: 0,
    pendingAnalyses: 0,
    averageMatchScore: 0
  })

  useEffect(() => {
    fetchAnalyses()
  }, [])

  const fetchAnalyses = async () => {
    try {
      const response = await axios.get('/api/v1/analysis/')
      const analysesData = response.data
      setAnalyses(analysesData)
      
      // Calculate statistics
      const completed = analysesData.filter((a: AnalysisData) => a.status === 'COMPLETED')
      const pending = analysesData.filter((a: AnalysisData) => a.status === 'PENDING' || a.status === 'PROCESSING')
      
      let totalMatchScore = 0
      let matchCount = 0
      completed.forEach((analysis: AnalysisData) => {
        if (analysis.career_recommendations) {
          analysis.career_recommendations.forEach(rec => {
            totalMatchScore += rec.skill_match_percentage
            matchCount++
          })
        }
      })
      
      setStats({
        totalDocuments: analysesData.length,
        completedAnalyses: completed.length,
        pendingAnalyses: pending.length,
        averageMatchScore: matchCount > 0 ? Math.round(totalMatchScore / matchCount) : 0
      })
    } catch (error) {
      console.error('Failed to fetch analyses:', error)
    } finally {
      setLoading(false)
    }
  }

  const getCareerIcon = (careerType: string) => {
    switch (careerType) {
      case 'corporate':
        return <BankOutlined />
      case 'freelance':
        return <TeamOutlined />
      case 'entrepreneurship':
        return <RocketOutlined />
      default:
        return <TrophyOutlined />
    }
  }

  const getCareerTypeLabel = (careerType: string) => {
    switch (careerType) {
      case 'corporate':
        return '企業転職'
      case 'freelance':
        return 'フリーランス'
      case 'entrepreneurship':
        return '起業'
      default:
        return careerType
    }
  }

  const formatSalary = (min: number, max: number) => {
    return `${(min / 10000).toFixed(0)}万円 - ${(max / 10000).toFixed(0)}万円`
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <Spin size="large" />
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-8">
        <Title level={2}>ダッシュボード</Title>
        <Text className="text-gray-600">こんにちは、{user?.full_name}さん</Text>
      </div>

      {/* Statistics Cards */}
      <Row gutter={[16, 16]} className="mb-8">
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="アップロード済み"
              value={stats.totalDocuments}
              prefix={<FileTextOutlined />}
              suffix="件"
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="分析完了"
              value={stats.completedAnalyses}
              prefix={<CheckCircleOutlined />}
              suffix="件"
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="分析中"
              value={stats.pendingAnalyses}
              prefix={<ClockCircleOutlined />}
              suffix="件"
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
        <Col xs={12} sm={6}>
          <Card>
            <Statistic
              title="平均マッチ度"
              value={stats.averageMatchScore}
              suffix="%"
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Recent Analyses */}
      <Card title="最近の分析結果" className="mb-8">
        {analyses.length === 0 ? (
          <Empty
            description="まだ書類がアップロードされていません"
            className="py-8"
          >
            <Link to="/upload">
              <Button type="primary" icon={<UploadOutlined />}>
                最初の書類をアップロード
              </Button>
            </Link>
          </Empty>
        ) : (
          <List
            dataSource={analyses.slice(0, 5)}
            renderItem={(analysis) => (
              <List.Item>
                <List.Item.Meta
                  avatar={<FileTextOutlined style={{ fontSize: '24px' }} />}
                  title={
                    <div className="flex items-center justify-between">
                      <span>{analysis.document.filename}</span>
                      {analysis.status === 'COMPLETED' ? (
                        <Tag color="success">分析完了</Tag>
                      ) : analysis.status === 'PROCESSING' ? (
                        <Tag color="processing">分析中</Tag>
                      ) : (
                        <Tag color="default">待機中</Tag>
                      )}
                    </div>
                  }
                  description={
                    <div>
                      {analysis.status === 'COMPLETED' && analysis.career_recommendations && (
                        <div className="mt-2">
                          <Row gutter={[8, 8]}>
                            {analysis.career_recommendations.map((rec, index) => (
                              <Col key={index} xs={24} sm={8}>
                                <Card size="small" className="hover:shadow-md transition-shadow">
                                  <div className="flex items-center mb-2">
                                    {getCareerIcon(rec.career_type)}
                                    <Text strong className="ml-2">{getCareerTypeLabel(rec.career_type)}</Text>
                                  </div>
                                  <Paragraph ellipsis className="mb-1 text-sm">{rec.title}</Paragraph>
                                  <Progress 
                                    percent={rec.skill_match_percentage} 
                                    size="small" 
                                    strokeColor={{
                                      '0%': '#108ee9',
                                      '100%': '#87d068',
                                    }}
                                  />
                                  <Text type="secondary" className="text-xs">
                                    {formatSalary(rec.salary_range_min, rec.salary_range_max)}
                                  </Text>
                                </Card>
                              </Col>
                            ))}
                          </Row>
                          <div className="mt-2">
                            <Link to={`/analysis/${analysis.id}`}>
                              <Button type="link" size="small">詳細を見る →</Button>
                            </Link>
                          </div>
                        </div>
                      )}
                      <Text type="secondary" className="text-xs">
                        {new Date(analysis.created_at).toLocaleString('ja-JP')}
                      </Text>
                    </div>
                  }
                />
              </List.Item>
            )}
          />
        )}
      </Card>

      {/* Quick Actions */}
      <Card title="クイックアクション">
        <Row gutter={[16, 16]}>
          <Col xs={24} sm={8}>
            <Link to="/upload">
              <Button type="primary" size="large" icon={<UploadOutlined />} block>
                新しい書類をアップロード
              </Button>
            </Link>
          </Col>
          <Col xs={24} sm={8}>
            <Link to="/profile">
              <Button size="large" icon={<TeamOutlined />} block>
                プロフィールを編集
              </Button>
            </Link>
          </Col>
          <Col xs={24} sm={8}>
            <Button size="large" icon={<FileTextOutlined />} block disabled>
              レポートをダウンロード（準備中）
            </Button>
          </Col>
        </Row>
      </Card>
    </div>
  )
}

export default DashboardPage