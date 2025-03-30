<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';
import axios from '@/utils/axios';
import { fetchServices } from '@/shared/fetchServices';
import BackButton from '@/components/BackButton.vue';

const route = useRoute();
const router = useRouter();
const toast = useToast();

const service = ref(null);
const professionals = ref([]);
const selectedProfessional = ref(null);
const address = ref('');
const remarks = ref('');
const contactNumber = ref('');

const loadServiceDetails = async () => {
  try {
    const services = await fetchServices();
    service.value = services.find(s => s.id === parseInt(route.params.id));
  } catch (error) {
    console.error('Error loading service details:', error);
    toast.error('Error loading service details');
  }
};

const loadProfessionals = async () => {
  try {
    const response = await axios.get(`/professionals`);
    professionals.value = response.data
      .filter(professional => professional.service.id === parseInt(route.params.id))
      .filter(professional => professional.status === 'approved')
      .sort((a, b) => b.rating - a.rating);
  } catch (error) {
    console.error('Error loading professionals:', error);
    toast.error('Error loading service professionals');
  }
};

const handleProfessionalSelection = (professionalId) => {
  selectedProfessional.value = professionals.value.find(prof => prof.id === professionalId);
};

const handleSubmit = async () => {
  if (!selectedProfessional.value || !address.value || !contactNumber.value) {
    toast.warning('Please select a professional, provide an address and contact number');
    return;
  }

  try {
    await axios.post('/service-requests', {
      service_id: service.value.id,
      professional_id: selectedProfessional.value.id,
      address: address.value,
      remarks: remarks.value || '',
      customer_contact_number: contactNumber.value,
    });
    toast.success('Service request created successfully');
    router.push({ name: 'CustomerServiceRequests' });
  } catch (error) {
    console.error('Error creating service request:', error);
    toast.error('Error creating service request');
  }
};

onMounted(() => {
  loadServiceDetails();
  loadProfessionals();
});

const searchQuery = ref('');
const filteredProfessionals = computed(() => {
  return professionals.value.filter(prof => 
    prof.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    prof.description.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    prof.service_pincodes.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    prof.rating.toString().includes(searchQuery.value)
  );
});

const filterProfessionals = () => {
  if (searchQuery.value) {
    professionals.value = filteredProfessionals.value;
  } else {
    loadProfessionals();
  }
};

</script>

<template>
  <BackButton to="/customer-dashboard/available-services" text="Back to Available Services" />
  
  <div class="container mt-4">
    <div v-if="service" class="row">
      <div class="col-md-4">
        <div class="card">
          <div class="card-body">
            <h4 class="card-title">{{ service.name }}</h4>
            <p class="card-text">{{ service.description }}</p>
            <ul class="list-unstyled">
              <li><strong>Base Price:</strong> ${{ service.base_price }}</li>
              <li><strong>Time Required:</strong> {{ service.time_required }} minutes</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="card">
          <div class="card-body">
            <div
                class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4 mb-2"
            >
                <h4>Available Professionals</h4>
                <form class="d-flex align-items-center" role="search" @submit.prevent>
                    <input
                        class="form-control me-2 form-control-sm"
                        type="search"
                        placeholder="Search by name, description, pincode or rating"
                        aria-label="Search"
                        v-model="searchQuery"
                        @input="filterProfessionals"
                    />
                    <i class="pi pi-search"></i>
                </form>
            </div>
            <div v-if="professionals.length > 0" class="table-responsive">
              <table class="table table-sm">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Service Description</th>
                    <th>Service Pincodes</th>
                    <th>Rating</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="prof in professionals" :key="prof.id">
                    <td>{{ prof.name }}</td>
                    <td>{{ prof.description }}</td>
                    <td>{{ prof.service_pincodes }}</td>
                    <td>{{ prof.rating || 'N/A' }}</td>
                    <td>
                      <button 
                        class="btn btn-primary btn-sm"
                        @click="handleProfessionalSelection(prof.id)"
                        data-bs-toggle="modal" 
                        data-bs-target="#bookingModal"
                      >
                        Book Now
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div v-else class="text-center">
              <p>No professionals available</p>
            </div>

            <!-- Booking Modal -->
            <div class="modal fade" id="bookingModal" tabindex="-1">
              <div class="modal-dialog">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title">Complete Booking</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                  </div>
                  <div class="modal-body text-center">
                    <form @submit.prevent="handleSubmit">
                      <div class="mb-3">
                        <label class="form-label">Service Address</label>
                        <textarea v-model="address" class="form-control" rows="3" required></textarea>
                      </div>

                      <div class="mb-3">
                        <label class="form-label">Additional Remarks</label>
                        <textarea v-model="remarks" class="form-control" rows="2"></textarea>
                      </div>

                      <div class="mb-3">
                        <label class="form-label">Contact Number</label>
                        <input type="tel" v-model="contactNumber" class="form-control" required>
                      </div>

                      <button 
                        type="submit" 
                        class="btn btn-primary"
                        data-bs-dismiss="modal"
                      >
                        Confirm Booking
                      </button>
                    </form>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center mt-4">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  </div>
</template>
