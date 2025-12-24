import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";

import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";

import DashboardONG from "../pages/dashboards/DashboardONG";
import DashboardAdotante from "../pages/dashboards/DashboardAdotante";
import DashboardDoador from "../pages/dashboards/DashboardDoador";

import RequireAuth from "../components/RequireAuth";

import NewAnimal from "../pages/NewAnimal";
import EditAnimal from "../pages/EditAnimal";

// ✅ ADICIONE ISTO
import AnimalProfile from "../pages/AnimalProfile";

function getAuth() {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("currentUser") || "null");
  return { token, user };
}

function PrivateRoute({ children }) {
  const { token } = getAuth();
  return token ? children : <Navigate to="/login" replace />;
}

function DashboardRedirect() {
  const { token, user } = getAuth();
  if (!token || !user) return <Navigate to="/login" replace />;

  if (user.role === "ONG") return <Navigate to="/dashboard/ong" replace />;
  if (user.role === "ADOTANTE") return <Navigate to="/dashboard/adotante" replace />;
  if (user.role === "DOADOR") return <Navigate to="/dashboard/doador" replace />;

  return <Navigate to="/" replace />;
}

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <DashboardRedirect />
            </PrivateRoute>
          }
        />

        {/* ✅ Perfil do animal */}
        <Route path="/animals/:id" element={<AnimalProfile />} />

        <Route
          path="/dashboard/ong"
          element={
            <RequireAuth role="ONG">
              <DashboardONG />
            </RequireAuth>
          }
        />

        <Route
          path="/dashboard/ong/animais/novo"
          element={
            <PrivateRoute>
              <NewAnimal />
            </PrivateRoute>
          }
        />

        {/* ✅ Alias para compatibilidade com botões antigos (ex: /animals/new) */}
        <Route
          path="/animals/new"
          element={
            <PrivateRoute>
              <NewAnimal />
            </PrivateRoute>
          }
        />

        <Route
          path="/dashboard/ong/animais/:id/editar"
          element={
            <PrivateRoute>
              <EditAnimal />
            </PrivateRoute>
          }
        />

        <Route
          path="/dashboard/adotante"
          element={
            <RequireAuth role="ADOTANTE">
              <DashboardAdotante />
            </RequireAuth>
          }
        />

        <Route
          path="/dashboard/doador"
          element={
            <PrivateRoute>
              <DashboardDoador />
            </PrivateRoute>
          }
        />

        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
