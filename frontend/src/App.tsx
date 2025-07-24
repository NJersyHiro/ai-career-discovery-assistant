import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from 'react-query'
import { Layout } from 'antd'
import { AuthProvider } from './contexts/AuthContext'
import { ProtectedRoute } from './components/auth/ProtectedRoute'
import MainLayout from './components/layout/MainLayout'
import HomePage from './features/home/HomePage'
import LoginPage from './features/auth/LoginPage'
import RegisterPage from './features/auth/RegisterPage'
import UploadPage from './features/document-upload/UploadPage'
import AnalysisPage from './features/career-analysis/AnalysisPage'
import DashboardPage from './features/dashboard/DashboardPage'
import TestPdfExtraction from './features/test/TestPdfExtraction'

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
        <AuthProvider>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/*" element={
              <MainLayout>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route path="/upload" element={
                    <ProtectedRoute>
                      <UploadPage />
                    </ProtectedRoute>
                  } />
                  <Route path="/analysis/:id" element={
                    <ProtectedRoute>
                      <AnalysisPage />
                    </ProtectedRoute>
                  } />
                  <Route path="/dashboard" element={
                    <ProtectedRoute>
                      <DashboardPage />
                    </ProtectedRoute>
                  } />
                  <Route path="/test-pdf" element={<TestPdfExtraction />} />
                </Routes>
              </MainLayout>
            } />
          </Routes>
        </AuthProvider>
      </Router>
    </QueryClientProvider>
  )
}

export default App