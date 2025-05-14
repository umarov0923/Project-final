<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api/index';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const router = useRouter();

interface Debt {
  id: number;
  total_amount: string;
  remaining_amount: string;
  due_date: string;
  is_paid: boolean;
  client: string;
}

interface Client {
  id: string;
  name: string;
}

const debts = ref<Debt[]>([]);
  const filter = ref('all'); 
const clients = ref<Client[]>([]);
const newDebt = ref({
  client: '',
  total_amount: ''
});
const isLoading = ref(false);
const toast = useToast();
const formatNumber = (num: number | string) => 
  new Intl.NumberFormat('en-US').format(Number(num))

// Загрузка данных
const fetchData = async () => {
  try {
    isLoading.value = true;
    const params = { filter: filter.value };
    
    const [debtsResponse, clientsResponse] = await Promise.all([
      api.get('/debts/', { params: params }),
      api.get('/clients/')
    ]);
    
    debts.value = debtsResponse.data;
    clients.value = clientsResponse.data;
  } catch (error) {
    toast.error('Failed to load data');
  } finally {
    isLoading.value = false;
  }
};

// Создание нового долга
const createDebt = async () => {
  if (!newDebt.value.client || !newDebt.value.total_amount) {
    toast.error('Please fill all fields');
    return;
  }

  try {
    await api.post('/debts/', {
      ...newDebt.value,
      client: newDebt.value.client,  // отправляется только id клиента
      total_amount: parseFloat(newDebt.value.total_amount)
    }, {
      headers: {
        "Authorization": `Bearer ${localStorage.getItem('access')}`
      }
    });

    console.log('Debt created:', newDebt.value);
    
    
    await fetchData();
    newDebt.value = { client: '', total_amount: '' };
    toast.success('Debt created successfully');
  } catch (error) {
    toast.error('Failed to create debt');
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="debts-container">
    <div class="filter-container">
      <select v-model="filter" @change="fetchData" class="styled-select">
        <option value="all">Все долги</option>
        <option value="overdue">Просроченные долги</option>
      </select>
    </div>
    <!-- Header -->
    <div class="section-header">
      <h1>Управление долгом</h1>
    </div>

    <!-- Add Debt Form -->
    <div class="form-card">
      <h2>Создать новый долг</h2>
      
      <div class="form-grid">
        <div class="input-group">
          <label>Клиент</label>
          <select 
            v-model="newDebt.client"
            class="styled-select"
          >
            <option value="" disabled>Выберите клиента</option>
            <option 
              v-for="client in clients"
              :key="client.id"
              :value="client.id"
            >
              {{ client.name }}
            </option>
          </select>
        </div>
        
        <div class="input-group">
          <label>Cумма ()</label>
          <input
            v-model.number="newDebt.total_amount"
            type="number"
            min="10000"
            step="1000"
            placeholder="Введите сумму"
            class="styled-input"
          >
        </div>
      </div>
      
      <button
        @click="createDebt"
        class="gradient-button"
        :disabled="!newDebt.client || !newDebt.total_amount"
      >
      Создать долг
      </button>
    </div>

    <!-- Debts List -->
    <div class="debts-list">
      <div v-if="isLoading" class="loading-skeleton">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <template v-else>
        <div 
          v-for="debt in debts"
          :key="debt.id"
          class="debt-card"
          @click="() => router.push(`/debts/${debt.id}/payments`)"
          :class="{ paid: debt.is_paid }"
        >
          <div class="debt-header">
            <div class="status-indicator" :class="{ paid: debt.is_paid }"></div>
            <h3>Debt #{{ debt.id }}</h3>
            <span class="due-date">
              Срок: {{ new Date(debt.due_date).toLocaleDateString() }}
            </span>
          </div>

          <div class="debt-body">
            <div class="client-info">
              <span>Клиент:</span>
              <span class="client-name">
                {{ clients.find(c => c.id === debt.client)?.name || 'Unknown' }}
              </span>
            </div>
            
            <div class="amounts">
              <div class="amount-group">
                <span>Общий:</span>
                <span class="total-amount">
                  {{ formatNumber(debt.total_amount) }}
                </span>
              </div>
              <div class="amount-group">
                <span>Оставшийся:</span>
                <span class="remaining-amount">
                  {{ formatNumber(debt.remaining_amount) }}
                </span>
              </div>
            </div>
          </div>

          <div class="progress-bar">
            <div 
              class="progress-fill"
              :style="{ width: `${(1 - (+debt.remaining_amount / +debt.total_amount)) * 100}%` }"
            ></div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.debts-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 2rem;
}

.section-header h1 {
  font-size: 2.2rem;
  color: var(--dark-gray);
  margin-bottom: 0.5rem;
}

.form-card {
  background: #fff;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-card h2 {
  font-size: 1.4rem;
  color: var(--dark-gray);
  margin-bottom: 1.5rem;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.styled-select {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--medium-gray);
  border-radius: 0.75rem;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  background: var(--white);
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23374851' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1em;
}


.styled-select:focus {
  outline: none;
  border-color: var(--emerald-green);
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
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

.gradient-button {
  background: linear-gradient(135deg, var(--emerald-green) 0%, var(--dark-emerald) 100%);
  color: var(--white);
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 0.95rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(16, 185, 129, 0.2);
  display: block;
  margin: 1rem auto 0;
  min-width: 160px;
}

.debts-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.debt-card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
}

.debt-card:hover {
  transform: translateY(-3px);
}

.debt-card.paid {
  background: #f8fafc;
  opacity: 0.8;
}

.debt-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.2rem;
  position: relative;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #ef4444;
}

.status-indicator.paid {
  background: #10b981;
}

.due-date {
  margin-left: auto;
  font-size: 0.9rem;
  color: var(--dark-gray);
  opacity: 0.8;
}

.debt-body {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.client-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.client-name {
  font-weight: 600;
  color: var(--primary-blue);
}

.amounts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.amount-group {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.total-amount {
  font-weight: 700;
  color: var(--dark-gray);
}

.remaining-amount {
  font-weight: 700;
  color: #ef4444;
}

.progress-bar {
  height: 6px;
  background: var(--light-gray);
  border-radius: 3px;
  margin-top: 1.5rem;
}

.progress-fill {
  height: 100%;
  background: var(--primary-blue);
  border-radius: 3px;
  transition: width 0.5s ease;
}

/* Адаптивность */
@media (max-width: 768px) {
  .debts-container {
    padding: 1rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .debt-card {
    padding: 1.2rem;
  }
}
</style>