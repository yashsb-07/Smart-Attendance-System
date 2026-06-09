import { useAuth } from "./context/AuthContext";

function App() {

    const {
        user,
        logout,
    } = useAuth();

    return (

        <div>

            <h1>
                Smart Attendance System
            </h1>

            <pre>
                {JSON.stringify(user)}
            </pre>

            <button
                onClick={logout}
            >
                Logout
            </button>

        </div>

    );
}

export default App;