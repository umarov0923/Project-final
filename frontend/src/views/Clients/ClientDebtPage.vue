<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';  // Импортируем useRoute
import api from '../../api/index';
import { useToast } from 'vue-toastification';


interface Debt {
  id: number;
  total_amount: string;
  remaining_amount: string;
  due_date: string;
  is_paid: boolean;
}

interface Client {
  id: string;
  name: string;
  balanse: string;
}


const client = ref<Client | null>(null); 
const debts = ref<Debt[]>([]);
const isLoading = ref(false);
const toast = useToast();
const formatNumber = (num: number | string) => 
  new Intl.NumberFormat('en-US').format(Number(num))

// Получаем clientId из маршрута
const route = useRoute();
const router = useRouter();
const clientId = route.params.id as string;  // Извлекаем clientId из параметра маршрута

// Поля формы создания долга
const newDebtAmount = ref('');
const newDebtDueDate = ref('');

// Логика создания нового долга
const createDebt = async () => {
  if (!newDebtAmount.value || !newDebtDueDate.value) {
    toast.error('Please fill in all fields');
    return;
  }

  try {
    await api.post('/debts/', {
      client: clientId,
      total_amount: newDebtAmount.value,
      due_date: newDebtDueDate.value,
    });
    toast.success('Debt created successfully');
    newDebtAmount.value = '';
    newDebtDueDate.value = '';
    fetchDebtsForClient(clientId); // обновляем список долгов
  } catch (error) {
    toast.error('Failed to create debt');
  }
};

// Загрузка долгов для выбранного клиента
const fetchDebtsForClient = async (clientId: string) => {
  if (!clientId) return;

  try {
    isLoading.value = true;
    const response = await api.get(`/clients/${clientId}/debts/`);
    client.value = response.data.client;  // Получаем информацию о клиенте
    debts.value = response.data.debts;
  } catch (error) {
    toast.error('Failed to load debts for the selected client');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchDebtsForClient(clientId);  // Загружаем долги для выбранного клиента
});
</script>

<template>
  <div class="client-debts-container">
    <!-- Header -->
    <div class="section-header">
      <h1>Долги клиента:{{ client?.name }}</h1>
      <p>Всего долгов: {{ formatNumber(client?.balanse || 0) }}</p>
    </div>
    <!-- Debt Creation Form -->
<div class="debt-creation-form">
  <h2>Создать новый долг</h2>
  <div class="form-group">
    <label>Сумма</label>
    <input type="number" v-model="newDebtAmount" placeholder="Введите сумму" />
  </div>
  <div class="form-group">
    <label>Срок до:</label>
    <input type="date" v-model="newDebtDueDate" />
  </div>
  <button @click="createDebt" class="create-debt-button">Create Debt</button>
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
              <span>Client:</span>
          
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
.debt-creation-form {
  background: #ffffff;
  padding: 2rem;
  border-radius: 1rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.debt-creation-form h2 {
  margin-bottom: 1.5rem;
  color: var(--dark-gray);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: var(--dark-gray);
}

.form-group input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid var(--light-gray);
  border-radius: 0.5rem;
  font-size: 1rem;
}

.create-debt-button {
  background-color: var(--primary-blue);
  color: white;
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 1rem;
  transition: background-color 0.3s ease;
}

.create-debt-button:hover {
  background-color: #2563eb;
}

.client-debts-container {
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
</style>
