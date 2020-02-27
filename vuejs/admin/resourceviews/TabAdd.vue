<template>
    <collection-add :schema="schema" :resourceURL="resourceURL" :newTab="false" />
</template>
<script>

import {mapGetters} from 'vuex'

export default {

    props: {
        data: {type: Object, default: null},
        options: {type: Object, default: null},
        resourceURL: {type: String, default: null},
    },

    computed: {
        schema() {
            return this.data || this.options.schema
        }
    },

}
</script>
