import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import App from './App.vue'
import router from './router'
import en from './i18n/en.json'
import es from './i18n/es.json'
import './assets/styles.css'

const i18n = createI18n({
    legacy: false,
    locale: localStorage.getItem('language') || 'en',
    fallbackLocale: 'en',
    messages: { en, es }
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(i18n)
app.mount('#app')
