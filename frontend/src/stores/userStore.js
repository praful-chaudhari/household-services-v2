import { defineStore } from "pinia";

export const userStore = defineStore("userStore", {
    state: () => ({
        authToken: localStorage.getItem("authToken") || null,
        roles: JSON.parse(localStorage.getItem("roles")) || [],
    }),

    actions: {
        setAuthToken(authToken) {
            this.authToken = authToken;
        },
        clearAuthToken() {
            this.authToken = null;
            localStorage.removeItem("authToken");
        },
        setUserRoles(roles) {
            this.roles = roles;
        },
        clearRoles() {
            this.roles = [];
        },
        logout() {
            this.clearAuthToken();
            this.clearRoles();
        },
    },

    getters: {
        isAuthenticated: (state) => !!state.authToken,
        getAuthToken: (state) => state.authToken,
        getRoles: (state) => state.roles,
        isAdmin: (state) => state.roles.includes("admin"),
        isCustomer: (state) => state.roles.includes("customer"),
        isProfessional: (state) => state.roles.includes("professional"),
    },
});
