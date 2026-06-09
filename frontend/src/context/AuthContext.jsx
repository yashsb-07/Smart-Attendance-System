import {
    createContext,
    useContext,
    useState,
    useEffect,
} from "react";

import {
    getCurrentUser,
} from "../services/authService";

import {
    getAccessToken,
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

                console.error(error);

            } finally {

                setLoading(false);

            }

        };

        loadUser();

    }, []);

    return (
        <AuthContext.Provider
            value={{
                user,
                setUser,
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