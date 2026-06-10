import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";

import UnauthorizedPage from "./pages/UnauthorizedPage";

import AdminPage from "./pages/AdminPage";
import TeacherPage from "./pages/TeacherPage";
import StudentPage from "./pages/StudentPage";

import RoleRoute from "./components/routes/RoleRoute";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/login"
                    element={<LoginPage />}
                />

                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <HomePage />
                        </ProtectedRoute>
                    }
                />

                <Route
                    path="/unauthorized"
                    element={<UnauthorizedPage />}
                />

                <Route
                    path="/admin"
                    element={
                        
                        <RoleRoute    
                            allowedRoles={["admin"]}>
                        </RoleRoute>
                        
                    }
                />

                <Route
                    path="/teacher"
                    element={

                        <RoleRoute
                            allowedRoles={["teacher"]}>
                        </RoleRoute>
                    }
                />

                <Route
                    path="/student"
                    element={
                        
                        <RoleRoute
                            allowedRoles={["student"]}>
                        </RoleRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}

export default App;