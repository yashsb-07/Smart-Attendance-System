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

                </Route>

            </Routes>

        </BrowserRouter>
    );
}

export default App;