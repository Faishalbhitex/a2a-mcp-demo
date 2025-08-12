import express from "express";
import type { Request, Response } from "express";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import { SimpleMCPCalculator } from "../shared/calculatorTools.js";
import cors from "cors";

const calculator = new SimpleMCPCalculator();
const getServer = () => {
  const server = new McpServer({
    name: "streamable-http-server-calculator",
    version: "1.0.0",
  }, { capabilities: { logging: {} } });

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
  return server;
}


const app = express();
app.use(express.json());

app.use(cors({
  origin: '*',
  exposedHeaders: ['Mcp-Session-id']
}));

app.post('/mcp-calculator', async (req: Request, res: Response) => {
  const server = getServer();
  try {
    const transport: StreamableHTTPServerTransport = new StreamableHTTPServerTransport({
      sessionIdGenerator: undefined,
    });
    await server.connect(transport);
    await transport.handleRequest(req, res, req.body);
    res.on('close', () => {
      console.log('Request closed');
      transport.close();
      server.close();
    });
  } catch (error) {
    console.error('Error handling MCP request:', error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: null,
      });
    }
  }
});

app.get('/mcp-calculator', async (_req: Request, res: Response) => {
  console.log('Received GET MCP request');
  res.writeHead(405).end(JSON.stringify({
    jsonrpc: "2.0",
    error: {
      code: -32000,
      message: "Method not allowed."
    },
    id: null
  }));
});

app.delete('/mcp-calculator', async (_req: Request, res: Response) => {
  console.log('Received DELETE MCP request');
  res.writeHead(405).end(JSON.stringify({
    jsonrpc: "2.0",
    error: {
      code: -32000,
      message: "Method not allowed."
    },
    id: null
  }));
});



// Start the server
const PORT = process.env.PORT || 3000; // Railway menyediakan PORT environment
const HOST = process.env.HOST || '0.0.0.0'; // Penting untuk Railway!

app.listen(PORT, HOST, () => {
  console.log(`MCP Stateless Streamable HTTPS Server listening on ${HOST}:${PORT}`);
  console.log('MCP Calculator Running..');
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});

// Handle server shutdown
process.on('SIGINT', async () => {
  console.log('Shutting down server...');
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('Received SIGTERM, shutting down gracefully...');
  process.exit(0);
});
