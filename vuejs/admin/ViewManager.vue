<template>
    <div class="view-manager">

        <v-btn-toggle :value="selectedView" @change="change" rounded>
            <v-btn v-for="(view, idx) in viewsList" :key="idx" :value="view.name">{{ view.title }}</v-btn>
        </v-btn-toggle>

        <v-tabs-items class="tab-container" :value="selectedView">
            <v-tab-item v-for="(view, idx) in viewsList" :key="idx" :value="view.name">
                <AdminView :viewName="view.name" />
            </v-tab-item>
        </v-tabs-items>

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

.view-manager
    width: 100%
    display: flex
    flex-wrap: wrap
    justify-content: center

.tab-container
    width: 100%

</style>