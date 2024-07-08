<template>
    <v-app>
        <Header/>

        <v-main>
            <ResultDocuments class="resultDocuments"/>
        </v-main>

        <AppFooter class="footer"/>
    </v-app>
</template>

<script setup>
import ResultDocuments from "@/components/ResultDocuments";
import Header from "@/components/Header";
import AppFooter from "@/components/AppFooter";
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
