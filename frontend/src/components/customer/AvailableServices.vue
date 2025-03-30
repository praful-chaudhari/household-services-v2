<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import { fetchServices } from '@/shared/fetchServices';
import { fetchServiceRequests } from '@/shared/fetchServiceRequests';
import { userStore } from '@/stores/userStore';

const toast = useToast();
const store = userStore();
const router = useRouter();
const services = ref([]);
const serviceRequests = ref([]);

const loadServices = async () => {
    try {
        services.value = await fetchServices();
    } catch (error) {
        console.error(error);
    }
};

const loadServiceRequests = async () => {
    try {
        serviceRequests.value = await fetchServiceRequests(null);
    } catch (error) {
        console.error(error);
    }
};

onMounted(() => {
  loadServices();
  loadServiceRequests();
});

const handleServiceClick = (service) => {
  router.push({ name: 'ServiceDetails', params: { id: service.id } });
};

const searchQuery = ref('');
const filteredServices = computed(() => {
  return services.value.filter(service => 
    service.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    service.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    service.base_price.toString().includes(searchQuery.value) ||
    service.time_required.toString().includes(searchQuery.value)
  );
});

const filterServices = () => {
  if (searchQuery.value) {
    services.value = filteredServices.value;
  } else {
    loadServices();
  }
};
</script>

<template>
    <div
        class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4 mb-2"
    >
        <h4>Available Services</h4>
        <form class="d-flex align-items-center" role="search" @submit.prevent>
          <input
          class="form-control me-2 form-control-sm"
          type="search"
          placeholder="Search by name, description, price or time"
          aria-label="Search"
          v-model="searchQuery"
          @input="filterServices"
          />
          <i class="pi pi-search"></i>
        </form>
    </div>
    <div v-if="services.length === 0" class="d-flex justify-content-center mt-4">
        <h4>No services found</h4>
    </div>
    
    <div class="row row-cols-1 row-cols-md-3 g-4 mb-5">
      <div v-for="service in services" :key="service.id" class="col">
        <div class="card h-100 card-btn" role="button" @click="handleServiceClick(service)" style="cursor: pointer;">
          <div class="card-body card-sm">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <ul class="list-unstyled">
              <li><strong>Base Price:</strong> ${{ service.base_price }}</li>
              <li><strong>Time Required:</strong> {{ service.time_required }} minutes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.card-btn {
  text-align: left;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s; /* Smooth transition for hover effects */
}

.card-btn:hover {
  transform: scale(1.03); /* Slight zoom effect on hover */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2); /* Add a shadow on hover */
}
</style>