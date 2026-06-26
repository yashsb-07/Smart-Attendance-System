import api from "../api/axios";
import { API_ENDPOINTS } from "../api/endpoints";

export const getDepartments = async () => {
    const response = await api.get(
        API_ENDPOINTS.DEPARTMENTS.LIST
    );

    return response.data;
};

export const createDepartment = async (data) => {
    const response = await api.post(
        API_ENDPOINTS.DEPARTMENTS.LIST,
        data
    );

    return response.data;
};