import { ROLES } from "../constants/authConstants";

export const navigationConfig = {

    [ROLES.ADMIN]: [

        {
            name: "Dashboard",
            path: "/",
            icon: "📊",
        },

        {
            name: "Departments",
            path: "/departments",
            icon: "🏢",
        },

        {
            name: "Students",
            path: "/students",
            icon: "🎓",
        },

        {
            name: "Attendance",
            path: "/attendance",
            icon: "📅",
        },

        {
            name: "Reports",
            path: "/reports",
            icon: "📈",
        },
    ],

    [ROLES.TEACHER]: [

        {
            name: "Dashboard",
            path: "/",
            icon: "📊",
        },

        {
            name: "Attendance",
            path: "/attendance",
            icon: "📅",
        },

        {
            name: "Students",
            path: "/students",
            icon: "🎓",
        },
    ],

    [ROLES.STUDENT]: [

        {
            name: "Dashboard",
            path: "/",
            icon: "📊",
        },

        {
            name: "Attendance History",
            path: "/attendance-history",
            icon: "📚",
        },

        {
            name: "Profile",
            path: "/profile",
            icon: "👤",
        },
    ],
};