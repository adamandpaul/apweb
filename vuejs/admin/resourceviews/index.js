
import ResourceInfo from './ResourceInfo.vue'
import AddChild from './AddChild.vue'
import TileResource from './TileResource.vue'

export default {
    install(Vue) {
        Vue.component('view-resource-info', ResourceInfo)
        Vue.component('view-add-child', AddChild)
        Vue.component('tile-resource', TileResource)
    },
}

