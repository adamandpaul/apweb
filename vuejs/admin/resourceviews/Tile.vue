<template>
    <div>
        <v-card outlined>

            <slot name="start" v-bind:resource="_tile" v-bind:resourceURL="resourceURL"></slot>

            <v-card-text class="grey lighten-5" v-if="_tile == null && resourceURL == null" >
                <slot name="no-resource">No resource</slot>
            </v-card-text>

            <v-list-item v-else three-line>

                <slot name="left" v-bind:resource="_tile" v-bind:resourceURL="resourceURL">
                    <v-list-item-action v-if="!newTab" class="left-action">
                        <v-btn text class="open primary right-action-btn" :to="routeTo"><v-icon>mdi-arrow-right</v-icon></v-btn>
                    </v-list-item-action> 
                </slot>

                <v-list-item-content v-if="loading">
                    <v-list-item-title>Loading {{ resourceURL }}...</v-list-item-title>
                </v-list-item-content>

                <v-list-item-content v-else-if="asyncError">
                    <v-list-item-title>Error loading {{ resourceURL }}.</v-list-item-title>
                </v-list-item-content>

                <template v-if="_tile != null">

                    <v-list-item-avatar v-if="_tile.thumbnail_url" tile height="128" width="128">
                        <v-img :src="_tile.thumbnail_url" />
                    </v-list-item-avatar>

                    <v-list-item-content>
                        <div class="overline mb-4">{{ _tile.meta_title }}</div>
                        <v-list-item-title>{{ _tile.title }}</v-list-item-title>
                        <v-list-item-subtitle>{{ _tile.description }}</v-list-item-subtitle>
                    </v-list-item-content>

                </template>
                
                <v-list-item-action v-if="newTab" class="right-action">
                    <v-btn text class="open right-action-btn" target="_blank" :to="routeTo"><v-icon>open_in_new</v-icon></v-btn>
                </v-list-item-action>

            </v-list-item>

            <slot name="end" v-bind:resource="_tile" v-bind:resourceURL="resourceURL"></slot>

        </v-card>
    </div>
</template>
<script>

import utils from '../../utils'

export default {

    props: {
        tile: {default: null},
        newTab: {type: Boolean, default: false},
        resourceURL: {type: String, default: null},
    },

    data() {
        return {
            asyncLoading: true,
            asyncError: null,
            asyncTile: null,
        }
    },

    watch: {
        resourceURL() {
            this.asyncLoad()
        },
    },

    computed: {
        routeTo() {
            if (this._tile) {
                return this.pathToString(this._tile.path)
            } else {
                return this.resourceURL
            }
        },
        loading() {
            return this.tile != null && this.asyncLoading;
        },
        _tile() {
            return this.tile || this.asyncTile;
        },
        resourceApi() {
            return this.$store.getters.resourceApiForResourceURL(this.resourceURL)
        },
    },

    methods: {

        pathToString: utils.pathToString,

        async asyncLoad() {

            // Clear current async response data
            this.asyncTile = null
            this.asyncError = null

            // if the new resourceURL is null then ensure that we are not loading
            if (this.resourceURL == null) {
                this.asyncLoading = false
                return
            }

            // load resource from server
            this.asyncLoading = true
            try {
                let resp = await this.resourceApi.get('@@admin-tile')
                this.asyncTile = resp.data.data
            } catch (err) {
                this.asyncError = err
            }
            this.asyncLoading = false

        }

    },

    mounted() {
        this.asyncLoad()
    },

}

</script>

<style lang="sass" scoped>

.right-action,
.left-action
    align-self: stretch
    .right-action-btn
        height: auto
        align-self: stretch
    



</style>
