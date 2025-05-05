const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

// Serve static files
app.use(express.static('public'));
const pathtosearch = path.resolve(__dirname, 'services', 'search', 'search.py')

// Search endpoint
app.get('/search', (req, res) => {
    const query = req.query.q;

    // Performs a execute to trigger the search python script. Not the safest but was the quickest implementation for example
    exec(`python ${pathtosearch} "${query}"`, (error, stdout, stderr) => {
        if (error) return res.status(500).send(error.message);
        res.send(stdout);
    });
});

app.listen(port, () => console.log(`Server running at http://localhost:${port}`));
