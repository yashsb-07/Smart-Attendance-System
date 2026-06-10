import { Navigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";

import AuthLoader from "../common/AuthLoader";

function RoleRoute({

    children,
    allowedRoles,

}) {

    const {
        user,
        loading,
    } = useAuth();

    if (loading) {

        return <AuthLoader />;
    }

    if (!user) {

        return (
            <Navigate
                to="/login"
                replace
            />
        );
    }

    if (
        !allowedRoles.includes(
            user.role
        )
    ) {

        return (
            <Navigate
                to="/unauthorized"
                replace
            />
        );
    }

    return children;
}

export default RoleRoute;