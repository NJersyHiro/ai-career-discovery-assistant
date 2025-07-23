import React from 'react'
import ReactDOM from 'react-dom/client'
import { ConfigProvider } from 'antd'
import jaJP from 'antd/locale/ja_JP'
import dayjs from 'dayjs'
import 'dayjs/locale/ja'
import App from './App'
import './index.css'

// Set dayjs locale to Japanese
dayjs.locale('ja')

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <ConfigProvider locale={jaJP}>
      <App />
    </ConfigProvider>
  </React.StrictMode>,
)