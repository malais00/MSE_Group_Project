// plugins/vuetify.js

// Styles
import '@mdi/font/css/materialdesignicons.css';
import 'vuetify/styles';

// Composables
import { createVuetify } from 'vuetify';

// Use like this:
// background-color: rgb(var(--v-theme-primary));
// <v-btn color="primary">Primary Button</v-btn>

const customTheme = {
    dark: false,
    colors: {
        primary: '#a51e37',
        secondary: '#386641',
        third: '#6A994E',
        fourth: '#A7C957',
        neutral: '#ffffff',
        white: '#ffffff',
        error: '#8f0808',
        success: '#4CAF50',
        warning: '#FB8C00',
        font: '#ffffff',
        cog: '#a51e37',
        slider: '#000000',
    }
};

// Dark theme
const customDarkTheme = {
    dark: true,
    colors: {
        primary: '#a51e37',
        secondary: '#386641',
        third: '#6A994E',
        fourth: '#A7C957',
        neutral: '#3a3a3a',
        white: '#ffffff',
        error: '#8f0808',
        success: '#4CAF50',
        warning: '#FB8C00',
        font: '#444444',
        cog: '#ffffff',
        slider: '#ffffff',
    }
};


// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
    theme: {
        defaultTheme: 'customTheme',
        themes: {
            customTheme,
            customDarkTheme
        }
    }
});
