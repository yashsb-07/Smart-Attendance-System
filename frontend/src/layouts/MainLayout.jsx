import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";
import useScreenSize from "../hooks/useScreenSize";
import SidebarOverlay from "../components/layout/SidebarOverlay";

function MainLayout() {

    const [collapsed, setCollapsed]
    = useState(
        window.innerWidth < 992
    );
    const isMobile = useScreenSize();

    return (

        <div className="layout-container">

            <SidebarOverlay
                show={
                    isMobile &&
                    !collapsed
                }
                onClick={() =>
                    setCollapsed(true)
                }
            />

            <Sidebar
                collapsed={collapsed}
                isMobile={isMobile}
            />

            <div className="main-content">

                <Navbar
                    collapsed={collapsed}
                    setCollapsed={setCollapsed}
                    isMobile={isMobile}
                />

                <div className="page-content">

                    <Outlet />

                </div>

                <Footer />

            </div>

        </div>

    );
}

export default MainLayout;