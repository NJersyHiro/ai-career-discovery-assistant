import React, { useState } from 'react'
import { Upload, Button, Card, Typography, Space, Alert, Spin } from 'antd'
import { UploadOutlined } from '@ant-design/icons'
import { UploadFile } from 'antd/es/upload'
import axios from 'axios'

const { Title, Paragraph, Text } = Typography

const TestPdfExtraction: React.FC = () => {
  const [fileList, setFileList] = useState<UploadFile[]>([])
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const handleUpload = async () => {
    if (fileList.length === 0) return

    const formData = new FormData()
    formData.append('file', fileList[0] as any)

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post('/api/v1/test/test-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })

      setResult(response.data)
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || '抽出エラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  const props = {
    onRemove: () => {
      setFileList([])
      setResult(null)
      setError(null)
    },
    beforeUpload: (file: UploadFile) => {
      setFileList([file])
      return false
    },
    fileList,
  }

  return (
    <div style={{ padding: '24px', maxWidth: '800px', margin: '0 auto' }}>
      <Title level={2}>PDF抽出テスト</Title>
      <Paragraph>
        PDFファイルをアップロードして、テキスト抽出が正常に動作するかテストできます。
      </Paragraph>

      <Card style={{ marginBottom: 24 }}>
        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <Upload {...props} accept=".pdf">
            <Button icon={<UploadOutlined />}>PDFファイルを選択</Button>
          </Upload>

          <Button
            type="primary"
            onClick={handleUpload}
            disabled={fileList.length === 0}
            loading={loading}
          >
            抽出テスト実行
          </Button>
        </Space>
      </Card>

      {loading && (
        <Card>
          <Spin size="large" />
          <Paragraph style={{ marginTop: 16, textAlign: 'center' }}>
            PDFを処理中...
          </Paragraph>
        </Card>
      )}

      {error && (
        <Alert message="エラー" description={error} type="error" showIcon />
      )}

      {result && (
        <Card title="抽出結果">
          <Space direction="vertical" style={{ width: '100%' }}>
            <div>
              <Text strong>ファイル名:</Text> {result.filename}
            </div>
            <div>
              <Text strong>ファイルサイズ:</Text> {result.file_size} bytes
            </div>
            <div>
              <Text strong>抽出成功:</Text> {result.success ? 'はい' : 'いいえ'}
            </div>
            {result.success && (
              <>
                <div>
                  <Text strong>抽出文字数:</Text> {result.extracted_text_length}
                </div>
                {result.first_500_chars && (
                  <div>
                    <Text strong>最初の500文字:</Text>
                    <Paragraph
                      style={{
                        marginTop: 8,
                        padding: 12,
                        background: '#f5f5f5',
                        borderRadius: 4,
                        whiteSpace: 'pre-wrap',
                      }}
                    >
                      {result.first_500_chars}
                    </Paragraph>
                  </div>
                )}
              </>
            )}
            {!result.success && result.error && (
              <Alert message="抽出エラー" description={result.error} type="error" />
            )}
          </Space>
        </Card>
      )}
    </div>
  )
}

export default TestPdfExtraction