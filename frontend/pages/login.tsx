import React, { useState } from "react";
import { useRouter } from "next/router";
import { useAuth } from "../components/AuthContext";

export default function LoginPage() {
  const [email, setEmail] = useState("admin@demo");
  const [password, setPassword] = useState("Admin123!");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const router = useRouter();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await login(email, password);
      router.push("/");
    } catch (err) {
      alert("Login failed: " + (err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="container">
      <div className="card" style={{ maxWidth: 480, margin: "0 auto" }}>
        <h2>Вход в DMS Demo</h2>
        <form onSubmit={onSubmit}>
          <div>
            <label>Email
              <input className="input" value={email} onChange={(e)=>setEmail(e.target.value)} />
            </label>
          </div>
          <div style={{ marginTop: 12 }}>
            <label>Пароль
              <input type="password" className="input" value={password} onChange={(e)=>setPassword(e.target.value)} />
            </label>
          </div>
          <div style={{ marginTop: 16 }}>
            <button className="button" type="submit" disabled={loading}>{loading ? "Входим..." : "Войти"}</button>
          </div>
        </form>
        <p className="small" style={{ marginTop: 12 }}>Используйте admin@demo / Admin123! или user@demo / User123!</p>
      </div>
    </main>
  );
}