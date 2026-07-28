import { describe, it, expect } from 'vitest';
import { getCoreInfo } from '../packages/core/src/index.js';
import { getMemoryInfo } from '../packages/memory/src/index.js';
import { getSecurityInfo } from '../packages/security/src/index.js';
import { getFilesystemMcpInfo } from '../mcp-servers/filesystem/src/index.js';
import { getTerminalMcpInfo } from '../mcp-servers/terminal/src/index.js';

describe('Milestone 1: Monorepo Architecture Initialization', () => {
  it('should initialize @zero/core correctly', () => {
    expect(getCoreInfo()).toContain('Project ZERO Core Engine');
  });

  it('should initialize @zero/memory correctly', () => {
    expect(getMemoryInfo()).toContain('Project ZERO Memory Subsystem');
  });

  it('should initialize @zero/security correctly', () => {
    expect(getSecurityInfo()).toContain('Project ZERO Capability Security Subsystem');
  });

  it('should initialize @zero/mcp-filesystem correctly', () => {
    expect(getFilesystemMcpInfo()).toContain('Filesystem MCP Tool Server');
  });

  it('should initialize @zero/mcp-terminal correctly', () => {
    expect(getTerminalMcpInfo()).toContain('Terminal MCP Tool Server');
  });
});
