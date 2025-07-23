import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Layout } from 'antd'
import MainLayout from './components/layout/MainLayout'
import HomePage from './features/home/HomePage'
import UploadPage from './features/document-upload/UploadPage'
import AnalysisPage from './features/career-analysis/AnalysisPage'
import DashboardPage from './features/dashboard/DashboardPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <MainLayout>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/analysis/:id" element={<AnalysisPage />} />
              <Route path="/dashboard" element={<DashboardPage />} />
            </Routes>
          </MainLayout>
        </Layout>
      </Router>
    </QueryClientProvider>
  )
}

export default App