<script setup>
import { watch, ref, computed } from "vue";
import { useToast } from "vue-toastification";
import axios from "@/utils/axios.js";
import { useRouter } from "vue-router";
import { userStore } from "../stores/userStore.js";

const toast = useToast();
const router = useRouter();
const store = userStore();

const email = ref("");
const password = ref("");

const isValidEmail = ref(true);
const isValidPassword = ref(true);

const isEmailTouched = ref(false);
const isPasswordTouched = ref(false);

const passwordErrorMessage = ref("Password must be at least 8 characters");

watch(email, () => {
    if (!isEmailTouched.value && email.value) {
        isEmailTouched.value = true;
    }
    isValidEmail.value = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value);
});

watch(password, () => {
    if (!isPasswordTouched.value && password.value) {
        isPasswordTouched.value = true;
    }
    isValidPassword.value = password.value.length >= 8;
});

const isFormInvalid = computed(() => {
    return !(
        isValidEmail.value &&
        isValidPassword.value &&
        email.value &&
        password.value
    );
});

const handleSubmit = async () => {
    if (!isFormInvalid.value) {
        try {
            const response = await axios.post("/login", {
                email: email.value,
                password: password.value,
            });
            toast.success("Login successful!");
            store.setAuthToken(response.data.token);
            store.setUserRoles(response.data.roles);
            localStorage.setItem("authToken", response.data.token);
            localStorage.setItem("roles", JSON.stringify(response.data.roles));
            resetForm();
            router.push("/dashboard");
        } catch (error) {
            if (error.status === 404) {
                isValidEmail.value = false;
                isEmailTouched.value = true;
            } else if (error.status === 401) {
                isValidPassword.value = false;
                isPasswordTouched.value = true;
                passwordErrorMessage.value = error.response.data.message;
            }
            console.error(error);
            toast.error(error.response.data.message);
        }
    }
};

const resetForm = () => {
    email.value = "";
    password.value = "";

    isValidEmail.value = true;
    isValidPassword.value = true;

    isEmailTouched.value = false;
    isPasswordTouched.value = false;
};
</script>

<template>
    <div class="d-flex justify-content-center align-items-center vh-100">
        <div class="card shadow p-5 border rounded-3">
            <h3 class="card-title text-center mb-4">Login</h3>
            <form @submit.prevent="handleSubmit">
                <div class="form-group mb-3">
                    <label class="form-label">Email</label>
                    <input
                        v-model="email"
                        type="email"
                        class="form-control"
                        :class="{
                            'is-invalid': !isValidEmail && isEmailTouched,
                        }"
                        placeholder="email@example.com"
                        required
                    />
                    <small
                        v-if="!isValidEmail && isEmailTouched"
                        style="color: red"
                        >Please enter valid email</small
                    >
                </div>
                <div class="form-group mb-4">
                    <label class="form-label">Password</label>
                    <input
                        v-model="password"
                        type="password"
                        class="form-control"
                        :class="{
                            'is-invalid': !isValidPassword && isPasswordTouched,
                        }"
                        placeholder="password"
                        required
                    />
                    <small
                        v-if="!isValidPassword && isPasswordTouched"
                        style="color: red"
                        >{{ passwordErrorMessage }}</small
                    >
                </div>
                <button
                    class="btn btn-primary w-100"
                    type="submit"
                    :disabled="isFormInvalid"
                >
                    Submit
                </button>
            </form>

            <p class="mt-3">
                Don't have an account?
                <RouterLink to="/auth/register">Register</RouterLink>
            </p>
        </div>
    </div>
</template>
