<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '@/utils/axios';
import { useToast } from 'vue-toastification';
import { formatDate } from '@/shared/formatDate';

const toast = useToast();
const serviceRequests = ref([]);

const fetchServiceRequests = async () => {
  try {
    const response = await axios.get('/service-requests');
    serviceRequests.value = response.data;
  } catch (error) {
    console.error(error);
    toast.error('Error fetching service requests');
  }
};

const activeSearchQuery = ref('');
const completedSearchQuery = ref('');

const activeRequests = computed(() => {
  let requests = serviceRequests.value
    .filter(request => request.status === 'requested' || request.status === 'accepted')
    .map(request => ({
      ...request,
      date_of_request: formatDate(request.date_of_request)
    }));

  if (activeSearchQuery.value) {
    const query = activeSearchQuery.value.toLowerCase();
    requests = requests.filter(request =>
      request.customer.name.toLowerCase().includes(query) ||
      request.address.toLowerCase().includes(query) ||
      request.customer_contact_number.toString().includes(query) ||
      request.date_of_request.toLowerCase().includes(query)
    );
  }

  return requests;
});

const completedRequests = computed(() => {
  let requests = serviceRequests.value
    .filter(request => ['closed', 'rejected', 'completed'].includes(request.status))
    .map(request => ({
      ...request,
      date_of_request: formatDate(request.date_of_request),
      date_of_completion: request.date_of_completion ? formatDate(request.date_of_completion) : '-'
    }));

  if (completedSearchQuery.value) {
    const query = completedSearchQuery.value.toLowerCase();
    requests = requests.filter(request =>
      request.customer.name.toLowerCase().includes(query) ||
      request.address.toLowerCase().includes(query) ||
      request.customer_contact_number.toString().includes(query) ||
      request.date_of_request.toLowerCase().includes(query) ||
      request.date_of_completion.toLowerCase().includes(query) ||
      request.status.toLowerCase().includes(query)
    );
  }

  return requests;
});

const handleAction = async (requestId, action) => {
  try {
    await axios.patch(`/service-requests/${requestId}`, {
      status: action
    });
    toast.success(`Service request ${action} successfully`);
    fetchServiceRequests();
  } catch (error) {
    console.error(error);
    toast.error(`Error ${action} service request`);
  }
};

onMounted(() => {
  fetchServiceRequests();
});
</script>

<template>
  <div class="container mt-4">
    <!-- Active Requests -->
    <div class="mb-5">
        <div
          class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4 mb-2"
        >
          <h4>Active Service Requests</h4>
          <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
            class="form-control me-2 form-control-sm"
            type="search"
            placeholder="Search by name, address, contact number, status or date of request"
            aria-label="Search"
            v-model="activeSearchQuery"
            @input="filterServiceRequests"
            />
            <i class="pi pi-search"></i>
          </form>
      </div>
      <div v-if="activeRequests.length === 0" class="text-center">
        <p>No active service requests found</p>
      </div>
      <table v-else class="table table-sm table-hover">
        <thead>
          <tr>
            <th>#</th>
            <th>Customer</th>
            <th>Requested On</th>
            <th>Address</th>
            <th>Customer Contact</th>
            <th>Remarks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(request, index) in activeRequests" :key="request.id">
            <td>{{ index + 1 }}</td>
            <td>{{ request.customer.name }}</td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.address }}</td>
            <td>{{ request.customer_contact_number }}</td>
            <td>{{ request.remarks || '-' }}</td>
            <td>
              <div v-if="request.status === 'requested'" class="btn-group btn-group-sm">
                <button 
                  @click="handleAction(request.id, 'accepted')"
                  type="button"
                  class="btn btn-success btn-sm"
                >
                  Accept
                  <span class="pi pi-check-circle ms-1"></span>
                </button>
                <span class="mx-1"></span>
                <button 
                  @click="handleAction(request.id, 'rejected')"
                  type="button"
                  class="btn btn-danger btn-sm"
                >
                  Reject
                  <span class="pi pi-times-circle ms-1"></span>
                </button>
              </div>
              <div v-else-if="request.status === 'accepted'" class="btn-group btn-group-sm">
                <button 
                  @click="handleAction(request.id, 'completed')"
                  type="button"
                  class="btn btn-success btn-sm"
                >
                  Complete
                  <span class="pi pi-check-circle ms-1"></span>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Completed/Rejected Requests -->
    <div>
      <div
          class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4 mb-2"
      >
          <h4>Completed/Rejected Requests</h4>
          <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
            class="form-control me-2 form-control-sm"
            type="search"
            placeholder="Search by name, address, contact number, status, date of request or date of completion"
            aria-label="Search"
            v-model="completedSearchQuery"
            @input="filterCompletedServiceRequests"
            />
            <i class="pi pi-search"></i>
          </form>
      </div>
      <div v-if="completedRequests.length === 0" class="text-center">
        <p>No completed or rejected requests found</p>
      </div>
      <table v-else class="table table-sm table-hover">
        <thead>
          <tr>
            <th>#</th>
            <th>Customer</th>
            <th>Status</th>
            <th>Requested On</th>
            <th>Completed On</th>
            <th>Address</th>
            <th>Customer Contact</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(request, index) in completedRequests" :key="request.id">
            <td>{{ index + 1 }}</td>
            <td>{{ request.customer.name }}</td>
            <td>
              <span :class="{
                'badge': true,
                'bg-danger': request.status === 'rejected',
                'bg-success': request.status === 'closed' || request.status === 'completed'
              }">
                {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
              </span>
            </td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.date_of_completion }}</td>
            <td>{{ request.address }}</td>
            <td>{{ request.customer_contact_number }}</td>
            <td>{{ request.remarks || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
