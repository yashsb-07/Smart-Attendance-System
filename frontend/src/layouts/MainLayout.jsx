import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

function MainLayout() {

    const [collapsed, setCollapsed] =
        useState(false);

    return (

        <div className="layout-container">

            <Sidebar
                collapsed={collapsed}
            />

            <div className="main-content">

                <Navbar
                    collapsed={collapsed}
                    setCollapsed={setCollapsed}
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