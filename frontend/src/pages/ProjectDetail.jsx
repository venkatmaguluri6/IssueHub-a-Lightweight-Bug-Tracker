import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import './ProjectDetail.css'

function ProjectDetail() {
  const { projectId } = useParams()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [project, setProject] = useState(null)
  const [issues, setIssues] = useState([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [filters, setFilters] = useState({
    q: '',
    status: '',
    priority: '',
    assignee: '',
    sort: '-created_at',
  })
  const [newIssue, setNewIssue] = useState({
    title: '',
    description: '',
    priority: 'medium',
    assignee_id: '',
  })
  const [members, setMembers] = useState([])
  const [isMaintainer, setIsMaintainer] = useState(false)

  useEffect(() => {
    fetchProject()
    fetchIssues()
    fetchMembers()
  }, [projectId])

  useEffect(() => {
    fetchIssues()
  }, [filters])

  const fetchProject = async () => {
    try {
      const response = await api.get(`/projects/${projectId}/`)
      setProject(response.data)
    } catch (err) {
      console.error('Failed to fetch project:', err)
      if (err.response?.status === 404) {
        navigate('/projects')
      } else if (err.response?.status === 403) {
        alert('You do not have access to this project')
        navigate('/projects')
      }
    }
  }

  const fetchIssues = async () => {
    try {
      const params = new URLSearchParams()
      Object.entries(filters).forEach(([key, value]) => {
        if (value) params.append(key, value)
      })
      const response = await api.get(`/projects/${projectId}/issues/?${params}`)
      // Ensure we always set an array
      const issuesData = response.data?.results || response.data
      setIssues(Array.isArray(issuesData) ? issuesData : [])
    } catch (err) {
      console.error('Failed to fetch issues:', err)
      setIssues([]) // Set empty array on error to prevent blank page
    } finally {
      setLoading(false)
    }
  }

  const fetchMembers = async () => {
    try {
      const response = await api.get(`/projects/${projectId}/members/`)
      const membersList = response.data?.results || response.data
      const membersArray = Array.isArray(membersList) ? membersList : []
      setMembers(membersArray)
      const userMembership = membersArray.find(m => m.user?.id === user?.id)
      setIsMaintainer(userMembership?.role === 'maintainer')
    } catch (err) {
      console.error('Failed to fetch members:', err)
      setMembers([]) // Set empty array on error
    }
  }

  const handleCreateIssue = async (e) => {
    e.preventDefault()
    try {
      const issueData = {
        ...newIssue,
        project: projectId,
        assignee_id: newIssue.assignee_id || null,
      }
      await api.post(`/projects/${projectId}/issues/`, issueData)
      setShowModal(false)
      setNewIssue({ title: '', description: '', priority: 'medium', assignee_id: '' })
      fetchIssues()
    } catch (err) {
      console.error('Failed to create issue:', err)
      alert(err.response?.data?.error?.message || 'Failed to create issue. Please try again.')
    }
  }

  const handleAddMember = async (e) => {
    e.preventDefault()
    const email = e.target.email.value
    const role = e.target.role.value
    try {
      await api.post(`/projects/${projectId}/members/`, {
        user_email: email,
        role: role,
      })
      e.target.reset()
      fetchMembers()
    } catch (err) {
      alert(err.response?.data?.error?.message || 'Failed to add member')
    }
  }

  if (loading && !project) {
    return <div className="loading">Loading project...</div>
  }

  if (!project && !loading) {
    return (
      <div className="loading">
        <p>Project not found or you don't have access.</p>
        <button onClick={() => navigate('/projects')} className="btn btn-primary">
          Back to Projects
        </button>
      </div>
    )
  }

  return (
    <div className="project-detail-page">
      <header className="header">
        <div className="container">
          <Link to="/projects">
            <h1>IssueHub</h1>
          </Link>
          <div className="header-actions">
            <span>Welcome, {user?.name}</span>
            <button onClick={logout} className="btn btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="container">
        {project && (
          <>
            <div className="project-header">
              <div>
                <h2>{project.name}</h2>
                <p className="project-key">{project.key}</p>
              </div>
              <button onClick={() => setShowModal(true)} className="btn btn-primary">
                + New Issue
              </button>
            </div>

            <div className="filters-section">
              <div className="filter-group">
                <input
                  type="text"
                  placeholder="Search issues..."
                  value={filters.q}
                  onChange={(e) => setFilters({ ...filters, q: e.target.value })}
                  className="search-input"
                />
              </div>
              <div className="filter-group">
                <select
                  value={filters.status}
                  onChange={(e) => setFilters({ ...filters, status: e.target.value })}
                >
                  <option value="">All Status</option>
                  <option value="open">Open</option>
                  <option value="in_progress">In Progress</option>
                  <option value="resolved">Resolved</option>
                  <option value="closed">Closed</option>
                </select>
              </div>
              <div className="filter-group">
                <select
                  value={filters.priority}
                  onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
                >
                  <option value="">All Priority</option>
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div className="filter-group">
                <select
                  value={filters.sort}
                  onChange={(e) => setFilters({ ...filters, sort: e.target.value })}
                >
                  <option value="-created_at">Newest First</option>
                  <option value="created_at">Oldest First</option>
                  <option value="-priority">Priority High</option>
                  <option value="priority">Priority Low</option>
                  <option value="status">Status A-Z</option>
                  <option value="-status">Status Z-A</option>
                </select>
              </div>
            </div>

            <div className="issues-list">
              {!Array.isArray(issues) || issues.length === 0 ? (
                <div className="empty-state">No issues found</div>
              ) : (
                issues.map((issue) => (
                  <div
                    key={issue.id}
                    className="issue-card"
                    onClick={() => navigate(`/issues/${issue.id}`)}
                  >
                    <div className="issue-header">
                      <h3>{issue.title}</h3>
                      <div className="issue-badges">
                        <span className={`badge ${issue.status}`}>{issue.status}</span>
                        <span className={`badge ${issue.priority}`}>{issue.priority}</span>
                      </div>
                    </div>
                    <p className="issue-description">{issue.description}</p>
                    <div className="issue-meta">
                      <span>#{issue.id}</span>
                      {issue.assignee && <span>Assigned to: {issue.assignee.name}</span>}
                      <span>Reporter: {issue.reporter.name}</span>
                    </div>
                  </div>
                ))
              )}
            </div>

            {isMaintainer && (
              <div className="members-section">
                <h3>Project Members</h3>
                <form onSubmit={handleAddMember} className="add-member-form">
                  <input
                    type="email"
                    name="email"
                    placeholder="User email"
                    required
                  />
                  <select name="role" required>
                    <option value="member">Member</option>
                    <option value="maintainer">Maintainer</option>
                  </select>
                  <button type="submit" className="btn btn-primary">Add Member</button>
                </form>
                <div className="members-list">
                  {members.map((member) => (
                    <div key={member.id} className="member-item">
                      <span>{member.user.name} ({member.user.email})</span>
                      <span className="role-badge">{member.role}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {showModal && (
        <div className="modal-overlay" onClick={() => setShowModal(false)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3>Create New Issue</h3>
            <form onSubmit={handleCreateIssue}>
              <div className="form-group">
                <label>Title</label>
                <input
                  type="text"
                  value={newIssue.title}
                  onChange={(e) => setNewIssue({ ...newIssue, title: e.target.value })}
                  required
                />
              </div>
              <div className="form-group">
                <label>Description</label>
                <textarea
                  value={newIssue.description}
                  onChange={(e) => setNewIssue({ ...newIssue, description: e.target.value })}
                  required
                  rows="5"
                />
              </div>
              <div className="form-group">
                <label>Priority</label>
                <select
                  value={newIssue.priority}
                  onChange={(e) => setNewIssue({ ...newIssue, priority: e.target.value })}
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                  <option value="critical">Critical</option>
                </select>
              </div>
              <div className="form-group">
                <label>Assignee (Optional)</label>
                <select
                  value={newIssue.assignee_id}
                  onChange={(e) => setNewIssue({ ...newIssue, assignee_id: e.target.value })}
                >
                  <option value="">Unassigned</option>
                  {members.map((member) => (
                    <option key={member.user.id} value={member.user.id}>
                      {member.user.name}
                    </option>
                  ))}
                </select>
              </div>
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

export default ProjectDetail

