const ACCESS_TOKEN = "accessToken";
const REFRESH_TOKEN = "refreshToken";

export const setTokens = (access, refresh) => {
    localStorage.setItem(ACCESS_TOKEN, access);
    localStorage.setItem(REFRESH_TOKEN, refresh);
};

export const getAccessToken = () => {
    return localStorage.getItem(ACCESS_TOKEN);
};

export const getRefreshToken = () => {
    return localStorage.getItem(REFRESH_TOKEN);
};

export const clearTokens = () => {
    localStorage.removeItem(ACCESS_TOKEN);
    localStorage.removeItem(REFRESH_TOKEN);
};