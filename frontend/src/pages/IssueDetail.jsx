import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import api from '../utils/api'
import './IssueDetail.css'

function IssueDetail() {
  const { issueId } = useParams()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const [issue, setIssue] = useState(null)
  const [comments, setComments] = useState([])
  const [loading, setLoading] = useState(true)
  const [newComment, setNewComment] = useState('')
  const [isMaintainer, setIsMaintainer] = useState(false)
  const [members, setMembers] = useState([])
  const [editMode, setEditMode] = useState(false)
  const [editData, setEditData] = useState({})

  useEffect(() => {
    fetchIssue()
    fetchComments()
  }, [issueId])

  const fetchIssue = async () => {
    try {
      const response = await api.get(`/issues/${issueId}/`)
      setIssue(response.data)
      setEditData({
        title: response.data.title,
        description: response.data.description,
        status: response.data.status,
        priority: response.data.priority,
        assignee_id: response.data.assignee?.id || '',
      })
      fetchProjectMembers(response.data.project)
    } catch (err) {
      console.error('Failed to fetch issue:', err)
    } finally {
      setLoading(false)
    }
  }

  const fetchProjectMembers = async (projectId) => {
    try {
      const response = await api.get(`/projects/${projectId}/members/`)
      const membersList = response.data.results || response.data
      setMembers(membersList)
      const userMembership = membersList.find(m => m.user.id === user?.id)
      setIsMaintainer(userMembership?.role === 'maintainer')
    } catch (err) {
      console.error('Failed to fetch members:', err)
    }
  }

  const fetchComments = async () => {
    try {
      const response = await api.get(`/issues/${issueId}/comments/`)
      setComments(response.data.results || response.data)
    } catch (err) {
      console.error('Failed to fetch comments:', err)
    }
  }

  const handleAddComment = async (e) => {
    e.preventDefault()
    if (!newComment.trim()) return

    try {
      await api.post(`/issues/${issueId}/comments/`, { body: newComment })
      setNewComment('')
      fetchComments()
    } catch (err) {
      console.error('Failed to add comment:', err)
    }
  }

  const handleUpdateIssue = async () => {
    try {
      await api.patch(`/issues/${issueId}/`, editData)
      setEditMode(false)
      fetchIssue()
    } catch (err) {
      console.error('Failed to update issue:', err)
      alert(err.response?.data?.error?.message || 'Failed to update issue')
    }
  }

  const handleDeleteIssue = async () => {
    if (!window.confirm('Are you sure you want to delete this issue?')) return

    try {
      await api.delete(`/issues/${issueId}/`)
      navigate(`/projects/${issue?.project}`)
    } catch (err) {
      console.error('Failed to delete issue:', err)
      alert(err.response?.data?.error?.message || 'Failed to delete issue')
    }
  }

  if (loading) {
    return <div className="loading">Loading...</div>
  }

  if (!issue) {
    return <div className="loading">Issue not found</div>
  }

  const canEdit = issue.reporter.id === user?.id || isMaintainer
  const canChangeStatus = isMaintainer

  return (
    <div className="issue-detail-page">
      <header className="header">
        <div className="container">
          <Link to={`/projects/${issue.project}`}>
            <h1>IssueHub</h1>
          </Link>
          <div className="header-actions">
            <span>Welcome, {user?.name}</span>
            <button onClick={logout} className="btn btn-secondary">Logout</button>
          </div>
        </div>
      </header>

      <div className="container">
        <div className="issue-detail">
          <div className="issue-main">
            <div className="issue-title-section">
              {editMode && canEdit ? (
                <input
                  type="text"
                  value={editData.title || issue.title}
                  onChange={(e) => setEditData({ ...editData, title: e.target.value })}
                  className="form-group"
                  style={{ flex: 1, marginRight: '20px', fontSize: '24px', padding: '10px' }}
                />
              ) : (
                <h2>{issue.title}</h2>
              )}
              <div className="issue-actions">
                {canEdit && (
                  <>
                    {editMode ? (
                      <>
                        <button onClick={handleUpdateIssue} className="btn btn-success">
                          Save
                        </button>
                        <button onClick={() => setEditMode(false)} className="btn btn-secondary">
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button onClick={() => setEditMode(true)} className="btn btn-primary">
                          Edit
                        </button>
                        <button onClick={handleDeleteIssue} className="btn btn-danger">
                          Delete
                        </button>
                      </>
                    )}
                  </>
                )}
              </div>
            </div>

            <div className="issue-meta-section">
              <div className="meta-item">
                <span className="meta-label">Status:</span>
                {editMode && canChangeStatus ? (
                  <select
                    value={editData.status}
                    onChange={(e) => setEditData({ ...editData, status: e.target.value })}
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </select>
                ) : (
                  <span className={`badge ${issue.status}`}>{issue.status}</span>
                )}
              </div>
              <div className="meta-item">
                <span className="meta-label">Priority:</span>
                {editMode && canEdit ? (
                  <select
                    value={editData.priority}
                    onChange={(e) => setEditData({ ...editData, priority: e.target.value })}
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                    <option value="critical">Critical</option>
                  </select>
                ) : (
                  <span className={`badge ${issue.priority}`}>{issue.priority}</span>
                )}
              </div>
              <div className="meta-item">
                <span className="meta-label">Assignee:</span>
                {editMode && canChangeStatus ? (
                  <select
                    value={editData.assignee_id}
                    onChange={(e) => setEditData({ ...editData, assignee_id: e.target.value })}
                  >
                    <option value="">Unassigned</option>
                    {members.map((member) => (
                      <option key={member.user.id} value={member.user.id}>
                        {member.user.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  <span>{issue.assignee ? issue.assignee.name : 'Unassigned'}</span>
                )}
              </div>
              <div className="meta-item">
                <span className="meta-label">Reporter:</span>
                <span>{issue.reporter.name}</span>
              </div>
              <div className="meta-item">
                <span className="meta-label">Created:</span>
                <span>{new Date(issue.created_at).toLocaleString()}</span>
              </div>
            </div>

            <div className="issue-description">
              <h3>Description</h3>
              {editMode && canEdit ? (
                <textarea
                  value={editData.description || issue.description}
                  onChange={(e) => setEditData({ ...editData, description: e.target.value })}
                  rows="10"
                  className="form-group textarea"
                />
              ) : (
                <p>{issue.description}</p>
              )}
            </div>

            <div className="comments-section">
              <h3>Comments ({comments.length})</h3>
              <div className="comments-list">
                {comments.map((comment) => (
                  <div key={comment.id} className="comment-item">
                    <div className="comment-header">
                      <strong>{comment.author.name}</strong>
                      <span className="comment-date">
                        {new Date(comment.created_at).toLocaleString()}
                      </span>
                    </div>
                    <p className="comment-body">{comment.body}</p>
                  </div>
                ))}
              </div>
              <form onSubmit={handleAddComment} className="comment-form">
                <textarea
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                  placeholder="Add a comment..."
                  rows="3"
                  required
                />
                <button type="submit" className="btn btn-primary">Add Comment</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default IssueDetail

