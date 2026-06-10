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

import AdminRoute from "./components/routes/AdminRoute";
import TeacherRoute from "./components/routes/TeacherRoute";
import StudentRoute from "./components/routes/StudentRoute";

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
                        <AdminRoute>
                            <AdminPage />
                        </AdminRoute>
                    }
                />

                <Route
                    path="/teacher"
                    element={
                        <TeacherRoute>
                            <TeacherPage />
                        </TeacherRoute>
                    }
                />

                <Route
                    path="/student"
                    element={
                        <StudentRoute>
                            <StudentPage />
                        </StudentRoute>
                    }
                />

            </Routes>

        </BrowserRouter>
    );
}

export default App;