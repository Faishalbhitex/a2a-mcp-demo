import type { CallToolResult } from "@modelcontextprotocol/sdk/types.js";

interface BaseSimpleMCPCalculator {
  add(a: number, b: number): Promise<CallToolResult>;
  subtract(a: number, b: number): Promise<CallToolResult>;
  multiply(a: number, b: number): Promise<CallToolResult>;
  divide(a: number, b: number): Promise<CallToolResult>;
}

export class SimpleMCPCalculator implements BaseSimpleMCPCalculator {
  async add(a: number, b: number): Promise<CallToolResult> {
    return {
      content: [{
        type: "text",
        text: String(a + b)
      }]
    };
  }

  async subtract(a: number, b: number): Promise<CallToolResult> {
    return {
      content: [{
        type: "text",
        text: String(a - b)
      }]
    };
  }

  async multiply(a: number, b: number): Promise<CallToolResult> {
    return {
      content: [{
        type: "text",
        text: String(a * b)
      }]
    };
  }

  async divide(a: number, b: number): Promise<CallToolResult> {
    if (b === 0) {
      return {
        content: [{
          type: "text",
          text: "Error: Division by zero"
        }],
        isError: true
      };
    }
    return {
      content: [{
        type: "text",
        text: String(a / b)
      }]
    };
  }
}
