import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import './Projects.css'

function Projects() {
  const [projects, setProjects] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [newProject, setNewProject] = useState({ name: '', key: '', description: '' })
  const [error, setError] = useState('')
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    fetchProjects()
  }, [])

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects/')
      setProjects(response.data.results || response.data || [])
    } catch (err) {
      console.error('Failed to fetch projects:', err)
      setProjects([]) // Set empty array on error
      if (err.response?.status === 401) {
        // Token expired, redirect to login
        logout()
      }
    } finally {
      setLoading(false)
    }
  }

  const handleCreateProject = async (e) => {
    e.preventDefault()
    setError('')

    if (!newProject.name || !newProject.key) {
      setError('Name and key are required')
      return
    }

    try {
      const response = await api.post('/projects/', newProject)
      setShowModal(false)
      setNewProject({ name: '', key: '', description: '' })
      await fetchProjects()
      // Navigate to the newly created project
      if (response.data?.id) {
        navigate(`/projects/${response.data.id}`)
      }
    } catch (err) {
      console.error('Failed to create project:', err)
      setError(err.response?.data?.error?.message || err.response?.data?.error?.details || 'Failed to create project')
    }
  }

  if (loading) {
    return <div className="loading">Loading projects...</div>
  }

  return (
    <div className="projects-page">
      <header className="header">
        <div className="container">
          <h1>IssueHub</h1>
          <div className="header-actions">
            <span>Welcome, {user?.name}</span>
            <button onClick={logout} className="btn btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="container">
        <div className="page-header">
          <h2>Projects</h2>
          <button onClick={() => setShowModal(true)} className="btn btn-primary">
            + New Project
          </button>
        </div>

        {projects.length === 0 ? (
          <div className="empty-state">
            <p>No projects yet. Create your first project to get started!</p>
          </div>
        ) : (
          <div className="projects-grid">
            {projects.map((project) => (
              <div
                key={project.id}
                className="project-card"
                onClick={() => navigate(`/projects/${project.id}`)}
              >
                <h3>{project.name}</h3>
                <p className="project-key">{project.key}</p>
                {project.description && <p className="project-description">{project.description}</p>}
                <div className="project-stats">
                  <span>{project.member_count || 0} members</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Create New Project</h3>
            <form onSubmit={handleCreateProject}>
              <div className="form-group">
                <label>Project Name</label>
                <input
                  type="text"
                  value={newProject.name}
                  onChange={(e) => setNewProject({ ...newProject, name: e.target.value })}
                  required
                  placeholder="e.g., Web Application"
                />
              </div>
              <div className="form-group">
                <label>Project Key</label>
                <input
                  type="text"
                  value={newProject.key}
                  onChange={(e) => setNewProject({ ...newProject, key: e.target.value.toUpperCase() })}
                  required
                  placeholder="e.g., WEBAPP"
                  maxLength={10}
                />
              </div>
              <div className="form-group">
                <label>Description (Optional)</label>
                <textarea
                  value={newProject.description}
                  onChange={(e) => setNewProject({ ...newProject, description: e.target.value })}
                  placeholder="Project description"
                  rows="3"
                />
              </div>
              {error && <div className="error">{error}</div>}
              <div className="modal-actions">
                <button type="button" onClick={() => setShowModal(false)} className="btn btn-secondary">
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Projects

