<template>
    <div>
        <div class="resultDocumentsContainer">
            <CategoryFilter/>
            <div
                v-if="loadingResults"
                class="readyInfo"
            >
                <v-progress-circular
                    indeterminate
                    size="64"
                    color="primary"
                />
            </div>
            <div
                v-else-if="searchResults.length !== 0"
                v-for="doc in searchResults"
            >
                <div class="docContainer">
                    <div style="display: flex; flex-direction: row; align-items: center">
<!--                        <v-icon size="x-large" style="margin-right: 16px">{{ doc.icon }}</v-icon>-->
                        <img :src="'https://uni-tuebingen.de/typo3conf/ext/project/Resources/Public/Images/favicon.ico'">
                        <div style="display: flex; flex-direction: column">
                            <h2>{{ doc.title }}</h2>
                            <a style="width: fit-content" :href="doc.url">{{ doc.url }}</a>
                            <p>{{ doc.preview }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div
                v-else
                class="readyInfo"
            >Ready when you are</div>
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
        },
        loadingResults: {
            type: Boolean,
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

.readyInfo {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
    font-size: 2em;
}
</style>
