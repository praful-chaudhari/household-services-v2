import axios from "axios";
import { userStore } from "../stores/userStore";

const instance = axios.create({
    baseURL: "http://127.0.0.1:5000",
    timeout: 1000,
    headers: {
        "Content-Type": "application/json",
    },
});

instance.interceptors.request.use((config) => {
    const store = userStore();
    const token = store.getAuthToken;
    if (token) {
        config.headers["Authentication-Token"] = token;
    }
    return config;
});

export default instance;
