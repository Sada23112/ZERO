import fs from 'node:fs';
import path from 'node:path';

export interface ToolCallRequest {
  tool: string;
  arguments: Record<string, unknown>;
}

export interface ToolCallResult {
  success: boolean;
  content?: string;
  error?: string;
}

export class FilesystemMcpServer {
  async handleToolCall(request: ToolCallRequest): Promise<ToolCallResult> {
    const { tool, arguments: args } = request;

    try {
      switch (tool) {
        case 'read_file': {
          const filePath = String(args.path);
          if (!fs.existsSync(filePath)) {
            return { success: false, error: `File not found: ${filePath}` };
          }
          const content = fs.readFileSync(filePath, 'utf-8');
          return { success: true, content };
        }

        case 'write_file': {
          const filePath = String(args.path);
          const content = String(args.content || '');
          fs.mkdirSync(path.dirname(filePath), { recursive: true });
          fs.writeFileSync(filePath, content, 'utf-8');
          return { success: true, content: `File written successfully to ${filePath}` };
        }

        case 'edit_file': {
          const filePath = String(args.path);
          const target = String(args.target);
          const replacement = String(args.replacement);

          if (!fs.existsSync(filePath)) {
            return { success: false, error: `File not found: ${filePath}` };
          }

          const existingContent = fs.readFileSync(filePath, 'utf-8');
          if (!existingContent.includes(target)) {
            return { success: false, error: `Target string not found in ${filePath}` };
          }

          const updatedContent = existingContent.replace(target, replacement);
          fs.writeFileSync(filePath, updatedContent, 'utf-8');
          return { success: true, content: `Successfully edited ${filePath}` };
        }

        case 'list_directory': {
          const dirPath = String(args.path || '.');
          if (!fs.existsSync(dirPath)) {
            return { success: false, error: `Directory not found: ${dirPath}` };
          }
          const entries = fs.readdirSync(dirPath, { withFileTypes: true });
          const resultList = entries.map((e) => `${e.isDirectory() ? '[DIR]' : '[FILE]'} ${e.name}`);
          return { success: true, content: resultList.join('\n') };
        }

        default:
          return { success: false, error: `Unknown filesystem tool: ${tool}` };
      }
    } catch (err) {
      return { success: false, error: `Filesystem tool error: ${err instanceof Error ? err.message : String(err)}` };
    }
  }
}
