import { useAuth } from "../../context/AuthContext";

function Navbar() {

    const { user } = useAuth();

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

                <span
                    className="navbar-brand"
                >
                    Smart Attendance System
                </span>

                <div>

                    <strong>
                        {user?.username}
                    </strong>

                    {" | "}

                    {user?.role}

                </div>

            </div>

        </nav>
    );
}

export default Navbar;