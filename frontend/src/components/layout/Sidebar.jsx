import {
    NavLink,
} from "react-router-dom";

import {
    useAuth,
} from "../../context/AuthContext";

import {
    navigationConfig,
} from "../../config/navigation";

function Sidebar({

    collapsed,
    isMobile,

}) {

    const { user } = useAuth();

    const menuItems =
        navigationConfig[
            user?.role
        ] || [];

    return (

        <div
            style={{
                width: collapsed
                ? "80px"
                : "260px",

                background: "#212529",

                color: "white",

                minHeight: "100vh",

                transition: "all 0.3s ease",

                padding: "20px",

                position: isMobile
                ? "fixed"
                : "relative",

                top: 0,

                left:
                isMobile && collapsed
                    ? "-260px"
                    : "0",

                zIndex: 1000,
            }}
        >

            <h5>

                {collapsed
                    ? "SA"
                    : "Smart Attendance"}

            </h5>

            <hr />

            {menuItems.map(
                (item) => (

                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            `
                            d-block
                            mb-3
                            p-2
                            text-decoration-none
                            ${
                                isActive
                                    ? "bg-primary text-white"
                                    : "text-white"
                            }
                            `
                        }
                    >

                        <>
                            {item.icon}

                            {!collapsed && (

                                <span className="ms-2">
                                    {item.name}
                                </span>

                            )}
                        </>

                    </NavLink>
                )
            )}

        </div>
    );
}

export default Sidebar;