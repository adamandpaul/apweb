<template>
    <div class="resource-manager">
        <div class="container">
            <div v-if="loading">
                Loading {{resourceURL}}...
            </div>
            <div v-else-if="error">
                Error...
            </div>
            <div v-else>
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

.resource-manager
    padding: 32px 16px

.container
    margin: 0 auto
    max-width: 980px

.view-manager
    margin-top: 32px

</style>
