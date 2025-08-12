import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { SimpleMCPCalculator } from "../shared/calculatorTools.js";

const server = new McpServer({
  name: "tool-server",
  version: "1.0.0"
});

const calculator = new SimpleMCPCalculator();

server.registerTool("add", {
  title: "Addition Tool",
  description: "Add two numbers",
  inputSchema: {
    a: z.number(),
    b: z.number()
  }
}, async ({ a, b }) => await calculator.add(a, b));

server.registerTool("multiply", {
  title: "Multiplication Tool",
  description: "Multiply two numbers",
  inputSchema: {
    a: z.number(),
    b: z.number()
  }
}, async ({ a, b }) => await calculator.multiply(a, b));

server.registerTool("subtract", {
  title: "Subtraction Tool",
  description: "Subtract two numbers",
  inputSchema: {
    a: z.number(),
    b: z.number()
  }
}, async ({ a, b }) => await calculator.subtract(a, b));

server.registerTool("divide", {
  title: "Division Tool",
  description: "Divide two numbers",
  inputSchema: {
    a: z.number(),
    b: z.number()
  }
}, async ({ a, b }) => await calculator.divide(a, b));

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.log('MCP server tools is running..');
}

main().catch((error) => {
  console.error("Server error:", error);
  process.exit(1);
});
