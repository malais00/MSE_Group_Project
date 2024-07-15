<template>
    <div>
        <div class="resultDocumentsContainer">
            <CategoryFilter/>
            <div
                v-for="doc in documents"
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
    data() {
        return {
            documents: [
                {
                    "title": "Best Online Cheese Shops to Buy From",
                    "preview": "Discover the top online cheese shops that deliver fresh and gourmet cheeses right to your doorstep. From artisan to imported varieties, find the best sources here.",
                    "url": "https://www.crazy-cheese.com/collections/crazy-cheese-2",
                    "icon": "mdi-cheese"
                },
                {
                    "title": "Top 10 Cheese Stores in the US",
                    "preview": "Explore the best cheese stores across the United States. Whether you're looking for local favorites or international cheeses, these shops have it all.",
                    "url": "https://de.wikipedia.org/wiki/Cheese",
                    "icon": "mdi-store"
                },
                {
                    "title": "Where to Buy Cheese Online: A Comprehensive Guide",
                    "preview": "Looking to buy cheese online? This comprehensive guide covers the best websites for purchasing a variety of cheeses, including rare and specialty options.",
                    "url": "https://www.cheeseonline.com/guide-to-buying-cheese-online",
                    "icon": "mdi-web"
                },
                {
                    "title": "The Best Places to Buy Cheese Near You",
                    "preview": "Find out where you can buy the best cheese near your location. This guide highlights local stores, markets, and delis known for their excellent cheese selections.",
                    "url": "https://www.localcheese.com/best-places-to-buy-cheese",
                    "icon": "mdi-map-marker"
                },
                {
                    "title": "Gourmet Cheese Delivered to Your Door: Top Services Reviewed",
                    "preview": "Get gourmet cheese delivered to your home with these top-rated services. From subscription boxes to specialty cheese shops, we've reviewed the best options.",
                    "url": "https://www.cheesedelivery.com/top-services-reviewed",
                    "icon": "mdi-truck-delivery"
                },
                {
                    "title": "Cheese Shopping: Best Online Retailers",
                    "preview": "Discover the best online retailers for cheese shopping. Learn about their selections, delivery options, and customer reviews to find your perfect cheese source.",
                    "url": "https://www.cheeseshopping.com/best-online-retailers",
                    "icon": "mdi-cart"
                },
                {
                    "title": "Local Cheese Shops: Where to Find the Best Cheese in Your City",
                    "preview": "Looking for the best local cheese shops? This guide covers top-rated cheese stores in major cities, offering a range of domestic and imported cheeses.",
                    "url": "https://www.citycheese.com/best-local-cheese-shops",
                    "icon": "mdi-city"
                },
                {
                    "title": "Top Online Cheese Stores for Every Cheese Lover",
                    "preview": "From aged cheddar to creamy brie, these online cheese stores cater to every cheese lover's taste. Check out our list of the best online shops for cheese.",
                    "url": "https://www.cheeselover.com/top-online-cheese-stores",
                    "icon": "mdi-heart"
                },
                {
                    "title": "Where to Buy Artisan Cheese Online",
                    "preview": "Love artisan cheese? Find out where to buy the best artisan cheeses online. These shops offer unique and handcrafted cheeses from small producers.",
                    "url": "https://www.artisancheese.com/where-to-buy-artisan-cheese",
                    "icon": "mdi-hand"
                },
                {
                    "title": "Cheese Buying Guide: Best Places to Purchase Cheese",
                    "preview": "Navigate the world of cheese buying with this guide. Discover the best places to purchase cheese, both online and in-store, for all your culinary needs.",
                    "url": "https://www.cheesebuyingguide.com/best-places-to-purchase",
                    "icon": "mdi-book-open"
                },
                {
                    "title": "Best Online Cheese Shops to Buy From",
                    "preview": "Discover the top online cheese shops that deliver fresh and gourmet cheeses right to your doorstep. From artisan to imported varieties, find the best sources here.",
                    "url": "https://www.cheeseshop.com/best-online-cheese-shops",
                    "icon": "mdi-cheese"
                },
                {
                    "title": "Top 10 Cheese Stores in the US",
                    "preview": "Explore the best cheese stores across the United States. Whether you're looking for local favorites or international cheeses, these shops have it all.",
                    "url": "https://www.cheesestoreus.com/top-10-cheese-stores",
                    "icon": "mdi-store"
                },
                {
                    "title": "Where to Buy Cheese Online: A Comprehensive Guide",
                    "preview": "Looking to buy cheese online? This comprehensive guide covers the best websites for purchasing a variety of cheeses, including rare and specialty options.",
                    "url": "https://www.cheeseonline.com/guide-to-buying-cheese-online",
                    "icon": "mdi-web"
                },
            ]
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
