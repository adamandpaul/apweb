<template>
    <collection-search-results :query="{}" :resourceURL="resourceURL" />
</template>
<script>

export default {
    props: {
        resourceURL: {type: String, default: null},
    },
}

</script>
