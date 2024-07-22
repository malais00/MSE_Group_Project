<template>
    <v-app>
        <Header
            @search-query="(query, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter) =>
            searchQuery(query, 0, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter, true)"
            @show-spellchecker="showSpellchecker = true"
            @hide-spellchecker="showSpellchecker = false"
            :show-spellchecker="showSpellchecker"
            :corrected-query="correctedQuery"
        />

        <v-main>
            <ResultDocuments
                :searchResults="searchResults"
                :loading-results="loadingResults"
                :maxDocumentsReached="maxDocumentsReached"
                :current-query="currentQueryReadOnly"
                class="resultDocuments"
                @fetchMoreResults="(index) => searchQuery(currentQueryReadOnly, index, b_okapi25_parameterReadOnly, k1_okapi25_parameterReadOnly, diversity_okapi25_parameterReadOnly, fairness_okapi25_parameterReadOnly, pagerank_weight_parameterReadOnly, false)"
            />
        </v-main>

        <AppFooter class="footer"/>
        <v-snackbar
            v-model="snackbarActivator"
            bottom
            timeout="5000"
            :color="snackbarColor"
            style="bottom: 9vh"
        >{{ snackbarText }}</v-snackbar>
    </v-app>
</template>

<script>
import ResultDocuments from "@/components/ResultDocuments";
import Header from "@/components/Header";
import AppFooter from "@/components/AppFooter";
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";

export default {
    name: "App",
    data() {
        return {
            ResultDocuments,
            Header,
            AppFooter,
            loadingResults: false,
            searchResults: [],
            currentQueryReadOnly: '',
            b_okapi25_parameterReadOnly: 0.0,
            k1_okapi25_parameterReadOnly: 0.0,
            diversity_okapi25_parameterReadOnly: 0.0,
            fairness_okapi25_parameterReadOnly: 0.0,
            pagerank_weight_parameterReadOnly: 0.0,
            snackbarActivator: false,
            snackbarText: '',
            snackbarColor: 'error',
            showSpellchecker: false,
            correctedQuery: '',
            maxDocumentsReached: false,
        }
    },
    methods: {
        // Search for documents based on the given query and index
        async searchQuery(query, index, b_okapi25_parameter, k1_okapi25_parameter, diversity_okapi25_parameter, fairness_okapi25_parameter, pagerank_weight_parameter, initialQuery=false) {
            this.currentQueryReadOnly = query;
            this.b_okapi25_parameterReadOnly = b_okapi25_parameter;
            this.k1_okapi25_parameterReadOnly = k1_okapi25_parameter;
            this.diversity_okapi25_parameterReadOnly = diversity_okapi25_parameter;
            this.fairness_okapi25_parameterReadOnly = fairness_okapi25_parameter;
            this.pagerank_weight_parameterReadOnly = pagerank_weight_parameter;
            // Check if query is empty
            if(query !== "") {
                if(initialQuery) {
                    this.maxDocumentsReached = false;
                    this.searchResults = [];
                }
                this.loadingResults = true;
                try {
                    const response = await request.getRequest("/query/"+query+"/"+index+"/okapi/"+b_okapi25_parameter+"/"+k1_okapi25_parameter+"/"+diversity_okapi25_parameter+"/"+fairness_okapi25_parameter+"/pagerank/"+pagerank_weight_parameter);
                    if(await checkResponseStatus(200, response)) {
                        const res = await response.json();
                        // If the response contains less than 10 documents, we reached the end of possible documents we can retrieve
                        if(res.length < 10) {
                            this.maxDocumentsReached = true;
                        }
                        if(initialQuery) {
                            if(res.length === 0) {
                                this.showSnackbar('No results found for your query.', 'error');
                            }
                            this.searchResults = res;
                        } else {
                            // If this isn't an initial query, we append the results to the existing ones
                            this.searchResults = this.searchResults.concat(res);
                        }
                        this.loadingResults = false;
                    } else {
                        this.showSnackbar('Something went wrong searching for documents.', 'error');
                        this.loadingResults = false;
                    }
                } catch (e) {
                    this.showSnackbar('Something went wrong searching for documents.', 'error');
                    this.loadingResults = false;
                }
                // Don't await this for performance reasons
                this.checkSpelling(query);
            }
        },

        // Check the spelling of the given query
        async checkSpelling(query) {
            const response = await request.getRequest("/query/spellcheck/"+query);
            if(await checkResponseStatus(200, response)) {
                const res = await response.json();
                if(res['misspelled']) {
                    this.showSpellchecker = true;
                    this.correctedQuery = res['corrected_query'];
                }
            }
        },

        // Show a snackbar with the given text and color
        showSnackbar(text, color) {
            this.snackbarActivator = true;
            this.snackbarText = text;
            this.snackbarColor = color;
        },
    }
}
</script>

<style lang="scss">
#app {
}

.resultDocuments {
    width: 100vw;
    height: calc(90vh - 40px);
    margin-top: 10vh;

}

.footer {

}
</style>

<style>
html, body {
    overflow: hidden; /* Hide scrollbar on main html and body */
    height: 100%; /* Ensure the body takes full height */
    margin: 0; /* Remove default margin */
}
</style>
