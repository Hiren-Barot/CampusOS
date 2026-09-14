import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "react-hot-toast";
import App from "./App.jsx";
import { AuthProvider } from "./context/AuthContext.jsx";
import ErrorBoundary from "./components/common/ErrorBoundary.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <ErrorBoundary>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <AuthProvider>
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: "rgb(var(--color-paper-raised))",
                color: "rgb(var(--color-ink))",
                border: "1px solid rgb(var(--color-hairline))",
                fontSize: "13px",
              },
              success: { iconTheme: { primary: "#4A7C59", secondary: "#fff" } },
              error: { iconTheme: { primary: "#C4432B", secondary: "#fff" } },
            }}
          />
          <App />
        </AuthProvider>
      </BrowserRouter>
    </ErrorBoundary>
  </React.StrictMode>
);