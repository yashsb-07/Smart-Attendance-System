import {
    BrowserRouter,
    Routes,
    Route,
} from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

import MainLayout from "./layouts/MainLayout";

import LoginPage from "./pages/LoginPage";
import HomePage from "./pages/HomePage";

import UnauthorizedPage from "./pages/UnauthorizedPage";

import TeachersPage from "./pages/TeachersPage";
import StudentsPage from "./pages/StudentsPage";
import AttendancePage from "./pages/AttendancePage";
import ReportsPage from "./pages/ReportsPage";
import ProfilePage from "./pages/ProfilePage";
import AttendanceHistoryPage from "./pages/AttendanceHistoryPage";

function App() {

    return (

        <BrowserRouter>

            <Routes>

                <Route
                    path="/login"
                    element={<LoginPage />}
                />

                <Route
                    path="/unauthorized"
                    element={
                        <UnauthorizedPage />
                    }
                />

                <Route
                    element={
                        <ProtectedRoute>
                            <MainLayout />
                        </ProtectedRoute>
                    }
                >

                    <Route
                        path="/"
                        element={<HomePage />}
                    />

                    <Route
                        path="/teachers"
                        element={<TeachersPage />}
                    />

                    <Route
                        path="/students"
                        element={<StudentsPage />}
                    />

                    <Route
                        path="/attendance"
                        element={<AttendancePage />}
                    />

                    <Route
                        path="/reports"
                        element={<ReportsPage />}
                    />

                    <Route
                        path="/profile"
                        element={<ProfilePage />}
                    />

                    <Route
                        path="/attendance-history"
                        element={
                            <AttendanceHistoryPage />
                        }
                    />

                </Route>

            </Routes>

        </BrowserRouter>
    );
}

export default App;