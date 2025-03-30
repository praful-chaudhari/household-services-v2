<script setup>
import { computed, reactive, ref, watch, onMounted } from "vue";
import { useToast } from "vue-toastification";
import { useRouter } from "vue-router";
import axios from "@/utils/axios.js";
import { fetchServices } from "@/shared/fetchServices";

const toast = useToast();
const router = useRouter();

const services = ref([]);

const loadServices = async () => {
    try {
        services.value = await fetchServices();
    } catch (error) {
        console.error(error);
    }
};

onMounted(async () => {
    loadServices();
});

const userTypes = [
    { label: "Customer", value: "customer" },
    { label: "Service Provider", value: "service_provider" },
];

const userData = reactive({
    userType: "customer",
    name: "",
    email: "",
    password: "",
    serviceId: "",
    serviceDescription: "",
    experience: "",
    pincodes: "",
});

const changeUserType = (userType) => {
    userData.userType = userType;
};

const isNameValid = ref(true);
const isEmailValid = ref(true);
const isPasswordValid = ref(true);
const isServiceTypeValid = ref(true);
const isServiceDescriptionValid = ref(true);
const isExperienceValid = ref(true);
const isPincodeValid = ref(true);

const isNameTouched = ref(false);
const isEmailTouched = ref(false);
const isPasswordTouched = ref(false);
const isServiceTypeTouched = ref(false);
const isServiceDescriptionTouched = ref(false);
const isExperienceTouched = ref(false);
const isPincodeTouched = ref(false);
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
    () => userData.serviceId,
    (serviceId) => {
        if (!isServiceTypeTouched.value && serviceId) {
            isServiceTypeTouched.value = true;
        }
        isServiceTypeValid.value = serviceId !== "";
    }
);

watch(
    () => userData.serviceDescription,
    (serviceDescription) => {
        if (!isServiceDescriptionTouched.value && serviceDescription) {
            isServiceDescriptionTouched.value = true;
        }
        isServiceDescriptionValid.value = serviceDescription.trim().length > 10;
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

watch(
    () => userData.pincodes,
    (pincodes) => {
        if (!isPincodeTouched.value && pincodes) {
            isPincodeTouched.value = true;
        }
        isPincodeValid.value = /^[0-9,]+$/.test(pincodes);
    }
);

const isFormInvalid = computed(() => {
    if (userData.userType === "customer") {
        return !(
            isNameValid.value &&
            isEmailValid.value &&
            isPasswordValid.value &&
            userData.name &&
            userData.email &&
            userData.password
        );
    } else {
        return !(
            isNameValid.value &&
            isEmailValid.value &&
            isPasswordValid.value &&
            isServiceTypeValid.value &&
            isServiceDescriptionValid.value &&
            isExperienceValid.value &&
            userData.name &&
            userData.email &&
            userData.password &&
            userData.serviceId &&
            userData.serviceDescription &&
            userData.experience &&
            userData.pincodes
        );
    }
});

const handleSubmit = async () => {
    if (isFormInvalid.value) {
        return;
    }

    if (userData.userType === "customer") {
        try {
            const response = await axios.post("/customer/register", {
                name: userData.name,
                email: userData.email,
                password: userData.password,
            });
            toast.success(response.data.message);
            router.push({ name: "login" });
        } catch (error) {
            console.error(error);
            toast.error(error.response.data.message);
        }
    } else {
        try {
            const response = await axios.post("/professional/register", {
                name: userData.name,
                email: userData.email,
                password: userData.password,
                serviceId: userData.serviceId,
                description: userData.serviceDescription,
                experience: userData.experience,
                pincodes: userData.pincodes,
            });
            toast.success(response.data.message);
            router.push({ name: "login" });
        } catch (error) {
            console.error(error);
            toast.error("Error registering");
        }
    }
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
                                : '',
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
                                        v-model="userData.serviceId"
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
                                            Select Service
                                        </option>
                                        <option
                                            v-for="(service, index) in services"
                                            :key="index"
                                            :value="service.id"
                                        >
                                        {{ service.name }} - ${{ service.base_price }} ({{ service.time_required }} mins)
                                        </option>
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
                                        >Please enter service description at
                                        least 10 characters long</small
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
                                <div class="form-group mb-3">
                                    <label class="form-label"
                                        >Service Pincodes</label
                                    >
                                    <input
                                        v-model="userData.pincodes"
                                        type="text"
                                        class="form-control"
                                        :class="{
                                            'is-invalid':
                                                isPincodeTouched &&
                                                !isPincodeValid,
                                        }"
                                        placeholder="123456, 123457, 123458, ..."
                                        required
                                    />
                                    <small
                                        v-if="
                                            isExperienceTouched &&
                                            !isExperienceValid
                                        "
                                        style="color: red"
                                        >Please enter valid pincodes</small
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
