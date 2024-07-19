<template>
    <div>
        <div class="resultDocumentsContainer" @scroll="handleScroll">
<!--            <CategoryFilter/>-->
            <div
                v-if="loadingResults && searchResults.length === 0"
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
                        <img alt="" :src="doc.icon ? doc.icon : ''">
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
            >Let's explore Tübingen</div>
            <div v-if="searchResults.length !== 0 && loadingResults">
                <v-progress-circular
                    indeterminate
                    size="64"
                    color="primary"
                />
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
        handleScroll(event) {
            const container = event.target;
            if (container.scrollTop + container.clientHeight >= container.scrollHeight - 500 && !this.loadingResults) {
                this.fetchMoreResults();
            }
        },
        fetchMoreResults() {
            if (!this.loadingResults && this.searchResults.length !== 0) {
                console.log("fetching more results: ", this.searchResults.length / 10);
                this.$emit('fetchMoreResults', this.searchResults.length / 10);
            }
        }
    }
}
</script>

<style lang="scss">
.resultDocumentsContainer {
    overflow: auto;
    color: rgb(var(--v-theme-font));
    padding: 2%;
    height: 100%;
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
