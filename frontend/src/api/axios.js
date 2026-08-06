import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000/api/",
    headers: {
        "Content-Type": "application/json",
    },
});

// Request Interceptor
api.interceptors.request.use((config) => {

    const token = localStorage.getItem("access_token");

    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
});

// Response Interceptor: refresh access token once on 401
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;

        if (
            error.response?.status === 401 &&
            originalRequest &&
            !originalRequest._retry &&
            !originalRequest.url.includes("accounts/token/refresh/")
        ) {
            originalRequest._retry = true;
            const refresh = localStorage.getItem("refresh_token");

            if (refresh) {
                try {
                    const refreshResponse = await axios.post(
                        "http://127.0.0.1:8000/api/accounts/token/refresh/",
                        { refresh },
                        {
                            headers: {
                                "Content-Type": "application/json",
                            },
                        }
                    );

                    localStorage.setItem("access_token", refreshResponse.data.access);
                    originalRequest.headers.Authorization = `Bearer ${refreshResponse.data.access}`;
                    return api(originalRequest);
                } catch (refreshError) {
                    localStorage.removeItem("access_token");
                    localStorage.removeItem("refresh_token");
                    window.location.href = "/login";
                    return Promise.reject(refreshError);
                }
            }
        }

        return Promise.reject(error);
    }
);

export default api;