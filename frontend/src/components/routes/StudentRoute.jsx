import { Navigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

function StudentRoute({ children }) {

    const { user, loading } = useAuth();

    if (loading) {
        return <h3>Loading...</h3>;
    }

    if (!user) {
        return <Navigate to="/login" replace />;
    }

    if (user.role !== "student") {
        return (
            <Navigate
                to="/unauthorized"
                replace
            />
        );
    }

    return children;
}

export default StudentRoute;