<template>
  <div>
    <h2>Create Invoice</h2>
    <div>
      <label>Customer ID:</label>
      <input type="number" v-model.number="form.customer_id" />
    </div>
    <div style="margin-top:10px;">
      <label>Notes:</label>
      <textarea v-model="form.notes" rows="3" style="width:100%"></textarea>
    </div>

    <h4 style="margin-top:10px;">Items</h4>
    <div v-for="(item, idx) in form.items" :key="idx" style="border:1px solid #ddd; padding:6px; margin-bottom:6px;">
      <div>
        <label>Product:</label>
        <select v-model.number="item.product_id">
          <option value="" disabled>Seçiniz</option>
          <option v-for="p in products" :key="p.id" :value="p.id">{{ p.name }}</option>
        </select>
      </div>
      <div>
        <label>Quantity:</label>
        <input type="number" min="1" v-model.number="item.quantity" />
      </div>
      <div>
        <label>Unit Price:</label>
        <input type="number" step="0.01" v-model.number="item.unit_price" />
      </div>
      <button @click="removeItem(idx)" style="margin-top:4px;">Remove item</button>
    </div>

    <button @click="addItem" style="margin-bottom:6px;">Add item</button>
    <div>
      <button @click="submit" style="margin-top:6px;">Create Invoice</button>
    </div>
  </div>
</template>

<script>
import api from '../api'

export default {
  data() {
    return {
      form: {
        customer_id: null,
        notes: '',
        items: [{ product_id: null, quantity: 1, unit_price: 0.0 }]
      },
      products: []  // dropdown ürünler için
    }
  },
  methods: {
    addItem() {
      this.form.items.push({ product_id: null, quantity: 1, unit_price: 0.0 })
    },
    removeItem(i) {
      this.form.items.splice(i, 1)
    },
    async fetchProducts() {
      try {
        const res = await api.get('products/')
        this.products = res.data
      } catch (e) {
        console.error(e)
        alert('Ürünleri çekerken hata oluştu')
      }
    },
    async submit() {
      if (!this.form.customer_id) return alert('Customer ID girilmeli')
      try {
        const payload = {
          customer_id: this.form.customer_id,
          notes: this.form.notes,
          items: this.form.items.map(it => ({
            product_id: it.product_id,
            quantity: it.quantity,
            unit_price: it.unit_price
          }))
        }
        const res = await api.post('invoices/', payload)
        alert('Fatura oluşturuldu: ID ' + res.data.id)
        // Formu sıfırla
        this.form = { customer_id: null, notes: '', items: [{ product_id: null, quantity: 1, unit_price: 0.0 }] }
      } catch (e) {
        console.error(e)
        alert('Fatura oluşturma hatası — konsolu kontrol et')
      }
    }
  },
  mounted() {
    this.fetchProducts()
  }
}
</script>
