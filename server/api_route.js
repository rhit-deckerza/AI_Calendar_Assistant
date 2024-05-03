import express from 'express';
import { getSystemMessage, getUserMessage } from './utilities.js';
import OpenAI from "openai";

export function getRouter() {
    const configuration = {
        // organization: process.env.OPENAI_ORG_ID,
        apiKey: "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",
    };
    const openai = new OpenAI(configuration);

    const router = express.Router();
    console.log("here")
    router.post('/prompt', async (req, res) => {
        console.log("recieved")
        // console.log(req.query)
        const { messages } = req.body;
        // console.log(messages)
        // HEREEEEEE
        const completion = await openai.chat.completions.create({
            model: 'gpt-3.5-turbo',
            messages: messages
        });

        const openaiResponse = completion.choices[0].message.content;
        // console.log("completion: ", completion)
        // console.log(openaiResponse)
        res.status(200);
        res.json({
            response: openaiResponse,
        });
    });

    return router;
}
