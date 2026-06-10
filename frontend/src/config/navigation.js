import { ROLES } from "../constants/authConstants";

export const navigationConfig = {

    [ROLES.ADMIN]: [

        {
            name: "Dashboard",
            path: "/",
        },

        {
            name: "Teachers",
            path: "/teachers",
        },

        {
            name: "Students",
            path: "/students",
        },

        {
            name: "Attendance",
            path: "/attendance",
        },

        {
            name: "Reports",
            path: "/reports",
        },
    ],

    [ROLES.TEACHER]: [

        {
            name: "Dashboard",
            path: "/",
        },

        {
            name: "Attendance",
            path: "/attendance",
        },

        {
            name: "Students",
            path: "/students",
        },
    ],

    [ROLES.STUDENT]: [

        {
            name: "Dashboard",
            path: "/",
        },

        {
            name: "Attendance History",
            path: "/attendance-history",
        },

        {
            name: "Profile",
            path: "/profile",
        },
    ],
};