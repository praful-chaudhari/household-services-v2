import { defineStore } from "pinia";

export const userStore = defineStore("userStore", {
    state: () => ({
        user: JSON.parse(localStorage.getItem("user")) || {},
    }),

    actions: {
        setUser(user) {
            this.user = user;
            localStorage.setItem("user", JSON.stringify(user));
        },
        clearUser() {
            localStorage.removeItem("user");
            this.user = {};
        },
        logout() {
            this.clearUser();
        },
    },

    getters: {
        isAuthenticated: (state) => !!state.user.authToken,
        getAuthToken: (state) => state.user.authToken,
        getRoles: (state) => state.user.roles,
        isAdmin: (state) => state.user.roles?.includes("admin") || false,
        isCustomer: (state) => state.user.roles?.includes("customer") || false,
        isProfessional: (state) => state.user.roles?.includes("professional") || false,
    },
});
