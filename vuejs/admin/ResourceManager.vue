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
                    <div v-if="thumbnail_url" class="thumbnail">
                        <img :src="thumbnail_url" />
                    </div>
                    <div class="details">
                        <div class="title">{{ title }}</div>
                        <div class="description">{{ description }}</div>
                    </div>
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
            'thumbnail_url',
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

    .container
        padding: 32px 0
        display: flex
        align-items: center

    .thumbnail
        background: white
        padding: 8px
        border-radius: 5px
        margin-right: 24px
        box-shadow: 3px 3px 6px 0px rgba(0,0,0,0.08)

        img
            display: block
            width: 128px

</style>
