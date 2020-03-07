
import TabProperties from './TabProperties.vue'
import TabSimpleContent from './TabSimpleContent.vue'
import TabSearch from './TabSearch.vue'
import TabContents from './TabContents.vue'
import TabAdd from './TabAdd.vue'
import TabEdit from './TabEdit.vue'
import TabApi from './TabApi.vue'
import Tile from './Tile.vue'
import CollectionBrowse from './CollectionBrowse.vue'
import CollectionSearchResults from './CollectionSearchResults.vue'
import CollectionAdd from './CollectionAdd.vue'
import TabUserRoles from './TabUserRoles.vue'
import SelectFromCollection from './SelectFromCollection.vue'

export default {
    install(Vue) {
        Vue.component('resource-tab-properties', TabProperties)
        Vue.component('resource-tab-simple-content', TabSimpleContent)
        Vue.component('resource-tab-search', TabSearch)
        Vue.component('resource-tab-contents', TabContents)
        Vue.component('resource-tab-add', TabAdd)
        Vue.component('resource-tab-edit', TabEdit)
        Vue.component('resource-tab-api', TabApi)
        Vue.component('resource-tile', Tile)
        Vue.component('collection-browse', CollectionBrowse)
        Vue.component('collection-search-results', CollectionSearchResults)
        Vue.component('collection-add', CollectionAdd)
        Vue.component('select-from-collection', SelectFromCollection)
        Vue.component('resource-tab-user-roles', TabUserRoles)
    },
}
