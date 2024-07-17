import {stemmer} from 'stemmer'

const preprocessQuery = async (query) => {
    query = query.toLowerCase();
    // Remove punctuation and special characters
    query = query.replace(/[^\w\s]/gi, '');
    // Split by spaces
    const words = query.split(/\s+/);

    const stemmedWords = words.map(word => stemmer(word));
    const result = stemmedWords.join(' ');
    console.log(result);
    return result;
};


export { preprocessQuery };
