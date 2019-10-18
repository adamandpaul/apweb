import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import ResourceViews from './resourceviews'

Vue.use(Vuetify, {
    iconfont: 'md',
})

const vuetify = new Vuetify()

export default {
    install() {
        Vue.use(ResourceViews)
    },
    vuetify,
}


