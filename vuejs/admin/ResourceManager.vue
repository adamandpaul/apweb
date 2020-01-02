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
            <div class="resource-header">
                <div class="container">
                    <div class="title">{{ title }}</div>
                    <div class="description">{{ description }}</div>
                </div>
            </div>
            <ViewManager class="view-manager" />
        </div>
    </div>
</template>
<script>

import ViewManager from './ViewManager.vue'
import {mapGetters} from 'vuex'

export default {

    components: {
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
        ]),
    },

}


</script>
<style lang="sass" scoped>

.container
    margin: 0 auto
    max-width: 980px


.resource-header
    background: #f5f5f5

</style>
