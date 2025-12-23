import React, { useEffect, useState } from "react";
import { useAuth } from "../components/AuthContext";
import { apiClient } from "../lib/api";
import Router from "next/router";

type ICSR = {
  id: number | string;
  title: string;
  narrative: string;
  created_at?: string;
};

export default function Home() {
  const { token, logout, isAuthenticated } = useAuth();
  const [icrs, setIcrs] = useState<ICSR[]>([]);
  const [title, setTitle] = useState("");
  const [narrative, setNarrative] = useState("");
  const [loading, setLoading] = useState(false);

  const client = apiClient(token || undefined);

  useEffect(() => {
    fetchList();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function fetchList() {
    try {
      const res = await client.get("/icrs");
      setIcrs(res.data || []);
    } catch (err) {
      console.error(err);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    if (!isAuthenticated) {
      Router.push("/login");
      return;
    }
    setLoading(true);
    try {
      const res = await client.post("/icrs", { title, narrative });
      setIcrs((s) => [res.data, ...s]);
      setTitle("");
      setNarrative("");
    } catch (err: any) {
      alert("Create failed: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  }

  async function runNER(text: string) {
    try {
      const res = await client.post("/ml/ner", { text });
      const ents = res.data?.entities || [];
      alert("Entities found:\n" + JSON.stringify(ents, null, 2));
    } catch (err) {
      alert("NER failed");
      console.error(err);
    }
  }

  return (
    <main className="container">
      <div className="header">
        <h1>DMS Showcase</h1>
        <div>
          <button className="button ghost" onClick={()=>Router.push("/login")}>Login</button>
          <button className="button" style={{ marginLeft: 8 }} onClick={logout}>Logout</button>
        </div>
      </div>

      <div className="card" style={{ marginBottom: 20 }}>
        <h3>Create ICSR</h3>
        <form onSubmit={handleCreate}>
          <div>
            <label>Title
              <input className="input" value={title} onChange={(e)=>setTitle(e.target.value)} required />
            </label>
          </div>
          <div style={{ marginTop: 12 }}>
            <label>Narrative
              <textarea className="input" value={narrative} onChange={(e)=>setNarrative(e.target.value)} rows={6} required />
            </label>
          </div>
          <div style={{ marginTop: 12 }}>
            <button className="button" type="submit" disabled={loading}>{loading ? "Creating..." : "Create (requires auth)"}</button>
            <button type="button" className="button ghost" style={{ marginLeft: 8 }} onClick={()=>runNER(narrative || title)}>Run NER</button>
          </div>
        </form>
      </div>

      <div className="card">
        <h3>ICSRs</h3>
        {icrs.length === 0 && <p>No records yet.</p>}
        <div>
          {icrs.map((i) => (
            <div key={String(i.id)} className="list-item">
              <strong>{i.title}</strong>
              <div>{i.narrative}</div>
              {i.created_at && <div className="small">{i.created_at}</div>}
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}