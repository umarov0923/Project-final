<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../../api/index';
import { useToast } from 'vue-toastification';
import { CurrencyDollarIcon, CreditCardIcon } from '@heroicons/vue/24/outline';

interface Payment {
  id: string;
  amount: string;
  debt: number;
  created_at: string;
  user: string;
}

interface Debt {
  id: number;
  client: string;
  total_amount: string;
}

const payments = ref<Payment[]>([]);
const debts = ref<Debt[]>([]);
const newPayment = ref({
  amount: '',
  debt: ''
});
const isLoading = ref(false);
const toast = useToast();

// Загрузка данных
const fetchData = async () => {
  try {
    isLoading.value = true;
    
    const [paymentsResponse, debtsResponse] = await Promise.all([
      api.get('/payments/'),
      api.get('/debts/')
    ]);
    
    payments.value = paymentsResponse.data;
    debts.value = debtsResponse.data;
  } catch (error) {
    toast.error('Failed to load data');
  } finally {
    isLoading.value = false;
  }
};

// Создание платежа
const createPayment = async () => {
  if (!newPayment.value.amount || !newPayment.value.debt) {
    toast.error('Please fill all fields');
    return;
  }

  try {
    await api.post('/payments/', {
      ...newPayment.value,
      amount: parseFloat(newPayment.value.amount)
    });
    
    await fetchData();
    newPayment.value = { amount: '', debt: '' };
    toast.success('Payment created successfully');
  } catch (error) {
    toast.error('Failed to create payment');
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="payments-container">
    <!-- Header -->
    <div class="section-header">
      <h1>
        <CreditCardIcon class="header-icon" />
        Управление оплатой
      </h1>
    </div>

    <!-- Add Payment Form -->
    <div class="form-card">
      <h2>
        <CurrencyDollarIcon class="form-icon" />
        Новый платеж
      </h2>
      
      <div class="form-grid">
        <div class="input-group">
          <label>Долг</label>
          <select 
            v-model="newPayment.debt"
            class="styled-select"
          >
            <option value="" disabled>Выберите долг</option>
            <option 
              v-for="debt in debts"
              :key="debt.id"
              :value="debt.id"
            >
              Debt #{{ debt.id }} (Client: {{ debt.client }})
            </option>
          </select>
        </div>
        
        <div class="input-group">
          <label>Сумма</label>
          <input
            v-model.number="newPayment.amount"
            type="number"
            min="0"
            step="0.01"
            placeholder="Введите сумму"
            class="styled-input"
          >
        </div>
      </div>
      
      <button
        @click="createPayment"
        class="gradient-button"
        :disabled="!newPayment.amount || !newPayment.debt"
      >
      Обработка платежа
      </button>
    </div>

    <!-- Payments List -->
    <div class="payments-list">
      <div v-if="isLoading" class="loading-skeleton">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <template v-else>
        <div 
          v-for="payment in payments"
          :key="payment.id"
          class="payment-card"
        >
          <div class="payment-header">
            <div class="payment-meta">
              <span class="payment-id">#{{ payment.id.slice(0,8) }}</span>
              <span class="payment-date">
                {{ new Date(payment.created_at).toLocaleDateString() }}
              </span>
            </div>
            <span class="payment-amount">
              {{ Number(payment.amount).toLocaleString(undefined, { minimumFractionDigits: 2 }) }}
            </span>
          </div>

          <div class="payment-body">
            <div class="debt-info">
              <span>Долг:</span>
              <span class="debt-id">
                #{{ payment.debt }}
              </span>
            </div>
            
            <div class="user-info">
              <span>Обработано:</span>
              <span class="user-id">
                {{ payment.user.slice(0,6) }}...
              </span>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>

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

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
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
.payments-container {
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
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.header-icon {
  width: 2rem;
  height: 2rem;
  color: var(--primary-blue);
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
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.form-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--primary-blue);
}

.payments-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.payment-card {
  background: #fff;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease;
}

.payment-card:hover {
  transform: translateY(-3px);
}

.payment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--light-gray);
}

.payment-meta {
  display: flex;
  flex-direction: column;
}

.payment-id {
  font-size: 0.9rem;
  color: var(--dark-gray);
  opacity: 0.7;
}

.payment-date {
  font-size: 0.85rem;
  color: var(--medium-gray);
}

.payment-amount {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--green);
}

.payment-body {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.debt-info, .user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.95rem;
}

.debt-id, .user-id {
  font-weight: 500;
  color: var(--primary-blue);
}

@media (max-width: 768px) {
  .payments-container {
    padding: 1rem;
  }

  .section-header h1 {
    font-size: 1.8rem;
  }

  .form-card {
    padding: 1.5rem;
  }

  .payment-card {
    padding: 1.2rem;
  }
  
  .payment-amount {
    font-size: 1.2rem;
  }
}
</style>