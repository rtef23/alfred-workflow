const convertTo = (text, encodingType = 'NFC') => {
    return text.normalize(encodingType);
}

export {
    convertTo
};