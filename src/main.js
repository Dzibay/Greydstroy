import { createApp } from 'vue'
import App from './App.vue'
import { reveal } from './directives/reveal'
import './styles/main.css'

const app = createApp(App)
app.directive('reveal', reveal)
app.mount('#app')
