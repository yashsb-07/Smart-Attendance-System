import React from "react";
import ReactDOM from "react-dom/client";

import './index.css'
import App from "./App";

import { AuthProvider } from "./context/AuthContext";

import "bootstrap/dist/css/bootstrap.min.css";

import "./styles/variables.css";
import "./styles/layout.css";
import "./styles/global.css";

ReactDOM.createRoot(
    document.getElementById("root")
).render(
    <React.StrictMode>
        <AuthProvider>
            <App />
        </AuthProvider>
    </React.StrictMode>
);