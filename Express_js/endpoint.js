const express = require('express');
const axios = require('axios');
const xml2js = require('xml2js');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(cors());

function parseXml(xml) {
    return new Promise((resolve, reject) => {
        xml2js.parseString(xml, { explicitArray: false }, (err, result) => {
            if (err) {
                reject(err);
            } else {
                resolve(result);
            }
        });
    });
}

async function extractTitlesFromEfetchResponse(xmlData) {
    try {
        const parsed = await parseXml(xmlData);
        
        const articles = parsed.PubmedArticleSet.PubmedArticle || 
                         parsed.PubmedArticleSet.PubmedBookArticle || 
                         [];
        
        const articlesArray = Array.isArray(articles) ? articles : [articles];
        
        const titles = articlesArray.map(article => {
            return article.MedlineCitation?.Article?.ArticleTitle || 
                   article.BookDocument?.ArticleTitle || 
                   'Título no disponible';
        });
        
        return titles;
    } catch (error) {
        console.error('Error al extraer títulos:', error);
        throw new Error('Error al procesar los datos de los artículos');
    }
}

app.get('/search', async (req, res) => {
    const searchTerm = req.query.term;

    if (!searchTerm) {
        return res.status(400).json({ error: 'Se requiere un término de búsqueda.' });
    }

    try {
        const esearchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${encodeURIComponent(searchTerm)}&retmode=xml`;
        const esearchResponse = await axios.get(esearchUrl);
        const parsedResponse = await parseXml(esearchResponse.data);

        const idList = parsedResponse.eSearchResult.IdList.Id;
        if (!idList || idList.length === 0) {
            return res.status(404).json({ error: 'No se encontraron resultados para el término de búsqueda.' });
        }

        const idsToFetch = idList.slice(0, 50);
        
        const efetchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=${idsToFetch.join(',')}&rettype=abstract&retmode=xml`;
        const efetchResponse = await axios.get(efetchUrl);
        const titles = await extractTitlesFromEfetchResponse(efetchResponse.data);

        res.json({ 
            count: titles.length,
            titles 
        });
    } catch (error) {
        if (error.response) {
            console.error('Error en la respuesta del servidor:', error.response.status, error.response.data);
            res.status(502).json({ error: 'Error en la comunicación con los servicios externos.' });
        } else if (error.request) {
            console.error('No se recibió respuesta del servidor:', error.request);
            res.status(504).json({ error: 'No se recibió respuesta del servidor externo.' });
        } else {
            console.error('Error interno:', error.message);
            res.status(500).json({ error: 'Error interno del servidor.' });
        }
    }
});

app.listen(PORT, () => {
    console.log(`Servidor corriendo en http://localhost:${PORT}`);
});