
import TabOverview from './TabOverview.vue'
import TabAdd from './TabAdd.vue'
import Tile from './Tile.vue'

export default {
    install(Vue) {
        Vue.component('resource-tab-overview', TabOverview)
        Vue.component('resource-tab-add', TabAdd)
        Vue.component('resource-tile', Tile)
    },
}
