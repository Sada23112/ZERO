import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { FilesystemMcpServer } from '../filesystem/src/filesystem-server.js';
import { TerminalMcpServer } from '../terminal/src/terminal-server.js';
import fs from 'node:fs';
import path from 'node:path';

describe('Milestones 13 & 14: Filesystem & Terminal MCP Tool Servers', () => {
  const fsServer = new FilesystemMcpServer();
  const termServer = new TerminalMcpServer();
  let testFile: string;

  beforeEach(() => {
    testFile = path.join(process.cwd(), `test_mcp_${Date.now()}.txt`);
  });

  afterEach(() => {
    if (fs.existsSync(testFile)) {
      fs.unlinkSync(testFile);
    }
  });

  it('Milestone 13: Should write, read, and edit files via Filesystem MCP', async () => {
    // 1. Write file
    const writeRes = await fsServer.handleToolCall({
      tool: 'write_file',
      arguments: { path: testFile, content: 'Hello Project ZERO' },
    });
    expect(writeRes.success).toBe(true);

    // 2. Read file
    const readRes = await fsServer.handleToolCall({
      tool: 'read_file',
      arguments: { path: testFile },
    });
    expect(readRes.success).toBe(true);
    expect(readRes.content).toBe('Hello Project ZERO');

    // 3. Edit file
    const editRes = await fsServer.handleToolCall({
      tool: 'edit_file',
      arguments: { path: testFile, target: 'Hello Project ZERO', replacement: 'Hello World Engine' },
    });
    expect(editRes.success).toBe(true);

    const readRes2 = await fsServer.handleToolCall({
      tool: 'read_file',
      arguments: { path: testFile },
    });
    expect(readRes2.content).toBe('Hello World Engine');
  });

  it('Milestone 14: Should execute terminal commands safely via Terminal MCP', async () => {
    const res = await termServer.runCommand('node -v');
    expect(res.success).toBe(true);
    expect(res.stdout).toContain('v');
    expect(res.exitCode).toBe(0);
  });
});
