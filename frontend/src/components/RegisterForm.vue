<script setup>
import { computed, reactive, ref, watch, onMounted } from "vue";
import { useToast } from "vue-toastification";
import axios from "@/utils/axios.js";

const userTypes = [
    { label: "Customer", value: "customer" },
    { label: "Service Provider", value: "service_provider" },
];

const toast = useToast();

const userData = reactive({
    userType: "customer",
    name: "",
    username: "",
    email: "",
    password: "",
    serviceType: "",
    serviceDescription: "",
    experience: "",
});

const services = ref([]);

onMounted(async () => {
    try {
        const response = await axios.get("/services");
        services.value = response.data;
    } catch (error) {
        toast.error("Error fetching services");
    }
});

const changeUserType = (userType) => {
    userData.userType = userType;
};

const isNameValid = ref(true);
const isUsernameValid = ref(true);
const isEmailValid = ref(true);
const isPasswordValid = ref(true);
const isServiceTypeValid = ref(true);
const isServiceDescriptionValid = ref(true);
const isExperienceValid = ref(true);

const isNameTouched = ref(false);
const isUsernameTouched = ref(false);
const isEmailTouched = ref(false);
const isPasswordTouched = ref(false);
const isServiceTypeTouched = ref(false);
const isServiceDescriptionTouched = ref(false);
const isExperienceTouched = ref(false);

watch(
    () => userData.name,
    (name) => {
        if (!isNameTouched.value && name) {
            isNameTouched.value = true;
        }
        isNameValid.value = name.trim().length > 0;
    }
);

watch(
    () => userData.username,
    (username) => {
        if (!isUsernameTouched.value && username) {
            isUsernameTouched.value = true;
        }
        isUsernameValid.value = username.trim().length > 0;
    }
);

watch(
    () => userData.email,
    (email) => {
        if (!isEmailTouched.value && email) {
            isEmailTouched.value = true;
        }
        isEmailValid.value = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
);

watch(
    () => userData.password,
    (password) => {
        if (!isPasswordTouched.value && password) {
            isPasswordTouched.value = true;
        }
        isPasswordValid.value = password.length >= 8;
    }
);

watch(
    () => userData.serviceType,
    (serviceType) => {
        if (!isServiceTypeTouched.value && serviceType) {
            isServiceTypeTouched.value = true;
        }
        isServiceTypeValid.value = serviceType.length !== 0;
    }
);

watch(
    () => userData.serviceDescription,
    (serviceDescription) => {
        if (!isServiceDescriptionTouched.value && serviceDescription) {
            isServiceDescriptionTouched.value = true;
        }
        isServiceDescriptionValid.value = serviceDescription.trim().length > 0;
    }
);

watch(
    () => userData.experience,
    (experience) => {
        if (!isExperienceTouched.value && experience) {
            isExperienceTouched.value = true;
        }
        isExperienceValid.value = experience > 0 && experience <= 100;
    }
);

const isFormInvalid = computed(() => {
    if (userData.userType === "customer") {
        return !(
            isNameValid.value &&
            isUsernameValid.value &&
            isEmailValid.value &&
            isPasswordValid.value &&
            userData.name &&
            userData.username &&
            userData.email &&
            userData.password
        );
    } else {
        return !(
            isNameValid.value &&
            isUsernameValid.value &&
            isEmailValid.value &&
            isPasswordValid.value &&
            isServiceTypeValid.value &&
            isServiceDescriptionValid.value &&
            isExperienceValid.value &&
            userData.name &&
            userData.username &&
            userData.email &&
            userData.password &&
            userData.serviceType &&
            userData.serviceDescription &&
            userData.experience
        );
    }
});

const handleSubmit = () => {
    if (isFormInvalid.value) {
        return;
    }

    toast.success("Registration successful!");
    console.log(userData.name);
    console.log(userData.username);
    console.log(userData.email);
    console.log(userData.password);
    console.log(userData.serviceType);
    console.log(userData.serviceDescription);
    console.log(userData.experience);
    resetForm();
};

const resetForm = () => {
    userData.name = "";
    userData.username = "";
    userData.email = "";
    userData.password = "";
    userData.serviceType = "";
    userData.serviceDescription = "";
    userData.experience = "";

    isNameValid.value = true;
    isUsernameValid.value = true;
    isEmailValid.value = true;
    isPasswordValid.value = true;
    isServiceTypeValid.value = true;
    isServiceDescriptionValid.value = true;
    isExperienceValid.value = true;

    isNameTouched.value = false;
    isUsernameTouched.value = false;
    isEmailTouched.value = false;
    isPasswordTouched.value = false;
    isServiceTypeTouched.value = false;
    isServiceDescriptionTouched.value = false;
    isExperienceTouched.value = false;
};
</script>

<template>
    <div class="container mt-5">
        <div class="card p-4 shadow">
            <div class="form-header sticky-top mb-3 p-3 shadow-sm">
                <h2 class="text-center mb-4">Registration</h2>

                <div class="btn-group mb-3 w-100" role="group">
                    <button
                        v-for="type in userTypes"
                        :key="type.value"
                        class="btn border"
                        :class="[
                            userData.userType === type.value
                                ? 'btn-secondary'
                                : 'btn-light',
                            type.value === 'customer'
                                ? 'rounded-start-pill'
                                : 'rounded-end-pill',
                        ]"
                        @click="changeUserType(type.value)"
                    >
                        {{ type.label }}
                    </button>
                </div>
            </div>

            <div class="form-body overflow-auto" style="max-height: 400px">
                <transition name="slide-fade" mode="out-in">
                    <div :key="userData.userType">
                        <form @submit.prevent="handleSubmit">
                            <div class="form-group mb-3">
                                <label class="form-label">Full Name</label>
                                <input
                                    v-model="userData.name"
                                    type="text"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            isNameTouched && !isNameValid,
                                    }"
                                    placeholder="John Doe"
                                    required
                                />
                                <small
                                    v-if="isNameTouched && !isNameValid"
                                    style="color: red"
                                    >Please enter valid name</small
                                >
                            </div>
                            <div class="form-group mb-3">
                                <label class="form-label">Username</label>
                                <input
                                    v-model="userData.username"
                                    type="text"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            isUsernameTouched &&
                                            !isUsernameValid,
                                    }"
                                    placeholder="johndoe"
                                    required
                                />
                                <small
                                    v-if="isUsernameTouched && !isUsernameValid"
                                    style="color: red"
                                    >Please enter valid username</small
                                >
                            </div>
                            <div class="form-group mb-3">
                                <label class="form-label">Email</label>
                                <input
                                    v-model="userData.email"
                                    type="email"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            isEmailTouched && !isEmailValid,
                                    }"
                                    placeholder="email@example.com"
                                    required
                                />
                                <small
                                    v-if="isEmailTouched && !isEmailValid"
                                    style="color: red"
                                    >Please enter valid email</small
                                >
                            </div>
                            <div class="form-group mb-3">
                                <label class="form-label">Password</label>
                                <input
                                    v-model="userData.password"
                                    type="password"
                                    class="form-control"
                                    :class="{
                                        'is-invalid':
                                            isPasswordTouched &&
                                            !isPasswordValid,
                                    }"
                                    placeholder="password"
                                    required
                                />
                                <small
                                    v-if="isPasswordTouched && !isPasswordValid"
                                    style="color: red"
                                    >Password must be at least 8
                                    characters</small
                                >
                            </div>

                            <div
                                v-if="userData.userType === 'service_provider'"
                            >
                                <div class="form-group mb-3">
                                    <label class="form-label"
                                        >Service Type</label
                                    >
                                    <select
                                        v-model="userData.serviceType"
                                        id="serviceType"
                                        class="form-select"
                                        :class="{
                                            'is-invalid':
                                                isServiceTypeTouched &&
                                                !isServiceTypeValid,
                                        }"
                                        required
                                    >
                                        <option disabled value="">
                                            Choose...
                                        </option>
                                        <option value="1">Option 1</option>
                                        <option value="2">Option 2</option>
                                    </select>
                                    <small
                                        v-if="
                                            isServiceTypeTouched &&
                                            !isServiceTypeValid
                                        "
                                        style="color: red"
                                        >Please select service type</small
                                    >
                                </div>
                                <div class="form-group mb-3">
                                    <label class="form-label"
                                        >Describe your service</label
                                    >
                                    <textarea
                                        v-model="userData.serviceDescription"
                                        type="text"
                                        class="form-control"
                                        :class="{
                                            'is-invalid':
                                                isServiceDescriptionTouched &&
                                                !isServiceDescriptionValid,
                                        }"
                                        placeholder="I offer..."
                                        required
                                    />
                                    <small
                                        v-if="
                                            isServiceDescriptionTouched &&
                                            !isServiceDescriptionValid
                                        "
                                        style="color: red"
                                        >Please enter service description</small
                                    >
                                </div>
                                <div class="form-group mb-3">
                                    <label class="form-label"
                                        >Experience (in years)</label
                                    >
                                    <input
                                        v-model="userData.experience"
                                        type="number"
                                        class="form-control"
                                        :class="{
                                            'is-invalid':
                                                isExperienceTouched &&
                                                !isExperienceValid,
                                        }"
                                        placeholder="3"
                                        required
                                    />
                                    <small
                                        v-if="
                                            isExperienceTouched &&
                                            !isExperienceValid
                                        "
                                        style="color: red"
                                        >Please enter valid experience
                                        (1-100)</small
                                    >
                                </div>
                            </div>
                            <div class="d-flex justify-content-center">
                                <button
                                    class="btn btn-primary w-75"
                                    type="submit"
                                    :disabled="isFormInvalid"
                                >
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
                </transition>
            </div>
            <div class="d-flex justify-content-center">
                <p class="mt-3">
                    Already have an account?
                    <RouterLink to="/auth/login">Login</RouterLink>
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.container {
    max-width: 500px;
}

/* Sticky Header */
.form-header {
    position: sticky;
    top: 0;
    z-index: 1000;
}

/* Transition Effect */
.slide-fade-enter-active,
.slide-fade-leave-active {
    transition: opacity 0.3s ease, transform 0.3s ease;
}
.slide-fade-enter-from,
.slide-fade-leave-to {
    opacity: 0;
    transform: translateY(10px);
}
</style>
