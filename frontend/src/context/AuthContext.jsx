import {
    createContext,
    useContext,
    useState,
    useEffect,
} from "react";

import {
    loginUser,
    getCurrentUser,
    logoutUser,
} from "../services/authService";

import {
    setTokens,
    clearTokens,
    getAccessToken,
    getRefreshToken,
} from "../utils/tokenService";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {

    const [user, setUser] = useState(null);

    const [loading, setLoading] = useState(true);

    useEffect(() => {

        const loadUser = async () => {

            try {

                const token = getAccessToken();

                if (!token) {
                    setLoading(false);
                    return;
                }

                const currentUser =
                    await getCurrentUser();

                setUser(currentUser);

            } catch (error) {

                clearTokens();

                setUser(null);

                
            } finally {

                setLoading(false);
            }
        };

        loadUser();

    }, []);

    const login = async (credentials) => {

        const response =
            await loginUser(credentials);

        setTokens(
            response.access,
            response.refresh
        );

        setUser(response.user);

        return response;
    };

    const logout = async () => {

        try {

            const refresh =
                getRefreshToken();

            if (refresh) {

                await logoutUser(refresh);
            }

        } catch (error) {

            console.error(error);

        } finally {

            clearTokens();

            setUser(null);

            window.location.href = "/login";
        }
    };

    return (

        <AuthContext.Provider
            value={{
                user,
                setUser,
                login,
                logout,
                loading,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    return useContext(AuthContext);
};