import axios from 'axios';

export async function fetchSystemPrompt() {
    try {
        const response = await axios.get("http://localhost:8080/prompts/prompt.txt");
        return response.data;  // Axios automatically handles the response to return data
    } catch (error) {
        console.error(`Error fetching file: ${error}`);
        throw error;  // Rethrow to allow the caller to handle it
    }
}
