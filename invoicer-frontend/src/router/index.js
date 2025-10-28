import { createRouter, createWebHistory } from 'vue-router'
import InvoiceList from '../components/InvoiceList.vue'
import InvoiceForm from '../components/InvoiceForm.vue'

const routes = [
  { path: '/', redirect: '/invoices' },
  { path: '/invoices', component: InvoiceList },
  { path: '/create-invoice', component: InvoiceForm }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
