<template>
    <div class="resource-manager">
        <div v-if="loading">
            <v-progress-linear indeterminate/>
            <div class="container loading">Loading {{resourceURL}}...</div>
        </div>
        <div v-else-if="error">
            <div class="container">
                <request-error :error="error" />
            </div>
        </div>
        <div v-else>
            <ResourceHeader />
            <ViewManager class="view-manager" />
        </div>
    </div>
</template>
<script>

import ResourceHeader from './ResourceHeader.vue'
import ViewManager from './ViewManager.vue'
import {mapGetters} from 'vuex'

export default {

    components: {
        ResourceHeader,
        ViewManager,
    },

    computed: {
        ...mapGetters([
            'path',
            'loading',
            'error',
            'resourceURL',
            'title',
            'description',
            'thumbnail_url',
        ]),
    },

}


</script>
<style lang="sass" scoped>

.container
    margin: 0 auto
    max-width: 980px

</style>
