<template>
    <div class="view-manager">

        <div class="tab-buttons-container">
            <v-btn-toggle class="tab-buttons" :value="selectedView" @change="change" rounded>
                <v-btn v-for="(view, idx) in viewsList" :key="idx" :value="view.name">{{ view.title }}</v-btn>
            </v-btn-toggle>
        </div>

        <div class="container">
            <v-tabs-items class="tab-container" :value="selectedView">
                <v-tab-item v-for="(view, idx) in viewsList" :key="idx" :value="view.name">
                    <AdminView :viewName="view.name" />
                </v-tab-item>
            </v-tabs-items>
        </div>

    </div>
</template>
<script>

import AdminView from './View.vue'
import {mapGetters} from 'vuex'

export default {

    components: {
        AdminView,
    },

    computed: {
        ...mapGetters([
            'selectedView',
            'viewsList',
        ]),

    },

    methods: {
        change(value) {
           this.$router.push({query: {"view": value}})
        },
    },

}
</script>

<style lang="sass" scoped>

.container
    margin: 0 auto
    max-width: 980px

.tab-buttons-container
    width: 100%
    display: flex
    flex-wrap: wrap
    justify-content: center

    background: #f5f5f5
    background-image: linear-gradient(#f5f5f5 50%, white 50%)
</style>