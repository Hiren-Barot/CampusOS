import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/auth/Login.jsx";
import Register from "./components/auth/Register.jsx";
import Layout from "./components/common/Layout.jsx";
import PrivateRoute from "./components/common/PrivateRoute.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Departments from "./pages/Departments.jsx";
import Users from "./pages/Users.jsx";
import Notices from "./pages/Notices.jsx";
import Assignments from "./pages/Assignments.jsx";
import Profile from "./pages/Profile.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      <Route
        element={
          <PrivateRoute>
            <Layout />
          </PrivateRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/notices" element={<Notices />} />
        <Route path="/assignments" element={<Assignments />} />
        <Route
          path="/users"
          element={
            <PrivateRoute allowedRoles={["faculty", "hod", "principal", "admin"]}>
              <Users />
            </PrivateRoute>
          }
        />
        <Route
          path="/departments"
          element={
            <PrivateRoute allowedRoles={["principal", "admin"]}>
              <Departments />
            </PrivateRoute>
          }
        />
        <Route path="/profile" element={<Profile />} />
      </Route>

      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
