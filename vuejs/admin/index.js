// Vuew + dependencies
import Vue from 'vue'
import Vuetify, {
    VFlex,
    VCard,
    VSubheader,
    VSlideYTransition,
    VLayout,
    VTextField,
    VTooltip,
    VIcon,
} from 'vuetify/lib'
import 'material-design-icons-iconfont/dist/material-design-icons.css'
import '@mdi/font/css/materialdesignicons.css'
import { Ripple } from 'vuetify/lib/directives'
import VJsonschemaForm from '@koumoul/vuetify-jsonschema-form'

// AP Web imports
import APWebStore from '../store'
import APWebSiteStore from '../site/store'

// Admin imports
import AdminStore from './store'
import AdminRoutes from './router'
import App from './App.vue'
import ResourceViews from './resourceviews'

// Configure Vue
Vue.config.productionTip = false

// Configure Vuetify
Vue.use(Vuetify, {
    iconfont: 'md',
    components: {
        VFlex,
        VCard,
        VSubheader,
        VSlideYTransition,
        VLayout,
        VTextField,
        VTooltip,
        VIcon,
    },
})
const vuetify = new Vuetify({})

// Configure JSON Schema Form
Vue.component('v-jsonschema-form', VJsonschemaForm)

// Configure Store
import Vuex from 'vuex'
Vue.use(Vuex)
const store = new Vuex.Store({
    modules: {
        apweb: APWebStore,
        site: APWebSiteStore,
        admin: AdminStore,
    }
})

// configure router
import VueRouter from 'vue-router'
Vue.use(VueRouter)
const router = new VueRouter({
    routes: AdminRoutes,
})

// configure admin
Vue.use(ResourceViews)


// Create Vue app
const app = new Vue({
    router,
    store,
    vuetify,
    render: h => h(App),
})
app.$mount('#app')
