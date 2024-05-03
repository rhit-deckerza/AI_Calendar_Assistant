import express from 'express'
import { getRouter } from './api_route.js';
import cors from 'cors'
import bodyParser from 'body-parser';
import path from 'path'
import { fileURLToPath } from 'url';
const app = express();

console.log(app)

// app.use(cors());c
app.use(bodyParser.json())




// app.all('*', (req, res) => {
//     res.status(200).send('Server is reachable');
// });
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);


app.listen(8080, () => {
    console.log('server listening on port 8080')
})

app.get('/prompts/prompt.txt', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'prompts', 'prompt.txt'));
});
const apiRouter = getRouter()

app.use('/api', apiRouter);
//https://dev.to/techcheck/creating-a-react-node-and-express-app-1ieg