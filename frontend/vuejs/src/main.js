import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.js'

let app =createApp(App).mount('#app')
    app.use(router)
        app.mount('#app')
