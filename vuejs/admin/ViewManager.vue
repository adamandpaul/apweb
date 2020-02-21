<template>
    <div class="view-manager">

        <div class="tab-buttons-container">
            <v-btn-toggle class="tab-buttons" :value="selectedView" @change="change" rounded>
                <v-btn value="default"><v-icon>{{ mdiCubeOutline }}</v-icon></v-btn>
                <v-btn v-for="(view, idx) in tabViews" :key="idx" :value="view.name">{{ view.title }}</v-btn>
                <v-btn v-if="secondaryViews.length > 0" value="secondaryViews"><v-icon>{{ mdiDotsVertical }}</v-icon></v-btn>
            </v-btn-toggle>
        </div>

        <div class="container">
            <v-tabs-items class="tab-container" :value="selectedView">
                <v-tab-item value="default">
                    <v-card class="resource-links" flat v-if="links.length > 0 || namedResources.length > 0">
                        <v-card-text>
                            <ResourceMenu
                                :items="namedResources" />
                            <ResourceLinkMenu
                                :items="links" />
                        </v-card-text>
                    </v-card>
                    <div v-for="(view, idx) in defaultViews" :key="idx">
                        <AdminView :view="view" />
                    </div>
                    <v-card v-if="defaultViews.length == 0">
                        <v-card-title class="grey lighten-2 text-center">
                            <span class="shrug">¯\_(ツ)_/¯</span>
                        </v-card-title>
                        <v-card-title class="grey--text">
                            No default view defined for this resource
                        </v-card-title>
                    </v-card>
                </v-tab-item>
                <v-tab-item v-for="(view, idx) in tabViews" :key="idx" :value="view.name">
                    <AdminView :view="view" />
                </v-tab-item>
                <v-tab-item v-if="secondaryViews.length > 0" value="secondaryViews">
                    <div v-for="(view, idx) in secondaryViews" :key="idx">
                        <hr v-if="idx != 0" />
                        <div class="title">{{ view.title }}</div>
                        <AdminView :view="view" />
                    </div>
                </v-tab-item>
            </v-tabs-items>
        </div>

    </div>
</template>
<script>

import AdminView from './View.vue'
import {mapGetters} from 'vuex'
import { mdiCubeOutline } from '@mdi/js';
import { mdiDotsVertical } from '@mdi/js';
import ResourceMenu from './ResourceMenu.vue'
import ResourceLinkMenu from './ResourceLinkMenu.vue'

export default {

    data() {
      return {
          mdiCubeOutline,
          mdiDotsVertical,
      }  
    },

    components: {
        AdminView,
        ResourceMenu,
        ResourceLinkMenu,
    },

    computed: {
        ...mapGetters([
            'selectedView',
            'viewsList',
            'namedResources',
            'links',
        ]),

        defaultViews() {
            const views = []
            for (const v of this.viewsList) {
                if (v.default) {
                    views.push(v)
                }
            }
            return views
        },

        tabViews() {
            const views = []
            for (const v of this.viewsList) {
                if (!v.secondary && !v.default) {
                    views.push(v)
                }
            }
            return views
        },

        secondaryViews() {
            const views = []
            for (const v of this.viewsList) {
                if (v.secondary) {
                    views.push(v)
                }
            }
            return views
        },

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


.resource-links
    margin-top: 25px


.shrug 
    display: block
    margin: 0 auto
    text-align: center
    font-size: 25px
</style>