import React from 'react'
import { Upload, Button, Card, Typography, message } from 'antd'
import { InboxOutlined } from '@ant-design/icons'
import type { UploadProps } from 'antd'
import { useAuth } from '@/contexts/AuthContext'
import { useNavigate } from 'react-router-dom'

const { Title, Paragraph } = Typography
const { Dragger } = Upload

const UploadPage: React.FC = () => {
  const { token } = useAuth()
  const navigate = useNavigate()
  
  const uploadProps: UploadProps = {
    name: 'file',
    multiple: false,
    action: '/api/v1/documents/upload',
    accept: '.pdf,.doc,.docx',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    onChange(info) {
      const { status, response } = info.file
      if (status === 'done') {
        message.success(`${info.file.name} のアップロードが完了しました`)
        // Navigate to analysis page if analysis ID is returned
        if (response && response.analysis_id) {
          navigate(`/analysis/${response.analysis_id}`)
        }
      } else if (status === 'error') {
        message.error(`${info.file.name} のアップロードに失敗しました`)
      }
    },
    onDrop(e) {
      console.log('Dropped files', e.dataTransfer.files)
    },
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <Title level={2}>書類をアップロード</Title>
        <Paragraph className="text-lg text-gray-600">
          履歴書や職務経歴書をアップロードして、AI分析を開始しましょう
        </Paragraph>
      </div>

      <Card>
        <Dragger {...uploadProps} className="p-8">
          <p className="ant-upload-drag-icon">
            <InboxOutlined className="text-6xl text-blue-500" />
          </p>
          <p className="ant-upload-text text-xl">
            クリックまたはドラッグ&ドロップでファイルをアップロード
          </p>
          <p className="ant-upload-hint text-gray-500">
            対応形式: PDF, Word (.doc, .docx)<br />
            最大ファイルサイズ: 10MB
          </p>
        </Dragger>
      </Card>

      <div className="mt-8 bg-blue-50 p-6 rounded-lg">
        <Title level={4}>アップロードのヒント</Title>
        <ul className="list-disc list-inside text-gray-700 space-y-2">
          <li>履歴書（りれきしょ）と職務経歴書（しょくむけいれきしょ）の両方をアップロードすると、より詳細な分析が可能です</li>
          <li>個人情報は安全に保護され、分析以外の目的では使用されません</li>
          <li>ファイルは暗号化されて保存されます</li>
        </ul>
      </div>
    </div>
  )
}

export default UploadPage