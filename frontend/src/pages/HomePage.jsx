import { useAuth } from "../context/AuthContext";

function HomePage() {

    const {
        user,
        logout,
    } = useAuth();

    return (

        <div className="container mt-5">

            <h1>
                Smart Attendance System
            </h1>

            <hr />

            <h4>
                Welcome {user?.username}
            </h4>

            <p>
                Role: {user?.role}
            </p>

            <button
                className="btn btn-danger"
                onClick={logout}
            >
                Logout
            </button>

        </div>
    );
}

export default HomePage;