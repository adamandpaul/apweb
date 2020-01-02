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
            <div class="container">
                <div class="description">{{ description }}</div>
                <ViewManager class="view-manager" />
            </div>
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
            'description',
        ]),
    },

}


</script>
<style lang="sass" scoped>

.container
    margin: 0 auto
    max-width: 980px

.view-manager
    margin-top: 32px

</style>
