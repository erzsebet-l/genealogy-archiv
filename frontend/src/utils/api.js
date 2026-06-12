// utils/api.js
const API_BASE = import.meta?.env?.VITE_API_BASE ?? 'http://localhost:8000'

export function authHeaders(contentType = false) {
  const token = localStorage.getItem('access_token')
  const h = {}
  if (token) h['Authorization'] = `Bearer ${token}`
  if (contentType) h['Content-Type'] = 'application/json'
  return h
}

let refreshPromise = null

async function refreshAccessToken() {
  if (refreshPromise) {
    console.log('[refresh] using existing promise')
    return refreshPromise
  }

  console.log('[refresh] creating new promise')

  refreshPromise = (async () => {
    const refresh = localStorage.getItem('refresh_token')
    if (!refresh) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
      throw new Error('Нет refresh токена')
    }

    const response = await fetch(`${API_BASE}/api/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh })
    })

    if (!response.ok) {
      console.log('[refresh] refresh request failed:', response.status)
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      window.location.href = '/login'
      throw new Error('Сессия истекла')
    }

    const data = await response.json()
    console.log('[refresh] got new access (FULL):', data.access)
    localStorage.setItem('access_token', data.access)
    if (data.refresh) localStorage.setItem('refresh_token', data.refresh)
    return data.access
  })()

  try {
    return await refreshPromise
  } finally {
    refreshPromise = null
  }
}

export async function api(url, options = {}) {
  let token = localStorage.getItem('access_token')

  if (!token) {
    window.location.href = '/login'
    throw new Error('Необходима авторизация')
  }

  const makeRequest = async (tokenValue) => {
    return fetch(`${API_BASE}${url}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
        'Authorization': `Bearer ${tokenValue}`,
      }
    })
  }

  let response = await makeRequest(token)

  if (response.status === 401) {
    console.log('[api] 401 for', url, '- refreshing...')
    try {
      const newToken = await refreshAccessToken()
      console.log('[api] retrying', url, 'with token (FULL):', newToken)
      response = await makeRequest(newToken)
      console.log('[api] retry result for', url, '->', response.status)
    } catch (refreshError) {
      window.location.href = '/login'
      throw refreshError
    }
  }

  if (!response.ok) {
    const text = await response.text()
    throw new Error(`HTTP ${response.status}: ${text.substring(0, 200)}`)
  }

  if (response.status === 204) return null
  return response.json()
}

export { API_BASE }