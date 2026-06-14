import { useAuth } from "../../context/AuthContext";

function Navbar({

    collapsed,
    setCollapsed,

}) {

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
                    className="
                        navbar-brand
                        fw-bold
                    "
                >
                    Smart Attendance
                </span>

                <div className="d-flex gap-3 align-items-center">

                    <button
                        className="btn btn-outline-primary"
                        onClick={() =>
                            setCollapsed(
                                !collapsed
                            )
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

                </div>

            </div>

        </nav>
    );
}

export default Navbar;