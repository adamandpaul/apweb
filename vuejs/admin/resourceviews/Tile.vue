<template>
    <div>
        <v-card outlined>
            <v-card-text>
                <router-link :to="routeTo" >
                    <div class="row">
                        <img v-if="tile.thumbnail_url" :src="tile.thumbnail_url" />
                        <div>{{ tile.title }}</div>
                    </div>
                </router-link>
            </v-card-text>
        </v-card>
    </div>
</template>
<script>

import utils from '../../utils'

export default {
    props: {
        tile: Object,
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

img
    float: left
    width: 64px

</style>
