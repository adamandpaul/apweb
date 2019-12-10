
import TabOverview from './TabOverview.vue'
import TabSearch from './TabSearch.vue'
import TabContents from './TabContents.vue'
import TabAdd from './TabAdd.vue'
import TabEdit from './TabEdit.vue'
import TabApiGet from './TabApiGet.vue'
import Tile from './Tile.vue'

export default {
    install(Vue) {
        Vue.component('resource-tab-overview', TabOverview)
        Vue.component('resource-tab-search', TabSearch)
        Vue.component('resource-tab-contents', TabContents)
        Vue.component('resource-tab-add', TabAdd)
        Vue.component('resource-tab-edit', TabEdit)
        Vue.component('resource-tab-api', TabApiGet)
        Vue.component('resource-tile', Tile)
    },
}
