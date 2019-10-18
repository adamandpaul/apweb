<template>
    <div class="view-manager">
        <v-tabs>
            <v-tabs-slider></v-tabs-slider>

            <v-tab v-for="(view, idx) in viewsList" :key="idx">{{ view.title }}</v-tab>
            <v-tab-item v-for="(view, idx) in viewsList" :key="idx">
                <v-card flat tile>
                    <v-card-text>
                        <AdminView :viewName="view.name" />
                    </v-card-text>
                </v-card>
            </v-tab-item>

        </v-tabs>
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
            'viewsList',
        ]),
    }
}
</script>
