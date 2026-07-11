import axios from 'axios'
import { toast } from 'react-toastify'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://taskmanager-t74i.onrender.com'

export const ENDPOINTS = {
    LOGIN: () => "/users/login",
    REGISTER: () => "/users/register",

    CREATE_TASK: () => "/tasks/create_task",

    GET_TASK: () => "/tasks/get-tasks",

    UPDATE_TASK: (id) => `/tasks/update-task/${id}`,

    DELETE_TASK: (id) => `/tasks/delete-task/${id}`,
}

export const instance = axios.create({
    baseURL: API_BASE_URL
});

instance.interceptors.request.use((config) => {
    const token = localStorage.getItem("token")
    if (token) {
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
}, (error) => Promise.reject(error))

instance.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401 && !error.config?.skipAuthRedirect) {
            localStorage.removeItem("token")
            toast.error("Your session has expired. Please log in again.")
            window.location.href = "/"
        }
        return Promise.reject(error)
    }
)
