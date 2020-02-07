<template>
    <div>
        <v-card outlined>

            <slot name="start" v-bind:resource="tile"></slot>

            <v-list-item three-line>
                
                <slot name="left" v-bind:resource="tile"></slot>

                <v-list-item-avatar v-if="tile.thumbnail_url" tile height="128" width="128">
                    <v-img :src="tile.thumbnail_url" />
                </v-list-item-avatar>
                <v-list-item-content>
                    <div class="overline mb-4">{{ tile.meta_title }}</div>
                    <v-list-item-title>{{ tile.title }}</v-list-item-title>
                    <v-list-item-subtitle>{{ tile.description }}</v-list-item-subtitle>
                </v-list-item-content>

                <v-list-item-action v-if="!newTab" class="right-action">
                    <v-btn text class="open primary right-action-btn" :to="routeTo"><v-icon>mdi-arrow-right</v-icon></v-btn>
                </v-list-item-action>

                <v-list-item-action v-if="newTab" class="right-action">
                    <v-btn text class="open right-action-btn" target="_blank" :to="routeTo"><v-icon>open_in_new</v-icon></v-btn>
                </v-list-item-action>
                
            </v-list-item>

            <slot name="end" v-bind:resource="tile"></slot>

        </v-card>
    </div>
</template>
<script>

import utils from '../../utils'

export default {
    props: {
        tile: Object,
        newTab: {type: Boolean, default: false},
    },
    computed: {
        routeTo() {
            return this.pathToString(this.tile.path)
        },
    },
    methods: {
        pathToString: utils.pathToString,
    },
}

</script>

<style lang="sass" scoped>

.right-action
    align-self: stretch
    .right-action-btn
        height: auto
        align-self: stretch
    



</style>
