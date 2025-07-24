import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import { message } from 'antd'

interface User {
  id: number
  email: string
  full_name?: string
}

interface AuthContextType {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, fullName?: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Configure axios defaults
// In development, we use the Vite dev server proxy, so no base URL needed
// In production, this would be set to the actual API URL
axios.defaults.baseURL = ''

// Add request interceptor to include token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [token, setToken] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const navigate = useNavigate()

  // Load user from token on mount
  useEffect(() => {
    const loadUser = async () => {
      const savedToken = localStorage.getItem('token')
      if (savedToken) {
        setToken(savedToken)
        try {
          const response = await axios.get('/api/v1/users/me')
          setUser(response.data)
        } catch (error) {
          console.error('Failed to load user:', error)
          localStorage.removeItem('token')
          setToken(null)
        }
      }
      setIsLoading(false)
    }
    loadUser()
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    try {
      const formData = new FormData()
      formData.append('username', email) // OAuth2 expects username field
      formData.append('password', password)

      const response = await axios.post('/api/v1/auth/login', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { access_token } = response.data
      localStorage.setItem('token', access_token)
      setToken(access_token)

      // Get user info
      const userResponse = await axios.get('/api/v1/users/me')
      setUser(userResponse.data)

      message.success('ログインに成功しました')
      navigate('/dashboard')
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'ログインに失敗しました')
      throw error
    }
  }, [navigate])

  const register = useCallback(async (email: string, password: string, fullName?: string) => {
    try {
      const response = await axios.post('/api/v1/auth/register', {
        email,
        password,
        full_name: fullName
      })

      message.success('アカウントを作成しました。ログインしてください。')
      navigate('/login')
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'アカウント作成に失敗しました')
      throw error
    }
  }, [navigate])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    message.info('ログアウトしました')
    navigate('/')
  }, [navigate])

  const value = {
    user,
    token,
    isLoading,
    login,
    register,
    logout,
    isAuthenticated: !!token && !!user
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}