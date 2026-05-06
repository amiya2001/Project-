const BASE = 'http://localhost:8000';

export const api = {
  ingest: async (filename: string, content: string, tags: string[] = []) => {
    const res = await fetch(`${BASE}/api/ingest/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({filename, content, tags})
    });
    return res.json();
  },

  getDocuments: async () => {
    const res = await fetch(`${BASE}/api/ingest/documents`);
    return res.json();
  },

  chat: async (session_id: string, message: string, top_k = 3) => {
    const res = await fetch(`${BASE}/api/chat/`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({session_id, message, top_k})
    });
    return res.json();
  },

  search: async (query: string, top_k = 3) => {
    const res = await fetch(`${BASE}/api/query/search`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query, top_k})
    });
    return res.json();
  },

  clearSession: async (session_id: string) => {
    await fetch(`${BASE}/api/chat/${session_id}`, {method: 'DELETE'});
  }
};