export const API_ENDPOINTS = {

    AUTH: {

        LOGIN: "/auth/login/",

        LOGOUT: "/auth/logout/",

        REFRESH: "/auth/refresh/",

        CURRENT_USER: "/auth/me",

    },

    DEPARTMENTS: {

        LIST: "/departments/",

        DETAIL: (id) =>
            `/departments/${id}/`,
    },

    TEACHERS: {

        LIST: "/teachers/",

        DETAIL: (id) =>
            `/teachers/${id}/`,
    },

    STUDENTS: {

        LIST: "/students/",

        DETAIL: (id) =>
            `/students/${id}/`,
    },

    ATTENDANCE: {

        LIST: "/attendance/",

        DETAIL: (id) =>
            `/attendance/${id}/`,
    },
};