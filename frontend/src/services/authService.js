import api from "../api/axios";

import { API_ENDPOINTS, } from "../api/endpoints";

export const loginUser = async (credentials) => {
    const response = await api.post(
        API_ENDPOINTS.AUTH.LOGIN,
        credentials
    );

    return response.data;
};

export const getCurrentUser = async () => {
    const response = await api.get(
        API_ENDPOINTS.AUTH.CURRENT_USER
    );

    return response.data;
};

export const refreshToken = async (refresh) => {
    const response = await api.post(
        API_ENDPOINTS.AUTH.REFRESH,
        {
            refresh,
        }
    );

    return response.data;
};

export const logoutUser = async (refresh) => {
    const response = await api.post(
        API_ENDPOINTS.AUTH.LOGOUT,
        {
            refresh,
        }
    );

    return response.data;
};