import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

async function main() {
  try {
    const client = new Client(
      {
        name: "stdio-calculator-client",
        version: "1.0.0"
      }
    );

    const transport: StdioClientTransport = new StdioClientTransport({
      command: "node",
      args: ["/data/data/com.termux/files/home/gemini-cli-example/ts-mcp-server/dist/server/stdioTools.js"]
    });


    await client.connect(transport);


    // List all tools 
    const allTool = await client.listTools();

    // Call a tool add
    const callToolAdd = await client.callTool({
      name: "add",
      arguments: {
        a: 2,
        b: 3
      }
    });

    console.log("List all tools type:", typeof allTool);
    console.log("List all tools:", JSON.stringify(allTool, null, 2));
    console.log("Call tool 'Add' type:", typeof callToolAdd);
    console.log("Call Tool 'Add' result:", JSON.stringify(callToolAdd, null, 2));

    await transport.close();
  } catch (error) {
    console.log('Error running client:', error);
    process.exit(1);
  }
}


main().catch((error: unknown) => {
  console.log("Error running MCP client:", error);
  process.exit(1);
});
