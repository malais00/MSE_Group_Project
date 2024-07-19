<template>
    <v-app>
        <Header
            @search-query="searchQuery"
        />

        <v-main>
            <ResultDocuments
                :searchResults="searchResults"
                :loading-results="loadingResults"
                class="resultDocuments"/>
        </v-main>

        <AppFooter class="footer"/>
    </v-app>
</template>

<script>
import ResultDocuments from "@/components/ResultDocuments";
import Header from "@/components/Header";
import AppFooter from "@/components/AppFooter";
import * as request from "@/api/request";
import {checkResponseStatus} from "@/util/check";
import {preprocessQuery} from "@/util/queryPreprocessing";

export default {
    name: "CategoryFilter",
    data() {
        return {
            ResultDocuments,
            Header,
            AppFooter,
            loadingResults: false,
            searchResults: [],
        }
    },
    methods: {
        async searchQuery(query) {
            if(query !== "") {
                this.loadingResults = true;
                const response = await request.getRequest("/query/"+query+"/1");
                await checkResponseStatus(200, response);
                const res = await response.json();
                this.searchResults = res;
                this.loadingResults = false;
            }
        },

        async getNextDocuments(query, index) {
            const response = await request.getRequest("/query/"+query+"/"+index);
            await checkResponseStatus(200, response);
            const res = await response.json();
            this.searchResults = res;
        },

        async getDetails(documentId) {
            const response = await request.getRequest("/document/details/"+documentId);
            await checkResponseStatus(200, response);
            const res = await response.json();
            const documentDetails = res;
        }
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
html {

}
</style>
