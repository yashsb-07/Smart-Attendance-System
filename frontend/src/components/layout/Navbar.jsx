import { useAuth } from "../../context/AuthContext";

function Navbar({

    collapsed,
    setCollapsed,

}) {

    const {
        user,
        logout,
    } = useAuth();

    return (

        <nav
            className="
                navbar
                navbar-expand-lg
                navbar-light
                bg-white
                shadow-sm
                px-4
            "
        >

            <div className="container-fluid">

                <span className="navbar-brand fw-bold">
                    Smart Attendance
                </span>

                <div className="d-flex align-items-center gap-3">

                    <button
                        className="btn btn-outline-primary"
                        onClick={() =>
                            setCollapsed(!collapsed)
                        }
                    >
                        ☰
                    </button>

                    <div>
                        <strong>
                            {user?.username}
                        </strong>

                        {" | "}

                        {user?.role}
                    </div>

                    <button
                        className="btn btn-danger btn-sm"
                        onClick={logout}
                    >
                        Logout
                    </button>

                </div>

            </div>

        </nav>
    );
}

export default Navbar;