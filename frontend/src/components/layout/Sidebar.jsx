import { Link } from "react-router-dom";

function Sidebar() {

    return (

        <div
            style={{
                width: "260px",
                background: "#212529",
                color: "white",
                minHeight: "100vh",
                padding: "20px",
            }}
        >

            <h4>
                Smart Attendance
            </h4>

            <hr />

            <div className="d-flex flex-column">

                <Link
                    to="/"
                    className="text-white mb-3"
                >
                    Home
                </Link>

                <Link
                    to="/admin"
                    className="text-white mb-3"
                >
                    Admin
                </Link>

                <Link
                    to="/teacher"
                    className="text-white mb-3"
                >
                    Teacher
                </Link>

                <Link
                    to="/student"
                    className="text-white mb-3"
                >
                    Student
                </Link>

            </div>

        </div>
    );
}

export default Sidebar;