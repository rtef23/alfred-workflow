import path from 'path';
import fs from 'fs';
import os from 'os';

const USER_HOME = os.homedir();
const WHALE_HOME_DIRECTORY = path.join(USER_HOME, 'Library/Application Support/Naver/Whale');
const WHALE_BOOKMARK_FILE = path.join(WHALE_HOME_DIRECTORY, '/Profile 1/Bookmarks');

const ENCODING = 'utf8';
const URL = 'url';
const FOLDER = 'folder';

const query = process.argv[2];

const bookmarkJson = JSON.parse(fs.readFileSync(WHALE_BOOKMARK_FILE, {
    encoding: ENCODING,
    flag: 'r'
}));

const { roots : { bookmark_bar } } = bookmarkJson;

console.log(JSON.stringify({
    items: search(query, bookmark_bar)
        .filter(({ isSearchTarget }) => isSearchTarget)
        .map(({ name, url }) => ({
            uid: name,
            title: name,
            arg: url
        }))
}));

function search(query, element) {
    const { type } = element;

    switch(type){
        case URL:
            return searchUrl(query, element);
        case FOLDER:
            return searchFolder(query, element);
        default:
            return null;
    }
}

function searchFolder(query, { children }) {
    return children
        .flatMap((child) => search(query, child));
}

function searchUrl(query, { url, name }) {
    return {
        url,
        name,
        isSearchTarget: !query? true : (url.includes(query) || name.includes(query))
    };
}