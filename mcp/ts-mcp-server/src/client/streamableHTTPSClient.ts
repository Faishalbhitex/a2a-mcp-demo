import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";
import { SSEClientTransport } from "@modelcontextprotocol/sdk/client/sse.js";


async function main() {
  let client: Client | undefined = undefined;
  const baseUrl = new URL('http://localhost:3000/mcp-calculator')

  try {
    client = new Client({
      name: 'streamable-http-calcultor-client',
      version: '1.0.0'
    });
    const transport = new StreamableHTTPClientTransport(
      new URL(baseUrl),
    );
    await client.connect(transport);
    console.log("Connected using Streaamble HTTP Tranport\n");

    const listTools = await client.listTools();
    const callToolMultiply = await client.callTool({
      name: 'multiply',
      arguments: {
        a: 2,
        b: 5
      }
    });
    console.log("MCP List Tools:", JSON.stringify(listTools, null, 2));
    console.log("MCP Call Tool 'multiply(2, 5):", JSON.stringify(callToolMultiply, null, 2));

    await transport.close();
  } catch (error) {
    console.log("Streamble HTTP connection failed, failing back to SSE transport");
    client = new Client({
      name: 'sse-calculator-client',
      version: '1.0.0'
    });
    const sseTransport: SSEClientTransport = new SSEClientTransport(baseUrl);
    await client.connect(sseTransport);
    console.log("Connected using SSE transport");

    const listTools = await client.listTools();
    const callToolDivide = await client.callTool({
      name: 'divide',
      arguments: {
        a: 4,
        b: 2
      }
    });
    console.log("MCP List Tools:", JSON.stringify(listTools, null, 2));
    console.log("MCP Call Tool 'divide(4, 2):", JSON.stringify(callToolDivide, null, 2));

    await sseTransport.close();
  }
}


main().catch((error: unknown) => {
  console.error('Error running MCP client', error);
  process.exit(1);
});
