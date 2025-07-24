import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, Spin, Typography, Progress, Tag, Space, Button, Row, Col, Statistic, Alert, List } from 'antd'
import { LoadingOutlined, CheckCircleOutlined, CloseCircleOutlined, ClockCircleOutlined } from '@ant-design/icons'
import axios from 'axios'
import { useAuth } from '@/contexts/AuthContext'

const { Title, Text, Paragraph } = Typography

interface CareerPath {
  id: number
  career_type: string
  title: string
  description: string
  skill_match_percentage: number
  required_skills: string[]
  skill_gaps: string[]
  salary_range_min?: number
  salary_range_max?: number
  market_demand?: string
  confidence_score: number
  next_steps: string[]
}

interface Analysis {
  id: number
  status: 'pending' | 'processing' | 'completed' | 'failed'
  created_at: string
  processing_time?: number
  career_paths?: any[]
  skill_gaps?: string[]
  error_message?: string
  gemini_response?: any
}

const AnalysisPage: React.FC = () => {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { token } = useAuth()
  const [analysis, setAnalysis] = useState<Analysis | null>(null)
  const [careerPaths, setCareerPaths] = useState<CareerPath[]>([])
  const [loading, setLoading] = useState(true)
  const [polling, setPolling] = useState(true)

  // Fetch analysis data
  const fetchAnalysis = async () => {
    try {
      const response = await axios.get(`/api/v1/analysis/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setAnalysis(response.data)

      // If completed, fetch career paths
      if (response.data.status === 'completed') {
        const pathsResponse = await axios.get(`/api/v1/analysis/${id}/career-paths`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        setCareerPaths(pathsResponse.data)
        setPolling(false)
      } else if (response.data.status === 'failed') {
        setPolling(false)
      }
    } catch (error) {
      console.error('Error fetching analysis:', error)
      setPolling(false)
    } finally {
      setLoading(false)
    }
  }

  // Poll for updates while processing
  useEffect(() => {
    fetchAnalysis()

    const interval = polling ? setInterval(() => {
      fetchAnalysis()
    }, 3000) : null

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [id, polling])

  // Render status icon
  const renderStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleOutlined style={{ color: '#52c41a', fontSize: 24 }} />
      case 'failed':
        return <CloseCircleOutlined style={{ color: '#ff4d4f', fontSize: 24 }} />
      case 'processing':
        return <LoadingOutlined style={{ fontSize: 24 }} />
      default:
        return <ClockCircleOutlined style={{ fontSize: 24 }} />
    }
  }

  // Render market demand tag
  const renderMarketDemand = (demand?: string) => {
    const colorMap: Record<string, string> = {
      'high': 'green',
      'medium': 'blue',
      'low': 'orange'
    }
    return demand ? <Tag color={colorMap[demand] || 'default'}>{demand.toUpperCase()}</Tag> : null
  }

  if (loading && !analysis) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <Spin size="large" tip="分析結果を読み込み中..." />
          </div>
        </Card>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-8">
        <Alert
          message="エラー"
          description="分析結果が見つかりません"
          type="error"
          showIcon
        />
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="mb-8 text-center">
        <Title level={2}>キャリア分析結果</Title>
        <Space>
          {renderStatusIcon(analysis.status)}
          <Text className="text-lg">
            {analysis.status === 'pending' && '分析待機中...'}
            {analysis.status === 'processing' && '分析中...'}
            {analysis.status === 'completed' && '分析完了'}
            {analysis.status === 'failed' && '分析失敗'}
          </Text>
        </Space>
      </div>

      {analysis.status === 'processing' && (
        <Card className="mb-6">
          <div className="text-center">
            <Spin size="large" />
            <Paragraph className="mt-4">
              AIがあなたの職務経歴書を分析しています。
              <br />
              通常1-2分程度かかります。
            </Paragraph>
          </div>
        </Card>
      )}

      {analysis.status === 'failed' && (
        <Alert
          message="分析エラー"
          description={analysis.error_message || '分析中にエラーが発生しました'}
          type="error"
          showIcon
          className="mb-6"
        />
      )}

      {analysis.status === 'completed' && careerPaths.length > 0 && (
        <>
          {/* Summary Statistics */}
          <Row gutter={16} className="mb-6">
            <Col span={8}>
              <Card>
                <Statistic
                  title="推奨キャリアパス"
                  value={careerPaths.length}
                  suffix="件"
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="平均マッチ度"
                  value={Math.round(
                    careerPaths.reduce((sum, path) => sum + path.skill_match_percentage, 0) / careerPaths.length
                  )}
                  suffix="%"
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card>
                <Statistic
                  title="処理時間"
                  value={analysis.processing_time ? Math.round(analysis.processing_time) : 0}
                  suffix="秒"
                />
              </Card>
            </Col>
          </Row>

          {/* Career Paths */}
          <Title level={3} className="mb-4">推奨キャリアパス</Title>
          {careerPaths.map((path) => (
            <Card key={path.id} className="mb-4">
              <Row gutter={16}>
                <Col span={16}>
                  <Title level={4}>{path.title}</Title>
                  <Paragraph>{path.description}</Paragraph>
                  
                  <Space className="mb-3">
                    <Tag color="blue">{path.career_type}</Tag>
                    {renderMarketDemand(path.market_demand)}
                    <Text>信頼度: {Math.round(path.confidence_score * 100)}%</Text>
                  </Space>

                  {path.salary_range_min && path.salary_range_max && (
                    <div className="mb-3">
                      <Text strong>予想年収: </Text>
                      <Text>
                        {path.salary_range_min.toLocaleString()}万円 〜 {path.salary_range_max.toLocaleString()}万円
                      </Text>
                    </div>
                  )}
                </Col>
                <Col span={8}>
                  <div className="text-center">
                    <Progress
                      type="circle"
                      percent={path.skill_match_percentage}
                      format={percent => `${percent}%`}
                      strokeColor={{
                        '0%': '#108ee9',
                        '100%': '#87d068',
                      }}
                    />
                    <div className="mt-2">
                      <Text strong>スキルマッチ度</Text>
                    </div>
                  </div>
                </Col>
              </Row>

              {/* Required Skills */}
              {path.required_skills.length > 0 && (
                <div className="mt-4">
                  <Text strong>必要なスキル:</Text>
                  <div className="mt-2">
                    {path.required_skills.map((skill, index) => (
                      <Tag key={index} color="green" className="mb-2">
                        {skill}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}

              {/* Skill Gaps */}
              {path.skill_gaps.length > 0 && (
                <div className="mt-4">
                  <Text strong>習得すべきスキル:</Text>
                  <div className="mt-2">
                    {path.skill_gaps.map((skill, index) => (
                      <Tag key={index} color="orange" className="mb-2">
                        {skill}
                      </Tag>
                    ))}
                  </div>
                </div>
              )}

              {/* Next Steps */}
              {path.next_steps.length > 0 && (
                <div className="mt-4">
                  <Text strong>次のステップ:</Text>
                  <List
                    size="small"
                    dataSource={path.next_steps}
                    renderItem={(step) => <List.Item>{step}</List.Item>}
                  />
                </div>
              )}
            </Card>
          ))}

          {/* Overall Skill Gaps */}
          {analysis.skill_gaps && analysis.skill_gaps.length > 0 && (
            <Card className="mt-6">
              <Title level={4}>全体的なスキルギャップ</Title>
              <Paragraph>
                以下のスキルを習得することで、より多くのキャリアオプションが開かれます：
              </Paragraph>
              <div>
                {analysis.skill_gaps.map((skill, index) => (
                  <Tag key={index} color="orange" className="mb-2 mr-2">
                    {skill}
                  </Tag>
                ))}
              </div>
            </Card>
          )}
        </>
      )}

      <div className="mt-8 text-center">
        <Space>
          <Button onClick={() => navigate('/upload')}>
            新しい書類をアップロード
          </Button>
          <Button type="primary" onClick={() => navigate('/dashboard')}>
            ダッシュボードに戻る
          </Button>
        </Space>
      </div>
    </div>
  )
}

export default AnalysisPage