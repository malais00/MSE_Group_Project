<template>
    <div>
        <div class="resultDocumentsContainer">
            <CategoryFilter/>
            <div
                v-for="doc in searchResults"
            >
                <div class="docContainer">
                    <div style="display: flex; flex-direction: row; align-items: center">
                        <v-icon size="x-large" style="margin-right: 16px">{{ doc.icon }}</v-icon>
                        <div style="display: flex; flex-direction: column">
                            <h2>{{ doc.title }}</h2>
                            <a style="width: fit-content" :href="doc.url">{{ doc.url }}</a>
                            <p>{{ doc.preview }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CategoryFilter from "@/components/CategoryFilter.vue";

export default {
    name: "ResultDocuments",
    components: {CategoryFilter},
    props: {
        searchResults: {
            type: Array,
            required: true
        }
    },
    data() {
        return {

        };
    },
    methods: {

    }
}
</script>

<style lang="scss">
.resultDocumentsContainer {
    overflow: scroll;
    color: rgb(var(--v-theme-font));
    padding: 2%;
}

.docContainer {
    display: flex;
    flex-direction: column;
    padding: 2vh 0;
}
</style>
