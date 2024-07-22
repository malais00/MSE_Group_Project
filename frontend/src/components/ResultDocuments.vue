<template>
    <div>
        <div class="resultDocumentsContainer" @scroll="handleScroll">
<!--            <CategoryFilter/>-->
            <div
                v-if="loadingResults && searchResults.length === 0 && !maxDocumentsReached"
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
                    <div class="percentileDiv"></div>
                    <div style="display: flex; flex-direction: row; align-items: center">
                        <div style="display: flex; flex-direction: column">
                            <div style="display: flex; flex-direction: row; align-items: center">
                                <v-icon v-if="doc.favicon === '' || doc.favicon === undefined">mdi-web</v-icon>
                                <img class="faviconDoc" alt="" :src="doc.favicon ? doc.favicon : ''">
                                <h2>{{ doc.title }}</h2>
                            </div>
                            <a style="width: fit-content" :href="doc.url">{{ doc.url }}</a>
                            <p>{{ getDocumentDescription(doc.url) }}</p>
                        </div>
                    </div>
                </div>
            </div>
            <div
                v-else
                class="readyInfo"
            >Let's explore Tübingen</div>
            <div v-if="searchResults.length !== 0 && loadingResults && !maxDocumentsReached">
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
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";

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
        },
        maxDocumentsReached: {
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
            if(this.maxDocumentsReached) {
                return;
            }
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
        },
        async getDocumentDescription(url) {
            const response = await request.getRequest("/query/"+query+"/"+index+"/okapi/"+b_okapi25_parameter+"/"+k1_okapi25_parameter+"/"+diversity_okapi25_parameter+"/"+fairness_okapi25_parameter+"/pagerank/"+pagerank_weight_parameter);
            if(await checkResponseStatus(200, response)) {
                const res = response.json();
                console.log(res);
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
    flex-direction: row;
    align-items: center;
    justify-content: flex-start;
    padding: 2vh 0;
}

.readyInfo {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 70vh;
    font-size: 2em;
}

.faviconDoc {
    width: 24px;
    height: 24px;
    margin-right: 8px
}

.percentileDiv {
    width: 12px;
    height: 48px;
    background: linear-gradient(to bottom, green, red);
    border-radius: 25px;
    border: 1px solid black;
}
</style>
