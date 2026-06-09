import axios from "axios";

import {
    getAccessToken,
    getRefreshToken,
    setTokens,
    clearTokens,
} from "../utils/tokenService";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api",
    headers: {
        "Content-Type": "application/json",
    },
});

api.interceptors.request.use(

    (config) => {

        const token =
            getAccessToken();

        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }

        return config;
    },

    (error) => Promise.reject(error)

);

api.interceptors.response.use(

    (response) => response,

    async (error) => {

        const originalRequest =
            error.config;

        if (
            error.response?.status === 401 &&
            !originalRequest._retry
        ) {

            originalRequest._retry = true;

            try {

                const refresh =
                    getRefreshToken();

                if (!refresh) {

                    clearTokens();

                    window.location.href =
                        "/login";

                    return Promise.reject(error);
                }

                const response =
                    await axios.post(
                        "http://127.0.0.1:8000/api/auth/refresh/",
                        {
                            refresh,
                        }
                    );

                const newAccess =
                    response.data.access;

                setTokens(
                    newAccess,
                    refresh
                );

                originalRequest.headers.Authorization =
                    `Bearer ${newAccess}`;

                return api(
                    originalRequest
                );

            } catch (refreshError) {

                clearTokens();

                window.location.href =
                    "/login";

                return Promise.reject(
                    refreshError
                );
            }
        }

        return Promise.reject(error);
    }

);

export default api;