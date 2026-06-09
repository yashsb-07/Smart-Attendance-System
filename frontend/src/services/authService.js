import api from "../api/axios";

export const loginUser = async (credentials) => {
    const response = await api.post(
        "/auth/login/",
        credentials
    );

    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get(
        "/auth/me/"
    );

    return response.data;
};

export const refreshToken = async (refresh) => {
    const response = await api.post(
        "/auth/refresh/",
        {
            refresh,
        }
    );

    return response.data;
};

export const logoutUser = async (refresh) => {
    const response = await api.post(
        "/auth/logout/",
        {
            refresh,
        }
    );

    return response.data;
};