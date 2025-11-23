import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Projects from './pages/Projects'
import ProjectDetail from './pages/ProjectDetail'
import IssueDetail from './pages/IssueDetail'
import './App.css'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="loading">Loading...</div>
  }
  
  return user ? children : <Navigate to="/login" />
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth()
  
  if (loading) {
    return <div className="loading">Loading...</div>
  }
  
  return !user ? children : <Navigate to="/projects" />
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="app">
          <Routes>
            <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
            <Route path="/signup" element={<PublicRoute><Signup /></PublicRoute>} />
            <Route path="/projects" element={<PrivateRoute><Projects /></PrivateRoute>} />
            <Route path="/projects/:projectId" element={<PrivateRoute><ProjectDetail /></PrivateRoute>} />
            <Route path="/issues/:issueId" element={<PrivateRoute><IssueDetail /></PrivateRoute>} />
            <Route path="/" element={<Navigate to="/projects" />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App

