// Vuew + dependencies
import Vue from 'vue'
import Vuetify, {
    VApp,
    VAlert,
    VProgressLinear,
    VBtnToggle,
    VBtn,
    VTabsItems,
    VTabItem,
    VForm,
    VCardTitle,
    VCardText,
    VCardActions,
    VDataTable,
    VDialog,
    VFlex,
    VCard,
    VCheckbox,
    VSubheader,
    VSlideYTransition,
    VLayout,
    VTextField,
    VTextarea,
    VTooltip,
    VToolbar,
    VToolbarItems,
    VImg,
    VIcon,
    VList,
    VListItem,
    VListItemGroup,
    VListItemTitle,
    VListItemSubtitle,
    VListItemContent,
    VListItemAction,
    VListItemAvatar,
    VSpacer,
    VSelect,
    VMenu,
    VExpansionPanels,
    VExpansionPanel,
    VExpansionPanelHeader,
    VExpansionPanelContent,
    VFileInput,
    VProgressCircular,
    VInput,
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
import RequestError from './RequestError'
import App from './App.vue'
import ResourceViews from './resourceviews'

// Configure Vue
Vue.config.productionTip = false

// Configure Vuetify
Vue.use(Vuetify, {
    iconfont: 'md',
    components: {
        VApp,
        VAlert,
        VProgressLinear,
        VBtnToggle,
        VBtn,
        VTabsItems,
        VTabItem,
        VForm,
        VCardTitle,
        VCardText,
        VCardActions,
        VCheckbox,
        VDataTable,
        VDialog,
        VFlex,
        VCard,
        VSubheader,
        VSlideYTransition,
        VLayout,
        VTextField,
        VTextarea,
        VTooltip,
        VToolbar,
        VToolbarItems,
        VIcon,
        VImg,
        VList,
        VListItem,
        VListItemGroup,
        VListItemTitle,
        VListItemSubtitle,
        VListItemContent,
        VListItemAction,
        VListItemAvatar,
        VSpacer,
        VSelect,
        VMenu,
        VExpansionPanels,
        VExpansionPanel,
        VExpansionPanelHeader,
        VExpansionPanelContent,
        VFileInput,
        VProgressCircular,
        VInput,
    },
})
const vuetify = new Vuetify({})

// Configure request-error component
Vue.component("request-error", RequestError)

// Configure JSON Schema Form
import './vutify-jsonschema-form'
//Vue.component('v-jsonschema-form', VJsonschemaForm)

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
    props: {
        apiBaseURL: {
            type: String,
            default: "/api/",
        },
    },
    router,
    store,
    vuetify,
    render: h => h(App),
})

export default app
