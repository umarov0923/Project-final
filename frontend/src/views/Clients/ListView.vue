<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import api from '../../api/index';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const router = useRouter();

interface Client {
  id: string;
  name: string;
  phone: string;
  balanse: string;
}

interface NewClient {
  name: string;
  phone: string;
}

const clients = ref<Client[]>([]);
const newClient = reactive<NewClient>({ name: '', phone: '' });
const isLoading = ref(false);
const isSubmitting = ref(false);
const toast = useToast();
const formatNumber = (num: number | string) => 
  new Intl.NumberFormat('en-US').format(Number(num))

const fetchClients = async () => {
  try {
    isLoading.value = true;
    const { data } = await api.get('/clients/');
    clients.value = data;
  } catch (error) {
    toast.error('Failed to fetch clients');
    console.error('Error fetching clients:', error);
  } finally {
    isLoading.value = false;
  }
};

const validateForm = (): boolean => {
  if (!newClient.name.trim()) {
    toast.error('Client name is required');
    return false;
  }
  
  if (!newClient.phone.trim()) {
    toast.error('Phone number is required');
    return false;
  }
  
  // Basic phone validation (could be enhanced with regex)
  if (newClient.phone.length > 13 && newClient.phone.length < 9) {
    toast.error('Please enter a valid phone number');
    return false;
  }
  
  return true;
};

const createClient = async () => {
  if (!validateForm()) return;
  
  try {
    isSubmitting.value = true;
    await api.post('/clients/', { name: newClient.name, phone: newClient.phone });
    
    // Clear form
    newClient.name = '';
    newClient.phone = '';
    
    // Refresh client list
    await fetchClients();
    
    toast.success('Client added successfully');
  } catch (error: any) {
    const errorMessage = error.response?.data?.message || 'Failed to create client';
    toast.error(errorMessage);
    console.error('Error creating client:', error);
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchClients);
</script>

<template>
  <div class="clients-container">
    <!-- Header -->
    <div class="clients-header">
      <h1>Управление клиентами</h1>
      <button class="refresh-button" @click="fetchClients" :disabled="isLoading">
        <svg class="refresh-icon" viewBox="0 0 24 24" :class="{ 'rotating': isLoading }">
          <path d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z"/>
        </svg>
        {{ isLoading ? 'Loading...' : 'Refresh' }}
      </button>
    </div>

    <!-- Add Client Form -->
    <div class="add-client-card">
      <h2>
        <svg class="user-plus-icon" viewBox="0 0 24 24">
          <path d="M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
        Добавить нового клиента
      </h2>
      
      <div class="client-form">
        <div class="form-grid">
          <div class="input-group">
            <label for="clientName">Имя</label>
            <input
              id="clientName"
              v-model.trim="newClient.name"
              placeholder="John Doe"
              class="styled-input"
              :class="{ 'input-error': newClient.name === '' }"
            >
          </div>
          <div class="input-group">
            <label for="clientPhone">Телефон</label>
            <input
              id="clientPhone"
              v-model.trim="newClient.phone"
              placeholder="+998 99 999 99 99"
              class="styled-input"
              :class="{ 'input-error': newClient.phone === '' }"
            >
          </div>
        </div>
        
        <button
          @click="createClient"
          :disabled="isSubmitting || (!newClient.name || !newClient.phone)"
          class="gradient-button submit-button"
        >
          <span v-if="isSubmitting" class="button-spinner"></span>
          <span>{{ isSubmitting ? 'Adding...' : 'Добавить клиента' }}</span>
        </button>
      </div>
    </div>

    <!-- Clients Grid -->
    <div class="clients-grid">
      <div v-if="isLoading" class="loading-skeleton">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <div v-else-if="clients.length === 0" class="no-clients">
        <svg class="no-data-icon" viewBox="0 0 24 24">
          <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
        </svg>
        <p>No clients found. Add your first client!</p>
      </div>

      <div v-else class="clients-list">
        <div 
          v-for="client in clients"
          :key="client.id"
          class="client-card"
          @click="() => router.push(`/clients/${client.id}/debt`)"
        >
          <div class="card-header">
            <div>
              <h3>{{ client.name }}</h3>
              <p>{{ client.phone }}</p>
            </div>
            <div class="client-id">
              ID: {{ client.id.slice(0,5) }}...
            </div>
          </div>
          
          <div class="card-balance">
            <span>Долг:</span>
            <span>{{ formatNumber(client.balanse) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
:root {
  --emerald-green: #10B981;
  --dark-emerald: #059669;
  --vibrant-blue: #2563EB;
  --electric-blue: #3B82F6;
  --light-gray: #F3F4F6;
  --medium-gray: #E5E7EB;
  --dark-gray: #374151;
  --red: #EF4444;
  --white: #FFFFFF;
}

.clients-container {
  min-height: 100vh;
  background-color: var(--light-gray);
  padding: 2rem;
  font-family: 'Segoe UI', sans-serif;
}

/* Header Styles */
.clients-header {
  max-width: 1200px;
  margin: 0 auto 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.clients-header h1 {
  font-size: 1.75rem;
  color: var(--dark-gray);
  font-weight: 700;
}

/* Refresh Button */
.refresh-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: var(--vibrant-blue);
  color: var(--white);
  border: none;
  border-radius: 0.6rem;
  padding: 0.6rem 1.2rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.9rem;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.15);
}

.refresh-button:hover:not(:disabled) {
  background-color: var(--electric-blue);
  transform: translateY(-1px);
  box-shadow: 0 3px 6px rgba(59, 130, 246, 0.25);
}

.refresh-icon {
  width: 1rem;
  height: 1rem;
  filter: brightness(0) invert(1);
}

.rotating {
  animation: spin 1s linear infinite;
}

/* Add Client Card */
.add-client-card {
  max-width: 1200px;
  margin: 0 auto 2rem;
  background: var(--white);
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.add-client-card h2 {
  font-size: 1.25rem;
  color: var(--dark-gray);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  justify-content: center;
}

.user-plus-icon {
  width: 1.25rem;
  height: 1.25rem;
  fill: var(--emerald-green);
}

/* Form Styles */
.client-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  align-items: center;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  width: 100%;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--dark-gray);
  font-size: 0.875rem;
  font-weight: 500;
}

.styled-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--medium-gray);
  border-radius: 0.75rem;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}

.styled-input:focus {
  border-color: var(--emerald-green);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

.input-error {
  border-color: var(--red);
}

.input-error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Main Action Button */
.gradient-button {
  background: linear-gradient(
    135deg,
    var(--emerald-green) 0%,
    var(--dark-emerald) 100%
  );
  color: var(--white);
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  font-weight: 600;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 auto;
  min-width: 160px;
  justify-content: center;
}

.gradient-button:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 3px 8px rgba(16, 185, 129, 0.3);
}

.button-spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: var(--white);
  animation: spin 1s linear infinite;
}

/* Clients Grid */
.clients-grid {
  max-width: 1200px;
  margin: 0 auto;
}

/* Client Cards */
.clients-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.client-card {
  background: var(--white);
  border-radius: 1rem;
  padding: 1.25rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  transition: transform 0.2s ease;
}

.client-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
}

.card-header h3 {
  font-size: 1.1rem;
  color: var(--dark-gray);
  margin-bottom: 0.25rem;
}

.card-header p {
  color: #6B7280;
  font-size: 0.875rem;
}

.client-id {
  background: var(--light-gray);
  padding: 0.375rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  color: var(--vibrant-blue);
  font-weight: 500;
}

.card-balance {
  border-top: 2px solid var(--medium-gray);
  padding-top: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-balance span:last-child {
  font-size: 1.1rem;
  color: var(--emerald-green);
  font-weight: 600;
}

/* Loading States */
.loading-skeleton {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.skeleton-card {
  background: var(--white);
  border-radius: 1rem;
  padding: 1.25rem;
  height: 120px;
  animation: pulse 2s infinite;
}

.no-clients {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: var(--white);
  border-radius: 1rem;
  padding: 2rem;
  text-align: center;
  color: var(--dark-gray);
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.no-data-icon {
  width: 2.5rem;
  height: 2.5rem;
  fill: var(--medium-gray);
  margin-bottom: 1rem;
}

/* Animations */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { background-color: rgba(243, 244, 246, 0.5); }
  50% { background-color: rgba(229, 231, 235, 0.5); }
}

/* Disabled States */
.gradient-button:disabled,
.refresh-button:disabled {
  background: var(--medium-gray);
  color: var(--dark-gray);
  box-shadow: none;
  transform: none;
  cursor: not-allowed;
  opacity: 0.7;
}

/* Mobile Responsive */
@media (max-width: 768px) {
  .clients-container {
    padding: 1.25rem;
  }
  
  .clients-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .refresh-button {
    width: 100%;
    justify-content: center;
    padding: 0.5rem;
  }
  
  .add-client-card {
    padding: 1rem;
  }
  
  .gradient-button {
    width: 100%;
    max-width: 200px;
    padding: 0.75rem;
    font-size: 0.9rem;
  }
  
  .no-clients {
    padding: 1.5rem;
  }
}
</style>