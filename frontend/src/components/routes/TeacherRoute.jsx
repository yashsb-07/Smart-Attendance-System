import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

function TeacherRoute({ children }) {

    const { user, loading } = useAuth();

    if (loading) {
        return <h3>Loading...</h3>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (user.role !== "teacher") {
        return (
            <Navigate
                to="/unauthorized"
                replace
            />
        );
    }

    return children;
}

export default TeacherRoute;