
import TabOverview from './TabOverview.vue'
import TabSearch from './TabSearch.vue'
import TabContents from './TabContents.vue'
import TabAdd from './TabAdd.vue'
import TabEdit from './TabEdit.vue'
import TabApi from './TabApi.vue'
import Tile from './Tile.vue'
import CollectionBrowse from './CollectionBrowse.vue'
import CollectionSearchResults from './CollectionSearchResults.vue'
import CollectionAdd from './CollectionAdd.vue'

export default {
    install(Vue) {
        Vue.component('resource-tab-overview', TabOverview)
        Vue.component('resource-tab-search', TabSearch)
        Vue.component('resource-tab-contents', TabContents)
        Vue.component('resource-tab-add', TabAdd)
        Vue.component('resource-tab-edit', TabEdit)
        Vue.component('resource-tab-api', TabApi)
        Vue.component('resource-tile-default', Tile)
        Vue.component('collection-browse', CollectionBrowse)
        Vue.component('collection-search-results', CollectionSearchResults)
        Vue.component('collection-add', CollectionAdd)
    },
}
