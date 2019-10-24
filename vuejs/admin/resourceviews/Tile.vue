<template>
    <div>
        <v-card outlined>
            <v-card-text>
                <router-link :to="routeTo" >{{ tile.title }}</router-link>
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
