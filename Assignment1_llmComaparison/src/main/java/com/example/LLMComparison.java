package com.example;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardOpenOption;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class LLMComparison {
    private static final String PROMPT = "Explain quantum computing to a 10-year-old";
    private static final String OUTPUT_FILE = "comparison_report.md";
    private static final String HUGGINGFACE_MODEL = "gpt2";  // Simple model that should work
    private static final ObjectMapper objectMapper = new ObjectMapper();
    private static final HttpClient httpClient = HttpClient.newBuilder()
            .version(HttpClient.Version.HTTP_2)
            .connectTimeout(Duration.ofSeconds(20))
            .build();

    private static Properties loadProperties() throws IOException {
        Properties props = new Properties();
        try (InputStream input = LLMComparison.class.getClassLoader().getResourceAsStream("application.properties")) {
            if (input == null) {
                System.out.println("Warning: application.properties not found, using environment variables only");
                return props;
            }
            props.load(input);
        }
        return props;
    }

    private static String getApiKey(Properties props, String keyName, String envVarName) {
        // First try environment variable
        String key = System.getenv(envVarName);

        // If not found in env, try properties file
        if (key == null || key.isBlank()) {
            key = props.getProperty(keyName);
        }

        // If still not found, return null
        if (key == null || key.isBlank()) {
            return null;
        }

        return key.trim();
    }

    // Store responses for the final report
    private static class LLMResponse {
        String modelName;
        String response;
        boolean success;

        LLMResponse(String modelName, String response, boolean success) {
            this.modelName = modelName;
            this.response = response;
            this.success = success;
        }
    }

    public static void main(String[] args) {
        try {
            // Load properties from application.properties
            Properties props = loadProperties();

            // Get API keys (tries environment variables first, then properties file)
            String openaiApiKey = getApiKey(props, "openai.api.key", "OPENAI_API_KEY");
            String anthropicApiKey = getApiKey(props, "anthropic.api.key", "ANTHROPIC_API_KEY");
            String huggingfaceApiKey = getApiKey(props, "huggingface.api.key", "HUGGINGFACE_API_KEY");

            System.out.println("🔍 Starting LLM Comparison...\n");
            System.out.println("Prompt: " + PROMPT + "\n");

            // Clear previous report
            Files.deleteIfExists(Path.of(OUTPUT_FILE));
            
            // Write report header
            writeToReport("# LLM Output Comparison\n\n");
            writeToReport("**Prompt:** " + PROMPT + "\n\n");

            List<LLMResponse> responses = new ArrayList<>();
            int successfulCalls = 0;

            // Try OpenAI
            if (openaiApiKey != null) {
                try {
                    System.out.println("🔵 Calling OpenAI API...");
                    String gptResponse = getOpenAIResponse(openaiApiKey);
                    responses.add(new LLMResponse("OpenAI GPT-3.5", gptResponse, true));
                    successfulCalls++;
                } catch (Exception e) {
                    System.err.println(" OpenAI API failed: " + e.getMessage());
                    responses.add(new LLMResponse("OpenAI GPT-3.5", "[Error: " + e.getMessage() + "]", false));
                }
            } else {
                System.out.println("OpenAI API key not found. ");
                responses.add(new LLMResponse("OpenAI GPT-3.5", "[API key not provided]", false));
            }

            // Try Anthropic Claude
            if (anthropicApiKey != null) {
                try {
                    System.out.println("\nCalling Anthropic Claude API...");
                    String claudeResponse = getClaudeResponse(anthropicApiKey);
                    responses.add(new LLMResponse("Anthropic Claude", claudeResponse, true));
                    successfulCalls++;
                } catch (Exception e) {
                    System.err.println(" Claude API failed: " + e.getMessage());
                    responses.add(new LLMResponse("Anthropic Claude", "[Error: " + e.getMessage() + "]", false));
                }
            } else {
                System.out.println(" Anthropic API key not found. ");
                responses.add(new LLMResponse("Anthropic Claude", "[API key not provided]", false));
            }

            // Try HuggingFace (optional)
            if (huggingfaceApiKey != null) {
                try {
                    System.out.println("\n Calling HuggingFace API...");
                    String hfResponse = getHuggingFaceResponse(huggingfaceApiKey);
                    responses.add(new LLMResponse("HuggingFace (" + HUGGINGFACE_MODEL + ")", hfResponse, true));
                    successfulCalls++;
                } catch (Exception e) {
                    System.err.println(" HuggingFace API failed: " + e.getMessage());
                    responses.add(new LLMResponse("HuggingFace (" + HUGGINGFACE_MODEL + ")", 
                        "[Error: " + e.getMessage() + "]", false));
                }
            } else {
                System.out.println("\nHuggingFace API key not set. ");
                responses.add(new LLMResponse("HuggingFace (" + HUGGINGFACE_MODEL + ")", 
                    "[API key not provided]", false));
            }

            // Generate the report
            for (LLMResponse response : responses) {
                printResponse(response.modelName, response.response);
                writeToReport("## " + response.modelName + " Response\n\n" + response.response + "\n\n");
            }

            // Add discussion section
            writeToReport("## Discussion\n\n" + 
                "| Aspect | OpenAI GPT-3.5 | Anthropic Claude | HuggingFace |\n" +
                "|--------|----------------|-------------------|-------------|\n" +
                "| Clarity | | | |\n" +
                "| Technical Accuracy | | | |\n" +
                "| Engagement | | | |\n" +
                "| Educational Value | | | |\n\n" +
                "**Key Observations:**\n" +
                "- \n" +
                "- \n" +
                "- \n"
            );

            if (successfulCalls == 0) {
                System.err.println("\n No APIs were successfully called. Please set up at least one API key:");
                System.exit(1);
            }

            System.out.println("\n✅ Comparison report has been saved to " + OUTPUT_FILE);
            System.out.println("📊 Successfully called " + successfulCalls + " API(s)");
            System.out.println("\n💡 Please fill in the comparison table in " + OUTPUT_FILE + " with your analysis.");

        } catch (Exception e) {
            System.err.println("\n An error occurred: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }

    private static String getOpenAIResponse(String apiKey) throws IOException, InterruptedException, URISyntaxException {
        ObjectNode requestBody = objectMapper.createObjectNode();
        requestBody.put("model", "gpt-3.5-turbo");
        requestBody.putArray("messages")
                .addObject()
                .put("role", "user")
                .put("content", PROMPT);
        requestBody.put("temperature", 0.7);
        requestBody.put("max_tokens", 500);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new URI("https://api.openai.com/v1/chat/completions"))
                .header("Content-Type", "application/json")
                .header("Authorization", "Bearer " + apiKey)
                .POST(HttpRequest.BodyPublishers.ofString(requestBody.toString()))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200) {
            throw new IOException("OpenAI API request failed with status: " + response.statusCode() + ". " + 
                "Make sure your API key is valid and has sufficient credits.");
        }

        JsonNode responseJson = objectMapper.readTree(response.body());
        return responseJson.path("choices").get(0).path("message").path("content").asText();
    }

    private static String getClaudeResponse(String apiKey) throws IOException, InterruptedException, URISyntaxException {
        ObjectNode requestBody = objectMapper.createObjectNode();
        requestBody.put("model", "claude-3-sonnet-20240229");  // More affordable than Opus
        requestBody.put("max_tokens", 500);
        requestBody.putArray("messages")
                .addObject()
                .put("role", "user")
                .put("content", PROMPT);

        HttpRequest request = HttpRequest.newBuilder()
                .uri(new URI("https://api.anthropic.com/v1/messages"))
                .header("Content-Type", "application/json")
                .header("x-api-key", apiKey)
                .header("anthropic-version", "2023-06-01")
                .POST(HttpRequest.BodyPublishers.ofString(requestBody.toString()))
                .build();

        HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

        if (response.statusCode() != 200) {
            throw new IOException("Anthropic API request failed with status: " + response.statusCode() + " " + response.body());
        }

        JsonNode responseJson = objectMapper.readTree(response.body());
        return responseJson.path("content").get(0).path("text").asText();
    }

    private static String getHuggingFaceResponse(String apiKey) throws IOException, InterruptedException, URISyntaxException {
        try {
            // Simple text generation API
            ObjectNode requestBody = objectMapper.createObjectNode();
            requestBody.put("inputs", PROMPT);
            
            // Simple parameters for text generation
            ObjectNode parameters = objectMapper.createObjectNode();
            parameters.put("max_length", 150);
            parameters.put("num_return_sequences", 1);
            requestBody.set("parameters", parameters);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(new URI("https://api-inference.huggingface.co/models/" + HUGGINGFACE_MODEL))
                    .header("Content-Type", "application/json")
                    .header("Authorization", "Bearer " + apiKey)
                    .POST(HttpRequest.BodyPublishers.ofString(requestBody.toString()))
                    .build();

            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());
            String responseBody = response.body();

            if (response.statusCode() != 200) {
                throw new IOException("HuggingFace API request failed with status: " + 
                    response.statusCode() + ". Response: " + responseBody);
            }

            // Parse the response - format is typically an array of generated text
            JsonNode responseJson = objectMapper.readTree(responseBody);
            if (responseJson.isArray() && responseJson.size() > 0) {
                JsonNode firstItem = responseJson.get(0);
                if (firstItem.has("generated_text")) {
                    return firstItem.get("generated_text").asText();
                }
                return firstItem.toString();
            }
            
            return responseBody; // Return raw response if we can't parse it
            
        } catch (Exception e) {
            throw new IOException("Error calling HuggingFace API: " + e.getMessage());
        }
    }



    private static void printResponse(String model, String response) {
        System.out.println("\n=== " + model + " Response ===");
        System.out.println(response);
        System.out.println("=".repeat(Math.max(30, model.length() + 20)));
    }

    private static void writeToReport(String content) throws IOException {
        Files.writeString(
                Path.of(OUTPUT_FILE),
                content,
                StandardOpenOption.CREATE,
                StandardOpenOption.APPEND
        );
    }
}