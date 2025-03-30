<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from '@/utils/axios';
import { useToast } from 'vue-toastification';
import { formatDate } from '@/shared/formatDate';

const toast = useToast();
const serviceRequests = ref([]);

const review = ref({
  rating: null,
  comment: ''
});

const currentRequest = ref(null);

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

const filteredActiveRequests = computed(() => {
  let requests = serviceRequests.value
    .filter(request => request.status === 'requested' || request.status === 'accepted' || request.status === 'completed')
    .map(request => ({
      ...request,
      date_of_request: formatDate(request.date_of_request)
    }));

  if (activeSearchQuery.value) {
    const query = activeSearchQuery.value.toLowerCase();
    requests = requests.filter(request => 
      request.service.name.toLowerCase().includes(query) ||
      (request.professional?.name || '').toLowerCase().includes(query) ||
      request.customer_contact_number.toString().includes(query) ||
      request.status.toLowerCase().includes(query) ||
      request.date_of_request.toLowerCase().includes(query) ||
      request.address.toLowerCase().includes(query)
    );
  }

  return requests;
});

const filteredCompletedRequests = computed(() => {
  let requests = serviceRequests.value
    .filter(request => ['closed', 'rejected'].includes(request.status))
    .map(request => ({
      ...request,
      date_of_request: formatDate(request.date_of_request),
      date_of_completion: request.date_of_completion ? formatDate(request.date_of_completion) : '-'
    }));

  if (completedSearchQuery.value) {
    const query = completedSearchQuery.value.toLowerCase();
    requests = requests.filter(request =>
      request.service.name.toLowerCase().includes(query) ||
      (request.professional?.name || '').toLowerCase().includes(query) ||
      request.customer_contact_number.toString().includes(query) ||
      request.status.toLowerCase().includes(query) ||
      request.date_of_request.toLowerCase().includes(query) ||
      request.date_of_completion.toLowerCase().includes(query) ||
      request.address.toLowerCase().includes(query)
    );
  }

  return requests;
});

onMounted(() => {
  fetchServiceRequests();
});

const handleAction = async (requestId, action) => {
  try {
    await axios.patch(`/service-requests/${requestId}`, {
      status: action
    }); 
    toast.success(`Request ${action} successfully`);
    fetchServiceRequests();
  } catch (error) {
    console.error(error);
    toast.error(`Error ${action} request`);
  }
};

const handleReview = async (serviceRequest) => {
  try {
    await axios.post(`/reviews/${serviceRequest.id}`, {
      rating: review.value.rating,
      comment: review.value.comment,
    }); 
    toast.success('Review submitted successfully');
    fetchServiceRequests();
  } catch (error) {
    console.error(error);
    toast.error('Error submitting review');
  }
};

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
            placeholder="Search by service, professional, contact number, status, date or address"
            aria-label="Search"
            v-model="activeSearchQuery"
            />
            <i class="pi pi-search"></i>
          </form>
      </div>
      <div v-if="filteredActiveRequests.length === 0" class="text-center">
        <p>No active service requests found</p>
      </div>
      <table v-else class="table table-sm table-hover">
        <thead>
          <tr>
            <th>#</th>
            <th>Service</th>
            <th>Professional</th>
            <th>Contact Number</th>
            <th>Status</th>
            <th>Requested On</th>
            <th>Address</th>
            <th>Remarks</th>
            <th v-if="filteredActiveRequests.some(req => req.status === 'accepted' || req.status === 'completed')">Actions</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(request, index) in filteredActiveRequests" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ request.service.name }}</td>
            <td>{{ request.professional?.name }}</td>
            <td>{{ request.customer_contact_number }}</td>
            <td>
              <span :class="{
                'badge': true,
                'bg-warning text-dark': request.status === 'requested',
                'bg-success': request.status === 'accepted' || request.status === 'completed'
              }">
                {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
              </span>
            </td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.address }}</td>
            <td>{{ request.remarks || '-' }}</td>
            <td>
              <button
                v-if="request.status === 'accepted'"
                @click="handleAction(request.id, 'completed')"
                type="button"
                class="btn btn-success btn-sm"
              >
                Complete
                <span class="pi pi-check-circle ms-1"></span>
              </button>
              <button
                v-if="request.status === 'completed'"
                @click="currentRequest = request"
                type="button"
                class="btn btn-success btn-sm"
                data-bs-toggle="modal"
                data-bs-target="#reviewModal"
              > 
                Close
                <span class="pi pi-check-circle ms-1"></span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Rejected/Closed Requests -->
    <div>
      <div
          class="d-flex justify-content-between align-items-center px-4 gap-3 mt-4 mb-2"
      >
          <h4>Completed/Rejected Requests</h4>
          <form class="d-flex align-items-center" role="search" @submit.prevent>
            <input
            class="form-control me-2 form-control-sm"
            type="search"
            placeholder="Search by service, professional, contact number, status, date or address"
            aria-label="Search"
            v-model="completedSearchQuery"
            />
            <i class="pi pi-search"></i>
          </form>
      </div>
      <div v-if="filteredCompletedRequests.length === 0" class="text-center">
        <p>No service requests found</p>
      </div>
      <table v-else class="table table-sm table-hover">
        <thead>
          <tr>
            <th>#</th>
            <th>Service</th>
            <th>Professional</th>
            <th>Contact Number</th>
            <th>Status</th>
            <th>Requested On</th>
            <th>Completed On</th>
            <th>Address</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr v-for="(request, index) in filteredCompletedRequests" :key="index">
            <td>{{ index + 1 }}</td>
            <td>{{ request.service.name }}</td>
            <td>{{ request.professional?.name }}</td>
            <td>{{ request.customer_contact_number }}</td>
            <td>
              <span :class="{
                'badge': true,
                'bg-danger': request.status === 'rejected',
                'bg-success': request.status === 'closed'
              }">
                {{ request.status.charAt(0).toUpperCase() + request.status.slice(1) }}
              </span>
            </td>
            <td>{{ request.date_of_request }}</td>
            <td>{{ request.date_of_completion }}</td>
            <td>{{ request.address }}</td>
            <td>{{ request.remarks || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <!-- Review Modal -->
  <div class="modal fade" id="reviewModal" tabindex="-1" aria-labelledby="reviewModalLabel" aria-hidden="true" data-bs-backdrop="static">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="reviewModalLabel">Review Service & Payment</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="handleReview(currentRequest)">
            <h6 class="mb-3">Review</h6>
            <div class="mb-3">
              <label for="rating" class="form-label">Rating</label>
              <select class="form-select" id="rating" v-model="review.rating" required>
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3">3</option>
                <option value="4">4</option>
                <option value="5">5</option>
              </select>
            </div>
            <div class="mb-3">
              <label for="comment" class="form-label">Comment</label>
              <textarea class="form-control" id="comment" v-model="review.comment" required></textarea>
            </div>

            <hr>
            <h6 class="mb-3">Payment Details</h6>
            <div class="mb-3">
              <label for="cardNumber" class="form-label">Card Number</label>
              <input type="text" class="form-control" id="cardNumber" placeholder="1234 5678 9012 3456" required>
            </div>
            <div class="row mb-3">
              <div class="col">
                <label for="expiryDate" class="form-label">Expiry Date</label>
                <input type="text" class="form-control" id="expiryDate" placeholder="MM/YY" required>
              </div>
              <div class="col">
                <label for="cvv" class="form-label">CVV</label>
                <input type="text" class="form-control" id="cvv" placeholder="123" required>
              </div>
            </div>
            <div class="mb-3">
              <label for="cardName" class="form-label">Name on Card</label>
              <input type="text" class="form-control" id="cardName" placeholder="John Doe" required>
            </div>

            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Submit Review & Pay</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>