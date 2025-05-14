<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import { useToast } from 'vue-toastification';

const route = useRoute();
const toast = useToast();

const debtId = route.params.id as string;

interface Payment {
  id: string;
  amount: string; // Serialized as string (e.g., "820000.00")
  created_at: string;
  user_email: string;
}

interface Debt {
  id: number;
  total_amount: string; // Serialized as string (e.g., "850000.00")
  remaining_amount: string; // Serialized as string (e.g., "10000.00")
}

const payments = ref<Payment[]>([]);
const debt = ref<Debt | null>(null);
const newPaymentAmount = ref('');
const isLoading = ref(false);
const isSubmitting = ref(false);

// Fetch debt details and payments
const fetchDebtAndPayments = async () => {
  try {
    isLoading.value = true;

    // Fetch debt details
    const debtRes = await api.get(`/debts/${debtId}/`);
    debt.value = debtRes.data;

    // Fetch payments
    const paymentsRes = await api.get(`/debts/${debtId}/payments/`);
    payments.value = paymentsRes.data;
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || 'Failed to load debt or payments';
    toast.error(errorMessage);
  } finally {
    isLoading.value = false;
  }
};

// Create a new payment
const createPayment = async () => {
  const amount = parseFloat(newPaymentAmount.value);
  if (!newPaymentAmount.value || amount <= 0) {
    toast.error('Сумма платежа должна быть больше 0');
    return;
  }

  if (debt.value && amount > parseFloat(debt.value.remaining_amount)) {
    toast.error(`Сумма платежа (${amount}) превышает остаток долга (${debt.value.remaining_amount})`);
    return;
  }

  try {
    isSubmitting.value = true;
    await api.post('/payments/', {
      amount,
      debt: debtId,
    });
    toast.success('Платеж успешно добавлен');
    newPaymentAmount.value = '';
    await fetchDebtAndPayments(); // Refresh debt and payments
  } catch (err: any) {
    const errorMessage = err.response?.data?.detail || 'Не удалось создать платеж';
    toast.error(errorMessage);
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchDebtAndPayments);
</script>

<template>
  <div class="debt-payments-page">
    <div class="section-header">
      <h1>Платежи по долгу #{{ debtId }}</h1>
    </div>
    <p class="section-description" v-if="debt">
      Общая сумма долга: {{ Number(debt.total_amount).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) }} <br />
      Остаток долга: {{ Number(debt.remaining_amount).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) }} 
    </p>
    <p v-else class="section-description">Загрузка данных долга...</p>

    <!-- Add Payment Form -->
    <div class="form-card">
      <h2>Добавить новый платеж</h2>
      <input
        v-model="newPaymentAmount"
        type="number"
        placeholder="Введите сумму"
        min="0"
        step="0.01"
        class="styled-input"
      />
      <button
        class="gradient-button"
        @click="createPayment"
        :disabled="!newPaymentAmount || isSubmitting || parseFloat(newPaymentAmount) <= 0"
      >
        {{ isSubmitting ? 'Обработка...' : 'Добавить платеж' }}
      </button>
    </div>

    <!-- List of Payments -->
    <div class="payments-list">
      <div v-if="isLoading" class="loading-skeleton">
        <div v-for="i in 3" :key="i" class="skeleton-card"></div>
      </div>

      <template v-else-if="payments.length">
        <div v-for="payment in payments" :key="payment.id" class="payment-card">
          <div class="payment-header">
            <div>
              <span class="payment-id">#{{ payment.id.slice(0, 8) }}</span>
              <span class="payment-date">
                {{ new Date(payment.created_at).toLocaleDateString('ru-RU') }}
              </span>
            </div>
            <span class="payment-amount">
              {{ Number(payment.amount).toLocaleString('ru-RU', { minimumFractionDigits: 2 }) }} 
            </span>
          </div>
          <div class="payment-body">
            <span>Обработано пользователем: {{ payment.user_email }}...</span>
          </div>
        </div>
      </template>

      <p v-else>Платежи по этому долгу отсутствуют.</p>
    </div>
  </div>
</template>

<style scoped>
/* Existing styles unchanged */
.debt-payments-page {
  padding: 2rem;
  max-width: 1000px;
  margin: 0 auto;
}

.section-header {
  margin-bottom: 2rem;
  text-align: center;
}

.section-header h1 {
  font-size: 2rem;
  margin-bottom: 0.5rem;
  color: var(--dark-gray);
}

.section-description {
  font-size: 1.1rem;
  color: var(--medium-gray);
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-card {
  background: #fff;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-card h2 {
  font-size: 1.3rem;
  margin-bottom: 1rem;
}

.styled-input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid var(--medium-gray);
  border-radius: 0.75rem;
  font-size: 1rem;
  margin-bottom: 1rem;
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

.payments-list {
  display: grid;
  gap: 1rem;
}

.payment-card {
  background: #fff;
  border-radius: 1rem;
  padding: 1rem 1.5rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
}

.payment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.payment-id {
  font-weight: 500;
  color: var(--primary-blue);
}

.payment-date {
  font-size: 0.85rem;
  color: var(--medium-gray);
}

.payment-amount {
  font-size: 1.3rem;
  font-weight: bold;
  color: var(--green);
}
</style>