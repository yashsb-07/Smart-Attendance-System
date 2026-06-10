import { Outlet } from "react-router-dom";

import Sidebar from "../components/layout/Sidebar";
import Navbar from "../components/layout/Navbar";
import Footer from "../components/layout/Footer";

function MainLayout() {

    return (

        <div className="layout-container">

            <Sidebar />

            <div className="main-content">

                <Navbar />

                <div className="page-content">

                    <Outlet />

                </div>

                <Footer />

            </div>

        </div>
    );
}

export default MainLayout;