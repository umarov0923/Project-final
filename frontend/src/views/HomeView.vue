<template>
  <div class="dashboard">
    <main v-if="authStore.accessToken" class="main-content">
      <!-- Ключевые метрики -->
      <div class="metrics-grid">
        <div class="metric-card">
          <h3>Всего клиентов</h3>
          <div class="metric-value">{{ totalClients }}</div>
        </div>

        <div class="metric-card">
          <h3>Общий Долг</h3>
          <div class="metric-value">{{ formatNumber(totalBalance) }}</div>
        </div>

        <div class="metric-card">
          <h3>Средний Долг</h3>
          <div class="metric-value">{{ formatNumber(averageBalance) }}</div>
        </div>

        <div class="metric-card">
          <h3>Активные клиенты</h3>
          <div class="metric-value">{{ activeClients }}</div>
        </div>
      </div>

      <!-- Распределение баланса -->
      <div class="balance-distribution">
        <div class="section-header">
          <h3>Распределение баланса</h3>
          <div class="total-sum">
            Общий Долг: {{ formatNumber(totalBalance) }}
          </div>
        </div>

        <div class="client-list">
          <div 
            v-for="client in clientsWithBalance" 
            :key="client.id" 
            class="client-card"
          >
            <div class="client-info">
              <div class="avatar">
                {{ getInitials(client.name) }}
              </div>
              <div class="client-main">
                <div class="name-row">
                  <span class="client-name">{{ client.name }}</span>
                  <div class="client-balance">
                    {{ formatNumber(client.balance) }}
                  </div>
                </div>
                <div class="progress-container">
                  <div class="progress-bar">
                    <div 
                      class="progress-fill" 
                      :style="{ 
                        width: getBalancePercentage(client.balance) + '%' 
                      }"
                    ></div>
                  </div>
                  <div class="percentage-info">
                    <span class="percentage">
                      {{ getBalancePercentage(client.balance).toFixed(1) }}%
                    </span>
                    <span class="contribution">
                      Вклад в общий Долг
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/index'

const authStore = useAuthStore()

interface Client {
  id: string
  name: string
  balanse: string
}

// Состояния данных
const clients = ref<Client[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

// Загрузка данных
const loadData = async () => {
  try {
    loading.value = true
    const clientsRes = await api.get('/clients/')
    clients.value = clientsRes.data
  } catch (err) {
    error.value = 'Ошибка загрузки данных'
    console.error('Error loading data:', err)
  } finally {
    loading.value = false
  }
}

// Вычисляемые свойства
const totalClients = computed(() => clients.value.length)
const totalBalance = computed(() =>
  clients.value.reduce((sum, client) => sum + parseFloat(client.balanse), 0)
)
const averageBalance = computed(() =>
  totalClients.value > 0 ? totalBalance.value / totalClients.value : 0
)
const activeClients = computed(() =>
  clients.value.filter(client => parseFloat(client.balanse) > 0).length
)

const clientsWithBalance = computed(() => {
  return clients.value
    .map(client => ({
      ...client,
      balance: parseFloat(client.balanse)
    }))
    .filter(client => client.balance > 0)
    .sort((a, b) => b.balance - a.balance)
})

// Методы
const getBalancePercentage = (clientBalance: number) => {
  if (totalBalance.value <= 0) return 0
  return (clientBalance / totalBalance.value) * 100
}

const formatNumber = (num: number | string) => 
  new Intl.NumberFormat('en-US').format(Number(num))

const getInitials = (name: string) => {
  return name.split(' ')
    .map(part => part[0])
    .join('')
    .toUpperCase()
}

// Инициализация
onMounted(async () => {
  try {
    await authStore.fetchUser()
    if (authStore.user) {
      await loadData()
    }
  } catch (err) {
    error.value = 'Ошибка аутентификации'
    authStore.logout()
  }
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 32px;
}

.metric-card {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  text-align: center;
}

.metric-card h3 {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0 0 8px 0;
}

.metric-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1e293b;
}

.balance-distribution {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.section-header h3 {
  font-size: 1.25rem;
  color: #1e293b;
  margin: 0;
}

.total-sum {
  background: #f8fafc;
  color: #475569;
  padding: 8px 16px;
  border-radius: 6px;
  font-size: 0.95rem;
}

.client-list {
  display: grid;
  gap: 16px;
}

.client-card {
  padding: 16px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background: #fff;
}

.client-info {
  display: flex;
  align-items: center;
  gap: 16px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  background: #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 500;
  color: #475569;
  flex-shrink: 0;
}

.client-main {
  flex: 1;
  min-width: 0;
}

.name-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.client-name {
  font-weight: 500;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.client-balance {
  color: #10b981;
  font-weight: 500;
}

.progress-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #10b981;
  transition: width 0.3s ease;
}

.percentage-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.percentage {
  color: #10b981;
  font-weight: 500;
}

.contribution {
  color: #64748b;
  font-size: 0.9rem;
}

@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }

  .metrics-grid {
    grid-template-columns: 1fr 1fr;
    gap: 12px;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .metrics-grid {
    grid-template-columns: 1fr;
  }

  .client-info {
    gap: 12px;
  }

  .client-name {
    font-size: 0.95rem;
  }

  .client-balance {
    font-size: 0.9rem;
  }
}
</style>