<template>
    <div>
        <SearchResults :query="{}" api="@@admin-search" />
    </div>
</template>
<script>

import SearchResults from './SearchResults.vue'

export default {

    components: {
        SearchResults,
    },

}

</script>
