<script setup>
import { computed, inject, reactive, ref, watch } from "vue";
import axios from "@/utils/axios.js";
import { useToast } from "vue-toastification";

const toast = useToast();

const loadServices = inject("loadServices");

const newServiceData = reactive({
    name: "",
    basePrice: 0,
    timeRequired: 0,
    description: "",
});

const isNameValid = ref(true);
const isBasePriceValid = ref(true);
const isTimeRequiredValid = ref(true);
const isDescriptionValid = ref(true);

const isNameTouched = ref(false);
const isBasePriceTouched = ref(false);
const isTimeRequiredTouched = ref(false);
const isDescriptionTouched = ref(false);

watch(
    () => newServiceData.name,
    (name) => {
        if (!isNameTouched.value && name) {
            isNameTouched.value = true;
        }
        isNameValid.value = name.trim().length > 0;
    }
);

watch(
    () => newServiceData.basePrice,
    (basePrice) => {
        if (!isBasePriceTouched.value && basePrice) {
            isBasePriceTouched.value = true;
        }
        isBasePriceValid.value = basePrice > 0 && basePrice <= 500;
    }
);

watch(
    () => newServiceData.timeRequired,
    (timeRequired) => {
        if (!isTimeRequiredTouched.value && timeRequired) {
            isTimeRequiredTouched.value = true;
        }
        isTimeRequiredValid.value = timeRequired >= 10 && timeRequired <= 600;
    }
);

watch(
    () => newServiceData.description,
    (description) => {
        if (!isDescriptionTouched.value && description) {
            isDescriptionTouched.value = true;
        }
        isDescriptionValid.value = description.trim().length > 10;
    }
);

const isFormInvalid = computed(() => {
    return !(
        isNameValid.value &&
        isBasePriceValid.value &&
        isTimeRequiredValid.value &&
        isDescriptionValid.value &&
        newServiceData.name &&
        newServiceData.basePrice &&
        newServiceData.timeRequired &&
        newServiceData.description
    );
});

const addNewService = async () => {
    if (!isFormInvalid.value) {
        try {
            const response = await axios.post("/services", newServiceData);
            loadServices();
            toast.success(response.data.message);
            clearForm();
        } catch (error) {
            console.error(error);
            toast.error("Error adding new service");
        }
    }
};

const clearForm = () => {
    newServiceData.name = "";
    newServiceData.basePrice = 0;
    newServiceData.timeRequired = 0;
    newServiceData.description = "";
    isNameTouched.value = false;
    isBasePriceTouched.value = false;
    isTimeRequiredTouched.value = false;
    isDescriptionTouched.value = false;
};
</script>

<template>
    <div class="d-flex justify-content-center align-items-center">
        <form @submit.prevent="addNewService">
            <div class="form-group mb-3">
                <label class="form-label">Name</label>
                <input
                    v-model="newServiceData.name"
                    type="text"
                    class="form-control"
                    :class="{
                        'is-invalid': !isNameValid && isNameTouched,
                    }"
                    placeholder="e.g. Plumbing"
                    required
                />
                <small v-if="!isNameValid && isNameTouched" style="color: red"
                    >Please enter valid service name</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Base Price</label>
                <input
                    v-model="newServiceData.basePrice"
                    type="number"
                    class="form-control"
                    :class="{
                        'is-invalid': !isBasePriceValid && isBasePriceTouched,
                    }"
                    placeholder="100"
                    required
                />
                <small
                    v-if="!isBasePriceValid && isBasePriceTouched"
                    style="color: red"
                    >Please enter valid base price</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Time Required (In minutes)</label>
                <input
                    v-model="newServiceData.timeRequired"
                    type="number"
                    class="form-control"
                    :class="{
                        'is-invalid':
                            !isTimeRequiredValid && isTimeRequiredTouched,
                    }"
                    placeholder="60"
                    required
                />
                <small
                    v-if="!isTimeRequiredValid && isTimeRequiredTouched"
                    style="color: red"
                    >Please enter valid time</small
                >
            </div>
            <div class="form-group mb-4">
                <label class="form-label">Description</label>
                <textarea
                    v-model="newServiceData.description"
                    type="text"
                    class="form-control"
                    :class="{
                        'is-invalid':
                            isDescriptionTouched && !isDescriptionValid,
                    }"
                    placeholder="Repairing tap..."
                    required
                />
                <small
                    v-if="!isDescriptionValid && isDescriptionTouched"
                    style="color: red"
                    >Please enter valid description at least 10 characters
                    long</small
                >
            </div>
            <button
                class="btn btn-primary w-100"
                data-bs-dismiss="modal"
                type="submit"
                :disabled="isFormInvalid"
            >
                Add
            </button>
        </form>
    </div>
</template>
