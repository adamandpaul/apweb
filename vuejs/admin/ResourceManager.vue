<template>
    <div>
        <div v-if="loading">
            Loading {{resourceURL}}...
        </div>
        <div v-else-if="error">
            Error...
        </div>
        <div v-else>
            Content...
        </div>
    </div>
</template>
<script>

import {mapGetters} from 'vuex'

export default {

    computed: {
        ...mapGetters([
            'path',
            'loading',
            'error',
            'resourceURL',
        ]),
    },
}


</script>
