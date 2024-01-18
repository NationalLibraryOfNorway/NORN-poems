function togglePoems(urn) {
    var poemsDiv = document.getElementById('poems-' + urn);
    poemsDiv.style.display = poemsDiv.style.display === 'none' ? 'block' : 'none';
}
