import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { removeToken } from '../utils/auth';
import todoApi from '../utils/todoApi';
import '../index.css';

const Dashboard = () => {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState({ title: '', description: '' });
  const [editTodo, setEditTodo] = useState(null);
  const [activeTab, setActiveTab] = useState('todos');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const navigate = useNavigate();

  const fetchTodos = async () => {
    try {
      const res = await todoApi.get('/all');
      setTodos(res.data.todos || []);
    } catch {
      alert('Session expired or unauthorized');
      navigate('/login');
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const handleLogout = () => {
    removeToken();
    navigate('/login');
  };

  const handleCreateOrUpdate = async (e) => {
    e.preventDefault();
    const todo = editTodo || newTodo;
    if (!todo.title) return alert('Title is required');

    try {
      if (editTodo) {
        await todoApi.put(`/update/${todo.id}`, todo);
        setEditTodo(null);
      } else {
        await todoApi.post('/create', todo);
        setNewTodo({ title: '', description: '' });
      }
      fetchTodos();
      setActiveTab('todos');
    } catch {
      alert('Failed to save todo');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this todo?')) return;
    try {
      await todoApi.delete(`/delete/${id}`);
      fetchTodos();
    } catch {
      alert('Delete failed');
    }
  };

  return (
    <div className="h-100 d-flex flex-column">
      {/* Navbar */}
      <div className="navbar-custom">
        <span className="fw-bold fs-5"> Todo Dashboard</span>
        <button onClick={handleLogout} className="logout-btn">
          Logout
        </button>
      </div>

      {/* Sidebar Toggle Button */}
      <div className="sidebar-toggle-container">
          <button
            className="btn btn-outline-secondary"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
          >
            <span className="d-inline d-md-none">
              {sidebarCollapsed ? '➡️' : '⬅️'}
            </span>
          </button>
        </div>
      {/* Layout */}
      <div className="dashboard-wrapper d-flex">
        {/* Sidebar */}
        <div className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
          <div
            className={`menu-item ${activeTab === 'todos' ? 'active' : ''}`}
            onClick={() => setActiveTab('todos')}
            title="View Todos"
          >
            📄 View Todos
          </div>
          <div
            className={`menu-item ${activeTab === 'add' ? 'active' : ''}`}
            onClick={() => {
              setEditTodo(null);
              setActiveTab('add');
            }}
            title="Add Todo"
          >
            ➕ Add Todo
          </div>
        </div>

        {/* Content */}
        <div className="content-area">
          {activeTab === 'add' && (
            <div className="card p-4 todo-form-card">
              <h4 className="mb-3">{editTodo ? '✏️ Edit Todo' : '📝 Add New Todo'}</h4>
              <form onSubmit={handleCreateOrUpdate} className="todo-form">
                <input
                  type="text"
                  className="form-control mb-2"
                  placeholder="Enter title"
                  value={editTodo ? editTodo.title : newTodo.title}
                  onChange={(e) =>
                    editTodo
                      ? setEditTodo({ ...editTodo, title: e.target.value })
                      : setNewTodo({ ...newTodo, title: e.target.value })
                  }
                  required
                />
                <input
                  type="text"
                  className="form-control mb-2"
                  placeholder="Enter description"
                  value={editTodo ? editTodo.description : newTodo.description}
                  onChange={(e) =>
                    editTodo
                      ? setEditTodo({ ...editTodo, description: e.target.value })
                      : setNewTodo({ ...newTodo, description: e.target.value })
                  }
                />
                <button className="btn btn-success" type="submit">
                  {editTodo ? 'Update' : 'Add'}
                </button>
              </form>
            </div>
          )}

          {activeTab === 'todos' && (
            <div className="card p-4">
              <h4 className="mb-4">🗂️ Your Todo List</h4>
              {todos.length === 0 ? (
                <p className="no-todo">No todos yet.</p>
              ) : (
                <div className="table-responsive">
                  <table className="table table-hover align-middle">
                    <thead className="table-light">
                      <tr>
                        <th>Title</th>
                        <th>Description</th>
                        <th style={{ width: '160px' }}>Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {todos.map((todo) => (
                        <tr key={todo.id}>
                          <td><strong>{todo.title}</strong></td>
                          <td>{todo.description}</td>
                          <td>
                            <button
                              className="btn btn-sm btn-outline-primary me-2"
                              onClick={() => {
                                setEditTodo(todo);
                                setActiveTab('add');
                              }}
                            >
                              Edit
                            </button>
                            <button
                              className="btn btn-sm btn-outline-danger"
                              onClick={() => handleDelete(todo.id)}
                            >
                              Delete
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
