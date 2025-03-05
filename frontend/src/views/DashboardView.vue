<script setup>
import { computed, defineAsyncComponent } from "vue";
import { userStore } from "@/stores/userStore";

// import CustomerDashboard from "@/components/customer/CustomerDashboard.vue";
// import ProfessionalDashboard from "@/components/professional/ProfessionalDashboard.vue";
// import AdminDashboard from "@/components/admin/AdminDashboard.vue";
const store = userStore();

const CustomerDashboard = defineAsyncComponent(() =>
    import("@/components/customer/CustomerDashboard.vue")
);
const ProfessionalDashboard = defineAsyncComponent(() =>
    import("@/components/professional/ProfessionalDashboard.vue")
);
const AdminDashboard = defineAsyncComponent(() =>
    import("@/components/admin/AdminDashboard.vue")
);

const dashboard = computed(() => {
    if (store.isAdmin) {
        console.log(store.getRoles);
        return AdminDashboard;
    } else if (userStore.isProfessional) {
        return ProfessionalDashboard;
    } else {
        return CustomerDashboard;
    }
});
</script>

<template>
    <component :is="dashboard" />
</template>
