<template>
  <div>
    <h2>Invoices</h2>
    <div v-if="loading">Yükleniyor...</div>
    <div v-else>
      <button @click="exportPDF" style="margin-bottom:10px;">Export PDF</button>
      <div id="invoice-table">
        <table border="1" cellpadding="6" cellspacing="0" style="width:100%; border-collapse:collapse;">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer</th>
              <th>Date</th>
              <th>Total</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="invoice in invoices" :key="invoice.id">
              <td>{{ invoice.id }}</td>
              <td>{{ invoice.customer?.name || '-' }}</td>
              <td>{{ invoice.date }}</td>
              <td>{{ calculateTotal(invoice) }}</td>
            </tr>
          </tbody>
        </table>
        <div v-if="invoices.length===0" style="margin-top:10px">Henüz fatura yok.</div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../api'
import html2pdf from 'html2pdf.js'

export default {
  data() {
    return {
      invoices: [],
      loading: true
    }
  },
  methods: {
    async fetchInvoices() {
      this.loading = true
      try {
        const res = await api.get('invoices/')
        this.invoices = res.data
      } catch (e) {
        console.error(e)
        alert('Fatura çekme hatası — konsolu kontrol et')
      } finally {
        this.loading = false
      }
    },
    calculateTotal(invoice) {
      if (!invoice.items) return 0
      return invoice.items.reduce((sum, item) => sum + (item.quantity * item.unit_price), 0).toFixed(2)
    },
    exportPDF() {
      const element = document.getElementById('invoice-table')
      html2pdf().from(element).save('invoices.pdf')
    }
  },
  mounted() {
    this.fetchInvoices()
  }
}
</script>
