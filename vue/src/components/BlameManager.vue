<template>
    <form>
        <label>Repo URL
            <input name="repo_url" type="text" v-model="repo_url"/>
        </label>
    </form>
</template>

<script>
    export default {
        name: 'BlameManager',
    }
</script>