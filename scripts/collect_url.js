let results = [];
document.querySelectorAll('img').forEach(img => {
    if (img.src && img.src.startsWith('http') && 
        img.naturalWidth > 150 && img.naturalHeight > 150) {
        results.push(img.src);
    }
});

// Affiche les URLs dans la console
console.log(results.join('\n'));
console.log('Total : ' + results.length + ' images trouvées');